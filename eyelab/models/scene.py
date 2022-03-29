from collections import namedtuple

from PySide6 import QtGui, QtCore, QtWidgets
from PySide6.QtCore import QRectF

from eyelab.models.utils import array2qgraphicspixmapitem

import eyepy as ep

import logging

logger = logging.getLogger("eyelab.scene")

Line = namedtuple("Line", ["a", "b", "c"])
Point = namedtuple("Point", ["x", "y"])


class CustomGraphicsScene(QtWidgets.QGraphicsScene):
    def __init__(self, parent, data: ep.EyeBscan, *args, **kwargs):
        super().__init__(*args, **kwargs, parent=parent)
        self.data = data

        self._widthForHeightFactor = 1

        self.background_on = True
        self.fake_cursor = self.addPixmap(
            QtGui.QPixmap(":/cursors/cursors/navigation_cursor.svg")
        )
        self.fake_cursor.setFlag(QtWidgets.QGraphicsItem.ItemIgnoresTransformations)
        self.fake_cursor.hide()

        self.set_image()

        self.grabber_cache = None
        self.setItemIndexMethod(QtWidgets.QGraphicsScene.NoIndex)

        logger.debug("CustomGraphicsScene: __init__ done")

    def drawBackground(self, painter: QtGui.QPainter, rect: QtCore.QRectF):
        if self.background_on:
            painter.fillRect(self.sceneRect(), self.backgroundBrush())
        else:
            painter.fillRect(self.sceneRect(), QtCore.Qt.NoBrush)

    def set_image(self):
        pixmap_item = array2qgraphicspixmapitem(self.data.data)
        pixmap = pixmap_item.pixmap()
        self.shape = (pixmap.height(), pixmap.width())
        self.setSceneRect(QRectF(pixmap.rect()))
        self._widthForHeightFactor = (
            1.0 * pixmap.size().width() / pixmap.size().height()
        )
        self.setBackgroundBrush(QtGui.QBrush(pixmap))

    def hide_background(self):
        if self.background_on:
            self.background_on = False
            self.invalidate(self.sceneRect(), QtWidgets.QGraphicsScene.BackgroundLayer)

    def show_background(self):
        if not self.background_on:
            self.background_on = True
            self.invalidate(self.sceneRect(), QtWidgets.QGraphicsScene.BackgroundLayer)

    def mouseMoveEvent(self, event):
        self.fake_cursor.hide()
        super().mouseMoveEvent(event)

    def mousePressEvent(self, event: "QGraphicsSceneMouseEvent") -> None:
        # Do not handle the event in ScrollHandDrag Mode to not interfere
        if self.views()[0].dragMode() == QtWidgets.QGraphicsView.ScrollHandDrag:
            return

        super().mousePressEvent(event)
        if not event.isAccepted():
            self.grabber_cache = self.mouseGrabberItem()
            if not self.grabber_cache is None:
                self.grabber_cache.ungrabMouse()
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: "QGraphicsSceneMouseEvent") -> None:
        if self.views()[0].dragMode() == QtWidgets.QGraphicsView.ScrollHandDrag:
            return

        super().mouseReleaseEvent(event)
        if not self.grabber_cache is None:
            self.grabber_cache.grabMouse()

    def mouseDoubleClickEvent(self, event: QtGui.QMouseEvent) -> None:
        view = self.views()[0]
        view.tool.mouse_doubleclick_handler(view.view_tab.current_item, event)
        event.accept()
