from PySide6 import QtWidgets, QtCore


class ItemGroup(QtWidgets.QGraphicsItem):
    def __init__(self, *args, parent=None, name="Areas", **kwargs):
        """Provide data to create a new annotation or the id of an existing
        annotation.
        """
        super().__init__(*args, parent=parent, **kwargs)

        self._data = {"visible": True, "z_value": 0.0, "name": name}

        self.setFlag(QtWidgets.QGraphicsItem.ItemHasNoContents, True)

    @property
    def view(self):
        return self.scene().views()[0]

    # Functions to make the QGraphicsItemGroup work as a item in a model tree
    @property
    def visible(self):
        return self.isVisible()

    @visible.setter
    def visible(self, value):
        self._data["visible"] = value
        self.setVisible(value)

    @property
    def z_value(self):
        return self.zValue()

    @z_value.setter
    def z_value(self, value):
        self._data["z_value"] = value
        self.setZValue(value)

    @property
    def name(self):
        return self._data["name"]

    @name.setter
    def name(self, value):
        self._data["name"] = value

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
        items = self.childItems()
        for i in range(row, row + count):
            item = items[i]
            item.changed = False
            item.scene().removeItem(item)
            item.delete_annotation(item._data["id"], item.type)

    def switchChildren(self, row1: int, row2: int):
        child1 = self.child(row1)
        child2 = self.child(row2)

        child1_z = child1.zValue()
        child2_z = child2.zValue()
        child1.setData("z_value", child2_z)
        child2.setData("z_value", child1_z)

    def delete_annotation(self, *args, **kwargs):
        # This method is intended to do nothing
        pass

    def boundingRect(self) -> QtCore.QRectF:
        return self.childrenBoundingRect()

    def mousePressEvent(self, event: "QGraphicsSceneMouseEvent") -> None:
        event.ignore()

    def mouseDoubleClickEvent(self, event: "QGraphicsSceneMouseEvent") -> None:
        event.ignore()

    def mouseReleaseEvent(self, event: "QGraphicsSceneMouseEvent") -> None:
        event.ignore()

    def mouseMoveEvent(self, event: "QGraphicsSceneMouseEvent") -> None:
        event.ignore()

    def show(self) -> None:
        self.visible = self._data["visible"]
        self.z_value = self._data["z_value"]
        self.name = self._data["name"]
        super().show()
