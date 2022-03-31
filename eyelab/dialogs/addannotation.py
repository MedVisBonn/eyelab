import json
import logging
from typing import List, Tuple

from PySide6 import QtCore, QtWidgets

from eyelab.views.ui.ui_add_annotation_dialog import Ui_AddAnnotationDialog

# from eyelab.models.treeview.itemmodel import TreeItemModel


logger = logging.getLogger(__name__)


class AddAnnotationDialog(QtWidgets.QDialog, Ui_AddAnnotationDialog):
    def __init__(self, model: "TreeItemModel", options: List[Tuple], parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.model = model
        self.options = options
        self.set_type_box()

        self.buttonBox.accepted.connect(self.add_annotation)
        self.buttonBox.rejected.connect(self.close)

    def set_type_box(self):
        for name, func in self.options.items():
            self.typeBox.addItem(name)

    def add_annotation(self):
        logger.debug("Add annotation layers")
        name = self.nameEdit.text()
        type = self.typeBox.currentText()

        self.options[type](name)
