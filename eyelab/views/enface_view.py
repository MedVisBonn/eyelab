from eyepy import EyeEnface
from PySide6 import QtGui, QtWidgets
from PySide6.QtCore import QPointF, Qt

from eyelab.models.viewtab import EnfaceTab
from eyelab.views.graphicsview import CustomGraphicsView


class EnfaceView(CustomGraphicsView):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)

        self.setContextMenuPolicy(Qt.ActionsContextMenu)

        bscan_overlay_action = QtGui.QAction()
        bscan_overlay_action.setCheckable(True)
        bscan_overlay_action.setChecked(True)
        bscan_overlay_action.setText("B-scan positions")
        bscan_overlay_action.triggered.connect(self.test)
        self.addAction(bscan_overlay_action)

    def test(self):
        print("test")

    def set_data(self, data: EyeEnface, name: str):
        self.data = data
        self.view_tab = EnfaceTab(self.data)
        self.setScene(self.view_tab.model.scene)
        self.zoomToFit()

    def map_from_sender(self, pos, sender):
        pass
        # tform = self.get_tform(sender)
        # result = tform((pos.x(), pos.y()))[0]
        # return QPointF(*result)

    def map_to_sender(self, pos, sender):
        tform = self.get_tform(sender)
        result = tform.inverse((pos.x(), pos.y()))[0]
        return QPointF(*result)

    def set_fake_cursor(self, pos, sender=None):
        pos = QPointF(pos.x(), pos.y())
        if not sender is None and sender != self:
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

    def get_tform(self, other_view):
        id_pair = (self.image_id, other_view.scene().image_id)
        print("here")
        if not id_pair in self._tforms:
            print("here_to")
            tmodel = "similarity"
            self._tforms[id_pair] = get_transformation(*id_pair, tmodel)
        return self._tforms[id_pair]

    # def scrollContentsBy(self, dx: int, dy: int) -> None:
    #    super().scrollContentsBy(dx, dy)
    #    self.viewChanged.emit(self)

    # def match_viewport(self, view: QtWidgets.QGraphicsView):
    #    print("match_viewport")
    #    if self.linked_navigation:
    #        rect = self.map_rect_from_sender(view.rect(), view)
    #        print("linked is true")
    #        self.fitInView(rect)

    # def map_rect_from_sender(self, rect: QtCore.QRect, sender):
    #    tform = self.get_tform(sender)
    #    print(tform)
    #    top_left = tform((rect.topLeft().x(), rect.topLeft().y()))[0]
    #    bot_right = tform((rect.bottomRight().x(), rect.bottomRight().y()))[0]
    #    return QtCore.QRectF(QtCore.QPointF(*top_left), QtCore.QPointF(*bot_right))
