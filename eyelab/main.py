import logging
import sys
from functools import partial
from PySide6 import QtWidgets, QtGui

import eyepy as ep
from eyelab.config import EYELAB_FOLDER

from eyelab.views.ui.ui_main_window import Ui_MainWindow
from eyelab.views.workspace import Workspace


class eyelab(QtWidgets.QMainWindow, Ui_MainWindow):
    """Create the main window that stores all of the widgets necessary for the application."""

    def __init__(self, parent=None):
        """Initialize the components of the main window."""
        super().__init__(parent)
        self.setupUi(self)

        self.volume_data = None

        self.actionImportVol.triggered.connect(
            partial(self.import_data, method=ep.import_heyex_vol, format="file")
        )
        self.actionImportHEXML.triggered.connect(
            partial(self.import_data, method=ep.import_heyex_xml, format="folder")
        )
        self.actionImportBSFolder.triggered.connect(
            partial(self.import_data, method=ep.import_bscan_folder, format="folder")
        )
        self.actionSave.triggered.connect(self.save)
        self.actionExport.triggered.connect(self.export)

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

        self.workspace = Workspace(parent=self)
        self.setCentralWidget(self.workspace)

        from eyepy.data import load

        ev = load("drusen_patient")
        ev.set_volume_map(
            "Drusen", ep.drusen(ev.layers["RPE"], ev.layers["BM"], ev.shape)
        )
        self.workspace.set_data(ev)

        # self.statusBar().showMessage("")

    def import_data(self, method, format):
        from PySide6.QtWidgets import QFileDialog

        if format == "file":
            path = QFileDialog.getOpenFileName()
        elif format == "folder":
            path = QFileDialog.getExistingDirectory()

        self.workspace.set_data(method(path))

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

    def save(self):
        pass

    def export(self):
        pass

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        # Save all unchanged annotations
        self.save()
        super().closeEvent(a0)


def main(log_level=logging.DEBUG):
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
    window = eyelab()
    desktop = QtGui.QScreen().availableGeometry()
    width = (desktop.width() - window.width()) / 2
    height = (desktop.height() - window.height()) / 2
    window.show()
    window.move(width, height)

    sys.exit(application.exec())


if __name__ == "__main__":
    main()
