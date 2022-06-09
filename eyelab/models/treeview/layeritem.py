import logging
from itertools import groupby
from typing import Any, Dict, List, Tuple

import eyepy as ep
import numpy as np
from PySide6.QtCore import QLineF, QPoint, QPointF, QRectF, Qt
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
    MoveKnot,
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
        return self.parentItem().layer_item

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
            command = layer_commands.DeleteKnot(self)
            get_undo_stack("main").push(command)
            event.accept()
            return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        index = self.bspline.knots.index(self)
        left_knot = self.bspline.knots[index - 1].center.x() if index > 0 else 0
        right_knot = (
            self.bspline.knots[index + 1].center.x()
            if index + 1 < len(self.bspline.knots)
            else self.scene().shape[1]
        )

        index = self.layer_item.cubic_splines.index(self.bspline)
        if index > 0 and left_knot == 0:
            left_knot = self.layer_item.cubic_splines[index - 1].knots[-1].center.x()
        if (
            index + 1 < len(self.layer_item.cubic_splines)
            and right_knot == self.scene().shape[1]
        ):
            right_knot = self.layer_item.cubic_splines[index + 1].knots[0].center.x()

        if left_knot < event.scenePos().x() < right_knot:
            command = MoveKnot(self, event.scenePos())
            get_undo_stack("main").push(command)
        event.accept()
        # super().mouseMoveEvent(event)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        # modifiers = QApplication.keyboardModifiers()
        if event.key() == Qt.Key_Delete:
            spline = self.parentItem()
            knot = self
            command = layer_commands.DeleteKnot(knot)
            get_undo_stack("main").push(command)
            event.accept()
            return
        super().keyPressEvent(event)


class CubicSpline(QGraphicsPathItem):
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
        self.update()

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
        self.update()
        start = np.floor(self.start.x()).astype(int)
        end = np.floor(self.end.x()).astype(int)
        if start == end:
            return {start: self.start.y()}

        n_points = end - start + 1
        x_indices = []
        y_indices = []
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
    def __init__(self, parent, heights, start: QPointF = None, end: QPointF = None):
        super().__init__(parent)
        self.heights = heights
        self._start = start
        self._end = end

        # self.setAcceptHoverEvents(True)
        # self.setFlag(QGraphicsItem.ItemIsFocusable)
        self.update()

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        # print(self.layer_item.focusItem())
        super().mousePressEvent(event)
        # print(self.layer_item.focusItem())

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
    def __init__(
        self, data: ep.EyeVolumeLayerAnnotation, index: int, parent: ItemGroup
    ):
        super().__init__(parent=parent)
        self.annotation_data = data
        self.index = index

        # Make sure knots are List[Curve[KnotDict]] and not List[KnotDict]
        knots = self.annotation_data.knots[self.index]
        if knots:
            if type(knots[0]) == dict:
                self.annotation_data.knots[self.index] = [
                    sorted(knots, key=lambda x: x["knot_pos"][0])
                ]
        self.cubic_splines = [CubicSpline(knots, self) for knots in self.knots]
        self.polygons = self._get_polygons()

        self.setFlag(QGraphicsItem.ItemIsPanel)
        self.setFlag(QGraphicsItem.ItemIsFocusable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)

        for cs in self.cubic_splines:
            left, right = self.get_neighbour_elements(cs)
            if left:
                left.end = cs.start
            if right:
                right.start = cs.end
        self.update()

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
            l = len(list(g))
            if k:
                polygon_regions.append(
                    (
                        QPointF(i + 0.5, self.height_map[i]),
                        QPointF(i + l - 0.5, self.height_map[i + l - 1]),
                    )
                )
            i += l

        return [self._get_polygon(start, end) for start, end in polygon_regions]

    def _get_polygon(self, start: QPointF, end: QPointF) -> PolygonPath:
        return PolygonPath(self, self.height_map, start, end)

    @property
    def height_map(self):
        return self.annotation_data.data[-(self.index + 1)]

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

    def as_array(self):
        """Return the annotated path as an array of shape (image width)

        The array has the same shape as the annotated image width. Regions
        which are not annotated become np.nan

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

        # x, y = self.cubic_spline.indices
        # self.annotation_data.data[-(self.index + 1), x] = y
        super().update()

    def view(self):
        return self.scene().views()[0]

    def mouseDoubleClickEvent(self, event):
        modifiers = QApplication.keyboardModifiers()
        if modifiers == Qt.ControlModifier:
            print(self.polygons, self.cubic_splines)
            event.ignore()
            return
        # if event.modifiers() &
        pos = event.scenePos()
        # Ignore event if not inside the scene
        if not self.scene().sceneRect().contains(pos):
            event.ignore()
            return

        # Find polygon/curve intersecting the new Knot
        cs = [cs for cs in self.cubic_splines if pos in cs]
        # if pos is in any existing curve add the knot to this curve
        if cs:
            command = layer_commands.AddKnot(cs[0], pos)
        elif type(self.focusItem()) == LayerItem or self.focusItem() is None:
            command = layer_commands.AddCurve(self, event.scenePos())
        # else if there is a focusitem add the knot to this items curve
        else:
            if type(self.focusItem()) is CubicSpline:
                bspline = self.focusItem()
            elif type(self.focusItem()) is CubicSplineKnotItem:
                bspline = self.focusItem().bspline
            else:
                print("unexpected focus item ", self.focusItem())
                return
            # Ignore event if there is other curve in between focusItem and new knot
            if any(
                [
                    pos.x() < cs.start.x() < bspline.start.x()
                    or bspline.end.x() < cs.end.x() < pos.x()
                    for cs in self.cubic_splines
                ]
            ):
                return
            command = layer_commands.AddKnot(bspline, pos)

        get_undo_stack("main").push(command)
        super().mouseDoubleClickEvent(event)

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

    # def contextMenuEvent(self, event: QGraphicsSceneContextMenuEvent) -> None:
    #    menu = QMenu()
    #    new_curve_action = QAction("New Curve")
    #    menu.addAction(new_curve_action)

    #    menu.exec(event.screenPos())

    #    new_curve_action.triggered.connect(lambda: self.setFocus())
    #    #super().contextMenuEvent(event)
