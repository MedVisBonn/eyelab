import logging

import numpy as np
from PySide6.QtCore import QLineF, QPointF, Qt
from PySide6.QtGui import QUndoCommand
from PySide6.QtWidgets import QGraphicsItem

from eyelab.models.treeview import layeritem

logger = logging.getLogger(__name__)


class AddLayeritem(QUndoCommand):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setText("Add Layer")

    def redo(self):
        logger.debug(f"Redo: {self.text()}")

    def undo(self):
        logger.debug(f"Undo: {self.text()}")


class DeleteLayeritem(QUndoCommand):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setText("Delete Layer")

    def redo(self):
        logger.debug(f"Redo: {self.text()}")

    def undo(self):
        logger.debug(f"Undo: {self.text()}")


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

    def undo(self):
        logger.debug(f"Undo: {self.text()}")
        self.polygon.start = self.old_start
        self.polygon.end = self.old_end

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

        self.polygon = layeritem.PolygonPath(
            None, self.layeritem.height_map, self.start, self.end
        )

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
        self.bspline = bspline

        self.layeritem = None
        self.mapping = None
        self.old_mapping = None

        super().__init__(parent)
        self.setText("Update Layer Array")

    def redo(self):
        logger.debug(f"Redo: {self.text()}")
        self.layeritem = (
            self.bspline.layer_item if not self.layeritem else self.layeritem
        )
        self.mapping = self.bspline.indices() if not self.mapping else self.mapping
        self.old_mapping = (
            {x: self.layeritem.height_map[x] for x in self.mapping.keys()}
            if not self.old_mapping
            else self.old_mapping
        )
        for x in self.mapping:
            self.layeritem.height_map[x] = self.mapping[x]

    def undo(self):
        logger.debug(f"Undo: {self.text()}")
        for x in self.old_mapping:
            self.layeritem.height_map[x] = self.old_mapping[x]

    def id(self):
        return 4

    def mergeWith(self, other: QUndoCommand) -> bool:
        if self.bspline != other.bspline:
            return False

        self.mapping = {**self.mapping, **other.mapping}
        self.old_mapping = {**other.old_mapping, **self.old_mapping}
        return True


class MoveKnot(QUndoCommand):
    def __init__(self, knot: QGraphicsItem, new_pos: QPointF, optimize_neighbours=True):
        self.knot = knot
        self.bspline = self.knot.bspline
        self.index = self.bspline.knots.index(self.knot)
        self.optimize_neighbours = optimize_neighbours

        # Make sure knots ara x centered in pixel
        new_pos.setX(np.floor(new_pos.x()) + 0.5)
        self.new_pos = new_pos
        self.old_pos = self.knot.center
        super().__init__()
        self.setText("Move Knot")

        # Create child command for optimizing control points
        self.optimize_cps = OptimizeControlPoints(
            self.knot, self.bspline, propagate=self.optimize_neighbours, parent=self
        )

        self.change_p1, self.change_p2 = None, None
        self.deleted_polygon = None
        (
            left_neighbours,
            right_neighbours,
        ) = self.bspline.layer_item.get_neighbour_polygons(self.bspline)

        if self.knot is self.bspline.knots[-1] and right_neighbours:
            for n in right_neighbours:
                # Find the closest neighbour that is not covered after the move
                if n.end.x() >= self.new_pos.x():
                    # Change the neighbour if the new pos is in its region
                    if self.old_pos.x() == n.start.x() or self.new_pos in n:
                        self.change_p1 = ChangePolygon(
                            n, start=self.new_pos, parent=self
                        )
                    break
                else:
                    # Delete polygon if it is covered
                    self.deleted_polygon = DeletePolygon(n, parent=self)

        if self.knot is self.bspline.knots[0] and left_neighbours:
            for n in left_neighbours:
                # Find the closest neighbour that is not covered after the move
                if n.start.x() <= self.new_pos.x():
                    if self.old_pos.x() == n.end.x() or self.new_pos in n:
                        self.change_p2 = ChangePolygon(n, end=self.new_pos, parent=self)
                    break
                else:
                    self.deleted_polygon = DeletePolygon(n, parent=self)

        self.update_array = UpdateLayerArray(self.bspline, parent=self)

        self.added_polygon = None
        if (
            self.knot is self.bspline.knots[-1]
            and self.new_pos.x() < self.old_pos.x()
            and not self.change_p1
        ):
            self.added_polygon = AddPolygon(
                self.bspline.layer_item,
                start=self.new_pos,
                end=self.old_pos,
                parent=self,
            )

        if (
            self.knot is self.bspline.knots[0]
            and self.new_pos.x() > self.old_pos.x()
            and not self.change_p2
        ):
            self.added_polygon = AddPolygon(
                self.bspline.layer_item,
                start=self.old_pos,
                end=self.new_pos,
                parent=self,
            )

    def redo(self) -> None:
        logger.debug(f"Redo: {self.text()}")
        self.knot.setPos(self.new_pos)
        self.knot.sync()
        super().redo()
        self.knot.bspline.update()

        if self.change_p1:
            self.change_p1.polygon.update()
        if self.change_p2:
            self.change_p2.polygon.update()
        if self.added_polygon:
            self.bspline.layer_item.update()

    def undo(self) -> None:
        logger.debug(f"Undo: {self.text()}")
        self.knot.setPos(self.old_pos)
        self.knot.sync()
        super().undo()
        self.knot.bspline.update()

    def mergeWith(self, other: "MoveKnot") -> bool:
        p1s = [c.polygon if c else None for c in [self.change_p1, other.change_p1]]
        p2s = [c.polygon if c else None for c in [self.change_p2, other.change_p2]]
        # Do only merge if the same knot is moved
        if other.knot != self.knot:
            return False
        # Do only merge if the new command does not delete a polygon
        if not other.deleted_polygon is None:
            return False
        # Do only merge if the old command did not add a polygon
        if not (self.added_polygon is None and other.added_polygon is None):
            return False
        # Do only merge if neighbouring polygons are the same or one of them is None
        if not (p1s[0] is None or p1s[1] is None or p1s[0] is p1s[1]):
            return False
        if not (p2s[0] is None or p2s[1] is None or p2s[0] is p2s[1]):
            return False

        self.new_pos = other.new_pos

        self.optimize_cps.mergeWith(other.optimize_cps)
        if self.change_p1 and other.change_p1:
            self.change_p1.mergeWith(other.change_p1)
        if self.change_p2 and other.change_p2:
            self.change_p2.mergeWith(other.change_p2)

        self.update_array.mergeWith(other.update_array)
        return True

    def id(self):
        return 1


class MoveControlKnot(QUndoCommand):
    def __init__(self, item: QGraphicsItem, new_pos: QPointF):
        self.cp = item
        self.knot = self.cp.parentItem()
        cp_in = self.knot.cp_in
        cp_out = self.knot.cp_out
        self.other_cp = cp_in if not self.cp is cp_in else cp_out

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
        optimize_neighbours=True,
        parent=None,
    ):
        self.bspline = bspline
        self.layeritem = self.bspline.layer_item

        pos.setX(np.floor(pos.x()) + 0.5)
        self.pos = pos
        self.optimize_neighbours = optimize_neighbours
        super().__init__(parent)
        self.setText("Add Knot")

        # Create new knot
        knot_dict = {
            "knot_pos": (pos.x(), pos.y()),
            "cp_in_pos": (pos.x() - 10, pos.y()),
            "cp_out_pos": (pos.x() + 10, pos.y()),
        }

        self.new_knot = layeritem.CubicSplineKnotItem(parent=None, knot_dict=knot_dict)

        # Get insertion index ToDo: Replace with bisect insort when Pysid6 works on Python3.10
        i = 0
        for k in self.bspline._knots:
            if knot_dict["knot_pos"][0] > k["knot_pos"][0]:
                i += 1
                continue
            break
        self.index = i
        # Create child command for optimizing control points
        OptimizeControlPoints(
            self.new_knot, self.bspline, propagate=self.optimize_neighbours, parent=self
        )

        # Create child commands to change neighbouring polygons if necessary
        left_neighbours, right_neighbours = self.layeritem.get_neighbour_polygons(
            self.bspline
        )
        if self.index == len(self.bspline.knots) and right_neighbours:
            for n in right_neighbours:
                if self.pos in n:
                    ChangePolygon(n, start=self.pos, parent=self)
                    break
                elif self.pos.x() < n.start.x():
                    break
                else:
                    DeletePolygon(n, parent=self)

        if self.index == 0 and left_neighbours:
            for n in left_neighbours:
                if self.pos in n:
                    ChangePolygon(n, end=self.pos, parent=self)
                    break
                elif self.pos.x() > n.end.x():
                    break
                else:
                    DeletePolygon(n, parent=self)

        self.update_array = UpdateLayerArray(self.bspline, parent=self)

    def redo(self) -> None:
        logger.debug(f"Redo: {self.text()}")
        self.new_knot.setParentItem(self.bspline)
        self.bspline._knots.insert(self.index, self.new_knot.knot_dict)
        self.bspline.knots.insert(self.index, self.new_knot)

        if not self.bspline.control_points_visible:
            self.new_knot.hide_control_points()

        self.new_knot.setFocus(Qt.MouseFocusReason)
        super().redo()
        self.bspline.update()

    def undo(self) -> None:
        logger.debug(f"Undo: {self.text()}")
        super().undo()

        self.new_knot.scene().removeItem(self.new_knot)
        self.bspline.knots.pop(self.index)
        self.bspline._knots.pop(self.index)
        self.bspline.update()


class DeleteKnot(QUndoCommand):
    def __init__(self, knot: "layeritem.CubicSplineKnotItem", optimize_neighbours=True):
        self.knot = knot
        self.optimize_neighbours = optimize_neighbours
        super().__init__()
        self.setText("Delete Knot")

        self.bspline = self.knot.bspline
        self.layeritem = self.bspline.layer_item
        self.index = self.bspline.knots.index(self.knot)

        left = self.bspline.knots[self.index - 1] if self.index - 1 > 0 else None
        right = (
            self.bspline.knots[self.index + 1]
            if self.index + 1 < len(self.bspline.knots)
            else None
        )
        if left and self.optimize_neighbours:
            OptimizeControlPoints(left, self.bspline, propagate=False, parent=self)
        if right and self.optimize_neighbours:
            OptimizeControlPoints(right, self.bspline, propagate=False, parent=self)

        neighbours = self.layeritem.get_neighbour_elements(self.bspline)
        if len(self.bspline.knots) == 1:
            # Delete Bspline object when last knot is removed
            DeleteCurve(self.bspline, self)
        elif self.knot is self.bspline.knots[0]:
            p = neighbours[0] if neighbours[0].end == self.knot.center else None
            if p:
                ChangePolygon(p, end=self.bspline.knots[1].center, parent=self)
        elif self.knot is self.bspline.knots[-1]:
            p = neighbours[1] if neighbours[1].start == self.knot.center else None
            if p:
                ChangePolygon(p, start=self.bspline.knots[-2].center, parent=self)

    def redo(self) -> None:
        logger.debug(f"Redo: {self.text()}")
        if len(self.bspline.knots) > 1:
            self.bspline.scene().removeItem(self.knot)
            self.bspline.knots.pop(self.index)
            self.bspline._knots.pop(self.index)

            self.bspline.update()
        super().redo()

    def undo(self) -> None:
        logger.debug(f"Undo: {self.text()}")
        super().undo()
        # If Curve was not removed
        if self.bspline.parentItem():
            self.bspline.knots.insert(self.index, self.knot)
            self.bspline._knots.insert(self.index, self.knot.knot_dict)
            self.knot.setParentItem(self.bspline)

            self.bspline.update()


class DeleteCurve(QUndoCommand):
    def __init__(self, bspline: "layeritem.CubicSpline", parent=None):
        self.bspline = bspline
        self.layeritem = bspline.layer_item
        self.index = self.layeritem.cubic_splines.index(self.bspline)

        super().__init__(parent)
        self.setText("Delete Knot")

        # Rejoin Polygons
        p1 = [
            p for p in self.layeritem.polygons if p.end == self.bspline.knots[0].center
        ]
        p2 = [
            p
            for p in self.layeritem.polygons
            if p.start == self.bspline.knots[-1].center
        ]
        if p1 and p2:
            JoinPolygons(p1[0], p2[0], self)

    def redo(self) -> None:
        logger.debug(f"Redo: {self.text()}")
        self.layeritem.cubic_splines.pop(self.index)
        self.knots = self.layeritem.knots.pop(self.index)
        self.layeritem.scene().removeItem(self.bspline)

        super().redo()

    def undo(self) -> None:
        logger.debug(f"Undo: {self.text()}")
        super().undo()
        self.layeritem.cubic_splines.insert(self.index, self.bspline)
        self.layeritem.knots.insert(self.index, self.knots)
        self.bspline.setParentItem(self.layeritem)


class DeletePolygon(QUndoCommand):
    def __init__(self, polygon: "layeritem.PolygonPath", parent=None):
        self.polygon = polygon
        self.layeritem = self.polygon.layer_item

        super().__init__(parent)
        self.setText("Delete Layer Region")

        start, stop = self.polygon.x_region
        self.slice = np.s_[int(np.floor(start)) : int(np.ceil(stop))]

    def redo(self) -> None:
        logger.debug(f"Redo: {self.text()}")
        self.index = self.layeritem.polygons.index(self.polygon)
        self.layeritem.polygons.pop(self.index)
        self.heights = np.copy(self.polygon.heights[self.slice])
        self.polygon.heights[self.slice] = np.nan
        self.layeritem.scene().removeItem(self.polygon)

        super().redo()

    def undo(self) -> None:
        logger.debug(f"Undo: {self.text()}")
        super().undo()
        self.layeritem.polygons.insert(self.index, self.polygon)
        self.polygon.heights[self.slice] = self.heights
        self.polygon.setParentItem(self.layeritem)


class OptimizeControlPoints(QUndoCommand):
    def __init__(
        self,
        knot: "layeritem.CubicSplineKnotItem",
        bspline: "layeritem.CubicSpline",
        propagate=False,
        parent=None,
    ):
        self.knot = knot
        self.bspline = bspline

        self.propagate = propagate
        super().__init__(parent)
        self.setText("Optimize Controllpoints")

        self.in_pos, self.out_pos = None, None
        self.old_in_pos, self.old_out_pos = None, None
        self.left, self.right = None, None
        if self.propagate:
            if not self.knot in self.bspline.knots:
                knots = sorted(
                    self.bspline.knots + [self.knot],
                    key=lambda x: x.knot_dict["knot_pos"][0],
                )
            else:
                knots = self.bspline.knots

            index = knots.index(self.knot)
            left = knots[index - 1] if index > 0 else None
            right = knots[index + 1] if index < len(knots) - 1 else None

            if left:
                self.left = OptimizeControlPoints(
                    left, self.bspline, propagate=False, parent=self
                )
            if right:
                self.right = OptimizeControlPoints(
                    right, self.bspline, propagate=False, parent=self
                )

    def redo(self) -> None:
        logger.debug(f"Redo: {self.text()}")
        if not self.old_in_pos:
            self.old_in_pos, self.old_out_pos = (
                self.knot.cp_in_pos,
                self.knot.cp_out_pos,
            )
        if not self.in_pos:
            self.in_pos, self.out_pos = self.bspline.optimize_controllpoints(self.knot)

        self.knot.cp_in = self.in_pos
        self.knot.cp_out = self.out_pos
        super().redo()

    def undo(self) -> None:
        logger.debug(f"Undo: {self.text()}")
        self.knot.cp_in = self.old_in_pos
        self.knot.cp_out = self.old_out_pos
        super().undo()

    def id(self) -> int:
        return 5

    def mergeWith(self, other: QUndoCommand) -> bool:
        if self.knot != other.knot:
            return False
        if not self.left and other.left:
            return False
        if not self.right and other.right:
            return False

        self.in_pos = other.in_pos
        self.out_pos = other.out_pos

        if self.propagate:
            if self.left:
                self.left.mergeWith(other.left)
            if self.right:
                self.right.mergeWith(other.right)
        return True


class AddCurve(QUndoCommand):
    def __init__(self, layer_item: "layeritem.LayerItem", pos: QPointF):
        self.layeritem = layer_item

        pos.setX(np.floor(pos.x()) + 0.5)
        self.pos = pos
        super().__init__()
        self.setText("New Curve")

        knot_dict = {
            "knot_pos": (pos.x(), pos.y()),
            "cp_in_pos": (pos.x() - 10, pos.y()),
            "cp_out_pos": (pos.x() + 10, pos.y()),
        }

        self.knots = []
        self.bspline = layeritem.CubicSpline(self.knots, None)
        self.new_knot = layeritem.CubicSplineKnotItem(parent=None, knot_dict=knot_dict)

        self.new_knot.setParentItem(self.bspline)
        self.bspline._knots.append(self.new_knot.knot_dict)
        self.bspline.knots.append(self.new_knot)

        if not self.bspline.control_points_visible:
            self.new_knot.hide_control_points()

        # Get insertion index
        i = 0
        for cs in self.layeritem.cubic_splines:
            if self.new_knot.center.x() > cs.start.x():
                i += 1
            else:
                break
        self.index = i

        # Split polygon if new Curve lies in it.
        polygon = [p for p in self.layeritem.polygons if self.pos in p]
        if polygon:
            polygon = polygon[0]
            SplitPolygons(polygon, self.pos, self)

        self.update_array = UpdateLayerArray(self.bspline, parent=self)

    def redo(self) -> None:
        logger.debug(f"Redo: {self.text()}")
        self.bspline.setParentItem(self.layeritem)
        self.layeritem.knots.insert(self.index, self.knots)
        self.layeritem.cubic_splines.insert(self.index, self.bspline)

        self.new_knot.setFocus(Qt.MouseFocusReason)

        super().redo()
        self.layeritem.update()

    def undo(self) -> None:
        logger.debug(f"Undo: {self.text()}")
        super().undo()
        self.bspline.scene().removeItem(self.bspline)
        self.layeritem.cubic_splines.pop(self.index)
        self.layeritem.knots.pop(self.index)
        self.layeritem.update()


class SplitPolygons(QUndoCommand):
    def __init__(self, polygon: "layeritem.PolygonPath", pos: QPointF, parent=None):
        self.polygon = polygon
        self.pos = pos

        self.layeritem = self.polygon.layer_item
        self.new_polygons = [
            layeritem.PolygonPath(
                None, self.polygon.heights, self.polygon.start, self.pos
            ),
            layeritem.PolygonPath(
                None, self.polygon.heights, self.pos, self.polygon.end
            ),
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


class JoinPolygons(QUndoCommand):
    def __init__(
        self, p1: "layeritem.PolygonPath", p2: "layeritem.PolygonPath", parent=None
    ):
        self.polygons = [p1, p2]

        self.layeritem = p1.layer_item
        self.new_polygon = layeritem.PolygonPath(None, p1.heights, p1.start, p2.end)
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
