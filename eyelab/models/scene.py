import logging
from collections import namedtuple
from typing import Union

import eyepy as ep
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import QRect, QRectF, Qt
from PySide6.QtGui import QColor, QPainter, QStaticText
from PySide6.QtWidgets import QGraphicsSceneContextMenuEvent

from eyelab.models.utils import array2qgraphicspixmapitem

logger = logging.getLogger("eyelab.scene")

Line = namedtuple("Line", ["a", "b", "c"])
Point = namedtuple("Point", ["x", "y"])


class CustomGraphicsScene(QtWidgets.QGraphicsScene):
    def __init__(self, parent, data: ep.EyeBscan, *args, **kwargs):
        super().__init__(*args, **kwargs, parent=parent)
        self.data = data

        self._widthForHeightFactor = 1

        self.background_on = True
        self.foreground_on = False
        self.fake_cursor = self.addPixmap(
            QtGui.QPixmap(":/cursors/cursors/navigation_cursor.svg")
        )
        self.fake_cursor.setFlag(QtWidgets.QGraphicsItem.ItemIgnoresTransformations)
        self.fake_cursor.hide()

        self.set_image()

        self.setItemIndexMethod(QtWidgets.QGraphicsScene.NoIndex)

        logger.debug("CustomGraphicsScene: __init__ done")

    def drawForeground(self, painter: QPainter, rect: Union[QRectF, QRect]) -> None:
        if self.foreground_on:
            text = QStaticText(f"Slice {self.data.index}")

            painter.setPen(QColor().fromRgb(255, 255, 255))
            font = painter.font()
            font.setPixelSize(8)
            painter.setFont(font)
            painter.drawStaticText(10, 10, text)

        super().drawForeground(painter, rect)

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
        # item = self.activePanel()
        # item.mouseMoveEvent(event)
        super().mouseMoveEvent(event)

    def mousePressEvent(self, event: "QGraphicsSceneMouseEvent") -> None:
        # Do not handle the event in ScrollHandDrag Mode to not interfere
        if self.views()[0].dragMode() == QtWidgets.QGraphicsView.ScrollHandDrag:
            return
        if event.button() == Qt.RightButton:
            self.activePanel().setFocus(Qt.OtherFocusReason)
            self.clearSelection()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: "QGraphicsSceneMouseEvent") -> None:
        if self.views()[0].dragMode() == QtWidgets.QGraphicsView.ScrollHandDrag:
            return
        super().mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event: QtGui.QMouseEvent) -> None:
        item = self.activePanel()
        item.mouseDoubleClickEvent(event)
        super().mouseDoubleClickEvent(event)

    def contextMenuEvent(self, event: QGraphicsSceneContextMenuEvent) -> None:
        # item = self.activePanel()
        # item.contextMenuEvent(event)
        super().contextMenuEvent(event)
