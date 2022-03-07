import logging

from PySide6 import QtWidgets, QtCore

from oat.models.config import DATA_ROLE
from oat.models.db import LineTypeModel, AreaTypeModel
from oat.modules.annotation.models.treeview.itemmodel import TreeItemModel
from oat.modules.annotation.models.treeview.areaitem import TreeAreaItemDB
from oat.modules.annotation.models.treeview.lineitem import TreeLineItemDB
from oat.views.ui.ui_add_annotation_dialog import Ui_AnnotationDialog
import json

logger = logging.getLogger(__name__)


class AddAnnotationDialog(QtWidgets.QDialog, Ui_AnnotationDialog):
    def __init__(self, tab_widget: QtWidgets.QTabWidget, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.tab_widget = tab_widget

        self.linetype_model = LineTypeModel(self)
        self.areatype_model = AreaTypeModel(self)

        self.area_checkboxes = []
        self.layer_checkboxes = []

        self.buttonBox.accepted.connect(self.add_annotations)
        self.buttonBox.rejected.connect(self.close)

        self.addLayerTypeButton.clicked.connect(self.add_layer_type)
        self.addAreaTypeButton.clicked.connect(self.add_area_type)

        self.add_area_options()
        # Add layer options only for OCT Tab
        if self.tab_widget.currentWidget().scene.urlprefix == "slice":
            self.add_line_options()
        else:
            self.addLayerTypeButton.setParent(None)
            self.layerLabel.setParent(None)
            self.line.setParent(None)

    def add_layer_type(self):
        pass

    def add_area_type(self):
        pass

    def get_checkbox(self, type_dict):
        checkBox = QtWidgets.QCheckBox(self)
        checkBox.setEnabled(True)
        checkBox.setCheckable(True)
        checkBox.setChecked(False)
        checkBox.setTristate(False)
        checkBox.setProperty("type_dict", type_dict)
        checkBox.setObjectName(f"{type_dict['name']}_{type_dict['id']}")
        checkBox.setText(type_dict["name"])
        return checkBox

    def add_area_options(self):
        # Iterate over area types
        area_types = self.areatype_model.get_area_types()
        for i, at in enumerate(area_types):
            if i % 3 == 0:
                rowLayout = QtWidgets.QHBoxLayout()
                self.areaLayout.addLayout(rowLayout)
            # Add checkbox for area type
            self.area_checkboxes.append(self.get_checkbox(at))
            rowLayout.addWidget(self.area_checkboxes[-1])

    def add_line_options(self):
        # Iterate over layer types
        line_types = self.linetype_model.get_line_types()
        # line_types = [{"name": "RPE", "id":1, "default_color": "red"},
        #               {"name": "BM", "id": 2, "default_color": "blue"},]
        for i, at in enumerate(line_types):
            if i % 3 == 0:
                rowLayout = QtWidgets.QHBoxLayout()
                self.layerLayout.addLayout(rowLayout)
            # Add checkbox for layer type
            self.layer_checkboxes.append(self.get_checkbox(at))
            rowLayout.addWidget(self.layer_checkboxes[-1])

            # Add checkbox for layer type

    def add_area_annotations(self, layer_model):
        for cb in self.area_checkboxes:
            if cb.isChecked():
                area_type_dict = cb.property("type_dict")
                area_annotation = {
                    "annotationtype_id": area_type_dict["id"],
                    "current_color": area_type_dict["default_color"],
                    "image_id": layer_model.scene.image_id,
                    "z_value": layer_model.rowCount(
                        QtCore.QModelIndex(layer_model.area_index)
                    ),
                }

                try:
                    new_item = TreeAreaItemDB.create(
                        area_annotation,
                        type=layer_model.scene.urlprefix,
                        shape=layer_model.scene.shape,
                    )
                    layer_model.appendRow(
                        new_item, parent=QtCore.QModelIndex(layer_model.area_index)
                    )
                except:
                    pass
                    # TODO: Log here

    def add_line_annotations(self, layer_model):
        logger.debug("Add layer annotations")
        for cb in self.layer_checkboxes:
            if cb.isChecked():
                layer_type_dict = cb.property("type_dict")
                layer_annotation = {
                    "annotationtype_id": layer_type_dict["id"],
                    "current_color": layer_type_dict["default_color"],
                    "image_id": layer_model.scene.image_id,
                    "z_value": (
                        layer_model.rowCount(QtCore.QModelIndex(layer_model.area_index))
                        + layer_model.rowCount(
                            QtCore.QModelIndex(layer_model.line_index)
                        )
                    ),
                    "line_data": json.dumps({"curves": [], "points": []}),
                }

                try:
                    new_item = TreeLineItemDB.create(
                        layer_annotation, shape=layer_model.scene.shape
                    )
                    layer_model.appendRow(
                        new_item, parent=QtCore.QModelIndex(layer_model.line_index)
                    )
                except Exception as e:
                    logger.debug(e)

    def get_all_layer_models(self):
        tabs = [self.tab_widget.widget(i) for i in range(self.tab_widget.count())]
        scenes = {"enface": [], "slice": []}
        for tab in tabs:
            # get all scenes for enface tabs
            if tab.scene.urlprefix == "enface":
                scenes["enface"].append(tab.model)
            elif tab.scene.urlprefix == "slice":
                bscan_scenes = tab.scene.views()[0].bscan_scenes
                for bs in bscan_scenes:
                    scenes["slice"].append(bs.scene_tab.model)
            else:
                raise ValueError("The urlprefix has to be 'enface' or 'slice'")

        return scenes

    def add_annotations(self):
        logger.debug("Add annotation layers")
        # Get all tabs in the tabview
        if self.modalitiesCheckBox.isChecked():
            scenes = self.get_all_layer_models()
        else:
            tab = self.tab_widget.currentWidget()
            if tab.scene.urlprefix == "enface":
                scenes = {"enface": [tab.model], "slice": []}
            elif tab.scene.urlprefix == "slice":
                scenes = {"enface": [], "slice": []}
                if self.slicesCheckBox.isChecked():
                    bscan_scenes = tab.scene.views()[0].bscan_scenes
                    for bs in bscan_scenes:
                        scenes["slice"].append(bs.scene_tab.model)
                else:
                    scenes["slice"].append(
                        tab.scene.views()[0].bscan_scene.scene_tab.model
                    )

            else:
                raise ValueError("The urlprefix has to be 'enface' or 'slice'")

        # Create AreaAnnotation of selected Type
        for t in ["enface", "slice"]:
            selected_scenes = scenes[t]
            for scene in selected_scenes:
                self.add_area_annotations(scene)

        # If current tab is OCT create LayerAnnotation of selected Type
        if self.tab_widget.currentWidget().scene.urlprefix == "slice":
            for scene in scenes["slice"]:
                self.add_line_annotations(scene)
