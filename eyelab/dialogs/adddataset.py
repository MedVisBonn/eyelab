import logging

from PySide6 import QtWidgets, QtCore

from oat.models.config import DATA_ROLE
from oat.models.db import LineTypeModel, AreaTypeModel
from oat.modules.annotation.models.treeview.itemmodel import TreeItemModel
from oat.modules.annotation.models.treeview.areaitem import TreeAreaItemDB
from oat.modules.annotation.models.treeview.lineitem import TreeLineItemDB
from oat.views.ui.ui_add_dataset_dialog import Ui_AddDatasetDialog
import json

logger = logging.getLogger(__name__)


class AddDatasetDialog(QtWidgets.QDialog, Ui_AddDatasetDialog):
    def __init__(self, dataset_model: QtCore.QAbstractTableModel, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.dataset_model = dataset_model

        self.buttonBox.accepted.connect(self.add_dataset)
        self.buttonBox.rejected.connect(self.close)

    def add_dataset(self):
        logger.debug("Add new dataset")
        dataset_dict = {
            "name": self.nameEdit.text(),
            "info": self.infoEdit.toPlainText(),
        }
        self.dataset_model.setData(self.dataset_model.index(-1, 0), dataset_dict)
