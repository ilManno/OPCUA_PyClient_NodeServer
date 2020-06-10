import logging

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor

from opcua import ua, Node

from utils import trycatchslot


logger = logging.getLogger(__name__)


class DataChangeCardUI(object):

    def __init__(self, window, uaclient, sub_handler, model):
        self.window = window
        self.uaclient = uaclient
        self._subhandler = sub_handler
        self.subscribed_nodes = []
        self.model = model

        # handle subscriptions
        self._subhandler.data_change_fired.connect(self._update_subscription_model, type=Qt.QueuedConnection)

    def clear(self):
        self.subscribed_nodes = []
        # remove all rows but not header!!
        self.model.removeRows(0, self.model.rowCount())

    def show_error(self, *args):
        self.window.show_error(*args)

    @trycatchslot
    def subscribe(self, node, variable):
        if node in self.subscribed_nodes:
            logger.warning("already subscribed to node: %s ", node)
            return
        self.subscribed_nodes.append(node)
        try:
            self.uaclient.subscribe_datachange(node, self._subhandler)
        except Exception as ex:
            self.window.show_error(ex)
            idx = self.model.indexFromItem(variable)
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

    def _update_subscription_model(self, node, value, status_code):
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
            i += 1
