import collections
from typing import Union

import eyepy as ep
import numpy as np
from eyepy.core.utils import DynamicDefaultDict
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import QAbstractItemModel

from eyelab.dialogs import AddAnnotationDialog
from eyelab.models.scene import CustomGraphicsScene
from eyelab.models.treeview.areaitem import AreaItem
from eyelab.models.treeview.itemgroup import ItemGroup
from eyelab.models.treeview.layeritem import LayerItem


class TreeItemGroup:
    def __init__(self, meta: dict, parent=None):
        self.itemData = meta
        self.parent = parent
        self.childItems = []

    def childNumber(self):
        if self.parent:
            return self.parent.childItems.index(self)
        return 0

    def child(self, number: int):
        if number < 0 or number > self.childCount() - 1:
            return None
        return self.childItems[number]

    def childCount(self):
        return len(self.childItems)

    def columnCount(self):
        return 1

    def data(self, column: str):
        if column in self.itemData:
            return self.itemData[column]
        raise Exception(f"column {column} not in data")

    def setData(self, column: str, value):
        if column in self.itemData:
            self.itemData[column] = value
            return True
        return False

    def appendChild(self, new_item: Union["TreeItem", "TreeItemGroup"]):
        items = self.childItems

        if items:
            z_value = float(items[-1].data("z_value") + 1)
        else:
            z_value = 0.0

        new_item.z_value = z_value

        new_item.parent = self
        self.childItems.append(new_item)

    def removeChildren(self, row: int, count: int):
        # Remove in reverse order to avoid index shifting issues
        for i in range(row + count - 1, row - 1, -1):
            self.childItems.pop(i)

    def switchChildren(self, row1: int, row2: int):
        child1 = self.child(row1)
        child2 = self.child(row2)

        child1_z = child1.data("z_value")
        child2_z = child2.data("z_value")
        child1.setData("z_value", child2_z)
        child2.setData("z_value", child1_z)


class TreeItem(TreeItemGroup):
    def __init__(self, data, parent=None):
        self.itemData = data.meta
        self.annotation = data
        self.parent = parent

    def childNumber(self):
        if self.parent:
            return self.parent.childItems.index(self)
        return 0

    def child(self, number: int):
        return None

    def childCount(self):
        return 0

    def data(self, column: str):
        if column in self.itemData:
            return self.itemData[column]
        raise Exception(f"column {column} not in data")

    def setData(self, column: str, value):
        if column == "name":
            self.itemData.name = value
            return True
        elif column in self.itemData:
            self.itemData[column] = value
            return True
        return False

    def appendChild(self, new_item):
        raise ValueError("You can only append childs to the TreeItemGroup")


class TreeItemModel(QtCore.QAbstractItemModel):
    def __init__(self, parent):
        super().__init__(parent=parent)

    def toggle_annotations(self):
        for row in range(self.tree_root.childCount()):
            index = self.index(row, 0)
            self.setData(index=index, data={"visible": not self.data(index)["visible"]})

    def rowCount(self, parent=QtCore.QModelIndex(), *args, **kwargs):
        parent_item = self.getItem(parent)
        return parent_item.childCount()

    def columnCount(self, parent=QtCore.QModelIndex(), *args, **kwargs):
        return self.tree_root.columnCount()

    def data(self, index: QtCore.QModelIndex, role=QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole:
            item = self.getItem(index)
            return item.itemData
        if role == QtCore.Qt.DisplayRole:
            pass

    def index(self, row, column, parent=QtCore.QModelIndex(), *args, **kwargs):
        if not parent.isValid():
            parent_item = self.tree_root
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
        parentItem = childItem.parent

        if parentItem is None:
            return QtCore.QModelIndex()

        return self.createIndex(parentItem.childNumber(), 0, parentItem)

    def headerData(self, column, Qt_Orientation, role=None):
        return None

    def getItem(self, index: QtCore.QModelIndex):
        if index.isValid():
            item = index.internalPointer()
            if item:
                return item
        return self.tree_root

    def flags(self, index: QtCore.QModelIndex):
        if not index.isValid():
            return QtCore.Qt.NoItemFlags

        return QtCore.Qt.ItemIsEditable | QAbstractItemModel.flags(self, index)

    # Provide support for editing and resizing
    def setData(self, index: QtCore.QModelIndex, data, role=QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole:
            item = self.getItem(index)
            for k in data:
                item.itemData[k] = data[k]
            self.dataChanged.emit(index, index)
            return True
        return False

    def appendRow(self, data, parent=QtCore.QModelIndex()):
        self.beginInsertRows(parent, self.rowCount(parent), self.rowCount(parent))
        self.getItem(parent).appendChild(data)
        self.endInsertRows()

    def switchRows(self, row1, row2, parent=QtCore.QModelIndex()):
        self.beginMoveRows(parent, row1, row1, parent, row2 + 1)
        self.getItem(parent).switchChildren(row1, row2)
        self.endMoveRows()

    def removeRows(self, row, count, parent=QtCore.QModelIndex()):
        if parent.isValid() and parent.internalPointer() != self.tree_root:
            self.beginRemoveRows(parent, row, row + count - 1)
            parent = self.getItem(parent)
            parent.removeChildren(row, count)
            self.endRemoveRows()
            return True
        return False

    def _items_from_index(self, index):
        raise NotImplementedError

    def activate(self, index):
        scene_items = self._items_from_index(index)
        for scene_item in scene_items.values():
            scene_item.setActive(True)

    def deactivate(self, index):
        scene_items = self._items_from_index(index)
        for scene_item in scene_items.values():
            scene_item.setActive(False)


class VolumeTreeItemModel(TreeItemModel):
    def __init__(self, data: ep.EyeVolume, parent):
        super().__init__(parent=parent)

        self._data = data
        self._current_slice = 0

        if "AreaSettings" not in self._data.meta:
            self._data.meta["AreaSettings"] = {
                "visible": True,
                "z_value": 0,
                "name": "Areas",
            }
        if "LayerSettings" not in self._data.meta:
            self._data.meta["LayerSettings"] = {
                "visible": True,
                "z_value": 0,
                "name": "Layers",
            }

        for bscan in self._data.meta["bscan_meta"]:
            if "disabled" not in bscan:
                bscan["disabled"] = False

        self._init_model()
        self._annotations = DynamicDefaultDict(
            lambda index: self._get_annotations(index)
        )

        self.annotation_items = collections.defaultdict(lambda: {})
        self.dataChanged.connect(self.sync_annotations_to_tab)

        self._scenes = {}

        # Set to first active slice
        self.next_slice(None)

    def duplicate_volume(self, index: QtCore.QModelIndex):
        """Duplicate a layer or area annotation with undo support."""
        from eyelab.commands import layeritem as layer_commands
        from eyelab.commands import get_undo_stack

        annotation = index.internalPointer().annotation
        name = annotation.name
        data = annotation.data

        if index.parent() == self.layers_index:
            # Use undo command for layer duplication
            command = layer_commands.AddLayeritem(
                self,
                name=f"Duplicate {name}",
                color=annotation.meta.get("current_color", "FF0000"),
            )
            # Override the layer annotation with duplicated data
            command.layer_annotation = ep.EyeVolumeLayerAnnotation(
                self._data,
                data.copy(),  # Copy the height map
                name=f"Duplicate {name}",
                current_color=annotation.meta.get("current_color", "FF0000"),
                visible=True,
                z_value=0,
            )
            get_undo_stack("main").push(command)
        elif index.parent() == self.areas_index:
            # Direct duplication for areas (no undo command yet)
            self.add_pixel_annotation(name=f"Duplicate {name}", voxel_map=data)

    @property
    def scene(self) -> CustomGraphicsScene:
        if self.current_slice not in self._scenes:
            # Create GraphicsScene if not yet created
            scene = CustomGraphicsScene(
                parent=self, data=self._data[self.current_slice]
            )
            # Set Annotations managed by the ViewTab
            scene.addItem(self.annotations)
            self._scenes[self.current_slice] = scene

            # Add foreground showing the B-scan index
            scene.foreground_on = True

        return self._scenes[self.current_slice]

    def set_current_scene(self):
        if self.tool.paint_preview.scene() == self.scene:
            self.scene.removeItem(self.tool.paint_preview)
        if self.scene.mouseGrabberItem() is not None:
            self.tool.paint_preview.setParentItem(self.scene.mouseGrabberItem())

    def next_slice(self, current_tool):
        slice = self.current_slice
        while slice < len(self._data) - 1:
            slice += 1
            if (
                self._data.meta["bscan_meta"][slice]["disabled"] is False
            ):  # slice is active
                self.current_slice = slice
                break

        if self.scene.mouseGrabberItem() is not None:
            current_tool.paint_preview.setParentItem(self.scene.mouseGrabberItem())

    def last_slice(self, current_tool):
        slice = self.current_slice
        while slice > 0:
            slice -= 1
            if (
                self._data.meta["bscan_meta"][slice]["disabled"] is False
            ):  # slice is active
                self.current_slice = slice
                break

        if self.scene.mouseGrabberItem() is not None:
            current_tool.paint_preview.setParentItem(self.scene.mouseGrabberItem())

    def sync_annotations_to_tab(self):
        self.annotations.update()

    @property
    def annotations(self):
        return self._annotations[self.current_slice]

    @property
    def current_slice(self):
        return self._current_slice

    @current_slice.setter
    def current_slice(self, value: int):
        self._current_slice = value
        # self.annotations.sync_with_volume()
        self.annotations.update()

    def _init_model(self):
        self.tree_root = TreeItemGroup(parent=None, meta={"name": "root"})
        self.tree_areas = TreeItemGroup(meta=self._data.meta["AreaSettings"])
        self.tree_layers = TreeItemGroup(meta=self._data.meta["LayerSettings"])

        self.areas_index = QtCore.QPersistentModelIndex(
            self.createIndex(0, 0, self.tree_areas)
        )
        self.layers_index = QtCore.QPersistentModelIndex(
            self.createIndex(1, 0, self.tree_layers)
        )

        for vm in self._data.volume_maps.values():
            vm.meta = {
                **{"visible": True, "z_value": 0, "current_color": "FF0000"},
                **vm.meta,
            }
            self.tree_areas.appendChild(TreeItem(data=vm))
        for layer in self._data.layers.values():
            layer.meta = {
                **{"visible": True, "z_value": 0, "current_color": "FF0000"},
                **layer.meta,
            }
            self.tree_layers.appendChild(TreeItem(data=layer))

        self.tree_root.appendChild(self.tree_areas)
        self.tree_root.appendChild(self.tree_layers)

    def add_annotation(self):
        from eyelab.commands import layeritem as layer_commands
        from eyelab.commands import get_undo_stack

        def add_layer_with_undo(name):
            command = layer_commands.AddLayeritem(self, name=name, color="FF0000")
            get_undo_stack("main").push(command)

        def add_pixel_direct(name):
            self.add_pixel_annotation(name, color="FF0000")

        options = {
            "Layers": add_layer_with_undo,
            "Areas": add_pixel_direct,
        }
        dialog = AddAnnotationDialog(self, options)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            # No need to emit layoutChanged here - the undo command handles it
            pass

    def _items_from_index(self, index):
        item = self.getItem(index)
        if type(item) is TreeItemGroup:
            return {}
        # Remove respective items from all Bscan scenes
        eyevolume_annotation = item.annotation
        return self.annotation_items[id(eyevolume_annotation)]

    def remove_annotation(self, index):
        """Remove annotation from eyevolume, all scenes and the overview"""
        if index.isValid():
            from eyelab.commands import layeritem as layer_commands
            from eyelab.commands import get_undo_stack

            item = self.getItem(index)
            eyevolume_annotation = item.annotation

            # Check if it's a layer annotation using isinstance
            if isinstance(eyevolume_annotation, ep.EyeVolumeLayerAnnotation):
                # This is a layer annotation - use undo command
                command = layer_commands.DeleteLayeritem(self, eyevolume_annotation)
                get_undo_stack("main").push(command)
            else:
                # This is a voxel/area annotation - use direct deletion
                self.layoutAboutToBeChanged.emit()
                # Remove respective items from all Bscan scenes
                scene_items = self.annotation_items.pop(id(eyevolume_annotation))
                for scene_item in scene_items.values():
                    scene_item.scene().removeItem(scene_item)
                    del scene_item
                # Remove from EyeVolume
                for annotations in [self._data._volume_maps, self._data._layers]:
                    if eyevolume_annotation in annotations:
                        annotations.remove(eyevolume_annotation)

                self.removeRows(index.row(), 1, index.parent())
                self.layoutChanged.emit()
                self.annotations.update()

    def add_layer_annotation(self, name, height_map=None, color="FF0000"):
        """Add a layer annotation directly without undo support.

        Note: For user-initiated actions with undo support, use add_annotation() instead.
        This method is kept for programmatic use (e.g., loading from file, duplication).
        """
        # Add to EyeVolume
        layer = self._data.add_layer_annotation(height_map=height_map, name=name)
        layer.meta = {
            **{"visible": True, "z_value": 0, "current_color": color},
            **layer.meta,
        }

        # Add in ViewTab - update
        self.appendRow(TreeItem(data=layer), parent=self.layers_index)

        # Add to every slice annotations exist for
        for index in self._annotations:
            root_item = self._annotations[index]
            layers_item_group = [
                c for c in root_item.childItems() if c.meta["name"] == "Layers"
            ][0]
            item = LayerItem(data=layer, index=index, parent=layers_item_group)
            self.annotation_items[id(layer)][index] = item

        return layer

    def add_pixel_annotation(self, name, pixel_map=None, color="FF0000"):
        # Add to EyeVolume
        pixel_map = self._data.add_pixel_annotation(voxel_map=pixel_map, name=name)
        pixel_map.meta = {
            **{"visible": True, "z_value": 0, "current_color": color},
            **pixel_map.meta,
        }

        # Add in ViewTab - update
        self.appendRow(TreeItem(data=pixel_map), parent=self.areas_index)
        # Add to every slice annotations exist for
        for index in self._annotations:
            root_item = self._annotations[index]
            areas_item_group = [
                c for c in root_item.childItems() if c.meta["name"] == "Areas"
            ][0]
            item = AreaItem(data=pixel_map, index=index, parent=areas_item_group)
            self.annotation_items[id(pixel_map)][index] = item

    def _get_annotations(self, index):
        root_item = ItemGroup(meta={})

        # Create AreaItems for the given index
        areas_item_group = ItemGroup(meta=self._data.meta["AreaSettings"])
        for name, volume_map in self._data.volume_maps.items():
            item = AreaItem(data=volume_map, index=index, parent=areas_item_group)
            # Save items organized by annotation for easier access
            self.annotation_items[id(volume_map)][index] = item

        # Create LayerItems for the given index
        layers_item_group = ItemGroup(meta=self._data.meta["LayerSettings"])
        for name, layer in self._data.layers.items():
            item = LayerItem(data=layer, index=index, parent=layers_item_group)
            # Save items organized by annotation for easier access
            self.annotation_items[id(layer)][index] = item

        areas_item_group.setParentItem(root_item)
        layers_item_group.setParentItem(root_item)
        return root_item


class EnfaceTreeItemModel(TreeItemModel):
    def __init__(self, data: ep.EyeEnface, parent):
        super().__init__(parent=parent)

        self._data = data

        if "AreaSettings" not in self._data.meta:
            self._data.meta["AreaSettings"] = {
                "visible": True,
                "z_value": 0,
                "name": "Areas",
            }

        self.annotation_items = {}
        self._init_model()
        self.annotations = self._get_annotations()

        self.dataChanged.connect(self.sync_annotations_to_tab)

        self.scene = CustomGraphicsScene(parent=self, data=self._data)
        self.scene.addItem(self.annotations)

    def sync_annotations_to_tab(self):
        # self.annotations.sync_with_volume()
        self.annotations.update()

    def _init_model(self):
        self.tree_root = TreeItemGroup(parent=None, meta={"name": "root"})
        self.tree_areas = TreeItemGroup(meta=self._data.meta["AreaSettings"])

        self.areas_index = QtCore.QPersistentModelIndex(
            self.createIndex(0, 0, self.tree_areas)
        )

        for vm in self._data.area_maps.values():
            vm.meta = {
                **{"visible": True, "z_value": 0, "current_color": "FF0000"},
                **vm.meta,
            }
            self.tree_areas.appendChild(TreeItem(data=vm))

        self.tree_root.appendChild(self.tree_areas)

    def _get_annotations(self):
        root_item = ItemGroup(meta={})

        # Create AreaItems for the given index
        areas_item_group = ItemGroup(meta=self._data.meta["AreaSettings"])
        for area_map in self._data._area_maps:
            item = AreaItem(
                data=area_map,
                index=np.s_[...],
                parent=areas_item_group,
            )
            self.annotation_items[id(area_map)] = item

        areas_item_group.setParentItem(root_item)
        return root_item

    def _items_from_index(self, index):
        item = self.getItem(index)
        if type(item) is TreeItemGroup:
            return {}
        # Remove respective items from all Bscan scenes
        voxel_annotation = item.annotation
        return {0: self.annotation_items[id(voxel_annotation)]}

    def add_annotation(self):
        dialog = AddAnnotationDialog(self, {"Areas": self.add_area_annotation})
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.layoutChanged.emit()
            self.annotations.update()

    def add_area_annotation(self, name, color="FF0000"):
        # Add to EyeVolume
        area_map = self._data.add_area_annotation(name=name)
        area_map.meta = {
            **{"visible": True, "z_value": 0, "current_color": color},
            **area_map.meta,
        }

        # Add in ViewTab - update
        self.appendRow(TreeItem(data=area_map), parent=self.areas_index)

        # Add to every slice annotations exist for
        root_item = self.annotations
        areas_item_group = [
            c for c in root_item.childItems() if c.meta["name"] == "Areas"
        ][0]
        item = AreaItem(data=area_map, parent=areas_item_group)
        self.annotation_items[id(area_map)] = item

    def remove_annotation(self, index):
        """Remove annotation from eyevolume, all scenes and the overview"""
        if index.isValid():
            self.layoutAboutToBeChanged.emit()
            item = self.getItem(index)
            # Remove respective item from scene
            area_annotation = item.annotation
            scene_item = self.annotation_items.pop(id(area_annotation))
            scene_item.scene().removeItem(scene_item)
            del scene_item

            # Remove from EyeEnface
            self._data._area_maps.remove(area_annotation)

            self.removeRows(index.row(), 1, index.parent())
            self.layoutChanged.emit()
            self.annotations.update()
