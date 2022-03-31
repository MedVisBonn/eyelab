from typing import Union

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtWidgets import QWidget

from eyelab.models.layereditor import LayerEntry, LayerGroupEntry


class TreeItemDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, parent):
        super().__init__(parent)

    def paint(
        self,
        painter: QtGui.QPainter,
        option: "QStyleOptionViewItem",
        index: QtCore.QModelIndex,
    ) -> None:
        super().paint(painter, option, index)
        self.parent().openPersistentEditor(index)

    def createEditor(
        self, parent: QWidget, option: "QStyleOptionViewItem", index: QtCore.QModelIndex
    ) -> QWidget:
        # SceneTab: parent.parent().parent()
        if index.parent().parent() == QtCore.QModelIndex():
            self.editor = LayerGroupEntry(parent)
        else:
            self.editor = LayerEntry(parent)
        self.editor.editorChanged.connect(self.update_model)
        return self.editor

    @QtCore.Slot()
    def update_model(self):
        editor = self.sender()
        self.commitData.emit(editor)

    def setEditorData(self, editor: QWidget, index: QtCore.QModelIndex) -> None:
        data = index.model().data(index, QtCore.Qt.EditRole)
        editor.label.setText(str(data["name"]))
        editor.set_visible(data["visible"])
        if type(editor) == LayerEntry:
            editor.set_color(data["current_color"].upper())

    def setModelData(
        self,
        editor: Union[LayerEntry, LayerGroupEntry],
        model: QtCore.QAbstractItemModel,
        index: QtCore.QModelIndex,
    ) -> None:
        data = {"visible": editor.visible, "name": editor.label.text()}
        if type(editor) is LayerEntry:
            data["current_color"] = editor.color

        model.setData(index, data, QtCore.Qt.EditRole)

    def sizeHint(
        self, option: "QStyleOptionViewItem", index: QtCore.QModelIndex
    ) -> QtCore.QSize:
        return LayerEntry(None).sizeHint()
