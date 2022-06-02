import logging

import numpy as np
from eyepy import EyeVolume
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import QPointF

from eyelab.models.scene import Line, Point
from eyelab.models.viewtab import VolumeTab
from eyelab.views.graphicsview import CustomGraphicsView

logger = logging.getLogger("eyelab.volumeview")


class VolumeView(CustomGraphicsView):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.data = None
        self._lines = None

        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)

    def reset(self):
        self.data = None
        self._lines = None

    def set_data(self, data: EyeVolume, name: str = "Volume"):
        logger.debug("VolumeView: set_data")
        self.reset()
        self.data = data
        self.name = name
        self.view_tab = VolumeTab(self.data, parent=self)
        self.setScene(self.view_tab.model.scene)

        self.zoomToFit()
        logger.debug("VolumeView: data is set")

    def map_to_localizer(self, pos):
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
        current_slice = self.view_tab.model.current_slice
        x = pos.x() - self.data[current_slice].meta["start_pos"][0] / lclzr_scale_x
        y = self.closest_slice(pos)
        return QPointF(x, y)

    def set_fake_cursor(self, pos, sender):
        # Turn localizer position to x pos and slice number for OCT
        pos = self.map_from_localizer(pos)
        # set slice

        if self.linked_navigation:
            self.view_tab.model.current_slice = int(pos.y())
            self.setScene(self.view_tab.model.scene)
            self.centerOn(pos)

        current_center = self.mapToScene(self.rect().center()).y()
        pos = QPointF(pos.x(), current_center)

        self.scene().fake_cursor.setPos(pos)
        self.scene().fake_cursor.show()

    def wheelEvent(self, event):
        if event.modifiers() == (QtCore.Qt.ControlModifier):
            if event.angleDelta().y() > 0:
                self.view_tab.next_slice()
            else:
                self.view_tab.last_slice()
            self.setScene(self.view_tab.model.scene)
            self.view_tab.model.activate(
                self.view_tab.imageTreeView.selectionModel().currentIndex()
            )

            if self.linked_navigation:
                current_slice = self.view_tab.model.current_slice
                pos_on_localizer = self.map_to_localizer(
                    QPointF(
                        self.mapToScene(event.position().toPoint()).x(), current_slice
                    )
                )
                self.cursorPosChanged.emit(pos_on_localizer, self)
            event.accept()
        else:

            super().wheelEvent(event)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        scene_pos = self.mapToScene(event.pos())
        current_slice = self.view_tab.model.current_slice
        localizer_pos = self.map_to_localizer(
            QtCore.QPointF(scene_pos.x(), current_slice)
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
