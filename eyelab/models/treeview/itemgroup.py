from PySide6 import QtCore, QtWidgets


class ItemGroup(QtWidgets.QGraphicsItem):
    def __init__(self, meta: dict, parent=None):
        """Provide data to create a new annotation or the id of an existing
        annotation.
        """
        super().__init__(parent=parent)

        self.meta = meta
        self.setFlag(QtWidgets.QGraphicsItem.ItemHasNoContents, True)

    def update(self):
        if self.meta:
            self.setVisible(self.meta["visible"])
            self.setZValue(self.meta["z_value"])

        for item in self.childItems():
            item.update()
        super().update

    def boundingRect(self) -> QtCore.QRectF:
        return self.childrenBoundingRect()
