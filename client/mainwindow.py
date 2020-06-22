import logging
import sys

from PyQt5.QtCore import QTimer, Qt, QSettings, QItemSelection, QCoreApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QMenu, QTabBar

from opcua import ua, Node

from widgets.attributes import AttrsWidget
from dialogs.call_method import CallMethodDialog
from logger import QtHandler
from widgets.subscriptions import SubTab, DataChangeUI
from widgets.references import RefsWidget
from widgets.tree import TreeWidget
from utils import trycatchslot

from dialogs.connect_settings import ConnectSettingsDialog
from dialogs.sub_settings import SubSettingsDialog
from dialogs.mi_settings import MiSettingsDialog
from mainwindow_ui import Ui_MainWindow
from opc_ua_client import OpcUaClient

logger = logging.getLogger(__name__)


class Window(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # fix stuff impossible to do in qtdesigner
        # remove dock titlebar for addressbar
        w = QWidget()
        self.ui.addrDockWidget.setTitleBarWidget(w)
        # add view actions in menu bar
        self.ui.menuView.addAction(self.ui.treeDockWidget.toggleViewAction())
        self.ui.menuView.addAction(self.ui.attrDockWidget.toggleViewAction())
        self.ui.menuView.addAction(self.ui.refDockWidget.toggleViewAction())
        self.ui.menuView.addAction(self.ui.logDockWidget.toggleViewAction())

        # we only show statusbar in case of errors
        self.ui.statusBar.hide()

        # setup QSettings for application and get a settings object
        QCoreApplication.setOrganizationName("UniCT")
        QCoreApplication.setApplicationName("OpcUaClient")
        self.settings = QSettings()
        self._address_list = self.settings.value("address_list", ["opc.tcp://localhost:4334/UA/NodeServer",
                                                                  "opc.tcp://localhost:51210/UA/SampleServer",
                                                                  "Clear all..."])
        print("ADR", self._address_list)
        self._address_list_max_count = int(self.settings.value("address_list_max_count", 10))

        self.opc_ua_client = OpcUaClient()

        # URL ComboBox
        address_list_len = len(self._address_list)
        for index in range(address_list_len):
            self.ui.addrComboBox.insertItem(index, self._address_list[index])
            icon = "icons/server.svg" if index < address_list_len - 1 else "icons/x.svg"
            self.ui.addrComboBox.setItemIcon(index, QIcon(icon))

        self.ui.addrComboBox.currentTextChanged.connect(self.clear_addresses)
        self.ui.addrComboBox.lineEdit().returnPressed.connect(self.handle_connect)
        self.ui.addrComboBox.setCompleter(None)

        # Objects Tree
        self.tree_ui = TreeWidget(self.ui.treeView, self.opc_ua_client.custom_objects)
        self.tree_ui.error.connect(self.show_error)
        self.setup_context_menu_tree()
        self.ui.treeView.selectionModel().selectionChanged.connect(self.show_refs)
        self.ui.treeView.selectionModel().selectionChanged.connect(self.show_attrs)

        # Context Menu
        self.ui.actionCopyPath.triggered.connect(self.tree_ui.copy_path)
        self.ui.actionCopyNodeId.triggered.connect(self.tree_ui.copy_nodeid)
        self.ui.actionCall.triggered.connect(self.call_method)
        self.ui.actionReload.triggered.connect(self.tree_ui.reload_current)
        self.ui.actionAddMonitoredItem.triggered.connect(self.add_monitored_item)
        self.ui.actionDeleteMonitoredItem.triggered.connect(self.delete_monitored_item)

        # populate contextual menu
        self.addAction(self.ui.actionAddMonitoredItem)
        self.addAction(self.ui.actionDeleteMonitoredItem)

        # References Widget
        self.refs_ui = RefsWidget(self.ui.refView)
        self.refs_ui.error.connect(self.show_error)

        # Attributes Widget
        self.attrs_ui = AttrsWidget(self.ui.attrView)
        self.attrs_ui.error.connect(self.show_error)
        self._contextMenu.addSeparator()
        self._contextMenu.addAction(self.ui.actionReload)
        self.ui.attrRefreshButton.clicked.connect(self.show_attrs)

        # Tabs Widget
        self.ui.tabWidget.tabBar().tabButton(0, QTabBar.RightSide).resize(0, 0)
        self.ui.tabWidget.setTabEnabled(0, False)
        self.ui.noSubLabel.hide()
        self.subTabs = []
        self.datachange_uis = []
        self.previous_index = -1
        self.ui.tabWidget.tabBarClicked.connect(self.add_sub_tab)
        self.ui.tabWidget.currentChanged.connect(self.restore_index)
        self.ui.tabWidget.tabCloseRequested.connect(self.remove_sub_tab)

        # Connection Buttons
        self.ui.connectButton.clicked.connect(self.handle_connect)
        # self.ui.treeView.expanded.connect(self._fit)
        self.ui.settingsButton.clicked.connect(self.show_connect_settings_dialog)

        # Main Window
        self.resize(int(self.settings.value("main_window_width", 800)),
                    int(self.settings.value("main_window_height", 600)))
        data = self.settings.value("main_window_state", None)
        if data:
            self.restoreState(data)

    def createPopupMenu(self):
        self.popup = QMenu()
        self.popup.addActions(self.ui.menuView.actions())
        return self.popup

    def add_sub_tab(self, index):
        if self.ui.tabWidget.isTabEnabled(index) and index == self.ui.tabWidget.count() - 1:
            uri = self.ui.addrComboBox.currentText()
            self.opc_ua_client.load_subscription_settings(uri)
            # Init Dialog with current settings
            dia = SubSettingsDialog(self.opc_ua_client.requestedPublishingInterval, self.opc_ua_client.requestedMaxKeepAliveCount,
                                    self.opc_ua_client.requestedLifetimeCount, self.opc_ua_client.maxNotificationsPerPublish,
                                    self.opc_ua_client.priority)
            ret = dia.exec_()
            if ret:
                self.opc_ua_client.requestedPublishingInterval, self.opc_ua_client.requestedMaxKeepAliveCount, \
                    self.opc_ua_client.requestedLifetimeCount, self.opc_ua_client.maxNotificationsPerPublish, \
                    self.opc_ua_client.priority = dia.get_selected_options()
                self.opc_ua_client.save_subscription_settings(uri)
                subTab = SubTab()
                self.ui.tabWidget.insertTab(index, subTab, f"Sub{index + 1}")
                self.ui.tabWidget.setTabToolTip(index, self.get_sub_tooltip())
                data_change_ui = DataChangeUI(self, self.opc_ua_client, subTab.subView)
                data_change_ui.create_subscription()
                self.subTabs.append(subTab)
                self.datachange_uis.append(data_change_ui)
            else:
                self.previous_index = self.get_current_tab_index()

    def restore_index(self, index):
        if index == self.ui.tabWidget.count() - 1 and self.previous_index != -1:
            self.ui.tabWidget.setCurrentIndex(self.previous_index)
            self.previous_index = -1

    def get_sub_tooltip(self):
        return f"PublishingInterval = {self.opc_ua_client.requestedPublishingInterval}\nKeepAliveCount = {self.opc_ua_client.requestedMaxKeepAliveCount}\nLifetimeCount = {self.opc_ua_client.requestedLifetimeCount}\nMaxNotificationsPerPublish = {self.opc_ua_client.maxNotificationsPerPublish}\nPriority = {self.opc_ua_client.priority}"

    def get_monitored_item_tooltip(self):
        tooltip = f"SamplingInterval = {self.opc_ua_client.samplingInterval}\nQueueSize = {self.opc_ua_client.queueSize}\nDiscardOldest = {self.opc_ua_client.discardOldest}\nDataChangeFilter = {self.opc_ua_client.dataChangeFilter}"
        if not self.opc_ua_client.dataChangeFilter:
            return tooltip
        datachange_trigger = ua.DataChangeTrigger(self.opc_ua_client.dataChangeTrigger).name
        deadband_type = ua.DeadbandType(self.opc_ua_client.deadbandType).name
        if deadband_type == "None_":
            filter_info = f"\nDataChangeTrigger = {datachange_trigger}\nDeadBandType = None"
        else:
            filter_info = f"\nDataChangeTrigger = {datachange_trigger}\nDeadBandType = {deadband_type}\nDeadBandValue = {self.opc_ua_client.deadbandValue}"
        return tooltip + filter_info

    def remove_sub_tab(self, index):
        self.datachange_uis[index].delete_subscription(index)
        del self.datachange_uis[index]
        self.ui.tabWidget.removeTab(index)
        del self.subTabs[index]
        if index == self.ui.tabWidget.count() - 1:
            self.ui.tabWidget.setCurrentIndex(index - 1)

    @trycatchslot
    def show_connect_settings_dialog(self):
        uri = self.ui.addrComboBox.currentText()
        try:
            # Query Endpoints
            endpoints = self.opc_ua_client.get_endpoints(uri)
            # Load security settings
            self.opc_ua_client.load_security_settings(uri)
            # Init Dialog with current settings
            dia = ConnectSettingsDialog(endpoints, self.opc_ua_client.security_mode, self.opc_ua_client.security_policy,
                                        self.opc_ua_client.certificate_path, self.opc_ua_client.private_key_path)
            ret = dia.exec_()
            if ret:
                self.opc_ua_client.security_mode, self.opc_ua_client.security_policy, self.opc_ua_client.certificate_path, self.opc_ua_client.private_key_path = dia.get_selected_options()
                self.opc_ua_client.save_security_settings(uri)
                self.connect()
        except Exception as ex:
            self.ui.addrComboBox.setFocus()
            self.show_error(ex)
            raise

    @trycatchslot
    def show_refs(self, selection):
        if isinstance(selection, QItemSelection):
            if not selection.indexes():  # no selection
                return
        node = self.get_current_node()
        if node:
            self.refs_ui.show_refs(node)

    @trycatchslot
    def show_attrs(self, selection):
        if isinstance(selection, QItemSelection):
            if not selection.indexes():  # no selection
                return
        node = self.get_current_node()
        if node:
            self.attrs_ui.show_attrs(node)

    def show_error(self, msg):
        logger.warning("showing error: %s")
        self.ui.statusBar.show()
        self.ui.statusBar.setStyleSheet("QStatusBar { background-color : red; color : black; }")
        self.ui.statusBar.showMessage(str(msg))
        QTimer.singleShot(1500, self.ui.statusBar.hide)

    def get_current_node(self, idx=None):
        return self.tree_ui.get_current_node(idx)

    def handle_connect(self):
        if self.ui.connectButton.text() == "Connect":
            self.connect()
        else:
            self.disconnect()

    @trycatchslot
    def connect(self):
        self.ui.connectButton.setText("Connecting...")
        self.ui.connectButton.setEnabled(False)
        self.ui.connectButton.repaint()
        uri = self.ui.addrComboBox.currentText()
        self.opc_ua_client.load_security_settings(uri)
        try:
            # Connect
            self.opc_ua_client.connect(uri)
            # Show widgets
            self._update_address_list(uri)
            self.opc_ua_client.load_custom_objects()
            self.tree_ui.set_root_node(self.opc_ua_client.client.get_root_node())
            self.ui.treeView.setFocus()
            self.load_current_node()
            self.ui.connectButton.setText("Disconnect")
            self.ui.connectButton.setEnabled(True)
            self.ui.settingsButton.setEnabled(False)
            self.ui.addrComboBox.setEnabled(False)
            self.ui.tabWidget.setTabEnabled(0, True)
            self.ui.noSubLabel.show()
        except Exception as ex:
            self.ui.connectButton.setText("Connect")
            self.ui.connectButton.setEnabled(True)
            self.ui.addrComboBox.setFocus()
            self.show_error(ex)
            raise

    def get_current_tab_index(self):
        return self.ui.tabWidget.currentIndex()

    def add_monitored_item(self, node=None):
        if not isinstance(node, Node):
            node = self.get_current_node()
            if node is None:
                return
        index = self.get_current_tab_index()
        if node in self.datachange_uis[index].subscribed_nodes:
            logger.warning("already subscribed to node: %s ", node)
            return
        uri = self.ui.addrComboBox.currentText()
        self.opc_ua_client.load_monitored_items_settings(uri)
        idx = self.ui.tabWidget.currentIndex()
        # Init Dialog with current settings
        dia = MiSettingsDialog(self.opc_ua_client.publishingIntervals[idx], self.opc_ua_client.queueSize,
                               self.opc_ua_client.discardOldest, self.opc_ua_client.dataChangeFilter,
                               self.opc_ua_client.dataChangeTrigger, self.opc_ua_client.deadbandType,
                               self.opc_ua_client.deadbandValue)
        ret = dia.exec_()
        if ret:
            self.opc_ua_client.samplingInterval, self.opc_ua_client.queueSize, self.opc_ua_client.discardOldest, \
                self.opc_ua_client.dataChangeFilter, self.opc_ua_client.dataChangeTrigger, self.opc_ua_client.deadbandType, \
                self.opc_ua_client.deadbandValue = dia.get_selected_options()
            self.opc_ua_client.save_monitored_items_settings(uri)
            self.datachange_uis[index].add_monitored_item(index, node)

    def delete_monitored_item(self):
        index = self.get_current_tab_index()
        self.datachange_uis[index].delete_monitored_item(index)

    def _update_address_list(self, uri):
        if uri in self._address_list:
            self._address_list.remove(uri)
        self._address_list.insert(0, uri)
        if len(self._address_list) > self._address_list_max_count:
            self._address_list.pop(-2)
        # update combo box
        self.ui.addrComboBox.clear()
        address_list_len = len(self._address_list)
        for index in range(address_list_len):
            self.ui.addrComboBox.insertItem(index, self._address_list[index])
            icon = "icons/server.svg" if index < address_list_len - 1 else "icons/x.svg"
            self.ui.addrComboBox.setItemIcon(index, QIcon(icon))

    def clear_addresses(self, text):
        if text == "Clear all...":
            for _ in range(len(self._address_list) - 1):
                self._address_list.pop(0)
                self.ui.addrComboBox.removeItem(0)
            self.ui.addrComboBox.clearEditText()

    def disconnect(self):
        try:
            self.opc_ua_client.delete_subscriptions()
            self.opc_ua_client.disconnect()
        except Exception as ex:
            self.show_error(ex)
            raise
        finally:
            self.save_current_node()
            self.tree_ui.clear()
            self.attrs_ui.clear()
            self.refs_ui.clear()
            for _ in range(self.ui.tabWidget.count() - 1):
                self.ui.tabWidget.removeTab(0)
            self.datachange_uis = []
            self.subTabs = []
            self.ui.connectButton.setText("Connect")
            self.ui.settingsButton.setEnabled(True)
            self.ui.addrComboBox.setEnabled(True)
            self.ui.noSubLabel.hide()
            self.ui.tabWidget.setTabEnabled(0, False)
            self.ui.addrComboBox.setFocus()

    def closeEvent(self, event):
        self.tree_ui.save_state()
        self.attrs_ui.save_state()
        self.refs_ui.save_state()
        self.settings.setValue("main_window_width", self.size().width())
        self.settings.setValue("main_window_height", self.size().height())
        self.settings.setValue("main_window_state", self.saveState())
        self.settings.setValue("address_list", self._address_list)
        self.disconnect()
        event.accept()

    def save_current_node(self):
        current_node = self.get_current_node()
        if current_node:
            mysettings = self.settings.value("current_node", None)
            if mysettings is None:
                mysettings = {}
            uri = self.ui.addrComboBox.currentText()
            mysettings[uri] = current_node.nodeid.to_string()
            self.settings.setValue("current_node", mysettings)

    def load_current_node(self):
        mysettings = self.settings.value("current_node", None)
        if mysettings is None:
            return
        uri = self.ui.addrComboBox.currentText()
        if uri in mysettings:
            nodeid = ua.NodeId.from_string(mysettings[uri])
            node = self.opc_ua_client.client.get_node(nodeid)
            self.tree_ui.expand_to_node(node)

    def setup_context_menu_tree(self):
        self.ui.treeView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.treeView.customContextMenuRequested.connect(self._show_context_menu_tree)
        self._contextMenu = QMenu()
        self.addAction(self.ui.actionCopyPath)
        self.addAction(self.ui.actionCopyNodeId)
        self._contextMenu.addSeparator()
        self._contextMenu.addAction(self.ui.actionCall)
        self._contextMenu.addSeparator()

    def addAction(self, action):
        self._contextMenu.addAction(action)

    def _show_context_menu_tree(self, position):
        node = self.get_current_node()
        if node:
            self._update_actions_state(node)
            self._contextMenu.exec_(self.ui.treeView.viewport().mapToGlobal(position))

    @trycatchslot
    def _update_actions_state(self, node):
        # Method action
        self.ui.actionCall.setEnabled(node.get_node_class() == ua.NodeClass.Method)
        # DataChange actions
        if node.get_node_class() != ua.NodeClass.Variable or self.ui.tabWidget.count() == 1:
            self.ui.actionAddMonitoredItem.setEnabled(False)
            self.ui.actionDeleteMonitoredItem.setEnabled(False)
        else:
            index = self.get_current_tab_index()
            datachange_ui = self.datachange_uis[index]
            self.ui.actionAddMonitoredItem.setEnabled(node not in datachange_ui.subscribed_nodes)
            self.ui.actionDeleteMonitoredItem.setEnabled(not self.ui.actionAddMonitoredItem.isEnabled())

    def call_method(self):
        node = self.get_current_node()
        dia = CallMethodDialog(self, self.opc_ua_client.client, node)
        dia.show()


def main():
    app = QApplication(sys.argv)
    client = Window()
    handler = QtHandler(client.ui.logTextEdit)
    logging.getLogger().addHandler(handler)
    logging.getLogger(__name__).setLevel(logging.INFO)
    logging.getLogger("widgets").setLevel(logging.INFO)
    # logging.getLogger("opcua").setLevel(logging.INFO)  # to enable logging of ua client library

    client.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
