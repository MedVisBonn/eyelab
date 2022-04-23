from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtWidgets import QWidget

from eyelab.views.ui.ui_layer_entry import Ui_LayerEntry
from eyelab.views.ui.ui_layergroup_entry import Ui_LayerGroupEntry


class LayerGroupEntry(QWidget, Ui_LayerGroupEntry):
    editorChanged = QtCore.Signal()

    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)

        self.visible_icon = QtGui.QIcon()
        self.visible_icon.addPixmap(
            QtGui.QPixmap(":/icons/icons/baseline-visibility-24px.svg"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.hidden_icon = QtGui.QIcon()
        self.hidden_icon.addPixmap(
            QtGui.QPixmap(":/icons/icons/baseline-visibility_off-24px.svg"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )

        self.visible = True
        self.hideButton.clicked.connect(self.toggle_visibility)

    def set_visible(self, value=True):
        if value:
            self.show()
        else:
            self.hide()

    def toggle_visibility(self):
        if self.visible:
            self.hide()
        else:
            self.show()
        self.editorChanged.emit()

    def hide(self):
        self.visible = False
        self.hideButton.setIcon(self.hidden_icon)

    def show(self):
        self.visible = True
        self.hideButton.setIcon(self.visible_icon)


class LayerEntry(QWidget, Ui_LayerEntry):
    editorChanged = QtCore.Signal()

    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)

        self.visible_icon = QtGui.QIcon()
        self.visible_icon.addPixmap(
            QtGui.QPixmap(":/icons/icons/baseline-visibility-24px.svg"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.hidden_icon = QtGui.QIcon()
        self.hidden_icon.addPixmap(
            QtGui.QPixmap(":/icons/icons/baseline-visibility_off-24px.svg"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )

        self.visible = True
        self.hideButton.clicked.connect(self.toggle_visibility)
        self.colorButton.clicked.connect(self.set_color)
        self.colorDialog = QtWidgets.QColorDialog()

        self.labelEdit.textChanged.connect(self.editorChanged)
        self.labelEdit.mousePressEvent = lambda x: self.mousePressEvent(x)

    def set_color(self, color=None):
        if not color:
            color = self.colorDialog.getColor(
                options=QtWidgets.QColorDialog.DontUseNativeDialog
            )
            if not color.isValid():
                return
            self.color = color.name()[1:]
        else:
            self.color = color
        self.colorButton.setStyleSheet(f"background-color: #{self.color}")
        self.editorChanged.emit()

    def set_visible(self, value=True):
        if value:
            self.show()
        else:
            self.hide()

    def toggle_visibility(self):
        if self.visible:
            self.hide()
        else:
            self.show()
        self.editorChanged.emit()

    def hide(self):
        self.visible = False
        self.hideButton.setIcon(self.hidden_icon)

    def show(self):
        self.visible = True
        self.hideButton.setIcon(self.visible_icon)

    def mouseDoubleClickEvent(self, event: QtGui.QMouseEvent) -> None:
        self.labelEdit.setFrame(True)
