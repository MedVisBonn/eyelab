import base64
import zlib
from typing import List, Dict

import numpy as np
import qimage2ndarray
from PySide6 import QtCore, QtWidgets, QtGui

import eyepy as ep


class TreeAreaItem(QtWidgets.QGraphicsPixmapItem):
    def __init__(self, *args, parent=None, data, meta, **kwargs):
        """Provide data to create a new annotation or the id of an existing
        annotation.
        """
        super().__init__(*args, parent=parent, **kwargs)
        self.annotation_data = data
        self.meta = meta
        height, width = self.annotation_data.shape

        self.qimage = QtGui.QImage(width, height, QtGui.QImage.Format_ARGB32)
        color = QtGui.QColor()
        color.setNamedColor(f"#{self.current_color}")
        self.qimage.fill(color)
        self.alpha_array = qimage2ndarray.alpha_view(self.qimage)
        self.setPixmap(QtGui.QPixmap())
        self.set_data()

        self.changed = False

        self.setFlag(QtWidgets.QGraphicsItem.ItemIsPanel)
        # self.setPanelModality(QtWidgets.QGraphicsItem.PanelModal)
        self.interaction_ongoing = False

    def shape(self) -> QtGui.QPainterPath:
        path = QtGui.QPainterPath()
        path.addRect(QtCore.QRectF(self.qimage.rect()))
        return path

    def setActive(self, active: bool) -> None:
        super().setActive(active)

    def update_pixmap(self):
        pixmap = self.pixmap()
        pixmap.convertFromImage(self.qimage)
        self.setPixmap(pixmap)

    def set_data(self):
        self.alpha_array[...] = 0.0
        self.alpha_array[self.annotation_data] = 255
        self.update_pixmap()

    def view(self):
        return self.scene().views()[0]

    def mousePressEvent(self, event):
        self.interaction_ongoing = True
        self.view().tool.mouse_press_handler(self, event)
        event.accept()

    def mouseReleaseEvent(self, event):
        self.interaction_ongoing = False
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
                self.annotation_data[int(offset_y + iy), int(offset_x + ix)] = True

        self.update_pixmap()
        self.changed = True

    def remove_pixels(self, pos, mask):
        size_x, size_y = mask.shape
        offset_x = pos.x() - (size_x - 1) / 2
        offset_y = pos.y() - (size_y - 1) / 2
        for ix, iy in np.ndindex(mask.shape):
            if mask[ix, iy]:
                self.alpha_array[int(offset_y + iy), int(offset_x + ix)] = 0.0
                self.annotation_data[int(offset_y + iy), int(offset_x + ix)] = False

        self.update_pixmap()
        self.changed = True

    # Functions to make the QGraphicsItemGroup work as a item in a model tree

    def hide_controlls(self):
        pass

    def show_controlls(self):
        pass

    @property
    def visible(self):
        return self.isVisible()

    @visible.setter
    def visible(self, value):
        self.meta["visible"] = value
        self.setVisible(value)

    @property
    def z_value(self):
        return self.zValue()

    @z_value.setter
    def z_value(self, value):
        self.meta["z-value"] = value
        self.setZValue(value)

    @property
    def current_color(self):
        if not "current_color" in self.meta:
            self.meta["current_color"] = "FF0000"
        return self.meta["current_color"]

    @current_color.setter
    def current_color(self, value):
        self.meta["current_color"] = value
        color = QtGui.QColor()
        color.setNamedColor(f"#{value}")
        qimage2ndarray.rgb_view(self.qimage)[:] = np.array(
            [color.red(), color.green(), color.blue()]
        )
        self.update_pixmap()

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
            self.scene().update(self.scene().sceneRect())
            return True
        return False

    def appendChild(self, data: "TreeAreaItem"):
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
            layer = TreeAreaItem(data=item_data)
            layer.setParentItem(self)

    def removeChildren(self, row: int, count: int):
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
