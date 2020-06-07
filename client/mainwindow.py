import logging
import sys

from PyQt5.QtCore import QTimer, Qt, QSettings, QItemSelection, QCoreApplication
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon, QPixmap
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QMenu, QListWidgetItem

from opcua import ua

from widgets.attributes import AttrsWidget
from dialogs.call_method import CallMethodDialog
from logger import QtHandler
from widgets.variables import DataChangeCardUI
from widgets.subscriptions import DataChangeUI
from widgets.card import Ui_CardWidget
from widgets.references import RefsWidget
from widgets.tree import TreeWidget
from widgets.sub_handler import DataChangeHandler
from utils import trycatchslot, get_icon

from dialogs.options import OptionsDialog
from mainwindow_ui import Ui_MainWindow
from client import UaClient


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
        self.tree_ui = TreeWidget(self.ui.treeView, self.uaclient.custom_objects)
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
        self.sub_handler = DataChangeHandler()
        self.datachange_ui = DataChangeUI(self, self.uaclient, self.sub_handler, self.uaclient.custom_objects)
        self._contextMenu.addSeparator()
        self._contextMenu.addAction(self.ui.actionReload)
        self.ui.attrRefreshButton.clicked.connect(self.show_attrs)

        # Cards Widget
        self.datachangecards = []

        # Connection Buttons
        self.ui.connectButton.clicked.connect(self.handle_connect)
        # self.ui.treeView.expanded.connect(self._fit)
        self.ui.optionsButton.clicked.connect(self.show_options_dialog)

        # Main Window
        self.resize(int(self.settings.value("main_window_width", 800)), int(self.settings.value("main_window_height", 600)))
        data = self.settings.value("main_window_state", None)
        if data:
            self.restoreState(data)

    def show_cards(self):
        for nodeid, object_type in self.uaclient.custom_objects.items():
            cardWidget = QWidget()
            cardUi = Ui_CardWidget()
            cardUi.setupUi(cardWidget)

            model = QStandardItemModel()
            cardUi.variablesView.setModel(model)

            width = 80
            height = 80

            icon = get_icon(object_type)
            cardUi.icon.setPixmap(QPixmap(icon).scaled(width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            cardUi.icon.setAlignment(Qt.AlignCenter)

            variables = self.uaclient.get_node(nodeid).get_children()

            d_rows = []
            p_rows = []

            for var in variables:
                if var.get_node_class() == ua.NodeClass.Variable:
                    name = var.get_display_name().to_string()
                    value = str(var.get_value())
                    row = [QStandardItem(name), QStandardItem(value)]
                    row[0].setData(var)
                    # Data Variable
                    if var.get_type_definition() == ua.TwoByteNodeId(ua.ObjectIds.BaseDataVariableType):
                        d_rows.append(row)
                        datachangecard_ui = DataChangeCardUI(self, self.uaclient, self.sub_handler, model)
                        datachangecard_ui.subscribe(var, row[0])
                        self.datachangecards.append(datachangecard_ui)
                    else: # Property
                        p_rows.append(row)

            #model.appendRow([QStandardItem("Properties:")])
            # Append property rows
            for p_row in p_rows:
                model.appendRow(p_row)

            #model.appendRow([QStandardItem("Data:")])
            # Append data_variable rows
            for d_row in d_rows:
                model.appendRow(d_row)

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
        self.uaclient.find_custom_objects()
        self.show_cards()
        self.tree_ui.set_root_node(self.uaclient.client.get_root_node())
        self.ui.treeView.setFocus()
        self.load_current_node()
        self.ui.connectButton.setText("Disconnect")
        self.ui.connectButton.setEnabled(True)
        self.ui.optionsButton.setEnabled(False)
        self.ui.addrComboBox.setEnabled(False)

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
