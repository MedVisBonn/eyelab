import logging
import bisect

import numpy as np
from PySide6.QtCore import QLineF, QPointF
from PySide6.QtGui import QUndoCommand
from PySide6.QtWidgets import QGraphicsItem

from eyelab.models.treeview import layeritem
from eyelab.models.treeview import itemmodel
import eyepy as ep

logger = logging.getLogger(__name__)


class AddLayeritem(QUndoCommand):
    def __init__(
        self,
        tree_item_model: "itemmodel.VolumeTreeItemModel",
        name="New Layer",
        color="default",
        parent=None,
    ):
        super().__init__(parent)
        self.setText("Add Layer")
        self.model = tree_item_model
        self.volume = self.model._data

        height_map = np.full((self.volume.shape[1:]), np.nan)
        self.layer_annotation = ep.EyeVolumeLayerAnnotation(
            self.volume,
            height_map,
            name=name,
            current_color=color,
            visible=True,
            z_value=0,
        )
        self.tree_item_index = None

    def redo(self):
        logger.debug(f"Redo: {self.text()}")

        try:
            # Add to EyeVolume
            self.volume._layers.append(self.layer_annotation)

            # Add in ViewTab - create TreeItem and store its index
            # Note: appendRow handles beginInsertRows/endInsertRows internally
            tree_item = itemmodel.TreeItem(data=self.layer_annotation)
            self.model.appendRow(tree_item, parent=self.model.layers_index)

            # Store the model index for later removal
            if self.tree_item_index is None:
                row = self.model.rowCount(self.model.layers_index) - 1
                self.tree_item_index = self.model.index(row, 0, self.model.layers_index)

            # Add to every slice annotations exist for
            for index in self.model._annotations:
                root_item = self.model._annotations[index]
                layers_item_group = [
                    c for c in root_item.childItems() if c.meta["name"] == "Layers"
                ][0]
                item = layeritem.LayerItem(
                    data=self.layer_annotation, index=index, parent=layers_item_group
                )
                self.model.annotation_items[id(self.layer_annotation)][index] = item

            self.model.annotations.update()
        except Exception as e:
            logger.error(f"Error in AddLayeritem.redo: {e}", exc_info=True)
            raise

    def undo(self):
        logger.debug(f"Undo: {self.text()}")

        try:
            # Remove respective items from all Bscan scenes
            scene_items = self.model.annotation_items.pop(id(self.layer_annotation), {})
            for scene_item in scene_items.values():
                if scene_item.scene():
                    scene_item.scene().removeItem(scene_item)

            # Remove from model tree
            # Note: removeRows handles beginRemoveRows/endRemoveRows internally
            if self.tree_item_index and self.tree_item_index.isValid():
                self.model.removeRows(
                    self.tree_item_index.row(), 1, self.model.layers_index
                )

            # Remove from EyeVolume
            if self.layer_annotation in self.volume._layers:
                self.volume._layers.remove(self.layer_annotation)

            self.model.annotations.update()
        except Exception as e:
            logger.error(f"Error in AddLayeritem.undo: {e}", exc_info=True)
            raise


class DeleteLayeritem(QUndoCommand):
    def __init__(
        self,
        tree_item_model: "itemmodel.VolumeTreeItemModel",
        layer_annotation: ep.EyeVolumeLayerAnnotation,
        parent=None,
    ):
        super().__init__(parent)
        self.setText("Delete Layer")
        self.model = tree_item_model
        self.layer_annotation = layer_annotation
        self.volume = self.layer_annotation.volume

        # Store the scene items before deletion
        self.scene_items_data = {}
        self.tree_item_index = None

    def redo(self):
        logger.debug(f"Redo: {self.text()}")

        try:
            # Store scene items before removing
            if id(self.layer_annotation) in self.model.annotation_items:
                self.scene_items_data = {}
                for index, scene_item in self.model.annotation_items[
                    id(self.layer_annotation)
                ].items():
                    # Store the index for later recreation
                    self.scene_items_data[index] = {
                        "index": index,
                        "parent": scene_item.parentItem(),
                    }

            # Remove respective items from all Bscan scenes
            scene_items = self.model.annotation_items.pop(id(self.layer_annotation), {})
            for scene_item in scene_items.values():
                if scene_item.scene():
                    scene_item.scene().removeItem(scene_item)

            # Find and store the tree item index before deletion
            if self.tree_item_index is None:
                layers_index = self.model.layers_index
                for row in range(self.model.rowCount(layers_index)):
                    idx = self.model.index(row, 0, layers_index)
                    item = self.model.getItem(idx)
                    if (
                        hasattr(item, "annotation")
                        and item.annotation == self.layer_annotation
                    ):
                        self.tree_item_index = idx
                        break

            # Remove from model tree
            # Note: removeRows handles beginRemoveRows/endRemoveRows internally
            if self.tree_item_index and self.tree_item_index.isValid():
                self.model.removeRows(
                    self.tree_item_index.row(), 1, self.model.layers_index
                )

            # Remove from EyeVolume
            if self.layer_annotation in self.volume._layers:
                self.volume._layers.remove(self.layer_annotation)

            self.model.annotations.update()
        except Exception as e:
            logger.error(f"Error in DeleteLayeritem.redo: {e}", exc_info=True)
            raise

    def undo(self):
        logger.debug(f"Undo: {self.text()}")

        try:
            # Add back to EyeVolume
            self.volume._layers.append(self.layer_annotation)

            # Add back to ViewTab
            # Note: appendRow handles beginInsertRows/endInsertRows internally
            tree_item = itemmodel.TreeItem(data=self.layer_annotation)
            self.model.appendRow(tree_item, parent=self.model.layers_index)

            # Recreate scene items for all slices
            for index, item_data in self.scene_items_data.items():
                parent = item_data["parent"]
                item = layeritem.LayerItem(
                    data=self.layer_annotation, index=index, parent=parent
                )
                self.model.annotation_items[id(self.layer_annotation)][index] = item

            self.model.annotations.update()
        except Exception as e:
            logger.error(f"Error in DeleteLayeritem.undo: {e}", exc_info=True)
            raise


class ClearHeights(QUndoCommand):
    def __init__(self, layeritem, start, end, parent=None):
        super().__init__(parent)
        self.setText("Clear Heights")

        self.layeritem = layeritem
        self.start = start
        self.end = end
        self.old_heights = None

    def redo(self):
        logger.debug(f"Redo: {self.text()}")
        layer_item = self.layeritem
        if self.old_heights is None:
            self.old_heights = np.copy(
                layer_item.height_map[int(self.start) : int(self.end)]
            )
        layer_item.height_map[int(self.start) : int(self.end)] = np.nan

    def undo(self):
        logger.debug(f"Undo: {self.text()}")
        layer_item = self.layeritem
        layer_item.height_map[int(self.start) : int(self.end)] = self.old_heights

    def id(self):
        return 6

    def mergeWith(self, other: QUndoCommand) -> bool:
        # Todo check the code below for correctness
        return False
        if self.layeritem != other.layeritem:
            return False

        # Extend the cleared region
        self.start = min(self.start, other.start)
        self.end = max(self.end, other.end)

        # Combine old heights
        new_old_heights = np.copy(self.old_heights)
        start_index = int(other.start) - int(self.start)
        end_index = start_index + len(other.old_heights)
        if start_index < 0:
            # Other command clears region before current command
            prepend_length = -start_index
            new_old_heights = np.concatenate(
                (other.old_heights[:prepend_length], new_old_heights)
            )
            start_index = 0
            end_index += prepend_length
        if end_index > len(new_old_heights):
            # Other command clears region after current command
            append_length = end_index - len(new_old_heights)
            new_old_heights = np.concatenate(
                (new_old_heights, other.old_heights[-append_length:])
            )
        new_old_heights[start_index:end_index] = other.old_heights
        self.old_heights = new_old_heights

        return True


class ChangePolygon(QUndoCommand):
    def __init__(
        self, polygon: "layeritem.PolygonPath", start=None, end=None, parent=None
    ):
        self.polygon = polygon
        self.layeritem = polygon.layer_item
        self.new_start = start if start else self.polygon.start
        self.new_end = end if end else self.polygon.end

        self.old_start = self.polygon.start
        self.old_end = self.polygon.end

        super().__init__(parent)
        self.setText("Change Layer Region")

    def redo(self):
        logger.debug(f"Redo: {self.text()}")
        self.polygon.start = self.new_start
        self.polygon.end = self.new_end
        self.polygon.update()

    def undo(self):
        logger.debug(f"Undo: {self.text()}")
        self.polygon.start = self.old_start
        self.polygon.end = self.old_end
        self.polygon.update()

    def id(self):
        return 3

    def mergeWith(self, other: QUndoCommand) -> bool:
        if self.polygon != other.polygon:
            return False

        self.new_start = other.new_start
        self.new_end = other.new_end
        return True


class AddPolygon(QUndoCommand):
    def __init__(self, layer_item: "layeritem.LayerItem", start, end, parent=None):
        self.layeritem = layer_item
        self.start = start
        self.end = end

        self.polygon = layeritem.PolygonPath(None, self.start, self.end)

        super().__init__(parent)
        self.setText("Add Layer Region")

    def redo(self):
        logger.debug(f"Redo: {self.text()}")
        polygons = sorted(
            self.layeritem.polygons + [self.polygon], key=lambda x: x.start.x()
        )
        self.index = polygons.index(self.polygon)
        self.layeritem.polygons.insert(self.index, self.polygon)
        self.polygon.setParentItem(self.layeritem)

    def undo(self):
        logger.debug(f"Undo: {self.text()}")
        self.layeritem.polygons.pop(self.index)
        self.polygon.scene().removeItem(self.polygon)


class UpdateLayerArray(QUndoCommand):
    def __init__(self, bspline: "layeritem.CubicSpline", parent=None):
        super().__init__(parent)
        self.setText("Update Layer Array")

        self.bspline = bspline

        self.layer_item = bspline.layer_item
        self.mapping = {}
        self.old_mapping = {}

    def redo(self):
        logger.debug(f"Redo: {self.text()}")
        self.mapping = self.bspline.indices() if not self.mapping else self.mapping
        self.old_mapping = (
            {x: self.layer_item.height_map[x] for x in self.mapping.keys()}
            if not self.old_mapping
            else self.old_mapping
        )
        for x in self.mapping:
            self.layer_item.height_map[x] = self.mapping[x]

    def undo(self):
        logger.debug(f"Undo: {self.text()}")
        for x in self.old_mapping:
            self.layer_item.height_map[x] = self.old_mapping[x]

    def id(self):
        return 4

    def mergeWith(self, other: QUndoCommand) -> bool:
        if self.bspline != other.bspline:
            return False

        self.mapping = {**self.mapping, **other.mapping}
        self.old_mapping = {**other.old_mapping, **self.old_mapping}
        return True


class MoveKnot(QUndoCommand):
    def __init__(self, knot: "layeritem.CubicSplineKnotItem", new_pos: QPointF):
        super().__init__()
        self.setText("Move Knot")

        self.knot = knot
        self.bspline = self.knot.bspline
        self.index = self.bspline.knots.index(self.knot)

        # Make sure knots are x centered in pixel
        new_pos.setX(np.floor(new_pos.x()) + 0.5)
        self.new_pos = new_pos
        self.old_pos = self.knot.center
        self.last_active_curve = self.bspline.layer_item.active_curve

    def redo(self) -> None:
        logger.debug(f"Redo: {self.text()}")
        self.bspline.layer_item.active_curve = self.bspline
        self.knot.setPos(self.new_pos)
        self.knot.sync()
        self.knot.bspline.update()

    def undo(self) -> None:
        logger.debug(f"Undo: {self.text()}")
        self.bspline.layer_item.active_curve = self.last_active_curve
        self.knot.setPos(self.old_pos)
        self.knot.sync()
        self.knot.bspline.update()

    def mergeWith(self, other: "MoveKnot") -> bool:
        # Do only merge if the same knot is moved
        if other.knot != self.knot:
            return False

        self.new_pos = other.new_ps
        return True

    def id(self):
        return 1


class MoveControlKnot(QUndoCommand):
    def __init__(self, item: QGraphicsItem, new_pos: QPointF):
        self.cp = item
        self.knot = self.cp.parentItem()
        cp_in = self.knot.cp_in
        cp_out = self.knot.cp_out
        self.other_cp = cp_in if self.cp is not cp_in else cp_out

        self.new_pos = new_pos
        self.old_pos = self.cp.pos()

        # Make sure control points move together to keep the curve smooth
        line = QLineF(self.cp.center, self.knot.center)
        line2 = QLineF(self.knot.center, self.other_cp.center)
        line.setLength(line.length() + line2.length())

        self.other_old = self.other_cp.pos()
        self.other_new = self.knot.mapFromScene(line.p2())

        UpdateLayerArray(self.knot.bspline, parent=self)

        super().__init__()
        self.setText("Move Control Knot")

    def redo(self) -> None:
        logger.debug(f"Redo: {self.text()}")
        self.cp.setPos(self.new_pos)
        self.other_cp.setPos(self.other_new)

        super().redo()
        self.knot.bspline.update()
        self.knot.set_lines()

    def undo(self) -> None:
        logger.debug(f"Undo: {self.text()}")
        self.cp.setPos(self.old_pos)
        self.cp.setPos(self.old_pos)
        self.other_cp.setPos(self.other_old)

        super().undo()
        self.knot.bspline.update()
        self.knot.set_lines()

    def mergeWith(self, other: "MoveKnot") -> bool:
        # Make sure other is a MoveKnot command for the same QGraphicsItem
        if other.cp != self.cp:
            return False

        other.old_pos = self.old_pos
        other.other_old = self.other_old
        return True

    def id(self):
        return 2


class AddKnot(QUndoCommand):
    def __init__(
        self,
        bspline: "layeritem.CubicSpline",
        pos: QPointF,
        parent=None,
    ):
        super().__init__(parent)
        self.setText("Add Knot")

        self.bspline = bspline
        self.layeritem = self.bspline.layer_item

        pos.setX(np.floor(pos.x()) + 0.5)
        self.pos = pos

        # Create new knot
        knot_dict = {
            "knot_pos": (pos.x(), pos.y()),
            "cp_in_pos": (pos.x() - 10, pos.y()),
            "cp_out_pos": (pos.x() + 10, pos.y()),
        }

        self.new_knot = layeritem.CubicSplineKnotItem(parent=None, knot_dict=knot_dict)
        # Get insertion index for new knot in sorted knot list
        self.index = bisect.bisect_left(
            self.bspline._knots,
            knot_dict["knot_pos"][0],
            key=lambda x: x["knot_pos"][0],
        )

        self.old_active_curve = self.layeritem.active_curve

    def redo(self) -> None:
        logger.debug(f"Redo: {self.text()}")
        self.new_knot.setParentItem(self.bspline)
        self.bspline._knots.insert(self.index, self.new_knot.knot_dict)
        self.bspline.knots.insert(self.index, self.new_knot)

        if not self.bspline.control_points_visible:
            self.new_knot.hide_control_points()

        self.new_knot.show()
        self.layeritem.active_curve = self.bspline
        self.bspline.update()

    def undo(self) -> None:
        logger.debug(f"Undo: {self.text()}")

        self.new_knot.scene().removeItem(self.new_knot)
        self.bspline.knots.pop(self.index)
        self.bspline._knots.pop(self.index)

        self.layeritem.active_curve = self.old_active_curve
        self.bspline.update()


class DeleteKnot(QUndoCommand):
    def __init__(self, knot: "layeritem.CubicSplineKnotItem"):
        super().__init__()
        self.setText("Delete Knot")

        self.knot = knot
        self.bspline = self.knot.bspline
        self.layeritem = self.bspline.layer_item
        self.index = self.bspline.knots.index(self.knot)

    def redo(self) -> None:
        logger.debug(f"Redo: {self.text()}")
        self.bspline.scene().removeItem(self.knot)
        self.bspline.knots.pop(self.index)
        self.bspline._knots.pop(self.index)

    def undo(self) -> None:
        logger.debug(f"Undo: {self.text()}")
        self.bspline.knots.insert(self.index, self.knot)
        self.bspline._knots.insert(self.index, self.knot.knot_dict)
        self.knot.setParentItem(self.bspline)


class DeleteCurve(QUndoCommand):
    def __init__(self, bspline: "layeritem.CubicSpline", parent=None):
        super().__init__(parent)
        self.setText("Delete Curve")
        self.bspline = bspline
        self.layeritem = bspline.layer_item
        self.index = self.layeritem.cubic_splines.index(self.bspline)
        self.curve_is_active = self.layeritem.active_curve is self.bspline

    def redo(self) -> None:
        logger.debug(f"Redo: {self.text()}")

        # Remove curve from scene and lists
        self.layeritem.cubic_splines.pop(self.index)
        self.knots = self.layeritem.knots.pop(self.index)
        self.layeritem.scene().removeItem(self.bspline)
        if self.curve_is_active:
            self.layeritem.active_curve = None

    def undo(self) -> None:
        logger.debug(f"Undo: {self.text()}")

        # Restore curve to scene and lists
        self.layeritem.cubic_splines.insert(self.index, self.bspline)
        self.layeritem.knots.insert(self.index, self.knots)
        self.bspline.setParentItem(self.layeritem)
        if self.curve_is_active:
            self.layeritem.active_curve = self.bspline


class DeletePolygon(QUndoCommand):
    def __init__(
        self, polygon: "layeritem.PolygonPath", heights_to_nan=True, parent=None
    ):
        super().__init__(parent)
        self.setText("Delete Polygon")

        self.heights_to_nan = heights_to_nan
        self.polygon = polygon
        self.layeritem = self.polygon.layer_item

        start, stop = self.polygon.x_region
        self.slice = np.s_[int(np.floor(start)) : int(np.ceil(stop))]

    def redo(self) -> None:
        logger.debug(f"Redo: {self.text()}")
        self.index = self.layeritem.polygons.index(self.polygon)
        self.layeritem.polygons.pop(self.index)
        if self.heights_to_nan:
            self.heights = np.copy(self.polygon.heights[self.slice])
            self.polygon.heights[self.slice] = np.nan
        self.layeritem.scene().removeItem(self.polygon)

    def undo(self) -> None:
        logger.debug(f"Undo: {self.text()}")
        self.layeritem.polygons.insert(self.index, self.polygon)
        if self.heights_to_nan:
            self.polygon.heights[self.slice] = self.heights
        self.polygon.setParentItem(self.layeritem)


class OptimizeControlPoints(QUndoCommand):
    def __init__(
        self,
        knot: "layeritem.CubicSplineKnotItem",
        parent=None,
    ):
        super().__init__(parent)
        self.setText("Optimize Controllpoints")

        self.knot = knot
        self.bspline = self.knot.bspline

        self.in_pos, self.out_pos = None, None
        self.old_in_pos, self.old_out_pos = None, None

    def redo(self) -> None:
        logger.debug(f"Redo: {self.text()}")
        self.old_in_pos, self.old_out_pos = (
            self.knot.cp_in_pos,
            self.knot.cp_out_pos,
        )
        self.in_pos, self.out_pos = self.bspline.optimize_controllpoints(self.knot)

        self.knot.cp_in = self.in_pos
        self.knot.cp_out = self.out_pos
        self.bspline.update()

    def undo(self) -> None:
        logger.debug(f"Undo: {self.text()}")
        self.knot.cp_in = self.old_in_pos
        self.knot.cp_out = self.old_out_pos
        self.bspline.update()

    def id(self) -> int:
        return 5


class AddCurve(QUndoCommand):
    def __init__(self, layer_item: "layeritem.LayerItem", pos: QPointF):
        super().__init__()
        self.setText("New Curve")

        self.layer_item = layer_item

        self.first_knot_index = pos.x()
        self.first_knot_height = pos.y()
        self.old_height = layer_item.height_map[int(self.first_knot_index)]

        pos.setX(np.floor(pos.x()) + 0.5)
        self.pos = pos

        knot_dict = {
            "knot_pos": (pos.x(), pos.y()),
            "cp_in_pos": (pos.x() - 10, pos.y()),
            "cp_out_pos": (pos.x() + 10, pos.y()),
        }

        self.knots = [knot_dict]
        self.bspline = layeritem.CubicSpline(self.knots, None)
        self.new_knot = self.bspline.knots[0]

        # Get insertion index
        i = 0
        for cs in self.layer_item.cubic_splines:
            if self.new_knot.center.x() > cs.start.x():
                i += 1
            else:
                break
        self.index = i

        self.last_active_curve = self.layer_item.active_curve

    def redo(self) -> None:
        logger.debug(f"Redo: {self.text()}")
        self.bspline.setParentItem(self.layer_item)
        self.layer_item.knots.insert(self.index, self.knots)
        self.layer_item.cubic_splines.insert(self.index, self.bspline)

        # set height_map for first knot
        self.layer_item.height_map[int(self.first_knot_index)] = self.first_knot_height

        self.new_knot.show()
        self.layer_item.active_curve = self.bspline
        self.layer_item.update()

    def undo(self) -> None:
        logger.debug(f"Undo: {self.text()}")
        self.bspline.scene().removeItem(self.bspline)
        self.layer_item.cubic_splines.pop(self.index)
        self.layer_item.knots.pop(self.index)
        # restore old height_map value
        self.layer_item.height_map[int(self.first_knot_index)] = self.old_height
        self.layer_item.active_curve = self.last_active_curve
        self.layer_item.update()


class SplitPolygons(QUndoCommand):
    def __init__(self, polygon: "layeritem.PolygonPath", pos: QPointF, parent=None):
        self.polygon = polygon
        self.pos = pos

        self.layeritem = self.polygon.layer_item
        self.new_polygons = [
            layeritem.PolygonPath(None, self.polygon.start, self.pos),
            layeritem.PolygonPath(None, self.pos, self.polygon.end),
        ]
        self.index = self.layeritem.polygons.index(self.polygon)
        super().__init__(parent)
        self.setText("Split Polygons")

    def redo(self) -> None:
        logger.debug(f"Redo: {self.text()}")
        for p in self.new_polygons:
            p.setParentItem(self.polygon.parentItem())

        self.polygon.scene().removeItem(self.polygon)
        self.layeritem.polygons = (
            self.layeritem.polygons[: self.index]
            + self.new_polygons
            + self.layeritem.polygons[self.index + 1 :]
        )

        self.layeritem.update()

    def undo(self) -> None:
        logger.debug(f"Undo: {self.text()}")
        self.polygon.setParentItem(self.new_polygons[0].parentItem())
        for p in self.new_polygons:
            p.scene().removeItem(p)

        self.layeritem.polygons = (
            self.layeritem.polygons[: self.index]
            + [self.polygon]
            + self.layeritem.polygons[self.index + 2 :]
        )
        self.layeritem.update()


class JoinPolygons(QUndoCommand):
    def __init__(
        self, p1: "layeritem.PolygonPath", p2: "layeritem.PolygonPath", parent=None
    ):
        self.polygons = [p1, p2]

        self.layeritem = p1.layer_item
        self.new_polygon = layeritem.PolygonPath(None, p1.start, p2.end)
        self.index = self.layeritem.polygons.index(p1)

        super().__init__(parent)
        self.setText("Join Polygons")

    def redo(self) -> None:
        logger.debug(f"Redo: {self.text()}")
        self.new_polygon.setParentItem(self.polygons[0].parentItem())
        for p in self.polygons:
            p.scene().removeItem(p)

        self.layeritem.polygons = (
            self.layeritem.polygons[: self.index]
            + [self.new_polygon]
            + self.layeritem.polygons[self.index + 2 :]
        )
        self.layeritem.update()

    def undo(self) -> None:
        logger.debug(f"Undo: {self.text()}")
        for p in self.polygons:
            p.setParentItem(self.new_polygon.parentItem())

        self.new_polygon.scene().removeItem(self.new_polygon)
        self.layeritem.polygons = (
            self.layeritem.polygons[: self.index]
            + self.polygons
            + self.layeritem.polygons[self.index + 1 :]
        )
        self.layeritem.update()
