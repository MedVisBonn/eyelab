from eyepy import EyeEnface
from PySide6 import QtWidgets
from PySide6.QtCore import QPointF, Qt

from eyelab.models.viewtab import EnfaceTab
from eyelab.views.graphicsview import CustomGraphicsView


class EnfaceView(CustomGraphicsView):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)

        self.setContextMenuPolicy(Qt.ActionsContextMenu)

    def set_data(self, data: EyeEnface, name: str):
        self.data = data
        self.view_tab = EnfaceTab(self.data)
        self.setScene(self.view_tab.model.scene)
        self.zoomToFit()

    def set_fake_cursor(self, pos, sender=None):
        pos = QPointF(pos.x(), pos.y())
        if sender is not None and sender != self:
            pos = self.map_from_sender(pos, sender)
        if self.linked_navigation:
            self.centerOn(pos)
        self.scene().fake_cursor.setPos(pos)
        self.scene().fake_cursor.show()
        self.viewport().update()

    def wheelEvent(self, event):
        if event.modifiers() == (Qt.ControlModifier):
            event.accept()
        else:
            super().wheelEvent(event)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        scene_pos = self.mapToScene(event.pos())
        self.cursorPosChanged.emit(scene_pos, self)
