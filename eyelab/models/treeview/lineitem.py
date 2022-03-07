from typing import List, Dict, Optional

import numpy as np
import json
from PySide6 import Qt, QtCore, QtWidgets, QtGui
import qimage2ndarray
import eyepy as ep

import logging

logger = logging.getLogger(__name__)


class ControllPointGraphicsItem(QtWidgets.QGraphicsRectItem):
    def __init__(self, parent, pos, **kwargs):
        super().__init__(parent=parent, **kwargs)

        self.setRect(QtCore.QRectF(QtCore.QPoint(-4, -4), QtCore.QPoint(4, 4)))
        self.setFlag(QtWidgets.QGraphicsItem.ItemIgnoresTransformations, True)
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
        self.parentItem().parentItem().interaction_ongoing = True
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

        self.parentItem().cp_in.stay_in_scene()
        self.parentItem().cp_out.stay_in_scene()
        self.parentItem().parentItem().update_line()
        logger.debug("set lines in controlPointGraphicsitem")
        self.parentItem().set_lines()

    def stay_in_scene(self):
        if self.center.x() < 0:
            self.setPos(
                self.mapToParent(self.mapFromScene(QtCore.QPointF(0, self.center.y())))
            )

        elif self.center.x() > self.scene().shape[1]:
            self.setPos(
                self.mapToParent(
                    self.mapFromScene(
                        QtCore.QPointF(self.scene().shape[1], self.center.y())
                    )
                )
            )

        if self.center.y() < 0:
            self.setPos(
                self.mapToParent(self.mapFromScene(QtCore.QPointF(self.center.x(), 0)))
            )
        elif self.center.y() > self.scene().shape[0]:
            self.setPos(
                self.mapToParent(
                    self.mapFromScene(
                        QtCore.QPointF(self.center.x(), self.scene().shape[0])
                    )
                )
            )

        self.parentItem().set_line_of(self)

    def mouseReleaseEvent(self, event: "QGraphicsSceneMouseEvent") -> None:
        super().mouseReleaseEvent(event)
        self.parentItem().parentItem().interaction_ongoing = False


class KnotGraphicsItem(QtWidgets.QGraphicsEllipseItem):
    def __init__(self, parent, pos, **kwargs):
        super().__init__(parent=parent, **kwargs)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIgnoresTransformations, True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)
        self.setRect(QtCore.QRectF(QtCore.QPoint(-5, -5), QtCore.QPoint(5, 5)))
        self.setPos(pos)

        pen = QtGui.QPen(QtGui.QColor("red"))
        pen.setCosmetic(True)
        self.setPen(pen)

        self.setFlag(QtWidgets.QGraphicsItem.ItemIsFocusable, True)

    def paint(
        self,
        painter: QtGui.QPainter,
        option: "QStyleOptionGraphicsItem",
        widget: Optional[QtWidgets.QWidget] = ...,
    ) -> None:
        super().paint(painter, option, widget)

    @property
    def center(self):
        return self.mapToScene(QtCore.QPointF(0, 0))

    def as_tuple(self):
        center = self.center
        return np.round(center.x(), 2), np.round(center.y(), 2)

    def mousePressEvent(self, event: "QGraphicsSceneMouseEvent") -> None:
        self.parentItem().parentItem().interaction_ongoing = True
        if event.buttons() & QtCore.Qt.RightButton:
            line_item = self.parentItem().parentItem()
            self.parentItem().parentItem().delete_knot(self.parentItem())
            event.accept()
            line_item.interaction_ongoing = False
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
        self.parentItem().parentItem().interaction_ongoing = False

    def stay_in_scene(self):
        if self.center.x() < 0:
            self.setPos(
                self.mapToParent(self.mapFromScene(QtCore.QPointF(0, self.center.y())))
            )

        elif self.center.x() > self.scene().shape[1]:
            self.setPos(
                self.mapToParent(
                    self.mapFromScene(
                        QtCore.QPointF(self.scene().shape[1], self.center.y())
                    )
                )
            )

        if self.center.y() < 0:
            self.setPos(
                self.mapToParent(self.mapFromScene(QtCore.QPointF(self.center.x(), 0)))
            )
        elif self.center.y() > self.scene().shape[0]:
            self.setPos(
                self.mapToParent(
                    self.mapFromScene(
                        QtCore.QPointF(self.center.x(), self.scene().shape[0])
                    )
                )
            )

    def mouseMoveEvent(self, event: "QGraphicsSceneMouseEvent") -> None:
        self.parentItem().mouseMoveEvent(event)
        self.stay_in_scene()
        self.parentItem().parentItem().optimize_controllpoints(self.parentItem())
        self.parentItem().cp_in.stay_in_scene()
        self.parentItem().cp_out.stay_in_scene()
        self.parentItem().parentItem().update_line()
        logger.debug("lines updated in knotgraphicsitem")

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
        knot_pos: QtCore.QPointF,
        cp_in_pos: QtCore.QPointF,
        cp_out_pos: QtCore.QPointF,
        **kwargs,
    ):
        """"""

        super().__init__(parent=parent, **kwargs)
        # Create knot
        self._knot = KnotGraphicsItem(self, self.mapFromScene(knot_pos))
        # Create control points
        pen = QtGui.QPen(QtGui.QColor("blue"))
        pen.setCosmetic(True)
        self.cps_visible = True

        self._cp_in = ControllPointGraphicsItem(self, cp_in_pos)
        self._line_in = QtWidgets.QGraphicsLineItem(
            QtCore.QLineF(
                self.mapFromScene(self.knot.center),
                self.mapFromScene(self.cp_in.center),
            ),
            parent=self,
        )
        self._line_in.setPen(pen)

        self._cp_out = ControllPointGraphicsItem(self, cp_out_pos)
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
        logger.debug("Shape of CubicSplineKnot")
        path = QtGui.QPainterPath()
        return path

    @property
    def center(self):
        return self.knot.center

    @classmethod
    def from_dict(cls, data, parent=None):
        new = cls(
            parent,
            QtCore.QPointF(*data["knot"]),
            QtCore.QPointF(*data["cpin"]),
            QtCore.QPointF(*data["cpout"]),
        )
        return new

    def as_dict(self):
        return {
            "knot": self.knot.as_tuple(),
            "cpin": self.cp_in.as_tuple(),
            "cpout": self.cp_out.as_tuple(),
        }

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
        # Remove previous controllpoint
        self._cp_in.setPos(self.mapFromScene(cp))
        self._set_line_in()

    @property
    def cp_out(self) -> ControllPointGraphicsItem:
        return self._cp_out

    @cp_out.setter
    def cp_out(self, cp):
        self.cp_out.setPos(self.mapFromScene(cp))
        self._set_line_out()

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


class TreeLineItem(QtWidgets.QGraphicsPathItem):
    def __init__(self, *args, data: ep.EyeBscanLayerAnnotation, parent=None, **kwargs):
        super().__init__(*args, parent=parent, **kwargs)
        self._data = data
        self.meta = self._data.eyevolumelayerannotation.meta

        self.setFlag(QtWidgets.QGraphicsItem.ItemIsPanel)

        self.control_points_visible = True
        self.interaction_ongoing = False
        self.changed = False

        self.set_data()

    def optimize_controllpoints(self, knot, distance_factor=0.25, propagate=True):
        self.current_curve_knots = sorted(
            self.current_curve_knots, key=lambda x: x.center.x()
        )
        knots = self.current_curve_knots
        index = knots.index(knot)

        options_widget = self.scene().current_tool.options_widget
        optimize_strength = options_widget.strengthCheckBox.isChecked()
        optimize_angle = options_widget.slopeCheckBox.isChecked()
        optimize_neighbours = options_widget.neighbourCheckBox.isChecked()

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

    def setActive(self, active: bool) -> None:
        if active:
            self.show_knots()
        else:
            self.hide_knots()
        super().setActive(active)

    def shape(self) -> QtGui.QPainterPath:
        # Create a path which closes without increasing its "area"
        # Only clicking exactly the line should activate this item
        logger.debug("Shape of LineItem")
        path = self.path()
        path.connectPath(self.path().toReversed())
        logger.debug("Shape of LineItem finished")
        return path

    def hide_knots(self):
        for knots in self.curve_knots:
            [k.hide() for k in knots]

    def show_knots(self):
        for knots in self.curve_knots:
            [k.show() for k in knots]

    def hide_control_points(self):
        for knots in self.curve_knots:
            [k.hide_control_points() for k in knots]
        self.control_points_visible = False

    def show_control_points(self):
        for knots in self.curve_knots:
            [k.show_control_points() for k in knots]
        self.control_points_visible = True

    def add_knot(self, pos):
        # if first knot, just add knot on the current path
        new_knot = CubicSplineKnotItem(
            self,
            pos,
            QtCore.QPointF(pos.x() - 1, pos.y()),
            QtCore.QPointF(pos.x() + 1, pos.y()),
        )
        self.current_curve_knots.append(new_knot)
        self.optimize_controllpoints(new_knot)
        if not self.control_points_visible:
            new_knot.hide_control_points()

        if len(self.current_curve_knots) > 1:
            self.update_line()
            logger.debug("lines updated in add_knot")

    def delete_knot(self, knot):
        for knots in self.curve_knots:
            if knot in knots:
                index = knots.index(knot)
                knot.prepareGeometryChange()
                self.scene().removeItem(knot)
                knots.remove(knot)
                # Optimize knots before and after the deleted knot
                if index > 0:
                    last_knot = knots[index - 1]
                    self.optimize_controllpoints(last_knot, propagate=False)
                if index < len(knots):
                    next_knot = knots[index]
                    self.optimize_controllpoints(next_knot, propagate=False)
        self.update_line()
        logger.debug("lines updated in delete knot")

    def as_array(self):
        """Return the annotated path as an array of shape (image width)

        The array has the same shape as the annotated image width. Regions
        which are not annoted become np.nan

        The array is build by painting the annotated path on a pixmap,
        converting it to a numpy array and computing the column-wise center of
        mass for the first channel.
        """

        height, width = self.scene().shape
        qimage = QtGui.QImage(width, height, QtGui.QImage.Format_RGB32)
        pixmap = QtGui.QPixmap().fromImage(qimage)
        pixmap.convertFromImage(qimage)
        pixmap.fill(QtCore.Qt.black)
        painter = QtGui.QPainter(pixmap)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(QtGui.QPen(QtGui.QColor("white")))
        painter.drawPath(self.path())
        painter.end()

        qimage = pixmap.toImage()
        array = qimage2ndarray.rgb_view(qimage)
        indices = np.ones(array.shape[:-1]) * np.arange(height)[..., np.newaxis]

        # Without annotation, set the array to nan
        annotated_region = array[..., 0].sum(axis=0) != 0
        heights = np.full(width, np.nan)
        heights[annotated_region] = np.average(
            indices[:, annotated_region], axis=0, weights=array[:, annotated_region, 0]
        )
        return heights

    @property
    def as_points(self):
        """Return the annotated path as discrete points

        There is one point returned for every image column even if there is no
        annotation for this column. In this case a point with a y-value of
        np.nan is returned"""
        width = self.scene().shape[1]
        return [(x, self.as_array()[x]) for x in range(width)]

    @property
    def current_curve_knots(self):
        # This is enough as long as we support only a single curve per layer
        # We might want to support multiple curves to support ungraded regions
        if len(self.curve_knots) == 0:
            self.curve_knots.append([])
        return self.curve_knots[0]

    @current_curve_knots.setter
    def current_curve_knots(self, value):
        self.curve_knots[0] = value

    @property
    def curve_paths(self):
        paths = []
        for knots in self.curve_knots:
            knots = sorted(knots, key=lambda x: x.center.x())
            if len(knots) > 1:
                paths.append(self.build_path(knots))
        return paths

    @property
    def line_paths(self):
        # Create polygons for annotated non curve regions
        paths = []
        points = np.array([(i, v) for i, v in enumerate(self._data.data)])
        for start, end in self.curve_regions:
            points[start : end + 1] = np.nan

        # Create QPainterPaths for every point collection.

        line = []
        for point in points:
            point_x, point_y = point
            if not (np.isnan(point_x) | np.isnan(point_y)):
                line.append(QtCore.QPointF(point[0] + 0.5, point[1] + 0.5))
            else:
                if not line == []:
                    new_line = QtGui.QPainterPath(line[0])
                    new_line.addPolygon(QtGui.QPolygonF(line[1:]))
                    paths.append(new_line)
                    line = []

        if not line == []:
            new_line = QtGui.QPainterPath(line[0])
            new_line.addPolygon(QtGui.QPolygonF(line[1:]))
            paths.append(new_line)
        return paths

    def build_path(self, knots):
        logger.debug("build curve path")
        for p, current_point in enumerate(knots):
            current = current_point.knot.center

            if p == 0:
                path = QtGui.QPainterPath(current)
                last_point = current_point
            else:
                path.cubicTo(
                    last_point.cp_out.center, current_point.cp_in.center, current
                )
                last_point = current_point
        logger.debug("curve path completed")
        return path

    def update_line(self, changed=True):
        paths = self.line_paths + self.curve_paths
        logger.debug("paths completed")
        paths = sorted(paths, key=lambda x: x.elementAt(0).x)
        logger.debug("paths sorted")
        if len(paths) > 0:
            path = paths[0]
            if len(paths) > 1:
                for i in range(len(paths) - 1):
                    path.connectPath(paths[i + 1])
            self.setPath(path)
        else:
            self.setPath(QtGui.QPainterPath())
        self.update()
        self.changed = changed

    @property
    def curve_regions(self):
        regions = []
        for knots in self.curve_knots:
            if len(knots) > 0:
                start_x = int(np.floor(knots[0].knot.as_tuple()[0]))
                end_x = int(np.ceil(knots[-1].knot.as_tuple()[0]))
                regions.append((start_x, end_x))
            else:
                self.curve_knots.remove(knots)
        return regions

    def set_data(self):
        logger.debug(f"Set data for {self.meta['name']}")

        # Add knots and controll points for every Curve
        self._data.knots = [
            sorted(
                [CubicSplineKnotItem.from_dict(k, parent=self) for k in curve],
                key=lambda x: x.knot.as_tuple()[0],
            )
            for curve in self._data.knots
        ]
        self.curve_knots = self._data.knots

        # Remove current knots before setting new knots
        # [[self.scene().removeItem(k) for k in c] for c in self.curve_knots]

        if not self.isActive():
            self.hide_knots()
        if not self.control_points_visible:
            self.hide_control_points()
        self.set_current_color()
        self.update_line(changed=False)
        logger.debug("lines updated in set_data")

    def view(self):
        return self.scene().views()[0]

    def mousePressEvent(self, event):
        event.ignore()
        # super().mousePressEvent(event)
        # self.view().tool.mouse_press_handler(self, event)
        # event.accept()

    def mouseDoubleClickEvent(self, event):
        self.view().tool.mouse_doubleclick_handler(self, event)
        # event.accept()

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

    def as_dict(self):
        points = self.line_data["points"]

        all_curves = []
        for knots in self.curve_knots:
            curve_knots = []
            for knot in knots:
                curve_knots.append(knot.as_dict())
            all_curves.append(curve_knots)
        return {"points": points, "curves": all_curves}

    # Functions to make the QGraphicsItemGroup work as a item in a model tree

    @property
    def visible(self):
        return self.isVisible()

    @visible.setter
    def visible(self, value):
        self.setVisible(value)

    @property
    def z_value(self):
        return self.zValue()

    @z_value.setter
    def z_value(self, value):
        self.setZValue(value)

    @property
    def current_color(self):
        if not "current_color" in self.meta:
            self.meta["current_color"] = "FF0000"
        return self.meta["current_color"]

    @current_color.setter
    def current_color(self, value):
        self.meta["current_color"] = value
        self.set_current_color()

    def set_current_color(self):
        color = QtGui.QColor()
        color.setNamedColor(f"#{self.current_color}")
        pen = QtGui.QPen(color)
        pen.setWidth(2)
        pen.setCosmetic(True)
        self.setPen(pen)
        self.update()

    def childNumber(self):
        if self.parentItem():
            return self.parentItem().childItems().index(self)
        return 0

    def childCount(self):
        return 0

    #    return len(self.childItems())

    # def child(self, number: int):
    #    if number < 0 or number >= self.childCount():
    #        return False
    #    return self.childItems()[number]

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
            self.delete_annotation(item._data["id"])

    def switchChildren(self, row1: int, row2: int):
        child1 = self.child(row1)
        child2 = self.child(row2)

        child1_z = child1.zValue()
        child2_z = child2.zValue()
        child1.setData("z_value", child2_z)
        child2.setData("z_value", child1_z)
