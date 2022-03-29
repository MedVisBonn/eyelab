from typing import List, Dict, Optional, Any

import numpy as np
from PySide6 import QtCore, QtWidgets, QtGui
import eyepy as ep

import logging

from eyelab.models.treeview.itemgroup import ItemGroup
from scipy.interpolate import interp1d

logger = logging.getLogger(__name__)


class ControllPointGraphicsItem(QtWidgets.QGraphicsRectItem):
    def __init__(self, parent, pos, **kwargs):
        super().__init__(parent=parent, **kwargs)

        self.setRect(QtCore.QRectF(QtCore.QPoint(-4, -4), QtCore.QPoint(4, 4)))
        self.setFlag(QtWidgets.QGraphicsItem.ItemIgnoresTransformations, True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemSendsGeometryChanges, True)
        self.setPos(pos)

        pen = QtGui.QPen(QtGui.QColor("blue"))
        pen.setCosmetic(True)
        self.setPen(pen)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)

    @property
    def center(self):
        return self.mapToScene(QtCore.QPointF(0, 0))

    def as_tuple(self):
        center = self.center
        return np.round(center.x(), 2), np.round(center.y(), 2)

    def mouseMoveEvent(self, event: "QGraphicsSceneMouseEvent") -> None:
        super().mouseMoveEvent(event)

        # Make sure control points move together to keep the curve smooth
        if self is self.parentItem().cp_in:
            line = QtCore.QLineF(self.center, self.parentItem().center)
            line2 = QtCore.QLineF(
                self.parentItem().center, self.parentItem().cp_out.center
            )
            line.setLength(line.length() + line2.length())
            self.parentItem().cp_out = line.p2()
        elif self is self.parentItem().cp_out:
            line = QtCore.QLineF(self.center, self.parentItem().center)
            line2 = QtCore.QLineF(
                self.parentItem().center, self.parentItem().cp_in.center
            )
            line.setLength(line.length() + line2.length())
            self.parentItem().cp_in = line.p2()

        self.parentItem().parentItem().parentItem().update_line()
        self.parentItem().set_lines()

    def itemChange(
        self, change: QtWidgets.QGraphicsItem.GraphicsItemChange, value: Any
    ) -> Any:
        if change == QtWidgets.QGraphicsItem.ItemPositionChange:
            self.parentItem().set_line_of(self)
            return value

        if change == QtWidgets.QGraphicsItem.ItemPositionHasChanged:
            self.parentItem().sync()

        return value

    def mouseReleaseEvent(self, event: "QGraphicsSceneMouseEvent") -> None:
        super().mouseReleaseEvent(event)


class KnotGraphicsItem(QtWidgets.QGraphicsEllipseItem):
    def __init__(self, parent, pos, **kwargs):
        super().__init__(parent=parent, **kwargs)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIgnoresTransformations, True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemSendsGeometryChanges, True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemSendsScenePositionChanges, True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsFocusable, True)

        self.setRect(QtCore.QRectF(QtCore.QPoint(-5, -5), QtCore.QPoint(5, 5)))
        self.setPos(pos)

        pen = QtGui.QPen(QtGui.QColor("red"))
        pen.setCosmetic(True)
        self.setPen(pen)

    def itemChange(
        self, change: QtWidgets.QGraphicsItem.GraphicsItemChange, value: Any
    ) -> Any:
        if change == QtWidgets.QGraphicsItem.ItemScenePositionHasChanged:
            self.stay_in_scene()
        if change == QtWidgets.QGraphicsItem.ItemPositionHasChanged:
            self.parentItem().parentItem().parentItem().update_line()
            self.parentItem().sync()

        return value

    def paint(
        self,
        painter: QtGui.QPainter,
        option: "QStyleOptionGraphicsItem",
        widget: Optional[QtWidgets.QWidget] = ...,
    ) -> None:
        super().paint(painter, option, widget)

    @property
    def center(self) -> QtCore.QPointF:
        return self.mapToScene(QtCore.QPointF(0, 0))

    def as_tuple(self):
        center = self.center
        return np.round(center.x(), 2), np.round(center.y(), 2)

    def mousePressEvent(self, event: "QGraphicsSceneMouseEvent") -> None:
        if event.buttons() & QtCore.Qt.RightButton:
            line_item = self.parentItem().parentItem()
            self.parentItem().parentItem().delete_knot(self.parentItem())
            event.accept()
        else:
            self.parentItem().mousePressEvent(event)

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        modifiers = QtWidgets.QApplication.keyboardModifiers()
        if modifiers == QtCore.Qt.ControlModifier:
            event.ignore()
            return
        if event.key() == QtCore.Qt.Key_Delete:
            self.parentItem().parentItem().delete_knot(self.parentItem())

    def mouseReleaseEvent(self, event: "QGraphicsSceneMouseEvent") -> None:
        self.parentItem().mouseReleaseEvent(event)

    def stay_in_scene(self):
        pos = self.center
        if pos.x() < 0:
            pos.setX(0)
        if pos.x() > self.scene().shape[1]:
            pos.setX(self.scene().shape[1])
        if pos.y() < 0:
            pos.setY(0)
        if pos.y() > self.scene().shape[0]:
            pos.setY(self.scene().shape[0])
        self.setPos(self.mapToParent(self.mapFromScene(pos)))

    def mouseMoveEvent(self, event: "QGraphicsSceneMouseEvent") -> None:
        self.parentItem().mouseMoveEvent(event)

    def focusInEvent(self, event: QtGui.QFocusEvent) -> None:
        super().focusInEvent(event)
        pen = QtGui.QPen(QtGui.QColor("yellow"))
        pen.setCosmetic(True)
        self.setPen(pen)
        self.update()

    def focusOutEvent(self, event: QtGui.QFocusEvent) -> None:
        super().focusOutEvent(event)
        pen = QtGui.QPen(QtGui.QColor("red"))
        pen.setCosmetic(True)
        self.setPen(pen)
        self.update()


class CubicSplineKnotItem(QtWidgets.QGraphicsItem):
    def __init__(
        self,
        parent,
        knot_dict: dict,
        **kwargs,
    ):
        """"""
        super().__init__(parent=parent, **kwargs)
        self.knot_dict = knot_dict
        # Create knot
        self._knot = None
        self._cp_in = None
        self._cp_out = None
        self._knot = KnotGraphicsItem(self, self.mapFromScene(self.knot_pos))
        # Create control points
        pen = QtGui.QPen(QtGui.QColor("blue"))
        pen.setCosmetic(True)
        self.cps_visible = True

        self._cp_in = ControllPointGraphicsItem(self, self.cp_in_pos)
        self._line_in = QtWidgets.QGraphicsLineItem(
            QtCore.QLineF(
                self.mapFromScene(self.knot.center),
                self.mapFromScene(self.cp_in.center),
            ),
            parent=self,
        )
        self._line_in.setPen(pen)

        self._cp_out = ControllPointGraphicsItem(self, self.cp_out_pos)
        self._line_out = QtWidgets.QGraphicsLineItem(
            QtCore.QLineF(
                self.mapFromScene(self.knot.center),
                self.mapFromScene(self.cp_out.center),
            ),
            parent=self,
        )
        self._line_out.setPen(pen)

        self.setFlag(QtWidgets.QGraphicsItem.ItemHasNoContents, True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemSendsGeometryChanges, True)

    def itemChange(
        self, change: QtWidgets.QGraphicsItem.GraphicsItemChange, value: Any
    ) -> Any:
        if change == QtWidgets.QGraphicsItem.ItemPositionChange:
            # self.knot.stay_in_scene()
            self.parentItem().optimize_controllpoints(self)
            self.parentItem().parentItem().update_line()

        if change == QtWidgets.QGraphicsItem.ItemPositionHasChanged:
            # Todo write to eyevolumelayerannotation
            pass
        return value

    def sync(self):
        if self.knot:
            self.knot_pos = self.knot.as_tuple()
        if self.cp_in:
            self.cp_in_pos = self.cp_in.as_tuple()
        if self.cp_out:
            self.cp_out_pos = self.cp_out.as_tuple()

    @property
    def knot_pos(self):
        return QtCore.QPointF(*self.knot_dict["knot_pos"])

    @knot_pos.setter
    def knot_pos(self, value: tuple):
        self.knot_dict["knot_pos"] = value

    @property
    def cp_in_pos(self):
        return QtCore.QPointF(*self.knot_dict["cp_in_pos"])

    @cp_in_pos.setter
    def cp_in_pos(self, value: tuple):
        self.knot_dict["cp_in_pos"] = value

    @property
    def cp_out_pos(self):
        return QtCore.QPointF(*self.knot_dict["cp_out_pos"])

    @cp_out_pos.setter
    def cp_out_pos(self, value: tuple):
        self.knot_dict["cp_out_pos"] = value

    def set_cp_out_length(self, length):
        line = QtCore.QLineF(self.center, self.cp_out.center)
        line.setLength(length)
        self.cp_out = line.p2()

    def set_cp_in_length(self, length):
        line = QtCore.QLineF(self.center, self.cp_in.center)
        line.setLength(length)
        self.cp_in = line.p2()

    def boundingRect(self) -> QtCore.QRectF:
        return self.childrenBoundingRect()

    def shape(self) -> QtGui.QPainterPath:
        path = QtGui.QPainterPath()
        return path

    @property
    def center(self) -> QtCore.QPointF:
        return self.knot.center

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
    def knot(self) -> KnotGraphicsItem:
        return self._knot

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
            QtCore.QLineF(
                self.mapFromScene(self.center), self.mapFromScene(self.cp_in.center)
            )
        )

    def _set_line_out(self):
        self._line_out.setLine(
            QtCore.QLineF(
                self.mapFromScene(self.center), self.mapFromScene(self.cp_out.center)
            )
        )


class CubicSpline(QtWidgets.QGraphicsPathItem):
    def __init__(self, knots: List[dict], parent: "LayerItem"):
        super().__init__(parent=parent)
        self._knots = knots
        self.control_points_visible = True
        # Add knots and controll points for every Curve
        self.knots = sorted(
            [CubicSplineKnotItem(parent=self, knot_dict=k) for k in self._knots],
            key=lambda x: x.knot.as_tuple()[0],
        )
        self.hide_knots()
        self.update_spline()

    def build_path(self) -> QtGui.QPainterPath:
        knots = sorted(self.knots, key=lambda x: x.center.x())
        if len(knots) == 0:
            return QtGui.QPainterPath()
        for i, current_knot in enumerate(knots):
            current = current_knot.center
            if i == 0:
                path = QtGui.QPainterPath(current)
                last_knot = current_knot
            else:
                path.cubicTo(
                    last_knot.cp_out.center, current_knot.cp_in.center, current
                )
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

    @property
    def x_region(self):
        if len(self.knots) == 0:
            return (0, 0)
        return self.knots[0].center.x(), self.knots[-1].center.x()

    @property
    def indices(self):
        start = np.rint(self.knots[0].center.x()).astype(int)
        end = np.rint(self.knots[-1].center.toPoint().x()).astype(int)

        n_points = end - start + 1
        x_indices = []
        y_indices = []
        for t in np.arange(n_points):
            point = self.path().pointAtPercent(t / n_points)
            if len(x_indices) == 0 or point.x() > x_indices[-1]:
                x_indices.append(point.x())
                y_indices.append(point.y())

        x_indices = np.array(x_indices)
        y_indices = np.array(y_indices)

        if n_points > 1:
            f = interp1d(
                x_indices, y_indices, assume_sorted=True, copy=False, bounds_error=True
            )
            x = np.arange(start + 1, end - 1, dtype=int)
            # Get height for the middle of each pixel
            y = f(x + 0.5)
        else:
            x, y = np.floor(x_indices).astype(int), y_indices

        return x, y

    def update_spline(self):
        self.setPath(self.build_path())
        self.update()

    def add_knot(self, pos):
        # if first knot, just add knot on the current path
        knot_dict = {
            "knot_pos": (pos.x(), pos.y()),
            "cp_in_pos": (pos.x() - 1, pos.y()),
            "cp_out_pos": (pos.x() + 1, pos.y()),
        }
        self._knots.append(knot_dict)
        new_knot = CubicSplineKnotItem(self, knot_dict)
        self.knots.append(new_knot)
        self.optimize_controllpoints(new_knot)
        if not self.control_points_visible:
            new_knot.hide_control_points()
        self.update_spline()

    def delete_knot(self, knot):
        index = self.knots.index(knot)
        knot.prepareGeometryChange()
        self.scene().removeItem(knot)
        self.knots.remove(knot)
        # Optimize knots before and after the deleted knot
        if index > 0:
            last_knot = self.knots[index - 1]
            self.optimize_controllpoints(last_knot, propagate=False)
        if index < len(self.knots):
            next_knot = self.knots[index]
            self.optimize_controllpoints(next_knot, propagate=False)

        self.update_spline()

    def shape(self) -> QtGui.QPainterPath:
        # Create a path which closes without increasing its "area"
        # Only clicking exactly the line should activate this item
        path = self.path()
        path.connectPath(self.path().toReversed())
        return path

    def optimize_controllpoints(self, knot, distance_factor=0.25, propagate=True):
        self.knots = sorted(self.knots, key=lambda x: x.center.x())
        knots = self.knots
        index = knots.index(knot)

        # options_widget = self.scene().current_tool.options_widget
        # optimize_strength = options_widget.strengthCheckBox.isChecked()
        # optimize_angle = options_widget.slopeCheckBox.isChecked()
        # optimize_neighbours = options_widget.neighbourCheckBox.isChecked()

        # meta = self.annotation_data.meta
        optimize_strength = True  # meta["spline:optimize_strength"]
        optimize_angle = True  # meta["spline:optimize_angle"]
        optimize_neighbours = True  # meta["spline:optimize_neighbours"]

        if propagate and optimize_neighbours:
            if index - 1 >= 0:
                self.optimize_controllpoints(knots[index - 1], propagate=False)
            if index + 1 <= len(knots) - 1:
                self.optimize_controllpoints(knots[index + 1], propagate=False)

        if len(knots) == 1:
            pos = knot.center
            source = QtCore.QLineF(QtCore.QPointF(pos.x() - 1, pos.y()), pos)
            target = QtCore.QLineF(pos, QtCore.QPointF(pos.x() + 1, pos.y()))

        elif index == 0:
            target = QtCore.QLineF(knot.center, knots[1].knot.center)
            source = (
                QtCore.QLineF()
                .fromPolar(target.length(), 180 + target.angle())
                .translated(knot.center)
            )
            source.setPoints(source.p2(), source.p1())

        elif index == len(knots) - 1:
            source = QtCore.QLineF(knots[-2].knot.center, knot.center)
            target = (
                QtCore.QLineF()
                .fromPolar(source.length(), source.angle())
                .translated(knot.center)
            )
        else:
            source = QtCore.QLineF(knots[index - 1].knot.center, knot.center)
            target = QtCore.QLineF(knot.center, knots[index + 1].knot.center)

        targetAngle = target.angleTo(source)
        if targetAngle > 180:
            angle = (source.angle() + source.angleTo(target) / 2) % 360
        else:
            angle = (target.angle() + target.angleTo(source) / 2) % 360

        if optimize_strength:
            length_in = source.length() * distance_factor
            length_out = target.length() * distance_factor
        else:
            length_in = knot._line_in.line().length()
            length_out = knot._line_out.line().length()

        if optimize_angle:
            angle_in = angle + 180
            angle_out = angle
        else:
            angle_in = (knot._line_in.line().angle()) % 360
            angle_out = knot._line_out.line().angle()

        revTarget = QtCore.QLineF.fromPolar(length_in, angle_in).translated(knot.center)
        knot.cp_in = revTarget.p2()

        revSource = QtCore.QLineF.fromPolar(length_out, angle_out).translated(
            knot.center
        )
        knot.cp_out = revSource.p2()


class PolygonPath(QtWidgets.QGraphicsPathItem):
    def __init__(self, heights, parent, start=None, end=None):
        super().__init__(parent)
        self.heights = heights
        self.points = self._points_from_heights(heights)
        self.polygon = QtGui.QPolygonF().fromList(self.points)

        self._start = start
        if start is None and self.points != []:
            self._start = self.points[0]

        self._end = end
        if end is None and self.points != []:
            self._end = self.points[-1]

        self._update_polygon()

    def _points_from_heights(self, heights):
        points = []
        for (
            i,
            h,
        ) in enumerate(heights):
            if not np.isnan(h):
                # +0.5 for points to sit in the middle and not start of each pixel (in x direction)
                points.append(QtCore.QPointF(i + 0.5, h))
        return points

    def _update_polygon(self):
        self.points = self._points_from_heights(self.heights)
        if self.points == []:
            self.setPath(QtGui.QPainterPath())
            self.update()
            return
        points = (
            [self._start]
            + [p for p in self.points if self._start.x() <= p.x() <= self._end.x()]
            + [self._end]
        )

        self.polygon = QtGui.QPolygonF().fromList(points)
        path = QtGui.QPainterPath()
        path.addPolygon(self.polygon)
        self.setPath(path)
        self.update()

    def set_start(self, point):
        self._start = point
        self._update_polygon()

    def set_end(self, point):
        self._end = point
        self._update_polygon()


class LayerItem(QtWidgets.QGraphicsPathItem):
    def __init__(
        self, data: ep.EyeVolumeLayerAnnotation, index: int, parent: ItemGroup
    ):
        super().__init__(parent=parent)
        self.annotation_data = data
        self.index = index
        self.cubic_spline = CubicSpline(self.annotation_data.knots[self.index], self)
        self.start_polygon = PolygonPath(
            self.annotation_data.data[-(self.index + 1)], self
        )
        self.end_polygon = PolygonPath(
            self.annotation_data.data[-(self.index + 1)], self
        )

        self.setFlag(QtWidgets.QGraphicsItem.ItemIsPanel)
        self.sync_with_volume()
        self.update_line()

    def add_knot(self, pos):
        self.cubic_spline.add_knot(pos)
        self.update_line()

    def delete_knot(self, knot):
        self.cubic_spline.delete_knot(knot)
        self.update_line()

    def setActive(self, active: bool) -> None:
        if active:
            self.cubic_spline.show_knots()
        else:
            self.cubic_spline.hide_knots()
        super().setActive(active)

    def as_array(self):
        """Return the annotated path as an array of shape (image width)

        The array has the same shape as the annotated image width. Regions
        which are not annoted become np.nan

        The array is build by painting the annotated path on a pixmap,
        converting it to a numpy array and computing the column-wise center of
        mass for the first channel.
        """
        heights = self.annotation_data.data[-(self.index + 1)]

        spline_region = self.cubic_spline.x_region
        width = spline_region[1] - spline_region[0]

        for t in np.linspace(0, 1, np.ceil(width).astype(int), endpoint=False):
            path = self.path()
            point = path.pointAtPercent(t)
            x = np.rint(point.x() - 0.5).astype(int)
            heights[x] = point.y() - 0.5

        return heights

    def update_line(self):
        # hasattr check for loading of new data. When old data is removed knots might fire an update althoug the cubic_spline is already removed.
        if hasattr(self, "cubic_spline") and len(self.cubic_spline.knots) != 0:
            if (
                self.start_polygon._start is None
                or self.cubic_spline.knots[0].center.x() < self.start_polygon._start.x()
            ):
                self.start_polygon._start = self.cubic_spline.knots[0].center
            if (
                self.end_polygon._end is None
                or self.cubic_spline.knots[-1].center.x() > self.end_polygon._end.x()
            ):
                self.end_polygon._end = self.cubic_spline.knots[-1].center

            self.cubic_spline.update_spline()
            x, y = self.cubic_spline.indices
            self.annotation_data.data[-(self.index + 1), x] = y

            self.start_polygon.set_end(self.cubic_spline.knots[0].center)
            self.end_polygon.set_start(self.cubic_spline.knots[-1].center)

        self.update()

    def view(self):
        return self.scene().views()[0]

    def mousePressEvent(self, event):
        event.ignore()
        # super().mousePressEvent(event)
        # self.view().tool.mouse_press_handler(self, event)
        # event.accept()

    def mouseDoubleClickEvent(self, event):
        self.view().tool.mouse_doubleclick_handler(self, event)
        event.accept()

    def mouseReleaseEvent(self, event):
        event.ignore()
        # super().mouseReleaseEvent(event)
        # self.view().tool.mouse_release_handler(self, event)
        # event.accept()

    def keyPressEvent(self, event):
        event.ignore()
        # self.view().tool.key_press_handler(self, event)
        # event.accept()

    def keyReleaseEvent(self, event):
        event.ignore()
        # self.view().tool.key_release_handler(self, event)
        # event.accept()

    def mouseMoveEvent(self, event):
        event.ignore()
        # super().mouseMoveEvent(event)
        # self.view().tool.mouse_move_handler(self, event)
        # event.accept()

    def sync_with_volume(self):
        self.setVisible(self.annotation_data.meta["visible"])
        self.setZValue(self.annotation_data.meta["z_value"])

        color = QtGui.QColor()
        color.setNamedColor(f"#{self.annotation_data.meta['current_color']}")

        pen = QtGui.QPen(color)
        pen.setWidth(2)
        pen.setCosmetic(True)
        self.setPen(pen)
        self.cubic_spline.setPen(pen)
        self.start_polygon.setPen(pen)
        self.end_polygon.setPen(pen)
        self.update()

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
            self.scene().update(self.scene().sceneRect())
            return True
        return False

    def appendChild(self, data: "TreeLineItem"):
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
