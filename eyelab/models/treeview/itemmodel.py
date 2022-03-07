from PySide6 import Qt, QtCore, QtWidgets
from PySide6.QtCore import QAbstractItemModel

from eyelab.models.treeview.areaitem import TreeAreaItem
from eyelab.models.treeview.lineitem import TreeLineItem
from eyelab.models.treeview.itemgroup import ItemGroup

import eyepy as ep


class TreeItemModel(QAbstractItemModel):
    def __init__(self, data, parent=None, *args, **kwargs):
        super().__init__(*args, **kwargs, parent=parent)
        self._data = data
        self.root_item = ItemGroup()

        self.area_root = ItemGroup(name="Areas")
        self.appendRow(self.area_root)
        self.area_index = QtCore.QPersistentModelIndex(self.index(0, 0))

    def show(self):
        self.root_item.show()

    def hide(self):
        self.root_item.hide()

    def rowCount(self, parent=QtCore.QModelIndex(), *args, **kwargs):
        parent_item = self.getItem(parent)
        if type(parent_item) in [TreeLineItem, TreeAreaItem]:
            return 0
        return parent_item.childCount()

    def columnCount(self, parent=QtCore.QModelIndex(), *args, **kwargs):
        return self.root_item.columnCount()

    def data(self, index: QtCore.QModelIndex(), role=None):
        if role == QtCore.Qt.EditRole:
            item = self.getItem(index)
            if type(item) is ItemGroup:
                item_data = {
                    key: item.data(key) for key in ["visible", "z_value", "name"]
                }
            else:
                item_data = {
                    key: item.data(key)
                    for key in ["current_color", "visible", "z_value", "name"]
                }
            return item_data

        if role == QtCore.Qt.DisplayRole:
            pass

    def index(self, row, column, parent=QtCore.QModelIndex(), *args, **kwargs):
        if not parent.isValid():
            parent_item = self.root_item
        else:
            parent_item = parent.internalPointer()

        child_item = parent_item.child(row)
        if child_item:
            return self.createIndex(row, column, child_item)
        return QtCore.QModelIndex()

    def parent(self, index: QtCore.QModelIndex):
        if not index.isValid():
            return QtCore.QModelIndex()

        childItem = self.getItem(index)
        parentItem = childItem.parentItem()

        if parentItem is None:
            return QtCore.QModelIndex()

        return self.createIndex(parentItem.childNumber(), 0, parentItem)

    def get_annotations(self):
        self._get_area_annotations()

    def _get_area_annotations(self):
        raise NotImplementedError
        # for name in self._data.area_maps:
        #    item = TreeAreaItem(self._data, name)
        #    self.appendRow(item, parent=QtCore.QModelIndex(self.area_index))

    def headerData(self, column, Qt_Orientation, role=None):
        if role != QtCore.Qt.DisplayRole:
            return None
        return [str(x) for x in range(8)][column]

    def getItem(self, index: QtCore.QModelIndex):
        if index.isValid():
            item = index.internalPointer()
            if item:
                return item
        return self.root_item

    def flags(self, index: QtCore.QModelIndex()):
        if not index.isValid():
            return QtCore.Qt.NoItemFlags

        return QtCore.Qt.ItemIsEditable | QAbstractItemModel.flags(self, index)

    # Provide support for editing and resizing

    def setData(self, index: QtCore.QModelIndex, value, role=None):
        if role == QtCore.Qt.EditRole:
            item = self.getItem(index)
            if type(item) is ItemGroup:
                for k, v in {
                    "visible": value.visible,
                    "name": value.label.text(),
                }.items():
                    item.setData(k, v)
                return True
            else:
                for k, v in {
                    "current_color": value.color,
                    "visible": value.visible,
                    "name": value.label.text(),
                }.items():
                    item.setData(k, v)
                return True
        return False

    @property
    def scene(self):
        return self.root_item.scene()

    def appendRow(self, data, parent=QtCore.QModelIndex()):
        self.beginInsertRows(parent, self.rowCount(parent), self.rowCount(parent))
        self.getItem(parent).appendChild(data)
        self.endInsertRows()

        if self.scene:
            self.scene.update()

    def switchRows(self, row1, row2, parent=QtCore.QModelIndex()):
        self.beginMoveRows(parent, row1, row1, parent, row2 + 1)
        self.getItem(parent).switchChildren(row1, row2)
        self.endMoveRows()
        if self.scene:
            self.scene.update()

    def removeRows(self, row, count, parent=QtCore.QModelIndex()):
        if parent.isValid() and parent.internalPointer() != self.root_item:
            self.beginRemoveRows(parent, row, row + count - 1)
            parent = self.getItem(parent)
            parent.removeChildren(row, count)
            self.endRemoveRows()
            if self.scene:
                self.scene.update()
            return True
        return False


class BscanTreeItemModel(TreeItemModel):
    def __init__(self, data: ep.EyeBscan, parent, *args, **kwargs):
        super().__init__(*args, **kwargs, data=data, parent=parent)

        self.line_root = ItemGroup(name="Lines")
        self.appendRow(self.line_root)
        self.line_index = QtCore.QPersistentModelIndex(self.index(1, 0))

        self.get_annotations()

    def get_annotations(self):
        self._get_area_annotations()
        self._get_line_annotations()

    def _get_area_annotations(self):
        for name, vm in self._data.volume.volume_maps.items():
            item = TreeAreaItem(data=vm.data[self._data.index], meta=vm.meta)
            self.appendRow(item, parent=QtCore.QModelIndex(self.area_index))

    def _get_line_annotations(self):
        for name in self._data.volume.layers:
            item = TreeLineItem(data=self._data.layers[name])
            self.appendRow(item, parent=QtCore.QModelIndex(self.line_index))


class EnfaceTreeItemModel(TreeItemModel):
    def __init__(self, data: ep.EyeEnface, parent, *args, **kwargs):
        super().__init__(*args, **kwargs, data=data, parent=parent)
        self.get_annotations()

    def get_annotations(self):
        self._get_area_annotations()

    def _get_area_annotations(self):
        for name, am in self._data.area_maps.items():
            item = TreeAreaItem(data=am._data, meta=am.meta)
            self.appendRow(item, parent=QtCore.QModelIndex(self.area_index))
