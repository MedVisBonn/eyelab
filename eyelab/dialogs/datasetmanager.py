import logging

from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import QMessageBox

from oat.models.config import DATA_ROLE
from oat.views.ui.ui_datasetmanager_dialog import Ui_DatasetManagerDialog
from .adddataset import AddDatasetDialog
from oat.models import DatasetsModel
import json

logger = logging.getLogger(__name__)


class CustomQSortFilterProxyModel(QtCore.QSortFilterProxyModel):
    def __init__(self, parent=None):
        super().__init__(parent)

    def filterAcceptsRow(
        self, source_row: int, source_parent: QtCore.QModelIndex
    ) -> bool:
        return True

    def filterAcceptsColumn(
        self, source_column: int, source_parent: QtCore.QModelIndex
    ) -> bool:
        header = self.sourceModel().headerData(source_column, QtCore.Qt.Horizontal)
        if header in ["Name"]:
            return True
        else:
            return False


class DatasetManagerDialog(QtWidgets.QDialog, Ui_DatasetManagerDialog):
    def __init__(self, datasets_model, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.datasets_model = datasets_model

        self.dataset_proxy_model = CustomQSortFilterProxyModel(self)
        self.dataset_proxy_model.setSourceModel(self.datasets_model)
        self.datasetTableView.setModel(self.dataset_proxy_model)
        self.datasetTableView.setSortingEnabled(True)

        header = self.datasetTableView.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        self.datasetTableView.verticalHeader().setVisible(False)
        self.datasetTableView.selectionModel().currentChanged.connect(
            self.set_editor_data
        )

        self.addDatasetButton.clicked.connect(self.add_dataset)
        self.deleteDatasetButton.clicked.connect(self.delete_dataset)

        # self.datasetTableView.setModel(self.dataset_model)
        self.addCollaboratorButton.clicked.connect(self.add_collaborator)
        self.deleteCollaboratorButton.clicked.connect(self.delete_collaborator)

        # self.datasetTableView.setModel(self.dataset_model)
        self.addCollectionButton.clicked.connect(self.add_collection)
        self.deleteCollectionButton.clicked.connect(self.delete_collection)

    def set_editor_data(self, current, previous):
        if self.descriptionTextEdit.document().isModified():
            self.set_model_data(current, previous)
        current_dataset = self.dataset_proxy_model.data(
            self.datasetTableView.currentIndex(), role=DATA_ROLE
        )
        if current_dataset is not None:
            self.descriptionTextEdit.setText(current_dataset["info"])

    def set_model_data(self, current, previous):
        self.dataset_proxy_model.setData(
            previous,
            {
                "info": self.descriptionTextEdit.toPlainText(),
            },
        )

    def add_dataset(self):
        dialog = AddDatasetDialog(self.datasets_model)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.dataset_proxy_model.invalidate()
            pass

    def ask_confirmation(self, question):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setText(question)
        msgBox.setWindowTitle("Attention")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            return True
        return False

    def delete_dataset(self):
        current_dataset = self.dataset_proxy_model.data(
            self.datasetTableView.currentIndex(), role=DATA_ROLE
        )
        if not current_dataset is None:
            msg = (
                f"Do you really want to delete the"
                f" \"{current_dataset['name']}\" dataset?"
            )
            if self.ask_confirmation(msg):
                index = self.dataset_proxy_model.mapToSource(
                    self.datasetTableView.currentIndex()
                )
                index = self.datasetTableView.currentIndex()
                self.dataset_proxy_model.removeRows(index.row(), 1, index.parent())
                self.dataset_proxy_model.invalidate()

    def add_collaborator(self):
        pass

    def delete_collaborator(self):
        if self.ask_confirmation():
            pass

    def add_collection(self):
        pass

    def delete_collection(self):
        if self.ask_confirmation():
            pass
