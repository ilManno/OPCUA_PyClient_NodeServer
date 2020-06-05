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
        self._event_sub = None
        self._subs_dc = {}
        self._subs_ev = {}
        self.security_mode = "None_"
        self.security_policy = "None"
        self.certificate_path = ""
        self.private_key_path = ""
        self.known_custom_types = ["BoilerType", "MotorType", "ValveType",
                                   "TempSensorType", "LevelIndicatorType"]

    def _reset(self):
        self.client = None
        self._connected = False
        self._datachange_sub = None
        self._event_sub = None
        self._subs_dc = {}
        self._subs_ev = {}

    @staticmethod
    def get_endpoints(uri):
        client = Client(uri, timeout=2)
        edps = client.connect_and_get_server_endpoints()
        for i, ep in enumerate(edps, start=1):
            logger.info('Endpoint %s:', i)
            for (n, v) in endpoint_to_strings(ep):
                logger.info('  %s: %s', n, v)
            logger.info('')
        return edps

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

    def get_node(self, nodeid):
        return self.client.get_node(nodeid)
    
    def connect(self, uri):
        logger.info("Connecting to %s with parameters %s, %s, %s, %s", uri, self.security_mode, self.security_policy, self.certificate_path, self.private_key_path)
        self.client = Client(uri)
        if self.security_mode != "None_" and self.security_policy != "None":
            self.client.set_security(
                getattr(crypto.security_policies, 'SecurityPolicy' + self.security_policy),
                self.certificate_path,
                self.private_key_path,
                mode=getattr(ua.MessageSecurityMode, self.security_mode)
            )
            # self.client.secure_channel_timeout = 10000
            # self.client.session_timeout = 10000
        self.client.application_uri = "urn:example.org:OpcUa:python-client"
        self.client.connect()
        self._connected = True
        self.save_security_settings(uri)

    def disconnect(self):
        if self._connected:
            print("Disconnecting from server")
            self._connected = False
            try:
                self.client.disconnect()
            finally:
                self._reset()

    def subscribe_datachange(self, node, handler):
        if not self._datachange_sub:
            self._datachange_sub = self.client.create_subscription(500, handler)
        handle = self._datachange_sub.subscribe_data_change(node)
        self._subs_dc[node.nodeid] = handle
        return handle

    def unsubscribe_datachange(self, node):
        self._datachange_sub.unsubscribe(self._subs_dc[node.nodeid])

    def delete_subscription(self):
        if self._datachange_sub:
            for handle in self._subs_dc.values():
                self._datachange_sub.unsubscribe(handle)
            self._datachange_sub.delete()
            print("Subscription correctly deleted")

    def get_custom_objects(self):
        custom_objects = []
        objects = self.client.get_objects_node().get_children()
        for obj in objects:
            if obj.get_type_definition() == ua.TwoByteNodeId(ua.ObjectIds.FolderType):
                folder_name = obj.get_display_name().to_string()
                if folder_name == "Actuators" or folder_name == "Sensors":
                    devices = obj.get_children()
                    for dev in devices:
                        references = dev.get_children_descriptions(refs=ua.ObjectIds.References)
                        for ref in references:
                            typename = ua.ObjectIdNames[ref.ReferenceTypeId.Identifier]
                            if typename == "HasTypeDefinition":
                                custom_type = ref.DisplayName.to_string()
                                if custom_type in self.known_custom_types:
                                    custom_objects.append((dev, custom_type))
                                break
        return custom_objects
