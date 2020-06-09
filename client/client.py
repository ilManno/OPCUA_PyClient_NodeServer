import logging

from PyQt5.QtCore import QSettings

from opcua import crypto, ua, Client
from opcua.tools import endpoint_to_strings


logger = logging.getLogger(__name__)


class UaClient:

    def __init__(self):
        self.settings = QSettings()
        self.client = None
        self._connected = False
        self._datachange_sub = None
        self._subs_dc = {}
        self.security_mode = "None_"
        self.security_policy = "None"
        self.certificate_path = ""
        self.private_key_path = ""
        self.custom_objects = {}
        self.known_custom_types = ["BoilerType", "MotorType", "ValveType",
                                   "TempSensorType", "LevelIndicatorType", "FlowSensorType"]

    def _reset(self):
        self.client = None
        self._connected = False
        self._datachange_sub = None
        self._subs_dc = {}

    @staticmethod
    def get_endpoints(uri):
        # Create client object and associate url of the server
        client = Client(uri)
        # Connect, ask server for endpoints, and disconnect
        edps = client.connect_and_get_server_endpoints()
        for i, ep in enumerate(edps, start=1):
            logger.info('Endpoint %s:', i)
            for (n, v) in endpoint_to_strings(ep):
                logger.info('  %s: %s', n, v)
            logger.info('')
        return edps

    def connect(self, uri):
        logger.info("Connecting to %s with parameters %s, %s, %s, %s", uri, self.security_mode, self.security_policy, self.certificate_path, self.private_key_path)
        # Create client object and associate url of the server
        self.client = Client(uri)
        if self.security_mode != "None_" and self.security_policy != "None":
            # Set SecureConnection mode
            self.client.set_security(
                getattr(crypto.security_policies, 'SecurityPolicy' + self.security_policy),
                self.certificate_path,
                self.private_key_path,
                mode=getattr(ua.MessageSecurityMode, self.security_mode)
            )
            # self.client.secure_channel_timeout = 10000  # Timeout for the secure channel
            # self.client.session_timeout = 10000  # Timeout for the session
        self.client.application_uri = "urn:example.org:OpcUa:python-client"
        # Open secure channel, create and activate session
        self.client.connect()
        self._connected = True
        self.save_security_settings(uri)

    def disconnect(self):
        if self._connected:
            print("Disconnecting from server")
            self._connected = False
            try:
                # Close session and secure channel
                self.client.disconnect()
            finally:
                self._reset()

    def subscribe_datachange(self, node, handler=None):
        if not self._datachange_sub:
            publishing_interval = 500
            # Create new subscription
            self._datachange_sub = self.client.create_subscription(publishing_interval, handler)
        # Subscribe for data change events for node
        # This will create a new monitored item in subscription
        handle = self._datachange_sub.subscribe_data_change(node)
        self._subs_dc[node.nodeid] = handle

    def unsubscribe_datachange(self, node):
        # Unsubscribe to data change using the handle returned while subscribing
        # This will remove the corresponding monitored item from subscription
        self._datachange_sub.unsubscribe(self._subs_dc[node.nodeid])
        del self._subs_dc[node.nodeid]

    def delete_subscription(self):
        if self._datachange_sub:
            # Remove all monitored items from subscription
            for handle in self._subs_dc.values():
                self._datachange_sub.unsubscribe(handle)
            # Delete subscription on server
            self._datachange_sub.delete()

    def get_node(self, nodeid):
        # Get node using NodeId object or a string representing a NodeId
        return self.client.get_node(nodeid)

    def find_custom_objects(self):
        # Get all children of objects node
        # By default hierarchical references and all node classes are returned
        objects = self.client.get_objects_node().get_children()
        for obj in objects:
            if obj.get_type_definition() == ua.TwoByteNodeId(ua.ObjectIds.FolderType):
                folder_name = obj.get_display_name().to_string()
                if folder_name == "Actuators" or folder_name == "Sensors":
                    devices = obj.get_children()
                    for dev in devices:
                        # Get HasTypeDefinition references
                        references = dev.get_children_descriptions(refs=ua.ObjectIds.HasTypeDefinition)
                        custom_type = references[0].DisplayName.to_string()
                        if custom_type in self.known_custom_types:
                            self.custom_objects[dev.nodeid] = custom_type

    def load_security_settings(self, uri):
        mysettings = self.settings.value("security_settings", None)
        if mysettings is not None and uri in mysettings:
            mode, policy, cert, key = mysettings[uri]
            self.security_mode = mode
            self.security_policy = policy
            self.certificate_path = cert
            self.private_key_path = key
        else:
            self.security_mode = "None_"
            self.security_policy = "None"
            self.certificate_path = ""
            self.private_key_path = ""

    def save_security_settings(self, uri):
        mysettings = self.settings.value("security_settings", None)
        if mysettings is None:
            mysettings = {}
        mysettings[uri] = [self.security_mode,
                           self.security_policy,
                           self.certificate_path,
                           self.private_key_path]
        self.settings.setValue("security_settings", mysettings)
