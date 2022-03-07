import logging
from functools import partial

import sys
from PySide6 import QtWidgets, QtGui

from eyelab.config import EYELAB_FOLDER
from oat.models import PatientsModel, CollectionsModel, DatasetsModel
from oat.models.config import DATA_ROLE, ID_ROLE
from oat.modules.annotation.views.annotation_view import AnnotationView
from oat.modules.navigation import NavigationView
from oat.modules.registration import RegistrationView
from oat.modules.registration.models.registration_model import RegistrationModel
from oat.modules.dialogs.login import LoginDialog
from oat.modules.dialogs.upload import (
    ImportCfpDialog,
    ImportVolDialog,
    ImportHexmlDialog,
    ImportFolderDialog,
    ImportNirDialog,
)
from oat.views.ui.ui_main_window import Ui_MainWindow

from oat.modules.dialogs.help import (
    ShortcutHelp,
    LayerAnnotationHelp,
    AreaAnnotationHelp,
    RegistrationHelp,
    IntroductionHelp,
)

import requests


class oat(QtWidgets.QMainWindow, Ui_MainWindow):
    """Create the main window that stores all of the widgets necessary for the application."""

    def __init__(self, parent=None):
        """Initialize the components of the main window."""
        super().__init__(parent)
        self.setupUi(self)

        self.models = {
            "patients": PatientsModel(),
            "collections": CollectionsModel(),
            "datasets": DatasetsModel(),
        }

        self.actionImportVol.triggered.connect(partial(self.upload, type="vol"))
        self.actionImportCfp.triggered.connect(partial(self.upload, type="cfp"))
        self.actionImportNir.triggered.connect(partial(self.upload, type="nir"))
        self.actionImportHEXML.triggered.connect(partial(self.upload, type="hexml"))
        self.actionImportBSFolder.triggered.connect(partial(self.upload, type="folder"))
        self.actionSave.triggered.connect(self.save)
        self.actionExport.triggered.connect(self.export)

        self.overview_view = NavigationView(models=self.models, parent=self)
        self.overview_view.annotateButton.clicked.connect(self.open_annotation_view)
        self.overview_view.registerButton.clicked.connect(self.open_registration_view)
        self.navigationDock.setWidget(self.overview_view)

        self.actionShortcutSheet.triggered.connect(lambda: self.open_help("shortcuts"))
        self.actionAreaAnnotationGuide.triggered.connect(
            lambda: self.open_help("area_annotation")
        )
        self.actionLayerAnnotationGuide.triggered.connect(
            lambda: self.open_help("layer_annotation")
        )
        self.actionRegistrationGuide.triggered.connect(
            lambda: self.open_help("registration")
        )
        self.actionIntroduction.triggered.connect(
            lambda: self.open_help("introduction")
        )

        # self.statusBar().showMessage("")

    def open_help(self, topic):
        if topic == "introduction":
            dialog = IntroductionHelp(self)
        elif topic == "shortcuts":
            dialog = ShortcutHelp(self)
        elif topic == "area_annotation":
            dialog = AreaAnnotationHelp(self)
        elif topic == "layer_annotation":
            dialog = LayerAnnotationHelp(self)
        elif topic == "registration":
            dialog = RegistrationHelp(self)
        else:
            raise ValueError("topic not available")

        if dialog.exec_() == QtWidgets.QDialog.Rejected:
            pass

    def open_annotation_view(self):
        self.save()
        overview = self.overview_view
        collection_id = overview.model._data(
            overview.tableView.selectionModel().currentIndex(), role=ID_ROLE
        )
        response = requests.get(
            f"{config.api_server}/collections/{collection_id}",
            headers=config.auth_header,
        )
        data = response.json()

        volume_ids = [d["id"] for d in data["volumeimages"]]
        volume_ids_with_localizer = [
            v["id"] for v in data["volumeimages"] if not v["localizer_image"] is None
        ]
        volume_ids_without_localizer = list(
            set(volume_ids) - set(volume_ids_with_localizer)
        )

        enface_ids = [e["id"] for e in data["enfaceimages"]]

        localizer_ids = [
            v["localizer_image"]["id"]
            for v in data["volumeimages"]
            if not v["localizer_image"] is None
        ]
        other_enface_ids = list(set(enface_ids) - set(localizer_ids))

        ao = AnnotationView(
            volume_ids_with_localizer,
            volume_ids_without_localizer,
            other_enface_ids,
            parent=self,
        )
        self.setCentralWidget(ao)

    def open_registration_view(self):
        self.save()
        overview = self.overview_view
        collection_id = overview.model._data(
            overview.tableView.selectionModel().currentIndex(), role=ID_ROLE
        )
        response = requests.get(
            f"{config.api_server}/collections/{collection_id}",
            headers=config.auth_header,
        )
        data = response.json()
        model = RegistrationModel(data)

        rv = RegistrationView(model)
        self.setCentralWidget(rv)

    def upload(self, type):
        if type == "cfp":
            dialog = ImportCfpDialog(models=self.models)
        elif type == "nir":
            dialog = ImportNirDialog(models=self.models)
        elif type == "vol":
            dialog = ImportVolDialog(models=self.models)
        elif type == "hexml":
            dialog = ImportHexmlDialog(models=self.models)
        elif type == "folder":
            dialog = ImportFolderDialog(models=self.models)
        else:
            raise ValueError("'type' has to be either 'cfp' or 'vol'")

        if dialog.exec() == QtWidgets.QDialog.Accepted:
            pass

    def save(self):
        if (
            type(self.centralWidget()) == RegistrationView
            or type(self.centralWidget()) == AnnotationView
        ):
            self.centralWidget().save()

    def export(self):
        # Get current Dataset
        id = self.navigationDock.widget().datasetComboBox.currentData(role=ID_ROLE)
        # Get all collections for dataset
        collections = self.models["collections"].get_collections(dataset_id=id)
        full_collections = [c for c in collections if c["enfaceimage_ids"] != []]

        # Export all enface images in selected format
        # Download nir

        # Save nir

        # Download cfp

        # Warp cfp

        # Save cfp

        # Export warped enface images

        # Export registration as JSON

        # Export BScans

        # Export Annotations

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        # Save all unchanged annotations
        self.save()
        super().closeEvent(a0)


def main(log_level=logging.INFO):
    # create logger for "oat" application
    logger = logging.getLogger("eyelab")
    logger.setLevel(logging.DEBUG)

    # create file handler which logs debug messages
    fh = logging.FileHandler(EYELAB_FOLDER / "eyelab.log")
    fh.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )
    fh.setFormatter(file_formatter)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(log_level)
    cmd_formatter = logging.Formatter("%(levelname)s - %(name)s - %(message)s")
    ch.setFormatter(cmd_formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    logger.info("Starting Application.")

    application = QtWidgets.QApplication(sys.argv)
    window = oat()
    desktop = QtGui.QScreen().availableGeometry()
    width = (desktop.width() - window.width()) / 2
    height = (desktop.height() - window.height()) / 2
    window.show()
    window.move(width, height)

    sys.exit(application.exec())


if __name__ == "__main__":
    main()
