import logging
from typing import List

from PySide6 import QtGui, QtCore, QtWidgets
from PySide6.QtWidgets import QWidget

from eyelab.views.ui.ui_workspace_view import Ui_WorkspaceView
from eyelab.views.data_view import DataView
from eyelab.models.viewtab import ViewTab

import eyepy as ep

logger = logging.getLogger("eyelab.workspace")


class Workspace(QWidget, Ui_WorkspaceView):
    def __init__(self, parent=None):
        """Holds DataView and Toolbox."""
        logger.debug("Workspace: __init__")
        super().__init__(parent)
        self.setupUi(self)

        self.data_view = DataView(parent=self)
        self.data_widget.layout().addWidget(self.data_view)

        self._tools = {}

        self.ctrl_key_actions = {
            QtCore.Qt.Key_X: self.toggle_linked_navigation,
            QtCore.Qt.Key_A: self.toggle_all_annotations,
            QtCore.Qt.Key_1: self.select_tool_0,
            QtCore.Qt.Key_2: self.select_tool_1,
        }

        self.graphic_views = [
            self.data_view.graphicsViewLocalizer,
            self.data_view.graphicsViewVolume,
        ]

        self.linked_navigation = False
        self.annotations_visible = True

    def set_data(self, data: ep.EyeVolume):
        logger.debug("Workspace: set_data")
        self.data = data
        self.data_view.set_data(data)

        self.layerOverview.clear()
        self.layerOverview.addTab(self.data_view.graphicsViewVolume.view_tab, "Volume")
        self.layerOverview.addTab(
            self.data_view.graphicsViewLocalizer.view_tab, "Localizer"
        )
        # self.layerOverview.currentChanged.connect(
        #    lambda index: self.layerOverview.widget(index).scene.setFocus() if index != -1 else None)
        self.layerOverview.repaint()

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
        if self.annotations_visible:
            self.annotations_visible = False
            for i in range(self.layerOverview.count()):
                self.layerOverview.widget(i).model.hide()
        else:
            self.annotations_visible = True
            for i in range(self.layerOverview.count()):
                self.layerOverview.widget(i).model.show()

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

        if not event.isAccepted():
            super().keyPressEvent(event)
