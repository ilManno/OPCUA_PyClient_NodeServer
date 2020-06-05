import logging
import sys
from datetime import datetime

from PyQt5.QtCore import pyqtSignal, QTimer, Qt, QObject, QSettings, QItemSelection, QCoreApplication
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon, QBrush, QColor, QPixmap
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QMenu, QAction, QListWidgetItem

from opcua import ua, Node

from widgets.attributes import AttrsWidget
from dialogs.call_method import CallMethodDialog
from logger import QtHandler
from widgets.card import Ui_CardWidget
from widgets.references import RefsWidget
from widgets.tree import TreeWidget
from utils import trycatchslot

from dialogs.options import OptionsDialog
from mainwindow_ui import Ui_MainWindow
from client import UaClient


logger = logging.getLogger(__name__)


class DataChangeHandler(QObject):
    data_change_fired = pyqtSignal(object, str, int, str)

    def datachange_notification(self, node, val, data):
        status_code = data.monitored_item.Value.StatusCode.value
        if data.monitored_item.Value.SourceTimestamp:
            timestamp = data.monitored_item.Value.SourceTimestamp.isoformat()
        elif data.monitored_item.Value.ServerTimestamp:
            timestamp = data.monitored_item.Value.ServerTimestamp.isoformat()
        else:
            timestamp = datetime.now().isoformat()
        self.data_change_fired.emit(node, str(val), status_code, timestamp)


class DataChangeUI(object):

    def __init__(self, window, uaclient):
        self.window = window
        self.uaclient = uaclient
        self._subhandler = DataChangeHandler()
        self.subscribed_nodes = []
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["DisplayName", "Value", "Timestamp"])
        self.window.ui.subView.setModel(self.model)
        self.window.ui.subView.setColumnWidth(1, 150)

        self.window.ui.actionSubscribeDataChange.triggered.connect(self._subscribe)
        self.window.ui.actionUnsubscribeDataChange.triggered.connect(self._unsubscribe)

        # populate contextual menu
        self.window.addAction(self.window.ui.actionSubscribeDataChange)
        self.window.addAction(self.window.ui.actionUnsubscribeDataChange)

        # handle subscriptions
        self._subhandler.data_change_fired.connect(self._update_subscription_model, type=Qt.QueuedConnection)
        
        # accept drops
        self.model.canDropMimeData = self.canDropMimeData
        self.model.dropMimeData = self.dropMimeData

        # Context menu
        self.window.ui.subView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.window.ui.subView.customContextMenuRequested.connect(self.showContextMenu)
        unsubscribeaction = QAction("Unsubscribe", self.model)
        unsubscribeaction.triggered.connect(self._unsubscribe_context)
        self._contextMenu = QMenu()
        self._contextMenu.addAction(unsubscribeaction)

    def canDropMimeData(self, mdata, action, row, column, parent):
        return True

    def dropMimeData(self, mdata, action, row, column, parent):
        node = self.uaclient.client.get_node(mdata.text())
        self._subscribe(node)
        return True

    def showContextMenu(self, position):
        item = self.get_current_item()
        if item:
            self._contextMenu.exec_(self.window.ui.subView.viewport().mapToGlobal(position))

    def get_current_item(self, col_idx=0):
        idx = self.window.ui.subView.currentIndex()
        idx = idx.siblingAtColumn(col_idx)
        return self.model.itemFromIndex(idx)

    def _unsubscribe_context(self):
        it = self.get_current_item()
        if it:
            self._unsubscribe(it.data())

    def clear(self):
        self.subscribed_nodes = []
        # remove all rows but not header!!
        self.model.removeRows(0, self.model.rowCount())

    def show_error(self, *args):
        self.window.show_error(*args)

    @trycatchslot
    def _subscribe(self, node=None):
        if not isinstance(node, Node):
            node = self.window.get_current_node()
            if node is None:
                return
        if node in self.subscribed_nodes:
            logger.warning("already subscribed to node: %s ", node)
            return
        text = str(node.get_display_name().Text)
        if node.get_parent().get_type_definition() == ua.FourByteNodeId(1002, 1):
            icon = QIcon("icons/temp_sensor.svg")
        elif node.get_parent().get_type_definition() == ua.FourByteNodeId(1003, 1):
            icon = QIcon("icons/flow_sensor.svg")
        elif node.get_parent().get_type_definition() == ua.FourByteNodeId(1006, 1):
            icon = QIcon("icons/boiler.svg")
        elif node.get_parent().get_type_definition() == ua.FourByteNodeId(1007, 1):
            icon = QIcon("icons/motor.svg")
        elif node.get_parent().get_type_definition() == ua.FourByteNodeId(1008, 1):
            icon = QIcon("icons/valve.svg")
        else:
            icon = QIcon("icons/object.svg")
        row = [QStandardItem(icon, text), QStandardItem("No Data yet"), QStandardItem("")]
        row[0].setData(node)
        self.model.appendRow(row)
        self.subscribed_nodes.append(node)
        try:
            self.uaclient.subscribe_datachange(node, self._subhandler)
        except Exception as ex:
            self.window.show_error(ex)
            idx = self.model.indexFromItem(row[0])
            self.model.takeRow(idx.row())
            raise

    @trycatchslot
    def _unsubscribe(self, node=None):
        if not isinstance(node, Node):
            node = self.window.get_current_node()
        if node is None:
            return
        self.uaclient.unsubscribe_datachange(node)
        self.subscribed_nodes.remove(node)
        i = 0
        while self.model.item(i):
            item = self.model.item(i)
            if item.data() == node:
                self.model.removeRow(i)
            i += 1

    def _update_subscription_model(self, node, value, status_code, timestamp):
        i = 0
        while self.model.item(i):
            item = self.model.item(i)
            if item.data() == node:
                it = self.model.item(i, 1)
                it.setText(value)
                if status_code == ua.StatusCodes.Good:
                    it.setForeground(QBrush(QColor("green")))
                elif status_code == ua.StatusCodes.Uncertain:
                    it.setForeground(QBrush(QColor("yellow")))
                else:  # StatusCode = Bad:
                    it.setForeground(QBrush(QColor("red")))
                it_ts = self.model.item(i, 2)
                it_ts.setText(timestamp)
            i += 1


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
                                                                  "Clear all..."])
        print("ADR", self._address_list)
        self._address_list_max_count = int(self.settings.value("address_list_max_count", 10))

        self.uaclient = UaClient()

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
        self.tree_ui = TreeWidget(self.ui.treeView)
        self.tree_ui.error.connect(self.show_error)
        self.setup_context_menu_tree()
        self.ui.treeView.selectionModel().selectionChanged.connect(self.show_refs)
        self.ui.treeView.selectionModel().selectionChanged.connect(self.show_attrs)

        # Context Menu
        self.ui.actionCopyPath.triggered.connect(self.tree_ui.copy_path)
        self.ui.actionCopyNodeId.triggered.connect(self.tree_ui.copy_nodeid)
        self.ui.actionCall.triggered.connect(self.call_method)
        self.ui.actionReload.triggered.connect(self.tree_ui.reload_current)

        # References Widget
        self.refs_ui = RefsWidget(self.ui.refView)
        self.refs_ui.error.connect(self.show_error)

        # Attributes Widget
        self.attrs_ui = AttrsWidget(self.ui.attrView)
        self.attrs_ui.error.connect(self.show_error)
        self.datachange_ui = DataChangeUI(self, self.uaclient)
        self._contextMenu.addSeparator()
        self._contextMenu.addAction(self.ui.actionReload)
        self.ui.attrRefreshButton.clicked.connect(self.show_attrs)

        # Connection Buttons
        self.ui.connectButton.clicked.connect(self.handle_connect)
        # self.ui.treeView.expanded.connect(self._fit)
        self.ui.optionsButton.clicked.connect(self.show_options_dialog)

        # Main Window
        self.resize(int(self.settings.value("main_window_width", 800)), int(self.settings.value("main_window_height", 600)))
        data = self.settings.value("main_window_state", None)
        if data:
            self.restoreState(data)

    def show_cards(self, custom_objects):
        for obj, custom_type in custom_objects:
            cardWidget = QWidget()
            cardUi = Ui_CardWidget()
            cardUi.setupUi(cardWidget)

            model = QStandardItemModel()
            cardUi.variablesView.setModel(model)

            if custom_type == "BoilerType":
                cardUi.icon.setPixmap(QPixmap("icons/boiler.svg").scaled(80, 80))
            elif custom_type == "MotorType":
                cardUi.icon.setPixmap(QPixmap("icons/motor.svg").scaled(80, 80))
            elif custom_type == "ValveType":
                cardUi.icon.setPixmap(QPixmap("icons/valve.svg").scaled(80, 80))
            elif custom_type == "TempSensorType":
                cardUi.icon.setPixmap(QPixmap("icons/temp_sensor.svg").scaled(80, 80))
            elif custom_type == "LevelIndicatorType":
                cardUi.icon.setPixmap(QPixmap("icons/flow_sensor.svg").scaled(80, 80))

            variables = obj.get_children()

            for var in variables:
                if var.get_node_class() == ua.NodeClass.Variable:
                    if var.get_type_definition() == ua.TwoByteNodeId(ua.ObjectIds.PropertyType):
                        # Read
                        print("Property")
                        cardUi.variablesView.addItem(var.get_display_name().to_string())
                        cardUi.variablesView.addItem(str(var.get_value()))
                    else:
                        print("Data Value")
                        # Subscribe
                        name = var.get_display_name().to_string()
                        value = str(var.get_value())
                        row = [QStandardItem(name), QStandardItem(value)]
                        row[0].setData(var)
                        model.appendRow(row)
                        #self.datachange_ui.subscribed_nodes.append(var)
                        #try:
                            #self.uaclient.subscribe_datachange(var, self.datachange_ui._subhandler)
                        #except Exception as ex:
                            #self.show_error(ex)
                            #idx = self.model.indexFromItem(row[0])
                            #self.model.takeRow(idx.row())
                            #raise

            item = QListWidgetItem()
            item.setSizeHint(cardWidget.sizeHint())
            self.ui.scadaWidget.addItem(item)
            self.ui.scadaWidget.setItemWidget(item, cardWidget)

    @trycatchslot
    def show_options_dialog(self):
        uri = self.ui.addrComboBox.currentText()
        try:
            # Query Endpoints
            endpoints = self.uaclient.get_endpoints(uri)
        except Exception as ex:
            self.show_error(ex)
            raise

        # Create dict of endpoints
        endpoints_dict = {"None_": set(), "Sign": set(), "SignAndEncrypt": set()}
        for edp in endpoints:
            mode = edp.SecurityMode.name
            policy = edp.SecurityPolicyUri.split("#")[1]
            endpoints_dict[mode].add(policy)
        # Load security settings
        self.uaclient.load_security_settings(uri)
        # Init Dialog with current settings
        dia = OptionsDialog(endpoints_dict, self.uaclient.security_mode, self.uaclient.security_policy, self.uaclient.certificate_path, self.uaclient.private_key_path)
        ret = dia.exec_()
        if ret:
            self.uaclient.security_mode, self.uaclient.security_policy, self.uaclient.certificate_path, self.uaclient.private_key_path = dia.get_selected_options()
            self.uaclient.save_security_settings(uri)
            self.handle_connect()

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
        self.uaclient.load_security_settings(uri)
        try:
            self.uaclient.connect(uri)
        except Exception as ex:
            self.ui.connectButton.setText("Connect")
            self.ui.connectButton.setEnabled(True)
            self.show_error(ex)
            raise

        self._update_address_list(uri)
        self.tree_ui.set_root_node(self.uaclient.client.get_root_node())
        self.ui.treeView.setFocus()
        self.load_current_node()
        self.ui.connectButton.setText("Disconnect")
        self.ui.connectButton.setEnabled(True)
        self.ui.optionsButton.setEnabled(False)
        self.ui.addrComboBox.setEnabled(False)
        custom_objects = self.uaclient.get_custom_objects()
        self.show_cards(custom_objects)

    def _update_address_list(self, uri):
        if uri in self._address_list:
            self._address_list.remove(uri)
        self._address_list.insert(0, uri)
        if len(self._address_list) > self._address_list_max_count:
            self._address_list.pop(-1)
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
            self.uaclient.delete_subscription()
            self.uaclient.disconnect()
        except Exception as ex:
            self.show_error(ex)
            raise
        finally:
            self.save_current_node()
            self.tree_ui.clear()
            self.attrs_ui.clear()
            self.refs_ui.clear()
            self.datachange_ui.clear()
            self.ui.scadaWidget.clear()
            self.ui.connectButton.setText("Connect")
            self.ui.optionsButton.setEnabled(True)
            self.ui.addrComboBox.setEnabled(True)

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
            node = self.uaclient.client.get_node(nodeid)
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
        if node.get_node_class() != ua.NodeClass.Variable:
            self.ui.actionSubscribeDataChange.setEnabled(False)
            self.ui.actionUnsubscribeDataChange.setEnabled(False)
        else:
            self.ui.actionSubscribeDataChange.setEnabled(node not in self.datachange_ui.subscribed_nodes)
            self.ui.actionUnsubscribeDataChange.setEnabled(not self.ui.actionSubscribeDataChange.isEnabled())

    def call_method(self):
        node = self.get_current_node()
        dia = CallMethodDialog(self, self.uaclient.client, node)
        dia.show()


def main():
    app = QApplication(sys.argv)
    client = Window()
    handler = QtHandler(client.ui.logTextEdit)
    logging.getLogger().addHandler(handler)
    logging.getLogger(__name__).setLevel(logging.INFO)
    logging.getLogger("uawidgets").setLevel(logging.INFO)
    # logging.getLogger("opcua").setLevel(logging.INFO)  # to enable logging of ua client library
   
    client.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
