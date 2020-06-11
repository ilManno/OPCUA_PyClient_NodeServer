import logging

from PyQt5.QtCore import pyqtSignal, QObject, QSettings, Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QMenu, QAction

from opcua import ua, Node

from utils import trycatchslot


logger = logging.getLogger(__name__)


class RefsWidget(QObject):

    error = pyqtSignal(Exception)
    reference_changed = pyqtSignal(Node)

    def __init__(self, view):
        super().__init__(view)
        self.view = view
        self.model = QStandardItemModel()

        self.view.setModel(self.model)
        self.settings = QSettings()
        self.model.setHorizontalHeaderLabels(['ReferenceType', 'NodeId', "BrowseName", "TypeDefinition"])
        state = self.settings.value("WindowState/refs_widget_state", None)
        if state is not None:
            self.view.horizontalHeader().restoreState(state)
        self.node = None

        self.reloadAction = QAction("Reload", self.model)
        self.reloadAction.triggered.connect(self.reload)

        self.view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.view.customContextMenuRequested.connect(self.showContextMenu)
        self._contextMenu = QMenu()
        self._contextMenu.addAction(self.reloadAction)

    def showContextMenu(self, position):
        if not self.node:
            return
        self._contextMenu.exec_(self.view.viewport().mapToGlobal(position))

    def clear(self):
        # remove all rows but not header
        self.model.removeRows(0, self.model.rowCount())
        self.node = None

    @trycatchslot
    def reload(self):
        node = self.node
        self.clear()
        self.show_refs(node)

    def save_state(self):
        self.settings.setValue("WindowState/refs_widget_state", self.view.horizontalHeader().saveState())

    def show_refs(self, node):
        self.clear()
        self.node = node
        self._show_refs(node)

    def _show_refs(self, node):
        try:
            refs = node.get_children_descriptions(refs=ua.ObjectIds.References)
        except Exception as ex:
            self.error.emit(ex)
            raise
        for ref in refs:
            self._add_ref_row(ref)

    def _add_ref_row(self, ref):
        if ref.ReferenceTypeId.Identifier in ua.ObjectIdNames:
            typename = ua.ObjectIdNames[ref.ReferenceTypeId.Identifier]
        else:
            typename = str(ref.ReferenceTypeId)
        if ref.NodeId.NamespaceIndex == 0 and ref.NodeId.Identifier in ua.ObjectIdNames:
            nodeid = ua.ObjectIdNames[ref.NodeId.Identifier]
        else:
            nodeid = ref.NodeId.to_string()
        if ref.TypeDefinition.Identifier in ua.ObjectIdNames:
            typedef = ua.ObjectIdNames[ref.TypeDefinition.Identifier]
        else:
            typedef = ref.TypeDefinition.to_string()
        titem = QStandardItem(typename)
        titem.setData(ref, Qt.UserRole)
        self.model.appendRow([
            titem,
            QStandardItem(nodeid),
            QStandardItem(ref.BrowseName.to_string()),
            QStandardItem(typedef)
        ])
