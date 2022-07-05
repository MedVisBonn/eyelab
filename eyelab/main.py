import logging
import os
import sys
from functools import partial
from pathlib import Path

import eyepy as ep
import numpy as np
import requests
from packaging import version
from PySide6 import QtWidgets
from PySide6.QtCore import QCoreApplication, QSize
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QFileDialog, QMessageBox

import eyelab as el
from eyelab.commands import get_undo_stack
from eyelab.commands.thin_out import ThinOut
from eyelab.config import EYELAB_FOLDER
from eyelab.dialogs.help import (
    AreaAnnotationHelp,
    IntroductionHelp,
    LayerAnnotationHelp,
    ShortcutHelp,
)
from eyelab.views.ui.ui_main_window import Ui_MainWindow
from eyelab.views.workspace import Workspace


class eyelab(QtWidgets.QMainWindow, Ui_MainWindow):
    """Create the main window that stores all of the widgets necessary for the application."""

    def __init__(self, parent=None):
        """Initialize the components of the main window."""
        super().__init__(parent)
        self.setupUi(self)

        self.save_path = None

        self.action_import_vol.triggered.connect(
            partial(self.import_data, method=ep.import_heyex_vol, format="file")
        )
        self.action_import_hexml.triggered.connect(
            partial(self.import_data, method=ep.import_heyex_xml, format="folder")
        )
        self.action_import_retouch.triggered.connect(
            partial(self.import_data, method=ep.import_retouch, format="folder")
        )
        self.action_import_duke.triggered.connect(
            partial(self.import_data, method=ep.import_duke_mat, format="file")
        )
        self.action_import_bsfolder.triggered.connect(
            partial(self.import_data, method=ep.import_bscan_folder, format="folder")
        )
        # self.action_save_annotations.triggered.connect(self.save_annotations)
        # self.action_save_annotations_as.triggered.connect(
        #    partial(self.save_annotations, save_as=True)
        # )
        # self.action_load_annotations.triggered.connect(self.load_annotations)
        self.action_open.triggered.connect(self.load)
        self.action_save.triggered.connect(self.save)
        self.action_save_as.triggered.connect(partial(self.save, save_as=True))
        self.action_shortcut_sheet.triggered.connect(
            lambda: self.open_help("shortcuts")
        )
        self.action_area_annotation_guide.triggered.connect(
            lambda: self.open_help("area_annotation")
        )
        self.action_layer_annotation_guide.triggered.connect(
            lambda: self.open_help("layer_annotation")
        )
        self.action_registration_guide.triggered.connect(
            lambda: self.open_help("registration")
        )
        self.action_introduction.triggered.connect(
            lambda: self.open_help("introduction")
        )
        self.action_About.triggered.connect(self.show_about)
        self.workspace = Workspace(parent=self)
        # Todo: reenable if areaitem is integrated in the undo/redo framework
        # self.workspace.undo_stack.cleanChanged.connect(
        #    lambda x: self.setWindowModified(not x)
        # )

        self._edit_menu_setup()
        self._tools_menu_setup()
        self.setCentralWidget(self.workspace)
        self.check_version()

        self.setWindowModified(False)
        # hide options for loading/saving annotations only
        self.menuAnnotations.deleteLater()

        # from eyepy.data import load

        # ev = load("drusen_patient")
        # ev.add_voxel_annotation(
        #    ep.drusen(ev.layers["RPE"], ev.layers["BM"], ev.shape), name="Drusen"
        # )
        # self.workspace.set_data(ev)
        # self.statusBar().showMessage("Ready")

    def setWindowModified(self, value: bool) -> None:
        super().setWindowModified(value)

        # Todo: reenable if areaitem is integrated in the undo/redo framework
        # self.action_save.setEnabled(value)
        # self.action_save_as.setEnabled(value)

    def setWindowFilePath(self, filePath: str) -> None:
        super().setWindowFilePath(filePath)
        self.setWindowTitle(f"EyeLab - {self.windowFilePath()}[*]")

    def _edit_menu_setup(self):
        self.action_undo = self.workspace.undo_stack.createUndoAction(self)
        self.action_redo = self.workspace.undo_stack.createRedoAction(self)

        undo_icon = QIcon()
        undo_icon.addFile(
            ":/icons/icons/baseline-undo-24px.svg", QSize(), QIcon.Normal, QIcon.Off
        )
        self.action_undo.setIcon(undo_icon)

        redo_icon = QIcon()
        redo_icon.addFile(
            ":/icons/icons/baseline-redo-24px.svg", QSize(), QIcon.Normal, QIcon.Off
        )
        self.action_redo.setIcon(redo_icon)

        self.action_undo.setShortcut(
            QCoreApplication.translate("MainWindow", "Ctrl+Z", None)
        )
        self.action_redo.setShortcut(
            QCoreApplication.translate("MainWindow", "Ctrl+Y", None)
        )

        self.menuEdit.addAction(self.action_undo)
        self.menuEdit.addAction(self.action_redo)

    def _tools_menu_setup(self):
        self.action_thin_out = QAction(
            QCoreApplication.translate("MainWindow", "&Thin Out"), self
        )
        self.action_thin_out.setStatusTip(
            QCoreApplication.translate(
                "MainWindow", "Deactivte B-scans for sparse annotation"
            )
        )
        self.action_thin_out.triggered.connect(
            lambda: get_undo_stack("main").push(
                ThinOut(self.workspace.data, n=5, region=(1 / 3, 2 / 3))
            )
        )

        self.menuTools.addAction(self.action_thin_out)

    def check_version(self):
        latest_url = "https://github.com/MedVisBonn/eyelab/releases/latest"
        current_version = f"v{el.__version__}"

        try:
            latest_version = (requests.get(latest_url).url).split("/")[-1]
        except requests.ConnectionError:
            return

        if version.parse(current_version) < version.parse(latest_version):
            msgBox = QMessageBox()
            msgBox.setText("A new version of EyeLab is available.")
            msgBox.setInformativeText(
                f"You are using version {current_version}. The latest version is {latest_version} and can be found <a href='{latest_url}'>here</a>."
            )
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.setDefaultButton(QMessageBox.Ok)
            ret = msgBox.exec()

    def show_about(self):
        version = el.__version__
        repository = f"https://github.com/MedVisBonn/eyelab/"
        msgBox = QMessageBox()
        msgBox.setWindowTitle("About")
        msgBox.setText(f"<h1>EyeLab v{version}<\h1>")
        msgBox.setInformativeText(
            f"<b>Repository:</b> <p> <a href='{repository}'>{repository}</a> </p>"
            f"<b>Contact:</b> <p> Olivier Morelle <br> oli4morelle@gmail.com </p>"
            f"<b>Cite:</b> <p> <a href='https://doi.org/10.5281/zenodo.6614972'>https://doi.org/10.5281/zenodo.6614972</a></p>"
        )
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.setDefaultButton(QMessageBox.Ok)
        msgBox.exec()

    @property
    def start_dir(self):
        if self.windowFilePath():
            return str(Path(self.windowFilePath()).parent)
        else:
            return str(Path.home())

    def import_data(self, method, format):
        if not self.workspace.data is None:
            message = "The import replaces all data you have in your workspace. Do you want to proceed?"
            ret = QMessageBox.question(
                self, "EyeLab", message, QMessageBox.Ok | QMessageBox.Cancel
            )

            if ret == QMessageBox.Cancel:
                return

        if format == "file":
            path = QFileDialog.getOpenFileName(dir=self.start_dir)[0]
        elif format == "folder":
            path = QFileDialog.getExistingDirectory(dir=self.start_dir)

        self.workspace.set_data(method(path))
        self.setWindowFilePath("")
        get_undo_stack("main").clear()

    def get_save_location(self):
        if "PYCHARM_HOSTED" in os.environ:
            options = QFileDialog.DontUseNativeDialog
        else:
            options = QFileDialog.Options()
        save_path, filter = QFileDialog.getSaveFileName(
            parent=self, caption="Save", filter="Eye files (*.eye)", options=options
        )
        if save_path:
            if not save_path.endswith(".eye"):
                save_path = save_path + ".eye"
            self.setWindowFilePath(save_path)
        return save_path

    def save(self, save_as=False):
        path = self.windowFilePath()
        if save_as is True or path == "" or path.startswith("/run/user"):
            self.get_save_location()
        if self.windowFilePath():
            self.statusBar().showMessage("Saving...")
            self.workspace.data.save(self.windowFilePath())
            get_undo_stack("main").setClean()
            self.statusBar().showMessage("Done", 2000)

    def load(self):
        if self.workspace.data is not None:
            message = "Loading data replaces the current data. Do you want to proceed?"
            ret = QMessageBox.question(
                self, "EyeLab", message, QMessageBox.Ok | QMessageBox.Cancel
            )

            if ret == QMessageBox.Cancel:
                return

        path = QFileDialog.getOpenFileName(
            parent=self,
            caption="Load",
            dir=self.start_dir,
            filter="Eye files (*.eye)",
        )[0]
        if path == "":
            return
        self.setWindowFilePath(path)

        self.statusBar().showMessage("Loading...")
        ev = ep.EyeVolume.load(path)
        self.workspace.set_data(ev)
        get_undo_stack("main").clear()
        self.statusBar().showMessage("Done", 2000)

    def open_help(self, topic):
        if topic == "introduction":
            dialog = IntroductionHelp(self)
        elif topic == "shortcuts":
            dialog = ShortcutHelp(self)
        elif topic == "area_annotation":
            dialog = AreaAnnotationHelp(self)
        elif topic == "layer_annotation":
            dialog = LayerAnnotationHelp(self)
        # elif topic == "registration":
        #    dialog = RegistrationHelp(self)
        else:
            raise ValueError("topic not available")

        if dialog.exec() == QtWidgets.QDialog.Rejected:
            pass


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
    # desktop = QtGui.QScreen().availableGeometry()
    # width = (desktop.width() - window.width()) / 2
    # height = (desktop.height() - window.height()) / 2
    # window.show()
    # window.move(width, height)
    window.showMaximized()

    sys.exit(application.exec())


if __name__ == "__main__":
    main()
