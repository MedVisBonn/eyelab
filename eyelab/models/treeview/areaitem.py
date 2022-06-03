import eyepy as ep
import numpy as np
import qimage2ndarray
from PySide6 import QtCore, QtGui, QtWidgets

from eyelab.models.treeview.itemgroup import ItemGroup


class AreaItem(QtWidgets.QGraphicsPixmapItem):
    def __init__(
        self,
        data: ep.EyeVolumeVoxelAnnotation,
        index: int = None,
        parent: ItemGroup = None,
    ):
        super().__init__(parent=parent)
        self.annotation_data = data
        self.index = index
        if self.index is None:
            self.slice = self.annotation_data.data
        else:
            self.slice = self.annotation_data.data[self.index]

        height, width = self.slice.shape
        self.qimage = QtGui.QImage(width, height, QtGui.QImage.Format_ARGB32)
        color = QtGui.QColor()
        color.setNamedColor(f"#{self.annotation_data.meta['current_color']}")
        self.qimage.fill(color)
        self.alpha_array = qimage2ndarray.alpha_view(self.qimage)
        self.setPixmap(QtGui.QPixmap())
        self.set_data()

        self.setFlag(QtWidgets.QGraphicsItem.ItemIsPanel)

    def update(self):
        self.setVisible(self.annotation_data.meta["visible"])
        self.setZValue(self.annotation_data.meta["z_value"])

        color = QtGui.QColor()
        color.setNamedColor(f"#{self.annotation_data.meta['current_color']}")
        qimage2ndarray.rgb_view(self.qimage)[:] = np.array(
            [color.red(), color.green(), color.blue()]
        )
        self.update_pixmap()
        super().update()

    def shape(self) -> QtGui.QPainterPath:
        path = QtGui.QPainterPath()
        path.addRect(QtCore.QRectF(self.qimage.rect()))
        return path

    def update_pixmap(self):
        pixmap = self.pixmap()
        pixmap.convertFromImage(self.qimage)
        self.setPixmap(pixmap)
        self.slice[...] = self.alpha_array

    def set_data(self):
        self.alpha_array[...] = 0.0
        self.alpha_array[self.slice] = 255
        self.update_pixmap()

    def view(self):
        return self.scene().views()[0]

    def mousePressEvent(self, event):
        self.view().tool.mouse_press_handler(self, event)
        event.accept()

    def mouseReleaseEvent(self, event):
        self.view().tool.mouse_release_handler(self, event)
        event.accept()

    def keyPressEvent(self, event):
        self.view().tool.key_press_handler(self, event)
        event.accept()

    def keyReleaseEvent(self, event):
        self.view().tool.key_release_handler(self, event)
        event.accept()

    def mouseMoveEvent(self, event):
        self.view().tool.mouse_move_handler(self, event)
        event.accept()

    def add_pixels(self, pos, mask):
        size_x, size_y = mask.shape
        offset_x = pos.x() - (size_x - 1) / 2
        offset_y = pos.y() - (size_y - 1) / 2

        for ix, iy in np.ndindex(mask.shape):
            if mask[ix, iy]:
                self.alpha_array[int(offset_y + iy), int(offset_x + ix)] = 255.0
                self.slice[int(offset_y + iy), int(offset_x + ix)] = True

        self.update_pixmap()

    def remove_pixels(self, pos, mask):
        size_x, size_y = mask.shape
        offset_x = pos.x() - (size_x - 1) / 2
        offset_y = pos.y() - (size_y - 1) / 2
        for ix, iy in np.ndindex(mask.shape):
            if mask[ix, iy]:
                self.alpha_array[int(offset_y + iy), int(offset_x + ix)] = 0.0
                self.slice[int(offset_y + iy), int(offset_x + ix)] = False

        self.update_pixmap()
