import logging
from pathlib import Path

from PySide6 import QtWidgets, QtCore

from oat import config
from oat.utils.api import upload_vol, upload_enface_file, upload_hexml, upload_folder
from oat.modules.dialogs import AddPatientDialog, AddCollectionDialog
from oat.views.ui.ui_upload_dialog import Ui_UploadDialog
from oat.models.config import ID_ROLE, DATA_ROLE

logger = logging.getLogger(__name__)


class ImportDialog(QtWidgets.QDialog, Ui_UploadDialog):
    def __init__(self, models, parent=None, filefilter=None):
        super().__init__(parent)
        self.setupUi(self)

        self.filefilter = filefilter

        self.patient_model = QtCore.QSortFilterProxyModel(self)
        self.patient_model.setSourceModel(models["patients"])
        self.patientDropdown.setModel(self.patient_model)
        self.addPatientButton.clicked.connect(self.add_patient)
        self.patientDropdown.currentIndexChanged.connect(self.update_collections)

        self.collection_model = QtCore.QSortFilterProxyModel(self)
        self.collection_model.setSourceModel(models["collections"])
        filter_key_column = [
            x
            for x in range(self.collection_model.columnCount())
            if self.collection_model.headerData(x, QtCore.Qt.Horizontal) == "Patient Id"
        ][0]
        self.collection_model.setFilterKeyColumn(filter_key_column)

        self.collectionDropdown.setModel(self.collection_model)
        self.collectionDropdown.setModelColumn(0)
        self.update_collections(0)
        self.addCollectionButton.clicked.connect(self.add_collection)

        # self.dataset_model = DatasetModel()
        # self.datasetDropdown.setModel(self.dataset_model)
        # self.addDatasetButton.clicked.connect(self.add_dataset)

        self.fileSelectButton.clicked.connect(self.select_file)
        self.buttonBox.accepted.connect(self.check_upload)

        self.fname = ""

    @property
    def patient_id(self):
        index = self.patientDropdown.currentIndex()
        return self.patient_model.headerData(
            index, QtCore.Qt.Vertical, QtCore.Qt.DisplayRole
        )

    @property
    def collection_id(self):
        index = self.collectionDropdown.currentIndex()
        return self.collection_model.headerData(
            index, QtCore.Qt.Vertical, QtCore.Qt.DisplayRole
        )

    @QtCore.Slot(int)
    def update_collections(self, index):
        self.collection_model.setFilterRegularExpression(
            QtCore.QRegularExpression(f"^{self.patient_id}$")
        )

    def add_patient(self):
        dialog = AddPatientDialog()
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.patient_model.sourceModel().reload_data()
            self.collection_model.sourceModel().reload_data()
            self.patientDropdown.setCurrentIndex(self.patient_model.rowCount() - 1)

    def add_collection(self):
        dialog = AddCollectionDialog(patient_id=self.patient_id)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.collection_model.sourceModel().reload_data()
            self.collectionDropdown.setCurrentIndex(
                self.collection_model.rowCount() - 1
            )

    def add_dataset(self):
        pass

    def select_file(self):
        self.fname, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Select Upload File",
            config.import_path,
            self.filefilter,
        )

        if self.fname != "":
            self.fileName.setText(str(Path(self.fname).name))

    def check_upload(self):
        if self.fname == "":
            QtWidgets.QMessageBox.warning(self, "Error", "No file selected for upload.")
        elif self.patientDropdown.currentText() == "":
            QtWidgets.QMessageBox.warning(self, "Error", "No patient selected.")
        elif self.collectionDropdown.currentText() == "":
            QtWidgets.QMessageBox.warning(self, "Error", "No collection selected.")
        else:
            self.upload()
            self.collection_model.sourceModel().reload_data()

    def upload(self):
        pass


class ImportCfpDialog(ImportDialog):
    def __init__(self, models, parent=None):
        super().__init__(
            models,
            parent,
            filefilter="CFP (*.bmp *.BMP *.tif *.TIF *.tiff *.TIFF *.jpeg *.jpg "
            "*.JPEG *.JPG *.png *.PNG)",
        )

    def upload(self):
        return upload_enface_file(
            self.fname,
            self.patient_id,
            self.collection_id,
            "CFP",
        )


class ImportNirDialog(ImportDialog):
    def __init__(self, models, parent=None):
        super().__init__(
            models,
            parent,
            filefilter="CFP (*.bmp *.BMP *.tif *.TIF *.tiff *.TIFF *.jpeg *.jpg "
            "*.JPEG *.JPG *.png *.PNG)",
        )

    def upload(self):
        return upload_enface_file(
            self.fname,
            self.patient_id,
            self.collection_id,
            "NIR",
        )


class ImportVolDialog(ImportDialog):
    def __init__(self, models, parent=None):
        super().__init__(models, parent, filefilter="Heyex Raw (*.vol)")

    def upload(self):
        return upload_vol(self.fname, self.patient_id, collection_id=self.collection_id)


class ImportHexmlDialog(ImportDialog):
    def __init__(self, models, parent=None):
        super().__init__(models, parent)

    def select_file(self):
        self.fname = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Select HEYEX XML folder", config.import_path
        )
        config.import_path = self.fname
        if self.fname != "":
            self.fileName.setText(str(Path(self.fname).name))

    def upload(self):
        return upload_hexml(
            self.fname, self.patient_id, collection_id=self.collection_id
        )


class ImportFolderDialog(ImportDialog):
    def __init__(self, models, parent=None):
        super().__init__(models, parent)

    def select_file(self):
        self.fname = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Select folder with B-Scans", config.import_path
        )
        config.import_path = self.fname
        if self.fname != "":
            self.fileName.setText(str(Path(self.fname).name))

    def upload(self):
        return upload_folder(
            self.fname, self.patient_id, collection_id=self.collection_id
        )
