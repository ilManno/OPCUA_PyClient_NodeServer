import logging

from PyQt5.QtCore import pyqtSignal, Qt, QObject, QSettings
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QBrush, QColor
from PyQt5.QtWidgets import QApplication, QMenu, QAction, QAbstractItemView

from opcua import ua
from opcua.common.ua_utils import val_to_string, data_type_to_string


logger = logging.getLogger(__name__)


class _Data(object):
    def is_editable(self):
        if self.uatype != ua.VariantType.ExtensionObject:
            return True
        return False


class AttributeData(_Data):
    def __init__(self, attr, value, uatype):
        self.attr = attr
        self.value = value
        self.uatype = uatype


class MemberData(_Data):
    def __init__(self, obj, name, value, uatype):
        self.obj = obj
        self.name = name
        self.value = value
        self.uatype = uatype


class ListData(_Data):
    def __init__(self, mylist, idx, val, uatype):
        self.mylist = mylist
        self.idx = idx
        self.value = val
        self.uatype = uatype


class AttrsWidget(QObject):

    error = pyqtSignal(Exception)
    attr_written = pyqtSignal(ua.AttributeIds, ua.DataValue)

    def __init__(self, view, show_timestamps=True):
        super().__init__(view)
        self.view = view
        self._timestamps = show_timestamps
        self.settings = QSettings()
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['Attribute', 'Value', 'DataType'])
        state = self.settings.value("WindowState/attrs_widget_state", None)
        if state is not None:
            self.view.header().restoreState(state)
        self.view.setModel(self.model)
        self.current_node = None
        self.view.setColumnWidth(0, 150)
        self.view.setColumnWidth(1, 150)
        self.view.expanded.connect(self._item_expanded)
        self.view.collapsed.connect(self._item_collapsed)
        self.view.setEditTriggers(QAbstractItemView.DoubleClicked)

        # Context menu
        self.view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.view.customContextMenuRequested.connect(self.showContextMenu)
        copyaction = QAction("Copy Value", self.model)
        copyaction.triggered.connect(self._copy_value)
        self._contextMenu = QMenu()
        self._contextMenu.addAction(copyaction)

    def save_state(self):
        self.settings.setValue("WindowState/attrs_widget_state", self.view.header().saveState())

    def _item_expanded(self, idx):
        if not idx.parent().isValid():
            # only for value attributes which are childs
            # maybe add more tests
            return
        it = self.model.itemFromIndex(idx.sibling(0, 1))
        it.setText("")

    def _item_collapsed(self, idx):
        it = self.model.itemFromIndex(idx.sibling(0, 1))
        data = it.data(Qt.UserRole)
        it.setText(val_to_string(data.value))

    def showContextMenu(self, position):
        item = self.get_current_item()
        if item:
            self._contextMenu.exec_(self.view.viewport().mapToGlobal(position))

    def get_current_item(self, col_idx=0):
        idx = self.view.currentIndex()
        idx = idx.siblingAtColumn(col_idx)
        return self.model.itemFromIndex(idx)

    def _copy_value(self):
        it = self.get_current_item(1)
        if it:
            QApplication.clipboard().setText(it.text())

    def clear(self):
        # remove all rows but not header!!
        self.model.removeRows(0, self.model.rowCount())

    def reload(self):
        self.show_attrs(self.current_node)

    def show_attrs(self, node):
        self.current_node = node
        self.clear()
        if self.current_node:
            self._show_attrs()
        self.view.expandToDepth(0)

    def _show_attrs(self):
        attrs = self.get_all_attrs()
        for attr, dv in attrs:
            try:
                # try/except to show as many attributes as possible
                if attr == ua.AttributeIds.Value:
                    self._show_value_attr(attr, dv)
                else:
                    self._show_attr(attr, dv)
            except Exception as ex:
                logger.exception("Exception while displaying attribute %s with value %s for node %s", attr, dv, self.current_node)
                self.error.emit(ex)

    def _show_attr(self, attr, dv):
        if attr == ua.AttributeIds.DataType:
            # FIXME: Could query for browsename here, it does not cost much
            string = data_type_to_string(dv.Value.Value)
        elif attr in (ua.AttributeIds.AccessLevel,
                      ua.AttributeIds.UserAccessLevel,
                      ua.AttributeIds.WriteMask,
                      ua.AttributeIds.UserWriteMask,
                      ua.AttributeIds.EventNotifier):
            string = enum_to_string(attr, dv.Value.Value)
        else:
            string = val_to_string(dv.Value.Value)
        name_item = QStandardItem(attr.name)
        vitem = QStandardItem(string)
        vitem.setData(AttributeData(attr, dv.Value.Value, dv.Value.VariantType), Qt.UserRole)
        self.model.appendRow([name_item, vitem, QStandardItem(dv.Value.VariantType.name)])

    def _show_value_attr(self, attr, dv):
        name_item = QStandardItem("Value")
        vitem = QStandardItem()
        items = self._show_val(name_item, None, "Value", dv.Value.Value, dv.Value.VariantType, dv.StatusCode.value)
        items[1].setData(AttributeData(attr, dv.Value.Value, dv.Value.VariantType), Qt.UserRole)
        row = [name_item, vitem, QStandardItem(dv.Value.VariantType.name)]
        self.model.appendRow(row)
        self._show_timestamps(name_item, dv)

    def _show_val(self, parent, obj, name, val, vtype, status_code=None):
        name_item = QStandardItem(name)
        vitem = QStandardItem()
        vitem.setText(val_to_string(val))
        vitem.setData(MemberData(obj, name, val, vtype), Qt.UserRole)
        row = [name_item, vitem, QStandardItem(vtype.name)]
        # Color value according to status code
        if status_code is not None:
            if status_code == ua.StatusCodes.Good:
                vitem.setForeground(QBrush(QColor("green")))
            elif status_code == ua.StatusCodes.Uncertain:
                vitem.setForeground(QBrush(QColor("yellow")))
            else:  # StatusCode = Bad:
                vitem.setForeground(QBrush(QColor("red")))
        # if we have a list or extension object we display children
        if isinstance(val, list):
            row[2].setText("List of " + vtype.name)
            self._show_list(name_item, val, vtype)
        elif vtype == ua.VariantType.ExtensionObject:
            self._show_ext_obj(name_item, val)
        parent.appendRow(row)
        return row

    def _show_list(self, parent, mylist, vtype):
        for idx, val in enumerate(mylist):
            name_item = QStandardItem(str(idx))
            vitem = QStandardItem()
            vitem.setText(val_to_string(val))
            vitem.setData(ListData(mylist, idx, val, vtype), Qt.UserRole)
            row = [name_item, vitem, QStandardItem(vtype.name)]
            parent.appendRow(row)
            if vtype == ua.VariantType.ExtensionObject:
                self._show_ext_obj(name_item, val)
    
    def refresh_list(self, parent, mylist, vtype):
        while parent.hasChildren():
            self.model.removeRow(0, parent.index())
        self._show_list(parent, mylist, vtype)

    def _show_ext_obj(self, item, val):
        item.setText(item.text() + ": " + val.__class__.__name__)
        for att_name, att_type in val.ua_types:
            member_val = getattr(val, att_name)
            if att_type.startswith("ListOf"):
                att_type = att_type[6:]
            attr = getattr(ua.VariantType, att_type)
            self._show_val(item, val, att_name, member_val, attr)

    def _show_timestamps(self, item, dv):
        #while item.hasChildren():
            #self.model.removeRow(0, item.index())
        string = val_to_string(dv.ServerTimestamp)
        item.appendRow([QStandardItem("Server Timestamp"), QStandardItem(string), QStandardItem(ua.VariantType.DateTime.name)])
        string = val_to_string(dv.SourceTimestamp)
        item.appendRow([QStandardItem("Source Timestamp"), QStandardItem(string), QStandardItem(ua.VariantType.DateTime.name)])

    def get_all_attrs(self):
        attrs = [attr for attr in ua.AttributeIds]
        dvs = self.current_node.get_attributes(attrs)
        res = []
        for idx, dv in enumerate(dvs):
            if dv.StatusCode.is_good() or (attrs[idx] == ua.AttributeIds.Value and (dv.StatusCode.value == ua.StatusCodes.Uncertain or dv.StatusCode.value == ua.StatusCodes.Bad)):
                res.append((attrs[idx], dv))
        res.sort(key=lambda x: x[0].name)
        return res


def attr_to_enum(attr):
    attr_name = attr.name
    if attr_name.startswith("User"):
        attr_name = attr_name[4:]
    return getattr(ua, attr_name)


def enum_to_string(attr, val):
    attr_enum = attr_to_enum(attr)
    string = ", ".join([e.name for e in attr_enum.parse_bitfield(val)])
    return string
