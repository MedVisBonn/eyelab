import base64
import zlib
from typing import List, Dict

import numpy as np
import qimage2ndarray
import requests
from PySide6 import Qt, QtCore

from oat import config


class TreeGraphicsItem(QtWidgets.QGraphicsPixmapItem):
    _defaults = {"visible": True}

    def __init__(
        self,
        *args,
        parent=None,
        data=None,
        is_panel=True,
        type="enface",
        shape,
        **kwargs,
    ):
        """Provide data to create a new annotation or the id of an existing
        annotation.
        """
        super().__init__(*args, parent=parent, **kwargs)
        self.shape = shape
        self.paintable = False
        if is_panel:
            self.paintable = True
            self.type = type
            # Dict of pixels for every
            self._data = data
            height, width = self.shape
            self.qimage = QtGui.QImage(width, height, QtGui.QImage.Format_ARGB32)
            color = QtGui.QColor()
            color.setNamedColor(f"#{self.current_color}")
            self.qimage.fill(color)
            self.alpha_array = qimage2ndarray.alpha_view(self.qimage)
            self.setPixmap(QtGui.QPixmap())
            self.set_data()

            self.pixels = self._data["mask"]
            self.changed = False
            self.setFlag(QtWidgets.QGraphicsItem.ItemIsFocusable)
            self.timer = QtCore.QTimer()
            self.timer.start(2500)
            self.timer.timeout.connect(self.sync)

            [setattr(self, key, value) for key, value in self._data.items()]

    def update_pixmap(self):
        pixmap = self.pixmap()
        pixmap.convertFromImage(self.qimage)
        self.setPixmap(pixmap)

    def set_data(self):
        self.alpha_array[...] = 0.0
        y_start = self._data["upperleft_y"]
        y_end = self._data["upperleft_y"] + self._data["size_y"]
        x_start = self._data["upperleft_x"]
        x_end = self._data["upperleft_x"] + self._data["size_x"]

        if self._data["mask"] != "":
            mask = base64.b64decode(self._data["mask"])
            mask = zlib.decompress(mask)
            size = self._data["size_x"] * self._data["size_y"]
            shape = (self._data["size_y"], self._data["size_x"])
            mask = np.unpackbits(np.frombuffer(mask, dtype=np.uint8))[:size].reshape(
                shape
            )
            self.alpha_array[y_start:y_end, x_start:x_end] = mask.astype(float) * 255
            self.update_pixmap()

    @classmethod
    def create(cls, data, shape, parent=None, type="enface"):
        data = {**cls._defaults, **data}
        item_data = cls.post_annotation(data, type=type)
        return cls(data=item_data, parent=parent, is_panel=True, type=type, shape=shape)

    @classmethod
    def from_annotation_id(cls, id, parent=None, type="enface"):
        item_data = cls.get_annotation(id, type=type)
        return cls(data=item_data, parent=parent, is_panel=True, type=type)

    @staticmethod
    def post_annotation(data, type="enface"):
        response = requests.post(
            f"{config.api_server}/{type}areaannotations/",
            headers=config.auth_header,
            json=data,
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(
                f"Status Code: {response.status_code}\n" f"{response.json()}"
            )

    @staticmethod
    def get_annotation(annotation_id, type="enface"):
        if type not in ["enface", "slice"]:
            msg = f"Parameter type has to be (enface|slice) not {type}"
            raise ValueError(msg)

        response = requests.get(
            f"{config.api_server}/{type}areaannotations/{annotation_id}",
            headers=config.auth_header,
        )
        if response.status_code == 200:
            r = response.json()
            annotation_type = r.pop("annotationtype")
            r = {**annotation_type, **r}
            return r
        else:
            raise ValueError(
                f"Status Code: {response.status_code}\n" f"{response.json()}"
            )

    @staticmethod
    def put_annotation(annotation_id, data, type="enface"):
        response = requests.put(
            f"{config.api_server}/{type}areaannotations/{annotation_id}",
            json=data,
            headers=config.auth_header,
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(
                f"Status Code: {response.status_code}\n" f"{response.json()}"
            )

    @staticmethod
    def delete_annotation(annotation_id, type="enface"):
        response = requests.delete(
            f"{config.api_server}/{type}areaannotations/{annotation_id}",
            headers=config.auth_header,
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(
                f"Status Code: {response.status_code}\n" f"{response.json()}"
            )

    @property
    def view(self):
        return self.scene().views()[0]

    def mousePressEvent(self, event):
        self.view.tool.mouse_press_handler(self, event)
        event.accept()

    def mouseReleaseEvent(self, event):
        self.view.tool.mouse_release_handler(self, event)
        event.accept()

    def keyPressEvent(self, event):
        self.view.tool.key_press_handler(self, event)
        event.accept()

    def keyReleaseEvent(self, event):
        self.view.tool.key_release_handler(self, event)
        event.accept()

    def mouseMoveEvent(self, event):
        self.view.tool.mouse_move_handler(self, event)
        event.accept()

    def sync(self):
        # Upload local changes if the layer is active
        if self.changed:
            mask = self.alpha_array == 255.0
            mask = np.packbits(mask).tobytes()
            mask = zlib.compress(mask)
            mask = base64.b64encode(mask).decode("ascii")
            self._data.update(
                mask=mask,
                size_x=self.shape[1],
                size_y=self.shape[0],
                upperleft_y=0,
                upperleft_x=0,
            )
            self._data = self.put_annotation(
                annotation_id=self._data["id"], data=self._data, type=self.type
            )
            self.set_data()
            self.changed = False

    def add_pixels(self, pos, mask):
        size_x, size_y = mask.shape
        offset_x = pos.x() - (size_x - 1) / 2
        offset_y = pos.y() - (size_y - 1) / 2

        for ix, iy in np.ndindex(mask.shape):
            if mask[ix, iy]:
                self.alpha_array[int(offset_y + iy), int(offset_x + ix)] = 255.0

        self.update_pixmap()
        self.changed = True

    def remove_pixels(self, pos, mask):
        size_x, size_y = mask.shape
        offset_x = pos.x() - (size_x - 1) / 2
        offset_y = pos.y() - (size_y - 1) / 2
        for ix, iy in np.ndindex(mask.shape):
            if mask[ix, iy]:
                self.alpha_array[int(offset_y + iy), int(offset_x + ix)] = 0.0

        self.update_pixmap()
        self.changed = True

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
        return self._data["current_color"]

    @current_color.setter
    def current_color(self, value):
        self._data["current_color"] = value
        color = QtGui.QColor()
        color.setNamedColor(f"#{self.current_color}")
        self.qimage.fill(color)
        self.set_data()
        self.update_pixmap()

    def childNumber(self):
        if self.parentItem():
            return self.parentItem().childItems().index(self)
        return 0

    def childCount(self):
        return len(self.childItems())

    def child(self, number: int):
        if number < 0 or number >= self.childCount():
            return False
        return self.childItems()[number]

    def columnCount(self):
        return 1

    def data(self, column: str):
        if column not in self._data:
            raise Exception(f"column {column} not in data")
        return getattr(self, column)

    def setData(self, column: str, value):
        if (column not in self._data) or type(self._data[column]) != type(value):
            return False

        setattr(self, column, value)
        if column == "visible" and value == True:
            if self.scene().mouseGrabberItem() is None:
                self.grabMouse()

        self.scene().update(self.scene().sceneRect())
        return True

    def appendChild(self, data: "TreeAreaItemDB"):
        items = self.childItems()

        if items:
            z_value = float(items[-1].zValue() + 1)
        else:
            z_value = 0.0

        data.z_value = z_value
        data.setParentItem(self)

    def removeChildren(self, row: int, count: int):
        if row < 0 or row > self.childCount():
            raise Exception("what went wrong here?")
        items = self.childItems()

        for i in range(row, row + count):
            item = items[i]
            item.scene().removeItem(item)
            self.delete_annotation(item._data["id"], item.type)

    def switchChildren(self, row1: int, row2: int):
        child1 = self.child(row1)
        child2 = self.child(row2)

        child1_z = child1.zValue()
        child2_z = child2.zValue()
        child1.setData("z_value", child2_z)
        child2.setData("z_value", child1_z)
