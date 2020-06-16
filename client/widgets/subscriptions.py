from datetime import datetime
import logging

from PyQt5.QtCore import Qt, QObject, pyqtSignal, QItemSelection
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon, QBrush, QColor
from PyQt5.QtWidgets import QMenu, QAction, QWidget, QGridLayout, QTableView, QAbstractItemView

from opcua import ua, Node

from utils import trycatchslot, get_icon

logger = logging.getLogger(__name__)


class SubTab(QWidget):

    def __init__(self):
        super().__init__()

        self.gridLayout = QGridLayout(self)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(6)

        self.subView = QTableView(self)
        self.subView.setAcceptDrops(True)
        self.subView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.subView.setDragDropOverwriteMode(False)
        self.subView.setDragDropMode(QAbstractItemView.DropOnly)
        self.subView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.subView.horizontalHeader().setStretchLastSection(True)

        self.gridLayout.addWidget(self.subView, 0, 0, 1, 1)


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

    def __init__(self, window, uaclient, view):
        self.window = window
        self.uaclient = uaclient
        self._subhandler = DataChangeHandler()
        self.subscribed_nodes = []

        self.view = view
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["ObjectName", "VariableName", "Value", "Timestamp"])
        self.view.setModel(self.model)
        self.view.setColumnWidth(1, 150)

        # handle subscriptions
        self._subhandler.data_change_fired.connect(self._update_subscription_model, type=Qt.QueuedConnection)

        # accept drops
        self.model.canDropMimeData = self.canDropMimeData
        self.model.dropMimeData = self.dropMimeData

        # Context menu
        self.view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.view.customContextMenuRequested.connect(self.showContextMenu)
        actionDeleteMonitoredItem = QAction("Delete Monitored Item", self.model)
        actionDeleteMonitoredItem.triggered.connect(self._delete_monitored_item_context)
        self._contextMenu = QMenu()
        self._contextMenu.addAction(actionDeleteMonitoredItem)

        self.view.selectionModel().selectionChanged.connect(self.highlight_node)

    def highlight_node(self, selection):
        if isinstance(selection, QItemSelection):
            if not selection.indexes():  # no selection
                return
        idx = self.view.currentIndex()
        idx = idx.siblingAtColumn(0)
        it = self.model.itemFromIndex(idx)
        if not it:
            return
        node = it.data()
        self.window.tree_ui.expand_to_node(node)

    def canDropMimeData(self, mdata, action, row, column, parent):
        node = self.uaclient.client.get_node(mdata.text())
        if node.get_node_class() == ua.NodeClass.Variable:
            return True
        return False

    def dropMimeData(self, mdata, action, row, column, parent):
        node = self.uaclient.client.get_node(mdata.text())
        self.window.add_monitored_item(node)
        return True

    def showContextMenu(self, position):
        item = self.get_current_item()
        if item:
            self._contextMenu.exec_(self.view.viewport().mapToGlobal(position))

    def get_current_item(self, col_idx=0):
        idx = self.view.currentIndex()
        idx = idx.siblingAtColumn(col_idx)
        return self.model.itemFromIndex(idx)

    def _delete_monitored_item_context(self):
        it = self.get_current_item()
        if it:
            index = self.window.ui.tabWidget.currentIndex()
            self.delete_monitored_item(index, it.data())

    def clear(self):
        self.subscribed_nodes = []
        # remove all rows but not header
        self.model.removeRows(0, self.model.rowCount())

    def show_error(self, *args):
        self.window.show_error(*args)

    def create_subscription(self):
        self.uaclient.create_subscription(self._subhandler)

    def delete_subscription(self, index):
        self.uaclient.delete_subscription(index)

    @trycatchslot
    def add_monitored_item(self, index, node):
        variable_name = node.get_display_name().Text
        descriptions = node.get_references(ua.ObjectIds.Aggregates, ua.BrowseDirection.Inverse, ua.NodeClass.Object, True)
        parent_node = node
        while not descriptions:
            parent_node = parent_node.get_parent()
            descriptions = parent_node.get_references(ua.ObjectIds.Aggregates, ua.BrowseDirection.Inverse, ua.NodeClass.Object, True)
        parent_nodeid = descriptions[0].NodeId
        if parent_nodeid in self.uaclient.custom_objects:
            custom_type = self.uaclient.custom_objects[parent_nodeid]
            icon = get_icon(custom_type)
        else:
            icon = "icons/object.svg"
        row = [QStandardItem(QIcon(icon), descriptions[0].DisplayName.Text), QStandardItem(variable_name), QStandardItem("No Data yet"), QStandardItem("")]
        row[0].setData(node)
        row[0].setData(self.window.get_monitored_item_tooltip(), Qt.ToolTipRole)
        self.model.appendRow(row)
        self.subscribed_nodes.append(node)
        try:
            self.uaclient.create_monitored_items(node, index)
            self.model.sort(0, Qt.AscendingOrder)
            self._color_rows()
        except Exception as ex:
            self.window.show_error(ex)
            idx = self.model.indexFromItem(row[0])
            self.model.takeRow(idx.row())
            self.subscribed_nodes.remove(node)
            raise

    def _color_rows(self):
        n_rows = self.model.rowCount()
        if n_rows > 1:
            change_color = False
            for row in range(1, n_rows):
                prev_object_name = self.model.data(self.model.index(row - 1, 0))
                curr_object_name = self.model.data(self.model.index(row, 0))
                if curr_object_name != prev_object_name:
                    change_color = not change_color
                if change_color:
                    color = QColor(240, 240, 240)  # grey
                else:
                    color = QColor(255, 255, 255)  # white
                for col in range(self.model.columnCount()):
                    item = self.model.item(row, col)
                    item.setData(QBrush(color), Qt.BackgroundRole)

    @trycatchslot
    def delete_monitored_item(self, index, node=None):
        if not isinstance(node, Node):
            node = self.window.get_current_node()
        if node is None:
            return
        self.uaclient.remove_monitored_item(node, index)
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
                it = self.model.item(i, 2)
                it.setText(value)
                if status_code == ua.StatusCodes.Good:
                    it.setForeground(QBrush(QColor("green")))
                elif status_code == ua.StatusCodes.Uncertain:
                    it.setForeground(QBrush(QColor("yellow")))
                else:  # StatusCode = Bad:
                    it.setForeground(QBrush(QColor("red")))
                it_ts = self.model.item(i, 3)
                it_ts.setText(timestamp)
            i += 1
