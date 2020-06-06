import logging

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon, QBrush, QColor
from PyQt5.QtWidgets import QMenu, QAction

from opcua import ua, Node

from utils import trycatchslot


logger = logging.getLogger("__main__")


class DataChangeUI(object):

    def __init__(self, window, uaclient, sub_handler):
        self.window = window
        self.uaclient = uaclient
        self._subhandler = sub_handler
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
            icon = QIcon("icons/level_indicator.svg")
        elif node.get_parent().get_type_definition() == ua.FourByteNodeId(1004, 1):
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
