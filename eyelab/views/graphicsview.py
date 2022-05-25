import logging
import math

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtWidgets import QGraphicsView

logger = logging.getLogger(__name__)


class CustomGraphicsView(QGraphicsView):
    cursorPosChanged = QtCore.Signal(QtCore.QPointF, QGraphicsView)

    viewChanged = QtCore.Signal(QGraphicsView)

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self._zoom = 0

        self.linked_navigation = False

        # How to position the scene when transformed (eg zoom)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorViewCenter)
        # How to position the scene when resizing the widget
        self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorViewCenter)
        # Get Move events even if no button is pressed
        self.setMouseTracking(True)
        self.deactivate_scroll_bars()

        self.setLineWidth(3)
        self.setPalette(QtGui.QPalette(QtCore.Qt.red, QtCore.Qt.black))
        self.setEnabled(False)

    def unlink_navigation(self):
        self.linked_navigation = False

    def link_navigation(self):
        self.linked_navigation = True

    @property
    def tool(self):
        return self.view_tab.current_tool

    def setEnabled(self, a0: bool) -> None:
        if a0:
            self.setFrameStyle(QtWidgets.QFrame.Raised | QtWidgets.QFrame.Panel)
        else:
            self.setFrameStyle(QtWidgets.QFrame.Plain | QtWidgets.QFrame.Panel)

        super().setEnabled(a0)

    def enterEvent(self, event):
        self.setEnabled(True)
        self.update_tool()

        if self.linked_navigation:
            tab_widget = self.view_tab.parent().parent()
            index = tab_widget.indexOf(self.view_tab)
            tab_widget.setCurrentIndex(index)

        self.scene().addItem(self.tool.paint_preview)

        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setEnabled(False)
        if self.tool.paint_preview.scene() == self.scene():
            self.scene().removeItem(self.tool.paint_preview)
        super().leaveEvent(event)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        scene_pos = self.mapToScene(event.pos())
        if self.tool.paint_preview.scene() == self.scene():
            self.tool.paint_preview.setPos(scene_pos.toPoint())
        self.cursorPosChanged.emit(scene_pos, self)

    def hasWidthForHeight(self):
        return True

    def widthForHeight(self, height):
        return math.ceil(height * self.scene()._widthForHeightFactor)

    def toggle_scroll_bars(self):
        if self._scroll_bars:
            self.deactivate_scroll_bars()
        else:
            self.activate_scroll_bars()

    def deactivate_scroll_bars(self):
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self._scroll_bars = False

    def activate_scroll_bars(self):
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self._scroll_bars = True

    def zoomToFit(self):
        self.fitInView(self.scene().sceneRect(), QtCore.Qt.KeepAspectRatio)
        self._zoom = 0

    def zoomToFeature(self):
        # Zoom in as long as more than 1/3 of width of the image is
        # visible
        while (
            self.mapToScene(self.rect()).boundingRect().width()
            > self.scene().width() / 3
        ):
            self.zoom_in()

    def zoom_in(self):
        self._zoom += 1
        self.scale(1.25, 1.25)

    def zoom_out(self):
        if self._zoom > 0:
            self._zoom -= 1
            self.scale(0.8, 0.8)

    def wheelEvent(self, event: QtGui.QWheelEvent) -> None:
        if event.angleDelta().y() > 0:
            self.zoom_in()
        else:
            self.zoom_out()

    def showEvent(self, event: QtGui.QShowEvent) -> None:
        super().showEvent(event)
        self.zoomToFit()

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        super().resizeEvent(event)
        self.zoomToFit()

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        super().mouseReleaseEvent(event)
        self.update_tool()

    def setScene(self, scene) -> None:
        super().setScene(scene)

    def update_tool(self):
        tool = self.view_tab.current_tool
        if tool.name == "inspection":
            self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
        else:
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
        self.viewport().setCursor(tool.cursor)
