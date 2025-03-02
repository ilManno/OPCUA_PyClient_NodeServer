import logging

from PyQt5.QtCore import QSettings

from opcua import crypto, ua, Client
from opcua.tools import endpoint_to_strings


logger = logging.getLogger("__main__")


class OpcUaClient:

    def __init__(self):
        self.settings = QSettings()
        self.client = None
        self._connected = False
        # Subscriptions
        self._datachange_subs = []  # list of tuples with subscription and dict with nodeids as keys and handles as values
        self.publishingEnabled = True  # Not necessary
        self.requestedPublishingInterval = 500
        self.publishingIntervals = []
        self.requestedMaxKeepAliveCount = 3000
        self.requestedLifetimeCount = 10000
        self.maxNotificationsPerPublish = 10000
        self.priority = 0
        # Monitored items
        self._client_handle = 0
        self.samplingInterval = self.requestedPublishingInterval
        self.queueSize = 0
        self.discardOldest = True
        self.dataChangeFilter = False
        self.dataChangeTrigger = ua.DataChangeTrigger.StatusValue  # 0 = Status, 1 = StatusValue, 2 = StatusValueTimestamp
        self.deadbandType = ua.DeadbandType.None_  # 0 = None, 1 = Absolute, 2 = Percent
        self.deadbandValue = 0
        self.numericTypes = [ua.VariantType.SByte, ua.VariantType.Byte, ua.VariantType.Int16, ua.VariantType.UInt16,
                             ua.VariantType.Int32, ua.VariantType.UInt32, ua.VariantType.Int64, ua.VariantType.UInt64,
                             ua.VariantType.Float, ua.VariantType.Double]
        # Security
        self.security_mode = "None"
        self.security_policy = "None"
        self.certificate_path = ""
        self.private_key_path = ""
        # Custom objects
        self.custom_objects = {}
        self.known_custom_types = ["BoilerType", "MotorType", "ValveType",
                                   "TempSensorType", "LevelIndicatorType", "FlowSensorType"]

    def _reset(self):
        self.client = None
        self._connected = False
        self._datachange_subs = []
        self.custom_objects = {}

    @staticmethod
    def get_endpoints(uri):
        # Create client object and associate url of the server
        client = Client(uri)
        # Connect, ask server for endpoints, and disconnect
        edps = client.connect_and_get_server_endpoints()
        for i, ep in enumerate(edps, start=1):
            logger.info('Endpoint %s:', i)
            for n, v in endpoint_to_strings(ep):
                logger.info('  %s: %s', n, v)
            logger.info('')
        return edps

    def connect(self, uri):
        logger.info("Connecting to %s with parameters %s, %s, %s, %s", uri, self.security_mode, self.security_policy, self.certificate_path, self.private_key_path)
        # Create client object and associate url of the server
        self.client = Client(uri)
        if self.security_mode != "None" and self.security_policy != "None":
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

    def create_subscription(self, handler):
        # Set subscription parameters
        params = ua.CreateSubscriptionParameters()
        params.PublishingEnabled = self.publishingEnabled
        params.RequestedPublishingInterval = self.requestedPublishingInterval
        params.RequestedMaxKeepAliveCount = self.requestedMaxKeepAliveCount
        params.RequestedLifetimeCount = self.requestedLifetimeCount
        params.MaxNotificationsPerPublish = self.maxNotificationsPerPublish
        params.Priority = self.priority
        datachange_sub = self.client.create_subscription(params, handler)
        self._datachange_subs.append((datachange_sub, {}))
        self.publishingIntervals.append(self.requestedPublishingInterval)

    def create_monitored_items(self, nodes, index):
        monitored_items = []
        if not isinstance(nodes, list):
            nodes = [nodes]
        for node in nodes:
            # Set item to monitor
            rv = ua.ReadValueId()
            rv.NodeId = node.nodeid
            rv.AttributeId = ua.AttributeIds.Value
            # Set monitoring parameters
            mparams = ua.MonitoringParameters()
            self._client_handle += 1
            mparams.ClientHandle = self._client_handle
            mparams.SamplingInterval = self.samplingInterval
            mparams.QueueSize = self.queueSize
            mparams.DiscardOldest = self.discardOldest
            # Create monitored item filter
            if self.dataChangeFilter:
                mfilter = ua.DataChangeFilter()
                mfilter.Trigger = ua.DataChangeTrigger(self.dataChangeTrigger)
                if self.deadbandType == ua.DeadbandType.Absolute:
                    if node.get_data_value().Value.VariantType in self.numericTypes:
                        mfilter.DeadbandType = self.deadbandType
                        mfilter.DeadbandValue = self.deadbandValue  # absolute float value or from 0 to 100 for percentage deadband
                    else:
                        self.deadbandType = ua.DeadbandType.None_
                        mfilter.DeadbandType = self.deadbandType
                elif self.deadbandType == ua.DeadbandType.Percent:
                    has_EURange = False
                    if node.get_type_definition().Identifier == ua.object_ids.ObjectIds.AnalogItemType:
                        # Get node properties
                        descriptions = node.get_references(ua.ObjectIds.HasProperty, ua.BrowseDirection.Forward, ua.NodeClass.Variable, False)
                        for desc in descriptions:
                            if desc.BrowseName.Name == "EURange" and self.get_node(desc.NodeId).get_value() is not None:
                                has_EURange = True
                    if has_EURange:
                        mfilter.DeadbandType = self.deadbandType
                        mfilter.DeadbandValue = self.deadbandValue  # absolute float value or from 0 to 100 for percentage deadband
                    else:
                        self.deadbandType = ua.DeadbandType.None_
                        mfilter.DeadbandType = self.deadbandType
            else:
                mfilter = None
            mparams.Filter = mfilter
            # Create monitored item request
            mir = ua.MonitoredItemCreateRequest()
            mir.ItemToMonitor = rv
            mir.MonitoringMode = ua.MonitoringMode.Reporting
            mir.RequestedParameters = mparams
            # Append to list
            monitored_items.append(mir)
        sub, monitored_items_handles = self._datachange_subs[index]
        handles = sub.create_monitored_items(monitored_items)
        for i in range(len(handles)):
            handle = handles[i]
            if type(handle) == ua.StatusCode:
                handle.check()
            monitored_items_handles[nodes[i].nodeid] = handle

    def remove_monitored_item(self, node, index):
        # Unsubscribe to data change using the handle stored while creating monitored item
        # This will remove the corresponding monitored item from subscription
        sub, monitored_items_handles = self._datachange_subs[index]
        sub.unsubscribe(monitored_items_handles[node.nodeid])
        del monitored_items_handles[node.nodeid]

    def delete_subscription(self, index):
        sub, monitored_items_handles = self._datachange_subs[index]
        # Remove all monitored items from subscription
        for handle in monitored_items_handles.values():
            sub.unsubscribe(handle)
        # Delete subscription on server
        sub.delete()
        del self._datachange_subs[index]
        del self.publishingIntervals[index]

    def delete_subscriptions(self):
        for sub, monitored_items_handles in self._datachange_subs:
            # Remove all monitored items from subscription
            for handle in monitored_items_handles.values():
                sub.unsubscribe(handle)
            # Delete subscription on server
            sub.delete()

    def get_node(self, nodeid):
        # Get node using NodeId object or a string representing a NodeId
        return self.client.get_node(nodeid)

    def load_custom_objects(self):
        """
        Function that populates custom_objects dictionary,
        with nodeids of custom objects as keys and
        string representations of their types as values
        """
        # Get Objects folder
        objects_folder = self.client.get_objects_node()
        # Get Organize references to objects inside folder
        descriptions = objects_folder.get_references(ua.ObjectIds.Organizes, ua.BrowseDirection.Forward, ua.NodeClass.Object, False)
        for desc in descriptions:
            if desc.TypeDefinition == ua.TwoByteNodeId(ua.ObjectIds.FolderType):
                folder_name = desc.BrowseName.Name
                if folder_name == "Actuators" or folder_name == "Sensors":
                    # Get folder node
                    folder_node = self.get_node(desc.NodeId)
                    # Get all objects inside folder
                    objects = folder_node.get_children(ua.ObjectIds.Organizes, ua.NodeClass.Object)
                    for obj in objects:
                        # Get HasTypeDefinition references
                        ref = obj.get_references(ua.ObjectIds.HasTypeDefinition, ua.BrowseDirection.Forward, ua.NodeClass.ObjectType, False)[0]
                        custom_type = ref.BrowseName.Name
                        if custom_type in self.known_custom_types:
                            self.custom_objects[obj.nodeid] = custom_type

    def load_security_settings(self, uri):
        mysettings = self.settings.value("security_settings", None)
        if mysettings is not None and uri in mysettings:
            mode, policy, cert, key = mysettings[uri]
            self.security_mode = mode
            self.security_policy = policy
            self.certificate_path = cert
            self.private_key_path = key
        else:
            self.security_mode = "None"
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

    def load_subscription_settings(self, uri):
        mysettings = self.settings.value("subscription_settings", None)
        if mysettings is not None and uri in mysettings:
            pub_interval, max_keepalive_count, lifetime_count, max_notifications, priority = mysettings[uri]
            self.requestedPublishingInterval = pub_interval
            self.requestedMaxKeepAliveCount = max_keepalive_count
            self.requestedLifetimeCount = lifetime_count
            self.maxNotificationsPerPublish = max_notifications
            self.priority = priority
        else:
            self.requestedPublishingInterval = 500
            self.requestedMaxKeepAliveCount = 3000
            self.requestedLifetimeCount = 10000
            self.maxNotificationsPerPublish = 10000
            self.priority = 0

    def save_subscription_settings(self, uri):
        mysettings = self.settings.value("subscription_settings", None)
        if mysettings is None:
            mysettings = {}
        mysettings[uri] = [self.requestedPublishingInterval,
                           self.requestedMaxKeepAliveCount,
                           self.requestedLifetimeCount,
                           self.maxNotificationsPerPublish,
                           self.priority]
        self.settings.setValue("subscription_settings", mysettings)

    def load_monitored_items_settings(self, uri):
        mysettings = self.settings.value("monitored_items_settings", None)
        if mysettings is not None and uri in mysettings:
            sampling_interval, queue_size, discard_oldest, data_change_filter, trigger, deadband_type, deadband_value = mysettings[uri]
            self.samplingInterval = sampling_interval
            self.queueSize = queue_size
            self.discardOldest = discard_oldest
            self.dataChangeFilter = data_change_filter
            self.dataChangeTrigger = trigger
            self.deadbandType = deadband_type
            self.deadbandValue = deadband_value
        else:
            self.samplingInterval = 250
            self.queueSize = 0
            self.discardOldest = True
            self.dataChangeFilter = False
            self.dataChangeTrigger = ua.DataChangeTrigger.StatusValue
            self.deadbandType = ua.DeadbandType.None_
            self.deadbandValue = 0

    def save_monitored_items_settings(self, uri):
        mysettings = self.settings.value("monitored_items_settings", None)
        if mysettings is None:
            mysettings = {}
        mysettings[uri] = [self.samplingInterval,
                           self.queueSize,
                           self.discardOldest,
                           self.dataChangeFilter,
                           self.dataChangeTrigger,
                           self.deadbandType,
                           self.deadbandValue]
        self.settings.setValue("monitored_items_settings", mysettings)
