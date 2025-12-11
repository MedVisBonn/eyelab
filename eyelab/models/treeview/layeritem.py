import logging
from itertools import groupby
from typing import Any, Dict, List, Tuple
import bisect

import eyepy as ep
import numpy as np
from PySide6.QtCore import QLineF, QPoint, QPointF, QRectF, Qt, QTimer
from PySide6.QtGui import QColor, QFocusEvent, QKeyEvent, QPainterPath, QPen, QPolygonF
from PySide6.QtWidgets import (
    QApplication,
    QGraphicsEllipseItem,
    QGraphicsItem,
    QGraphicsLineItem,
    QGraphicsPathItem,
    QGraphicsRectItem,
    QGraphicsSceneHoverEvent,
    QGraphicsSceneMouseEvent,
)
from scipy.interpolate import interp1d

from eyelab.commands import get_undo_stack
from eyelab.commands import layeritem as layer_commands
from eyelab.commands.layeritem import (
    DeleteCurve,
    DeletePolygon,
    MoveControlKnot,
)
from eyelab.models.treeview.itemgroup import ItemGroup

logger = logging.getLogger(__name__)


class ControllPointGraphicsItem(QGraphicsRectItem):
    def __init__(self, parent, pos, **kwargs):
        super().__init__(parent=parent, **kwargs)
        self.setFlag(QGraphicsItem.ItemIgnoresTransformations, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemSendsScenePositionChanges)

        self.setRect(QRectF(QPoint(-4, -4), QPoint(4, 4)))
        self.setPos(pos)

        pen = QPen(QColor("blue"))
        pen.setCosmetic(True)
        self.setPen(pen)

    @property
    def center(self):
        return self.mapToScene(QPointF(0, 0))

    def as_tuple(self):
        center = self.center
        return np.round(center.x(), 2), np.round(center.y(), 2)

    def mouseMoveEvent(self, event: "QGraphicsSceneMouseEvent") -> None:
        command = MoveControlKnot(self, self.mapToParent(event.pos()))
        get_undo_stack("main").push(command)
        super().mouseMoveEvent(event)

    def itemChange(self, change: QGraphicsItem.GraphicsItemChange, value: Any) -> Any:
        if (
            change == QGraphicsItem.ItemPositionChange
            or change == QGraphicsItem.ItemScenePositionHasChanged
        ):
            self.parentItem().set_line_of(self)

            if self is self.parentItem().cp_in:
                self.parentItem().knot_dict["cp_in_pos"] = self.as_tuple()
            elif self is self.parentItem().cp_out:
                self.parentItem().knot_dict["cp_out_pos"] = self.as_tuple()
            return value

        return value


class CubicSplineKnotItem(QGraphicsEllipseItem):
    def __init__(
        self,
        parent,
        knot_dict: dict,
        **kwargs,
    ):
        """"""
        super().__init__(parent=parent, **kwargs)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsFocusable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        self.setFlag(QGraphicsItem.ItemIgnoresTransformations, True)

        self.knot_dict = knot_dict
        # Create knot
        self._cp_in = None
        self._cp_out = None

        self.setRect(QRectF(QPoint(-5, -5), QPoint(5, 5)))
        self.setPos(self.mapFromScene(self.knot_pos))
        pen = QPen(QColor("red"))
        pen.setCosmetic(True)
        self.setPen(pen)

        # Create control points
        pen = QPen(QColor("blue"))
        pen.setCosmetic(True)
        self.cps_visible = True

        self._cp_in = ControllPointGraphicsItem(self, self.mapFromScene(self.cp_in_pos))
        self._line_in = QGraphicsLineItem(
            QLineF(
                self.mapFromScene(self.center),
                self.mapFromScene(self.cp_in.center),
            ),
            parent=self,
        )
        self._line_in.setPen(pen)

        self._cp_out = ControllPointGraphicsItem(
            self, self.mapFromScene(self.cp_out_pos)
        )
        self._line_out = QGraphicsLineItem(
            QLineF(
                self.mapFromScene(self.center),
                self.mapFromScene(self.cp_out.center),
            ),
            parent=self,
        )
        self._line_out.setPen(pen)

    def itemChange(self, change: QGraphicsItem.GraphicsItemChange, value: Any) -> Any:
        if change == QGraphicsItem.ItemPositionChange and self.scene():
            newPos = QPointF(value)
            rect = self.scene().sceneRect()

            if not rect.contains(newPos):
                # Keep the item inside the scene rect.
                newPos.setX(min(rect.right(), max(newPos.x(), rect.left())))
                newPos.setY(min(rect.bottom(), max(newPos.y(), rect.top())))

            self.knot_dict["knot_pos"] = self.as_tuple()
            return newPos
        return value

    @property
    def bspline(self) -> "CubicSpline":
        return self.parentItem()

    @property
    def layer_item(self) -> "LayerItem":
        return self.parentItem().parentItem()

    def as_tuple(self):
        center = self.center
        return np.round(center.x(), 2), np.round(center.y(), 2)

    def sync(self):
        self.knot_pos = self.as_tuple()
        if self.cp_in:
            self.cp_in_pos = self.cp_in.as_tuple()
        if self.cp_out:
            self.cp_out_pos = self.cp_out.as_tuple()

    @property
    def knot_pos(self):
        return QPointF(*self.knot_dict["knot_pos"])

    @knot_pos.setter
    def knot_pos(self, value: tuple):
        self.knot_dict["knot_pos"] = value

    @property
    def cp_in_pos(self):
        return QPointF(*self.knot_dict["cp_in_pos"])

    @cp_in_pos.setter
    def cp_in_pos(self, value: tuple):
        self.knot_dict["cp_in_pos"] = value

    @property
    def cp_out_pos(self):
        return QPointF(*self.knot_dict["cp_out_pos"])

    @cp_out_pos.setter
    def cp_out_pos(self, value: tuple):
        self.knot_dict["cp_out_pos"] = value

    def set_cp_out_length(self, length):
        line = QLineF(self.center, self.cp_out.center)
        line.setLength(length)
        self.cp_out = line.p2()

    def set_cp_in_length(self, length):
        line = QLineF(self.center, self.cp_in.center)
        line.setLength(length)
        self.cp_in = line.p2()

    @property
    def center(self) -> QPointF:
        return self.mapToScene(QPointF(0, 0))

    def hide_control_points(self):
        self.cps_visible = False
        self._cp_in.hide()
        self._cp_out.hide()
        self._line_in.hide()
        self._line_out.hide()

    def show_control_points(self):
        self.cps_visible = True
        self._cp_in.show()
        self._cp_out.show()
        self._line_in.show()
        self._line_out.show()

    @property
    def cp_in(self) -> ControllPointGraphicsItem:
        return self._cp_in

    @cp_in.setter
    def cp_in(self, cp):
        self._cp_in.setPos(self.mapFromScene(cp))
        self._set_line_in()
        self.cp_in_pos = self.cp_in.as_tuple()

    @property
    def cp_out(self) -> ControllPointGraphicsItem:
        return self._cp_out

    @cp_out.setter
    def cp_out(self, cp):
        self.cp_out.setPos(self.mapFromScene(cp))
        self._set_line_out()
        self.cp_out_pos = self.cp_out.as_tuple()

    def set_lines(self):
        if self.cps_visible:
            self._set_line_out()
            self._set_line_in()

    def set_line_of(self, cp: ControllPointGraphicsItem):
        if cp == self.cp_in:
            self._set_line_in()
        elif cp == self.cp_out:
            self._set_line_out()

    def _set_line_in(self):
        self._line_in.setLine(
            QLineF(self.mapFromScene(self.center), self.mapFromScene(self.cp_in.center))
        )

    def _set_line_out(self):
        self._line_out.setLine(
            QLineF(
                self.mapFromScene(self.center), self.mapFromScene(self.cp_out.center)
            )
        )

    def focusInEvent(self, event: QFocusEvent) -> None:
        pen = self.pen()
        pen.setStyle(Qt.DotLine)
        self.setPen(pen)
        super().focusInEvent(event)

    def focusOutEvent(self, event: QFocusEvent) -> None:
        pen = self.pen()
        pen.setStyle(Qt.SolidLine)
        self.setPen(pen)
        super().focusOutEvent(event)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        if event.buttons() & Qt.RightButton:
            self.layer_item._delete_knot_macro(self)
            event.accept()
            return
        self.parentItem().parentItem().active_curve = self.parentItem()
        event.accept()

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        # Make sure knot does not cross neighboring knots in same spline
        knot_index = self.bspline.knots.index(self)
        spline_index = self.layer_item.cubic_splines.index(self.bspline)

        if knot_index > 0:
            left_barrier = self.bspline.knots[knot_index - 1].center.x()
        else:
            if spline_index > 0:
                left_barrier = (
                    self.layer_item.cubic_splines[spline_index - 1].knots[-1].center.x()
                )
            else:
                left_barrier = 0

        if knot_index + 1 < len(self.bspline.knots):
            right_barrier = self.bspline.knots[knot_index + 1].center.x()
        else:
            if spline_index + 1 < len(self.layer_item.cubic_splines):
                right_barrier = (
                    self.layer_item.cubic_splines[spline_index + 1].knots[0].center.x()
                )
            else:
                right_barrier = self.scene().shape[1]

        # Make sure event x-pos is within barriers by setting it
        event_pos = event.scenePos()
        if event_pos.x() < left_barrier:
            event_pos.setX(left_barrier)
        elif event_pos.x() > right_barrier:
            event_pos.setX(right_barrier)

        self._move_knot_macro(event_pos)
        event.accept()

    def keyPressEvent(self, event: QKeyEvent) -> None:
        # modifiers = QApplication.keyboardModifiers()
        if event.key() == Qt.Key_Delete:
            self.layer_item._delete_knot_macro(self)
            event.accept()
            return
        super().keyPressEvent(event)

    def _move_knot_macro(self, new_pos: QPointF):
        """Macro for moving a knot - used to group multiple MoveKnot commands"""
        old_pos = self.center
        left_neighbours, right_neighbours = self.layer_item.get_neighbour_polygons(
            self.bspline
        )

        stack = get_undo_stack("main")
        stack.beginMacro("Move Knot")
        stack.push(layer_commands.MoveKnot(self, new_pos))
        stack.push(layer_commands.OptimizeControlPoints(self))
        # If not first knot optimize knot before
        if self.bspline.knots.index(self) > 0:
            previous_knot = self.bspline.knots[self.bspline.knots.index(self) - 1]
            stack.push(layer_commands.OptimizeControlPoints(previous_knot))
        # I fnot last knot optimize knot after
        if self.bspline.knots.index(self) + 1 < len(self.bspline.knots):
            next_knot = self.bspline.knots[self.bspline.knots.index(self) + 1]
            stack.push(layer_commands.OptimizeControlPoints(next_knot))

        # if knot is first or last in curve, update/remove neighboring polygons
        if self is self.bspline.knots[-1]:
            if right_neighbours:
                if new_pos.x() > old_pos.x():
                    for n in right_neighbours:
                        # Find the closest neighbour that is not covered after the move
                        if n.end.x() <= new_pos.x():
                            # Delete polygon if it is covered, do not set heights to nan since the curve already covers it
                            stack.push(
                                layer_commands.DeletePolygon(n, heights_to_nan=False)
                            )
                        elif n.end.x() > new_pos.x() and n.start.x() < new_pos.x():
                            # Change the neighbour if the new pos is in its region
                            stack.push(layer_commands.ChangePolygon(n, start=new_pos))
                            break
                        elif new_pos.x() < n.start.x():
                            break

                elif new_pos.x() < old_pos.x():
                    # If the curve shrinks (rightmost knot moves left)
                    if int(right_neighbours[0].start.x()) == int(old_pos.x()):
                        # Disconnect neighbour polygon
                        new_start = QPointF(
                            old_pos.x() + 1,
                            self.layer_item.height_map[int(old_pos.x() + 1)],
                        )
                        stack.push(
                            layer_commands.ChangePolygon(
                                right_neighbours[0], start=new_start
                            )
                        )
                    # Set the heights of the uncovered region to nan
                    stack.push(
                        layer_commands.ClearHeights(
                            layeritem=self.layer_item,
                            start=new_pos.x() + 1,
                            end=old_pos.x() + 1,
                        )
                    )
            else:
                # No right neighbours, just clear heights
                if new_pos.x() < old_pos.x():
                    stack.push(
                        layer_commands.ClearHeights(
                            layeritem=self.layer_item,
                            start=new_pos.x() + 1,
                            end=old_pos.x() + 1,
                        )
                    )

        if self is self.bspline.knots[0]:
            if left_neighbours:
                if new_pos.x() < old_pos.x():
                    for n in left_neighbours:
                        # Find the closest neighbour that is not covered after the move
                        if n.start.x() >= new_pos.x():
                            # Delete polygon if it is covered, do not set heights to nan since the curve already covers it
                            stack.push(
                                layer_commands.DeletePolygon(n, heights_to_nan=False)
                            )
                        elif n.start.x() < new_pos.x() and n.end.x() > new_pos.x():
                            # Change the neighbour if the new pos is in its region
                            stack.push(layer_commands.ChangePolygon(n, end=new_pos))
                            break
                        elif new_pos.x() > n.end.x():
                            break

                elif new_pos.x() > old_pos.x():
                    # If the curve shrinks (leftmost knot moves right)
                    # Set the heights of the uncovered region to nan
                    if int(left_neighbours[0].end.x()) == int(old_pos.x()):
                        # Disconnect neighbour polygon
                        new_end = QPointF(
                            old_pos.x() - 1,
                            self.layer_item.height_map[int(old_pos.x() - 1)],
                        )
                        stack.push(
                            layer_commands.ChangePolygon(
                                left_neighbours[0], end=new_end
                            )
                        )
                    stack.push(
                        layer_commands.ClearHeights(
                            layeritem=self.layer_item,
                            start=old_pos.x(),
                            end=new_pos.x(),
                        )
                    )

            else:
                # No left neighbours, just clear heights
                if new_pos.x() > old_pos.x():
                    stack.push(
                        layer_commands.ClearHeights(
                            layeritem=self.layer_item,
                            start=old_pos.x(),
                            end=new_pos.x(),
                        )
                    )
        stack.push(layer_commands.UpdateLayerArray(self.bspline))
        stack.endMacro()


class CubicSpline(QGraphicsPathItem):
    """Editable cubic Bezier spline curve for layer manipulation.

    Consists of knots (CubicSplineKnotItem) with control points.
    Covers a region of the height map from first to last knot.
    """

    def __init__(self, knots: List[dict], parent: "LayerItem"):
        super().__init__(parent=parent)
        self._knots = knots
        self.control_points_visible = False
        # Add knots and controll points for every Curve
        self.knots = [
            CubicSplineKnotItem(parent=self, knot_dict=k) for k in self._knots
        ]

        self.hide_control_points()
        self.hide_knots()

        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsItem.ItemIsFocusable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)

    def setParentItem(self, parent: "LayerItem") -> None:
        super().setParentItem(parent)

    @property
    def start(self) -> QPointF:
        return self.knots[0].center

    @property
    def end(self) -> QPointF:
        return self.knots[-1].center

    @property
    def x_region(self) -> Tuple[float, float]:
        if len(self.knots) == 0:
            return 0.0, 0.0
        return self.start.x(), self.end.x()

    def __contains__(self, item):
        if self.start.x() < item.x() < self.end.x():
            return True
        return False

    def _build_path(self) -> QPainterPath:
        knots = self.knots
        if len(knots) == 0:
            return QPainterPath()

        path = QPainterPath(knots[0].center)
        last_knot = knots[0]
        if len(knots) == 1:
            return path

        for i, current_knot in enumerate(knots[1:], 1):
            current = current_knot.center
            path.cubicTo(last_knot.cp_out.center, current_knot.cp_in.center, current)
            last_knot = current_knot
        return path

    def hide_knots(self):
        for knot in self.knots:
            knot.hide()

    def show_knots(self):
        for knot in self.knots:
            knot.show()

    def hide_control_points(self):
        for knot in self.knots:
            knot.hide_control_points()
        self.control_points_visible = False

    def show_control_points(self):
        for knot in self.knots:
            knot.show_control_points()
        self.control_points_visible = True

    def indices(self):
        # Older versions of EyeLab did not set all knots to x.5
        # Add or subtract 0.5 before determining start and end of  the indices
        # to make sure that start and end are in the correct range - no
        # out of bounds error by interpolator

        start = np.ceil(self.start.x() - 0.5).astype(int)
        end = np.floor(self.end.x() - 0.5).astype(int)

        if start == end:
            return {start: self.start.y()}

        n_points = end - start + 1
        x_indices = []
        y_indices = []
        self.setPath(self._build_path())
        for t in np.linspace(0, 1, n_points * 2):
            point = self.path().pointAtPercent(t)
            x_indices.append(point.x())
            y_indices.append(point.y())

        x_indices = np.round(np.array(x_indices), 5)
        y_indices = np.array(y_indices)

        f = interp1d(
            x_indices, y_indices, assume_sorted=True, copy=False, bounds_error=True
        )
        x = np.arange(start, end + 1, dtype=int)
        # Get height for the middle of each pixel
        y = f(x + 0.5)

        return {xi: yi for xi, yi in zip(x, y)}

    def update(self):
        self.setPath(self._build_path())
        super().update()

    def add_knot(self, knot: CubicSplineKnotItem) -> None:
        knot.setParentItem(self)
        if len(self._knots) > 0:
            # Get insertion index
            i = 0
            for k in self._knots:
                if knot.center.x() > k["knot_pos"][0]:
                    i += 1
                    continue
                break
            self._knots.insert(i, knot.knot_dict)
            self.knots.insert(i, knot)
        else:
            self._knots.append(knot.knot_dict)
            self.knots.append(knot)

        if not self.control_points_visible:
            knot.hide_control_points()

    def shape(self) -> QPainterPath:
        # Create a path which closes without increasing its "area"
        # Only clicking exactly the line should activate this item
        path = self.path()
        path.connectPath(self.path().toReversed())
        return path

    def optimize_controllpoints(self, knot, distance_factor=0.35):
        knots = self.knots
        index = knots.index(knot)

        # options_widget = self.scene().current_tool.options_widget
        # optimize_strength = options_widget.strengthCheckBox.isChecked()
        # optimize_angle = options_widget.slopeCheckBox.isChecked()
        # optimize_neighbours = options_widget.neighbourCheckBox.isChecked()

        # meta = self.annotation_data.meta
        optimize_strength = True  # meta["spline:optimize_strength"]
        optimize_angle = True  # meta["spline:optimize_angle"]

        if len(knots) == 1:
            pos = knot.center
            source = QLineF(QPointF(pos.x() - 10, pos.y()), pos)
            target = QLineF(pos, QPointF(pos.x() + 10, pos.y()))

        elif index == 0:
            target = QLineF(knot.center, knots[1].center)
            source = (
                QLineF()
                .fromPolar(target.length(), 180 + target.angle())
                .translated(knot.center)
            )
            source.setPoints(source.p2(), source.p1())

        elif index == len(knots) - 1:
            source = QLineF(knots[-2].center, knot.center)
            target = (
                QLineF()
                .fromPolar(source.length(), source.angle())
                .translated(knot.center)
            )
        else:
            source = QLineF(knots[index - 1].center, knot.center)
            target = QLineF(knot.center, knots[index + 1].center)

        targetAngle = target.angleTo(source)
        if targetAngle > 180:
            angle = (source.angle() + source.angleTo(target) / 2) % 360
        else:
            angle = (target.angle() + target.angleTo(source) / 2) % 360

        if optimize_strength:
            length_in = source.dx() * distance_factor
            length_out = target.dx() * distance_factor
        else:
            length_in = knot._line_in.line().length()
            length_out = knot._line_out.line().length()

        if optimize_angle:
            angle_in = angle + 180
            angle_out = angle
        else:
            angle_in = (knot._line_in.line().angle()) % 360
            angle_out = knot._line_out.line().angle()

        revTarget = QLineF.fromPolar(length_in, angle_in).translated(knot.center)
        cp_in = revTarget.p2()

        revSource = QLineF.fromPolar(length_out, angle_out).translated(knot.center)
        cp_out = revSource.p2()
        return cp_in, cp_out

    @property
    def layer_item(self) -> "LayerItem":
        return self.parentItem()

    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        pen = self.pen()
        pen.setWidth(pen.width() + 3)
        self.setPen(pen)
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        pen = self.pen()
        pen.setWidth(pen.width() - 3)
        self.setPen(pen)
        super().hoverLeaveEvent(event)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        self.layer_item.active_curve = self
        super().mousePressEvent(event)

    def focusInEvent(self, event: QFocusEvent) -> None:
        pen = self.pen()
        pen.setStyle(Qt.DotLine)
        self.setPen(pen)
        super().focusInEvent(event)

    def focusOutEvent(self, event: QFocusEvent) -> None:
        pen = self.pen()
        pen.setStyle(Qt.SolidLine)
        self.setPen(pen)
        super().focusOutEvent(event)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key_Delete:
            command = DeleteCurve(self)
            get_undo_stack("main").push(command)
            event.accept()
            return
        super().keyPressEvent(event)


class PolygonPath(QGraphicsPathItem):
    """Non-editable path showing height_map regions NOT covered by cubic splines.

    Auto-generated from height_map data. Start/end points connect to
    neighboring curve knots. Updated when curves are added/removed/moved.
    """

    def __init__(self, parent: "LayerItem", start: QPointF = None, end: QPointF = None):
        super().__init__(parent)
        if parent:
            self.heights = parent.height_map
        self._start = start
        self._end = end

        # self.setAcceptHoverEvents(True)
        # self.setFlag(QGraphicsItem.ItemIsFocusable)
        # self.update()

    def setParentItem(self, parent: QGraphicsItem) -> None:
        self.heights = parent.height_map
        super().setParentItem(parent)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        super().mousePressEvent(event)

    def shape(self) -> QPainterPath:
        # Create a path which closes without increasing its "area"
        # Only clicking exactly the line should activate this item
        path = self.path()
        path.connectPath(self.path().toReversed())
        return path

    @property
    def layer_item(self) -> "LayerItem":
        return self.parentItem()

    def _get_points(self):
        points = []
        if self._start is None:
            start_index = 0
        else:
            start_index = int(np.floor(self._start.x()))
            points.append(self._start)

        if self._end is None:
            end_index = len(self.heights)
        else:
            end_index = int(np.ceil(self._end.x()))

        # Make sure there are no Nans between start and stop - interpolate
        if any(np.isnan(self.heights[start_index:end_index])):
            x = np.arange(start_index, end_index, dtype=int)
            x_full = x[~np.isnan(self.heights[x])]
            x_empty = x[np.isnan(self.heights[x])]
            if len(x_full) > 1:
                f = interp1d(
                    x_full,
                    self.heights[x_full],
                    assume_sorted=True,
                    copy=False,
                    bounds_error=False,
                    fill_value="extrapolate",
                )
                # Get height for the middle of each pixel
                y = f(x_empty + 0.5)
                self.heights[x_empty] = y

        for i in range(start_index, end_index):
            # +0.5 for points to sit in the middle and not start of each pixel (in x direction)
            points.append(QPointF(i + 0.5, self.heights[i]))

        if self._end is not None:
            points.append(self._end)
        return points

    def update(self):
        points = self._get_points()
        if points == []:
            self.setPath(QPainterPath())
            super().update()
            return

        self.polygon = QPolygonF().fromList(points)
        path = QPainterPath()
        path.addPolygon(self.polygon)
        self.setPath(path)
        super().update()

    @property
    def start(self) -> QPointF:
        return self._start

    @start.setter
    def start(self, point: QPointF) -> None:
        self._start = point
        self.update()

    @property
    def end(self) -> QPointF:
        return self._end

    @end.setter
    def end(self, point: QPointF) -> None:
        self._end = point
        self.update()

    @property
    def x_region(self) -> Tuple[float, float]:
        return self.start.x(), self.end.x()

    def __contains__(self, item):
        if self.start.x() < item.x() < self.end.x():
            return True
        return False

    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        pen = self.pen()
        pen.setWidth(pen.width() + 3)
        self.setPen(pen)
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        pen = self.pen()
        pen.setWidth(pen.width() - 3)
        self.setPen(pen)
        super().hoverLeaveEvent(event)

    def focusInEvent(self, event: QFocusEvent) -> None:
        pen = self.pen()
        pen.setStyle(Qt.DotLine)
        self.setPen(pen)
        super().focusInEvent(event)

    def focusOutEvent(self, event: QFocusEvent) -> None:
        pen = self.pen()
        pen.setStyle(Qt.SolidLine)
        self.setPen(pen)
        super().focusOutEvent(event)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key_Delete:
            command = DeletePolygon(self)
            get_undo_stack("main").push(command)
            event.accept()
            return
        super().keyPressEvent(event)


class LayerItem(QGraphicsPathItem):
    """Graphics item representing a layer annotation for one B-scan slice.

    Architecture:
    - Height map (annotation_data.data[index]) is the PRIMARY data source
    - Cubic splines provide editable curves for manipulation
    - Polygons fill gaps between curves (auto-generated from height_map)

    Data Flow:
    1. User edits knots/curves
    2. Commands update height_map immediately (via UpdateLayerArray)
    3. Polygons read from height_map and connect to curve endpoints
    4. All changes are undo/redo-able via QUndoCommand system

    Key Invariants:
    - Height map always reflects current curve state
    - Knots are at pixel centers (x = floor(x) + 0.5)
    - Curves are sorted by x-position
    - Polygons fill non-curve regions of height_map
    """

    def __init__(
        self, data: ep.EyeVolumeLayerAnnotation, index: int, parent: ItemGroup
    ):
        super().__init__(parent=parent)
        self.annotation_data = data
        self.index = index

        # Keep track of the currently active curve (for adding knots)
        self.active_curve = None

        # Make sure knots are List[Curve[KnotDict]] and not List[KnotDict]
        knots = self.annotation_data.knots[self.index]
        if knots:
            if isinstance(knots[0], dict):
                self.annotation_data.knots[self.index] = [
                    sorted(knots, key=lambda x: x["knot_pos"][0])
                ]

        # Create cubic splines first
        self.cubic_splines = [CubicSpline(knots, self) for knots in self.knots]

        # Create polygons from height_map regions NOT covered by curves
        # This must happen AFTER curves are created so we know which regions to exclude
        self.polygons = self._get_polygons()

        self.setFlag(QGraphicsItem.ItemIsPanel)
        self.setFlag(QGraphicsItem.ItemIsFocusable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)

        # Connect polygon endpoints to neighboring curve knots
        # This must happen AFTER both curves and polygons are created
        for cs in self.cubic_splines:
            left, right = self.get_neighbour_elements(cs)
            if left and isinstance(left, PolygonPath):
                left.end = cs.start
            if right and isinstance(right, PolygonPath):
                right.start = cs.end

        self.update()

        self._single_click_timer = QTimer(None, singleShot=True)
        self._single_click_timer.setSingleShot(True)
        self._single_click_timer.timeout.connect(self._handle_single_click_timeout)

    def get_neighbour_elements(self, layer_element):
        elements = sorted(self.cubic_splines + self.polygons, key=lambda x: x.start.x())
        index = elements.index(layer_element)
        left = elements[index - 1] if index > 0 else None
        right = elements[index + 1] if index + 1 < len(elements) else None
        return left, right

    def get_neighbour_polygons(self, layer_element):
        """Get polygons starting left and right from the given element

        The returned elements are ordered by their distance to the given elements

        :returns (left_neighbours, right_neighbours)
        """
        elements = sorted(
            self.polygons + [layer_element], key=lambda x: (x.start.x(), x.end.x())
        )
        index = elements.index(layer_element)
        return elements[:index][::-1], elements[index + 1 :]

    @property
    def knots(self):
        return self.annotation_data.knots[self.index]

    def _get_polygons(self) -> List[PolygonPath]:
        """Create polygons from the layer height maps in regions outside the cubic splines

        Polygons cover A-scans that are not part of a Cubic Spline and are connected to the first/last knot
        of neighbouring Cubic splines.
        """
        # Get polygon regions:
        layer_copy = self.height_map.copy()
        # Create a polygon for every non spline region
        for cs in self.cubic_splines:
            layer_copy[int(np.floor(cs.start.x())) : int(np.ceil(cs.end.x()))] = np.nan

        layer_copy = ~np.isnan(layer_copy)
        # Collect ranges of polygon regions (python indexing)
        i = 0
        polygon_regions = []

        for k, g in groupby(layer_copy):
            gl = len(list(g))
            if k:
                polygon_regions.append(
                    (
                        QPointF(i + 0.5, self.height_map[i]),
                        QPointF(i + gl - 0.5, self.height_map[i + gl - 1]),
                    )
                )
            i += gl

        return [PolygonPath(self, start, end) for start, end in polygon_regions]

    @property
    def height_map(self):
        return self.annotation_data.data[self.index]

    def validate_state(self, context: str = "") -> bool:
        """Validate that height_map and curve/polygon state are consistent.

        Useful for debugging. Call after major operations to catch bugs early.
        Returns True if valid, False otherwise (logs errors).
        """
        issues = []

        # Check that curves are sorted by x position
        for i in range(len(self.cubic_splines) - 1):
            if self.cubic_splines[i].end.x() >= self.cubic_splines[i + 1].start.x():
                issues.append(
                    f"Curves overlap or out of order: curve {i} ends at {self.cubic_splines[i].end.x()}, curve {i+1} starts at {self.cubic_splines[i+1].start.x()}"
                )

        # Check that polygons are sorted by x position
        for i in range(len(self.polygons) - 1):
            if self.polygons[i].end.x() >= self.polygons[i + 1].start.x():
                issues.append(
                    f"Polygons overlap or out of order: polygon {i} ends at {self.polygons[i].end.x()}, polygon {i+1} starts at {self.polygons[i+1].start.x()}"
                )

        # Check that knot x-positions are at pixel centers (x.5)
        for i, cs in enumerate(self.cubic_splines):
            for j, knot in enumerate(cs.knots):
                x = knot.center.x()
                if abs(x - (np.floor(x) + 0.5)) > 0.01:
                    issues.append(
                        f"Curve {i} knot {j} x-position not at pixel center: {x}"
                    )

        # Check that curve regions in height_map are not NaN
        for i, cs in enumerate(self.cubic_splines):
            start_x = int(np.floor(cs.start.x()))
            end_x = int(np.ceil(cs.end.x()))
            if end_x > start_x:
                curve_heights = self.height_map[start_x:end_x]
                nan_count = np.isnan(curve_heights).sum()
                if nan_count > 0:
                    issues.append(
                        f"Curve {i} region [{start_x}:{end_x}] has {nan_count} NaN values in height_map"
                    )

        if issues:
            logger.error(
                f"LayerItem validation failed{' at ' + context if context else ''}:"
            )
            for issue in issues:
                logger.error(f"  - {issue}")
            return False

        return True

    def setActive(self, active: bool) -> None:
        if active:
            for cs in self.cubic_splines:
                cs.show_knots()
                # cs.show_control_points()
        else:
            for cs in self.cubic_splines:
                cs.hide_knots()
                # cs.hide_control_points()
        super().setActive(active)

    def update(self):
        self.setVisible(self.annotation_data.meta["visible"])
        self.setZValue(self.annotation_data.meta["z_value"])

        color = QColor()
        color.setNamedColor(f"#{self.annotation_data.meta['current_color']}")

        pen = QPen(color)
        pen.setWidth(2)
        pen.setCosmetic(True)
        self.setPen(pen)

        for cs in self.cubic_splines:
            cs.setPen(pen)
            cs.update()

        for p in self.polygons:
            p.setPen(pen)
            p.update()

        super().update()

    def view(self):
        return self.scene().views()[0]

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        # Only start timer if there is no CubicSpline or CubicSplineKnotItem at the position
        pos = event.scenePos()

        # Check if there's a curve or knot at the click position
        items_at_pos = self.scene().items(pos)
        has_curve_or_knot = any(
            isinstance(item, (CubicSpline, CubicSplineKnotItem))
            for item in items_at_pos
        )

        interval = QApplication.doubleClickInterval()
        if not has_curve_or_knot and not self._single_click_timer.isActive():
            self._single_click_timer.start(interval)

        super().mousePressEvent(event)

    def _handle_single_click_timeout(self):
        """Handle single-click after timeout to set active curve."""
        logger.debug("Reset active curve")
        self.active_curve = None

    def mouseDoubleClickEvent(self, event):
        """Handle double-click to add knots or curves."""
        if self._single_click_timer.isActive():
            self._single_click_timer.stop()

        pos = event.scenePos()

        # Ignore event if not inside the scene
        if not self.scene().sceneRect().contains(pos):
            event.ignore()
            return

        # Find polygon/curve intersecting the new Knot
        cs = [cs for cs in self.cubic_splines if pos in cs]
        # if pos is in any existing curve add the knot to this curve
        if cs:
            self._add_knot_macro(cs[0], pos)
        # else if there is no active curve, create a new curve
        elif self.active_curve is None:
            self._add_curve_macro(pos)
        # else if there is an active curve add the knot to this curve
        else:
            bspline = self.active_curve
            # New Curve if there is other curve in between active curve and new knot
            if any(
                [
                    pos.x() < cs.start.x() < bspline.start.x()
                    or bspline.end.x() < cs.end.x() < pos.x()
                    for cs in self.cubic_splines
                ]
            ):
                self._add_curve_macro(pos)
            else:
                self._add_knot_macro(bspline, pos)

        # Accept event instead of super().. to prevent second mousePressEvent
        event.accept()

    def _add_curve_macro(self, pos: QPointF):
        stack = get_undo_stack("main")
        stack.beginMacro("Add Curve")
        stack.push(layer_commands.AddCurve(self, pos))

        # Split polygon if new Curve lies in it.
        polygon = [p for p in self.polygons if pos in p]
        if polygon:
            polygon = polygon[0]
            stack.push(layer_commands.SplitPolygons(polygon, pos))
        stack.endMacro()

    def _add_knot_macro(self, bspline, pos: QPointF):
        stack = get_undo_stack("main")
        stack.beginMacro("Add Knot")
        # Instantiate command first to access the new knot
        add_knot_command = layer_commands.AddKnot(bspline, pos)
        stack.push(add_knot_command)

        # Optimize the new knot
        stack.push(layer_commands.OptimizeControlPoints(add_knot_command.new_knot))

        # Optimize control points of neighbouring knots
        if len(bspline.knots) >= 2:
            right_index = (
                bisect.bisect_left(bspline.knots, pos.x(), key=lambda x: x.center.x())
                + 1
            )
            if right_index < len(bspline.knots):
                stack.push(
                    layer_commands.OptimizeControlPoints(bspline.knots[right_index])
                )
            left_index = right_index - 2
            if left_index >= 0:
                stack.push(
                    layer_commands.OptimizeControlPoints(bspline.knots[left_index])
                )

        # Create child commands to change neighbouring polygons if necessary
        left_neighbours, right_neighbours = self.get_neighbour_polygons(bspline)
        for n in right_neighbours:
            if pos in n:
                stack.push(layer_commands.ChangePolygon(n, start=pos))
                break
            elif pos.x() < n.start.x():
                break
            else:
                stack.push(layer_commands.DeletePolygon(n))

        for n in left_neighbours:
            if pos in n:
                stack.push(layer_commands.ChangePolygon(n, end=pos))
                break
            elif pos.x() > n.end.x():
                break
            else:
                stack.push(layer_commands.DeletePolygon(n))

        stack.push(layer_commands.UpdateLayerArray(bspline))
        stack.endMacro()

    def _delete_knot_macro(self, knot: CubicSplineKnotItem):
        stack = get_undo_stack("main")
        stack.beginMacro("Delete Knot")

        bspline = knot.bspline

        left_neighbours, right_neighbours = self.get_neighbour_polygons(bspline)
        # Run DeleteCurve if last knot is removed
        if len(bspline.knots) == 1:
            stack.push(layer_commands.DeleteCurve(bspline))
            if left_neighbours and right_neighbours:
                stack.push(
                    layer_commands.JoinPolygons(left_neighbours[0], right_neighbours[0])
                )
        else:
            is_fist = knot is knot.bspline.knots[0]
            is_last = knot is knot.bspline.knots[-1]

            stack.push(layer_commands.DeleteKnot(knot))
            for k in bspline.knots:
                stack.push(layer_commands.OptimizeControlPoints(k))

            if is_fist and left_neighbours and left_neighbours[0].end == knot.center:
                stack.push(
                    layer_commands.ChangePolygon(
                        left_neighbours[0], end=bspline.knots[1].center
                    )
                )
            elif (
                is_last
                and right_neighbours
                and right_neighbours[0].start == knot.center
            ):
                stack.push(
                    layer_commands.ChangePolygon(
                        right_neighbours[0], start=bspline.knots[-2].center
                    )
                )

        stack.push(layer_commands.UpdateLayerArray(bspline))
        stack.endMacro()

    def childNumber(self):
        if self.parentItem():
            return self.parentItem().childItems().index(self)
        return 0

    def childCount(self):
        return 0

    def columnCount(self):
        return 1

    def data(self, column: str):
        if column in ["visible", "z_value", "current_color"]:
            return getattr(self, column)
        elif column == "name":
            return self.meta["name"]

        raise Exception(f"column {column} not in data")

    def setData(self, column: str, value):
        if column in ["visible", "z_value", "current_color"]:
            setattr(self, column, value)
            self.update()
            return True
        return False

    def appendChild(self, data):
        items = self.childItems()

        if items:
            z_value = float(items[-1].zValue() + 1)
        else:
            z_value = 0.0

        data.z_value = z_value
        data.setParentItem(self)

    def insertChildren(self, row: int, count: int, data: List[Dict] = None):
        if row < 0:
            return False

        items = self.childItems()

        if items:
            z = float(items[-1].zValue() + 1)
        else:
            z = 0.0
        z_values = [float(x) for x in range(z, z + count)]

        for i, z_value in enumerate(z_values):
            if data:
                item_data = data[i]
            else:
                item_data = {}
            item_data.update(z_value=z_value)
            layer = type(self)(data=item_data)
            layer.setParentItem(self)

    def removeChildren(self, row: int, count: int):
        if row < 0 or row > self.childCount():
            raise Exception("what went wrong here?")
        items = self.childItems()

        for i in range(row, row + count):
            item = items[i]
            item.scene().removeItem(item)

    def switchChildren(self, row1: int, row2: int):
        child1 = self.child(row1)
        child2 = self.child(row2)

        child1_z = child1.zValue()
        child2_z = child2.zValue()
        child1.setData("z_value", child2_z)
        child2.setData("z_value", child1_z)

    # def contextMenuEvent(self, event: QGraphicsSceneContextMenuEvent) -> None:
    #    menu = QMenu()
    #    new_curve_action = QAction("New Curve")
    #    menu.addAction(new_curve_action)

    #    menu.exec(event.screenPos())

    #    new_curve_action.triggered.connect(lambda: self.setFocus())
    #    #super().contextMenuEvent(event)
