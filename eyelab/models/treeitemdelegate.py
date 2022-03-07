from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtWidgets import QWidget

from eyelab.models.layereditor import LayerEntry, LayerGroupEntry


class TreeItemDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, parent):
        super().__init__(parent)
        self._visible = True

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
        if data["name"] == "RPE":
            idealRPE_action = QtGui.QAction("idealRPE", editor)
            scene_tab = editor.parent().parent().parent()
            idealRPE_action.triggered.connect(scene_tab.compute_idealRPE)
            editor.addAction(idealRPE_action)
        editor.set_visible(data["visible"])
        if type(editor) == LayerEntry:
            editor.set_color(data["current_color"].upper())

    def setModelData(
        self,
        editor: QWidget,
        model: QtCore.QAbstractItemModel,
        index: QtCore.QModelIndex,
    ) -> None:
        model.setData(index, editor, QtCore.Qt.EditRole)

    def sizeHint(
        self, option: "QStyleOptionViewItem", index: QtCore.QModelIndex
    ) -> QtCore.QSize:
        return LayerEntry(None).sizeHint()
