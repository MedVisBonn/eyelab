# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.1.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore

from . import resources_rc


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(836, 618)
        self.action_undo = QAction(MainWindow)
        self.action_undo.setObjectName(u"action_undo")
        self.action_undo.setCheckable(False)
        self.action_undo.setEnabled(True)
        icon = QIcon()
        icon.addFile(
            u":/icons/icons/baseline-undo-24px.svg", QSize(), QIcon.Normal, QIcon.Off
        )
        self.action_undo.setIcon(icon)
        self.action_redo = QAction(MainWindow)
        self.action_redo.setObjectName(u"action_redo")
        icon1 = QIcon()
        icon1.addFile(
            u":/icons/icons/baseline-redo-24px.svg", QSize(), QIcon.Normal, QIcon.Off
        )
        self.action_redo.setIcon(icon1)
        self.action_import_vol = QAction(MainWindow)
        self.action_import_vol.setObjectName(u"action_import_vol")
        self.action_save_annotations = QAction(MainWindow)
        self.action_save_annotations.setObjectName(u"action_save_annotations")
        self.action_save_annotations.setEnabled(True)
        self.action_save_annotations.setVisible(True)
        self.action_import_bsfolder = QAction(MainWindow)
        self.action_import_bsfolder.setObjectName(u"action_import_bsfolder")
        self.action_layer_annotation_guide = QAction(MainWindow)
        self.action_layer_annotation_guide.setObjectName(
            u"action_layer_annotation_guide"
        )
        self.action_area_annotation_guide = QAction(MainWindow)
        self.action_area_annotation_guide.setObjectName(u"action_area_annotation_guide")
        self.action_registration_guide = QAction(MainWindow)
        self.action_registration_guide.setObjectName(u"action_registration_guide")
        self.action_registration_guide.setVisible(False)
        self.action_shortcut_sheet = QAction(MainWindow)
        self.action_shortcut_sheet.setObjectName(u"action_shortcut_sheet")
        self.action_introduction = QAction(MainWindow)
        self.action_introduction.setObjectName(u"action_introduction")
        self.action_import_retouch = QAction(MainWindow)
        self.action_import_retouch.setObjectName(u"action_import_retouch")
        self.action_import_duke = QAction(MainWindow)
        self.action_import_duke.setObjectName(u"action_import_duke")
        self.action_import_hexml = QAction(MainWindow)
        self.action_import_hexml.setObjectName(u"action_import_hexml")
        self.action_load_annotations = QAction(MainWindow)
        self.action_load_annotations.setObjectName(u"action_load_annotations")
        self.action_load_annotations.setEnabled(True)
        self.action_load_annotations.setVisible(True)
        self.action_save_annotations_as = QAction(MainWindow)
        self.action_save_annotations_as.setObjectName(u"action_save_annotations_as")
        self.action_save_annotations_as.setEnabled(True)
        self.action_save_annotations_as.setVisible(True)
        self.action_open = QAction(MainWindow)
        self.action_open.setObjectName(u"action_open")
        self.action_save = QAction(MainWindow)
        self.action_save.setObjectName(u"action_save")
        self.action_save_as = QAction(MainWindow)
        self.action_save_as.setObjectName(u"action_save_as")
        self.action_About = QAction(MainWindow)
        self.action_About.setObjectName(u"action_About")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 836, 22))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuUpload = QMenu(self.menuFile)
        self.menuUpload.setObjectName(u"menuUpload")
        self.menuAnnotations = QMenu(self.menuFile)
        self.menuAnnotations.setObjectName(u"menuAnnotations")
        self.menuAnnotations.setEnabled(False)
        self.menuEdit = QMenu(self.menubar)
        self.menuEdit.setObjectName(u"menuEdit")
        self.menuEdit.setEnabled(True)
        self.menuEdit.setTearOffEnabled(False)
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        self.menuTools = QMenu(self.menubar)
        self.menuTools.setObjectName(u"menuTools")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.action_open)
        self.menuFile.addAction(self.action_save)
        self.menuFile.addAction(self.action_save_as)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.menuUpload.menuAction())
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.menuAnnotations.menuAction())
        self.menuUpload.addAction(self.action_import_vol)
        self.menuUpload.addAction(self.action_import_hexml)
        self.menuUpload.addSeparator()
        self.menuUpload.addAction(self.action_import_retouch)
        self.menuUpload.addAction(self.action_import_duke)
        self.menuUpload.addSeparator()
        self.menuUpload.addAction(self.action_import_bsfolder)
        self.menuAnnotations.addAction(self.action_load_annotations)
        self.menuAnnotations.addSeparator()
        self.menuAnnotations.addAction(self.action_save_annotations)
        self.menuAnnotations.addAction(self.action_save_annotations_as)
        self.menuHelp.addAction(self.action_introduction)
        self.menuHelp.addAction(self.action_layer_annotation_guide)
        self.menuHelp.addAction(self.action_area_annotation_guide)
        self.menuHelp.addAction(self.action_registration_guide)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.action_shortcut_sheet)
        self.menuHelp.addAction(self.action_About)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            QCoreApplication.translate("MainWindow", u"EyeLab", None)
        )
        self.action_undo.setText(
            QCoreApplication.translate("MainWindow", u"&Undo", None)
        )
        # if QT_CONFIG(shortcut)
        self.action_undo.setShortcut(
            QCoreApplication.translate("MainWindow", u"Ctrl+Z", None)
        )
        # endif // QT_CONFIG(shortcut)
        self.action_redo.setText(
            QCoreApplication.translate("MainWindow", u"&Redo", None)
        )
        # if QT_CONFIG(shortcut)
        self.action_redo.setShortcut(
            QCoreApplication.translate("MainWindow", u"Ctrl+Y", None)
        )
        # endif // QT_CONFIG(shortcut)
        self.action_import_vol.setText(
            QCoreApplication.translate("MainWindow", u"Heyex Raw (.&vol)", None)
        )
        self.action_save_annotations.setText(
            QCoreApplication.translate("MainWindow", u"Save", None)
        )
        self.action_import_bsfolder.setText(
            QCoreApplication.translate("MainWindow", u"B-Scans from &folder", None)
        )
        self.action_layer_annotation_guide.setText(
            QCoreApplication.translate("MainWindow", u"&Layer Annotation Guide", None)
        )
        self.action_area_annotation_guide.setText(
            QCoreApplication.translate("MainWindow", u"&Area Annotation Guide", None)
        )
        self.action_registration_guide.setText(
            QCoreApplication.translate("MainWindow", u"Registration Guide", None)
        )
        self.action_shortcut_sheet.setText(
            QCoreApplication.translate("MainWindow", u"&Shortcut Sheet", None)
        )
        self.action_introduction.setText(
            QCoreApplication.translate("MainWindow", u"&Introduction", None)
        )
        self.action_import_retouch.setText(
            QCoreApplication.translate("MainWindow", u"&RETOUCH", None)
        )
        self.action_import_duke.setText(
            QCoreApplication.translate("MainWindow", u"&Duke (Farsiu 2014)", None)
        )
        self.action_import_hexml.setText(
            QCoreApplication.translate("MainWindow", u"Heyex XML (.&xml)", None)
        )
        self.action_load_annotations.setText(
            QCoreApplication.translate("MainWindow", u"Load", None)
        )
        self.action_save_annotations_as.setText(
            QCoreApplication.translate("MainWindow", u"Save As", None)
        )
        self.action_open.setText(
            QCoreApplication.translate("MainWindow", u"&Open", None)
        )
        # if QT_CONFIG(shortcut)
        self.action_open.setShortcut(
            QCoreApplication.translate("MainWindow", u"Ctrl+O", None)
        )
        # endif // QT_CONFIG(shortcut)
        self.action_save.setText(
            QCoreApplication.translate("MainWindow", u"&Save", None)
        )
        # if QT_CONFIG(shortcut)
        self.action_save.setShortcut(
            QCoreApplication.translate("MainWindow", u"Ctrl+S", None)
        )
        # endif // QT_CONFIG(shortcut)
        self.action_save_as.setText(
            QCoreApplication.translate("MainWindow", u"Save &As", None)
        )
        # if QT_CONFIG(shortcut)
        self.action_save_as.setShortcut(
            QCoreApplication.translate("MainWindow", u"Ctrl+A", None)
        )
        # endif // QT_CONFIG(shortcut)
        self.action_About.setText(
            QCoreApplication.translate("MainWindow", u"A&bout", None)
        )
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"&File", None))
        self.menuUpload.setTitle(
            QCoreApplication.translate("MainWindow", u"&Import", None)
        )
        self.menuAnnotations.setTitle(
            QCoreApplication.translate("MainWindow", u"Annotations", None)
        )
        self.menuEdit.setTitle(QCoreApplication.translate("MainWindow", u"&Edit", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"&Help", None))
        self.menuTools.setTitle(
            QCoreApplication.translate("MainWindow", u"&Tools", None)
        )

    # retranslateUi
