import logging

import eyepy as ep
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtGui import QCloseEvent, QUndoStack
from PySide6.QtWidgets import QMessageBox, QWidget

from eyelab.commands import get_undo_stack
from eyelab.views.ui.ui_workspace_view import Ui_WorkspaceView

logger = logging.getLogger("eyelab.workspace")


class Workspace(QWidget, Ui_WorkspaceView):
    def __init__(self, parent=None):
        """Holds DataView and Toolbox."""
        logger.debug("Workspace: __init__")
        super().__init__(parent)
        self.setupUi(self)

        self.undo_stack = get_undo_stack("main", self)
        self.graphic_views = [
            self.data_view.graphicsViewLocalizer,
            self.data_view.graphicsViewVolume,
        ]

        self._tools = {}

        self.ctrl_key_actions = {
            QtCore.Qt.Key_X: self.toggle_linked_navigation,
            # QtCore.Qt.Key_A: self.toggle_all_annotations,
            # QtCore.Qt.Key_1: self.select_tool_0,
            # QtCore.Qt.Key_2: self.select_tool_1
        }

        self.linked_navigation = False
        self.annotations_visible = True

        self.data = None

    def closeEvent(self, event: QCloseEvent) -> None:
        # Save all unchanged annotations
        if self.undo_stack.isClean():
            super().closeEvent(event)
            return

        answer = QMessageBox.question(
            self,
            None,
            "You have unsaved changes. Save before closing?",
            QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
        )
        if answer & QMessageBox.Save:
            # the user chose "Save"
            self.actionSaveAnnotations.trigger()
        elif answer & QMessageBox.Cancel:
            # the user canceled
            event.ignore()

    def set_data(self, data: ep.EyeVolume):
        logger.debug("Workspace: set_data")
        self.data = data
        self.data_view.set_data(data)
        self.undo_stack.clear()

        self.layer_overview.clear()
        self.layer_overview.addTab(self.data_view.graphicsViewVolume.view_tab, "Volume")
        self.layer_overview.addTab(
            self.data_view.graphicsViewLocalizer.view_tab, "Localizer"
        )
        self.layer_overview.repaint()

    @property
    def scenes(self):
        return [view.scene() for view in self.graphic_views]

    def toggle_linked_navigation(self):
        if self.linked_navigation:
            self.linked_navigation = False
            for view in self.graphic_views:
                view.unlink_navigation()

        else:
            self.linked_navigation = True
            for view in self.graphic_views:
                view.link_navigation()

    def toggle_all_annotations(self):
        for i in range(self.layer_overview.count()):
            self.layer_overview.widget(i).model.toggle_annotations()

    def select_tool_0(self):
        self.select_tool(0)

    def select_tool_1(self):
        self.select_tool(1)

    def select_tool(self, number):
        for view in self.graphic_views:
            if view.isEnabled():
                layout = view.view_tab.toolsWidget.layout()
                widget = layout.itemAt(number).widget()
                if not widget is None:
                    widget.click()

    def uncheck_buttons(self):
        for button in [self.penButton, self.navigationButton]:
            button.setChecked(False)

    def toogle_scroll_bars(self):
        [view.toggle_scroll_bars() for view in self.graphic_views]

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        modifiers = QtWidgets.QApplication.keyboardModifiers()
        if modifiers == QtCore.Qt.ControlModifier:
            if event.key() in self.ctrl_key_actions:
                self.ctrl_key_actions[event.key()]()
                event.accept()
        super().keyPressEvent(event)
