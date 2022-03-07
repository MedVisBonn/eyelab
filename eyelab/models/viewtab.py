import collections

from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import QWidget

from eyelab.models.treeitemdelegate import TreeItemDelegate

# from eyelab.dialogs import AddAnnotationDialog
from eyelab.views.ui.ui_scene_tab import Ui_SceneTab
from eyelab.models.treeview.itemmodel import BscanTreeItemModel, EnfaceTreeItemModel
from eyelab.models.treeview.lineitem import TreeLineItem
from eyelab.models.treeview.areaitem import TreeAreaItem
from eyelab.tools import line_tools, area_tools, basic_tools

import json
import eyepy as ep

import logging

logger = logging.getLogger("eyelab.viewtab")


class ViewTab(QWidget, Ui_SceneTab):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.data = data

        self.addButton.clicked.connect(self.add_annotation_layer)
        self.deleteButton.clicked.connect(self.remove_annotation_layer)
        self.upButton.clicked.connect(self.layer_up)
        self.downButton.clicked.connect(self.layer_down)

        self.opacitySlider.valueChanged.connect(self.set_opacity)

        self.line_tools = line_tools()
        self.area_tools = area_tools()
        self.basic_tools = basic_tools()
        # self.setTools(self.basic_tools)

    @property
    def scene(self):
        return self.model.root_item.scene()

    def configure_imageTreeView(self):
        self.ImageTreeView.setModel(self.model)
        self.ImageTreeView.header().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        for col in range(1, self.model.columnCount()):
            self.ImageTreeView.hideColumn(col)
        self.ImageTreeView.setHeaderHidden(True)
        self.ImageTreeView.setItemDelegate(TreeItemDelegate(self.ImageTreeView))
        self.ImageTreeView.setRootIsDecorated(False)
        self.ImageTreeView.selectionModel().currentRowChanged.connect(
            self.on_currentChanged
        )
        self.ImageTreeView.expandAll()

    @property
    def current_item(self):
        model_index = self.ImageTreeView.selectionModel().currentIndex()
        item = self.model.getItem(model_index)
        return item

    def tools(self):
        return self._tools

    def setTools(self, tools=None, default="inspection"):
        if tools is None:
            tools = self.basic_tools
        self._tools = tools
        self._set_tool_buttons()
        self._switch_to_tool(default)()

    def _set_tool_buttons(self):
        layout = self.toolsWidget.layout()
        # Remove previous tools
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().setParent(None)
        # Add current tools
        for i, (name, tool) in enumerate(self.tools().items()):
            layout.addWidget(tool.button, 1, i, 1, 1)
            tool.button.clicked.connect(self._switch_to_tool(name))

    def _switch_to_tool(self, name):
        def func():
            tool = self._tools[name]
            for n, t in self._tools.items():
                t.button.setChecked(False)
                t.disable()
            tool.button.setChecked(True)

            # Show tool options
            self.toolboxWidget.layout().removeWidget(self.optionsWidget)
            self.optionsWidget.setParent(None)
            self.toolboxWidget.layout().addWidget(tool.options_widget)

            self.optionsWidget = tool.options_widget
            self.toolboxWidget.repaint()

            self.scene.current_tool = tool
            tool.enable()

        return func

    def set_opacity(self, value):
        self.model.root_item.setOpacity(value / 100)

    def layer_up(self):
        selected = self.ImageTreeView.selectionModel().currentIndex()

        parent = selected.parent()
        row1 = selected.row()
        row2 = row1 - 1

        if 0 < row1 <= parent.internalPointer().childCount():
            self.model.switchRows(row2, row1, parent)
            # self.ImageTreeView.selectionModel().currentRowChanged.emit(
            #    self.model.index(row1, 0, parent),
            #    self.model.index(row2, 0, parent))

    def layer_down(self):
        selected = self.ImageTreeView.selectionModel().currentIndex()

        parent = selected.parent()
        row1 = selected.row()
        row2 = row1 + 1

        if 0 <= row1 < parent.internalPointer().childCount() - 1:
            self.model.switchRows(row1, row2, parent)
            # self.ImageTreeView.selectionModel().currentRowChanged.emit(
            #    self.model.index(row1, 0, parent),
            #    self.model.index(row2, 0, parent))

    def add_annotation_layer(self):
        tab_widget = self.parent().parent()
        dialog = AddAnnotationDialog(tab_widget)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.model.layoutChanged.emit()
            self.scene.update()

    def remove_annotation_layer(self):
        index = self.ImageTreeView.selectionModel().currentIndex()
        if index.isValid():
            self.model.layoutAboutToBeChanged.emit()
            self.model.removeRows(index.row(), 1, index.parent())
            self.model.layoutChanged.emit()
            self.scene.update()

    @QtCore.Slot("QModelIndex", "QModelIndex")
    def on_currentChanged(self, current, previous):
        current = self.model.getItem(current)
        previous = self.model.getItem(previous)

        # Change activated item
        previous.setActive(False)
        current.setActive(True)
        previous.ungrabMouse()
        current.grabMouse()

        # Set tools for current item
        if issubclass(type(current), TreeLineItem):
            self.setTools(self.line_tools, default="spline")
            if issubclass(type(previous), TreeLineItem):
                if previous.control_points_visible:
                    current.show_control_points()
                else:
                    current.hide_control_points()
        elif issubclass(type(current), TreeAreaItem):
            self.setTools(self.area_tools, default="pen")


class VolumeTab(ViewTab):
    def __init__(self, data: ep.EyeVolume, parent=None):
        super().__init__(data, parent)
        self.current_slice = 0
        self.meta = {}
        self.models = collections.defaultdict(
            lambda: BscanTreeItemModel(data=self.data[self.current_slice], parent=self)
        )

        self.configure_imageTreeView()

    @property
    def model(self):
        return self.models[self.current_slice]

    def set_slice(self, index: int):
        self.current_slice = index
        self.ImageTreeView.setModel(self.model)
        self.ImageTreeView.expandAll()

    def add_line_annotation(self, data):
        new_item = TreeLineItem.create(data, shape=self.model.scene.shape)
        self.model.appendRow(new_item, parent=QtCore.QModelIndex(self.model.line_index))

    def remove_annotation_layer(self):
        index = self.ImageTreeView.selectionModel().currentIndex()
        if index.isValid():
            self.model.layoutAboutToBeChanged.emit()
            self.model.removeRows(index.row(), 1, index.parent())
            self.model.layoutChanged.emit()
            self.scene.update()

    def compute_idealRPE(self):
        try:
            rpe_height = self.ImageTreeView.model().get_layer_height("RPE")
            bm_height = self.ImageTreeView.model().get_layer_height("BM")
        except ValueError as e:
            QtWidgets.QMessageBox.warning(
                self,
                "Layer Warning",
                "Computing the idealRPE requires a BM and"
                " RPE annotation. \n\n{}".format(str(e)),
            )
            return None
        ideal_rpe = ep.core.drusen.normal_rpe(rpe_height, bm_height, self.scene.shape)

        linetype_model = LineTypeModel(self)
        line_types = linetype_model.get_line_types()
        try:
            layer_type_dict = [l for l in line_types if l["name"] == "idealRPE"][0]
        except IndexError:
            layer_type_dict = linetype_model.create_type(
                {
                    "name": "idealRPE",
                    "public": True,
                    "default_color": "ff0000",
                    "description": "The ideal RPE position",
                }
            )

        layer_data = {
            "annotationtype_id": layer_type_dict["id"],
            "current_color": layer_type_dict["default_color"],
            "image_id": self.scene.image_id,
            "z_value": (
                self.model.rowCount(QtCore.QModelIndex(self.model.area_index))
                + self.model.rowCount(QtCore.QModelIndex(self.model.line_index))
            ),
            "line_data": json.dumps(
                {
                    "curves": [],
                    "points": [(x, ideal_rpe[x]) for x in range(len(ideal_rpe))],
                }
            ),
        }
        self.add_line_annotation(layer_data)


class EnfaceTab(ViewTab):
    def __init__(self, data: ep.EyeEnface, parent=None):
        super().__init__(data, parent)
        self.model = EnfaceTreeItemModel(data=self.data, parent=self)

        self.configure_imageTreeView()
