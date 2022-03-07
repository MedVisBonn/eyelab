from PySide6 import QtWidgets, QtCore, Qt
from PySide6.QtCore import QPointF

from eyepy import EyeVolume

from eyelab.views.graphicsview import CustomGraphicsView
from eyelab.models.scene import CustomGraphicsScene
from eyelab.models.scene import Point, Line
from eyelab.models.viewtab import VolumeTab
import numpy as np

import logging

logger = logging.getLogger("eyelab.volumeview")


class VolumeView(CustomGraphicsView):
    cursorPosChanged = QtCore.Signal(QtCore.QPointF, CustomGraphicsView)
    sceneChanged = QtCore.Signal()

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.current_slice = None
        self._bscan_scenes = {}
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)

        self.data = None

        self._lines = None

    @property
    def bscan_scene(self) -> CustomGraphicsScene:
        if not self.current_slice in self._bscan_scenes:
            # Create GraphicsScene if not yet created
            scene = CustomGraphicsScene(parent=self, data=self.data[self.current_slice])
            # Set Annotations managed by the ViewTab
            scene.addItem(self.view_tab.model.root_item)
            scene.toolChanged.connect(self.update_tool)
            self._bscan_scenes[self.current_slice] = scene

        return self._bscan_scenes[self.current_slice]

    def set_data(self, data: EyeVolume, name: str = "Volume"):
        logger.debug("VolumeView: set_data")
        self.data = data
        self.name = name
        self.current_slice = 0
        self.view_tab = VolumeTab(self.data)

        self.setScene(self.bscan_scene)

        self.zoomToFit()
        logger.debug("VolumeView: data is set")

    def set_current_scene(self):
        if self.tool.paint_preview.scene() == self.scene():
            self.scene().removeItem(self.tool.paint_preview)
        self.setScene(self.bscan_scene)
        if not self.scene().mouseGrabberItem() is None:
            self.tool.paint_preview.setParentItem(self.scene().mouseGrabberItem())

        self.view_tab.set_slice(self.current_slice)
        self.sceneChanged.emit()

    def next_slice(self):
        if self.current_slice < len(self.data) - 1:
            self.current_slice += 1
            self.set_current_scene()

    def last_slice(self):
        if self.current_slice > 0:
            self.current_slice -= 1
            self.set_current_scene()

    def map_to_localizer(self, pos):
        # x = StartX + xpos
        # y = StartY + StartY-EndY/lenx * xpos
        slice_n = pos.toPoint().y()
        lclzr_scale_x = self.data.localizer.scale_x
        lclzr_scale_y = self.data.localizer.scale_y
        start_y = self.data[slice_n].meta["start_pos"][1] / lclzr_scale_y
        end_y = self.data[slice_n].meta["end_pos"][1] / lclzr_scale_y
        size_x = self.data.size_x

        x = self.data[slice_n].meta["start_pos"][0] / lclzr_scale_x + pos.x()
        y = start_y + (start_y - end_y) / size_x * pos.x()

        return QPointF(x, y)

    def map_from_localizer(self, pos):
        lclzr_scale_x = self.data.localizer.scale_x
        x = pos.x() - self.data[self.current_slice].meta["start_pos"][0] / lclzr_scale_x
        y = self.closest_slice(pos)
        return QPointF(x, y)

    def set_fake_cursor(self, pos, sender):
        # Turn localizer position to x pos and slice number for OCT
        pos = self.map_from_localizer(pos)
        # set slice

        if self.linked_navigation:
            self.current_slice = int(pos.y())
            self.set_current_scene()
            self.centerOn(pos)

        current_center = self.mapToScene(self.rect().center()).y()
        pos = QPointF(pos.x(), current_center)

        self.scene().fake_cursor.setPos(pos)
        self.scene().fake_cursor.show()

        # ToDo: this is an overkill, update only cursor position
        self.viewport().update()

    def wheelEvent(self, event):
        if event.modifiers() == (QtCore.Qt.ControlModifier):
            if event.angleDelta().y() > 0:
                self.next_slice()
            else:
                self.last_slice()

            pos_on_localizer = self.map_to_localizer(
                QPointF(
                    self.mapToScene(event.position().toPoint()).x(), self.current_slice
                )
            )
            self.cursorPosChanged.emit(pos_on_localizer, self)
            event.accept()
        else:

            super().wheelEvent(event)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        scene_pos = self.mapToScene(event.pos())
        if self.tool.paint_preview.scene() == self.scene():
            self.tool.paint_preview.setPos(scene_pos.toPoint())
        localizer_pos = self.map_to_localizer(
            QtCore.QPointF(scene_pos.x(), self.current_slice)
        )
        self.cursorPosChanged.emit(localizer_pos, self)

    def _slice_lines(self):
        lines = []
        for bscan in self.data:
            scale = np.array([self.data.localizer.scale_x, self.data.localizer.scale_y])

            start = bscan.meta["start_pos"] / scale
            end = bscan.meta["end_pos"] / scale

            p1 = Point(*start)
            p2 = Point(*end)
            a = p1.y - p2.y
            b = p2.x - p1.x
            c = a * p2.x + b * p2.y
            lines.append(Line(a, b, -c))
        return lines

    @property
    def slice_lines(self):
        if self._lines is None:
            self._lines = self._slice_lines()

        return self._lines

    def closest_slice(self, pos):
        # Todo: Make this faster for smooth registered navigation
        point = Point(pos.x(), pos.y())

        smallest_dist = self.point_line_distance(point, self.slice_lines[0])
        for i, line in enumerate(self.slice_lines):
            dist = self.point_line_distance(point, line)
            if dist <= smallest_dist:
                smallest_dist = dist
            else:
                return i - 1
        return i

    @staticmethod
    def point_line_distance(point, line):
        return np.abs(line.a * point.x + line.b * point.y + line.c) / np.sqrt(
            line.a ** 2 + line.b ** 2
        )
