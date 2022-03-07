# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.2.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    QTime,
    QUrl,
    Qt,
)
from PySide6.QtGui import (
    QAction,
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QMenu,
    QMenuBar,
    QSizePolicy,
    QStatusBar,
    QVBoxLayout,
    QWidget,
)
from . import resources_rc


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(836, 618)
        self.actionSave_as = QAction(MainWindow)
        self.actionSave_as.setObjectName(u"actionSave_as")
        self.actionOpen_Project = QAction(MainWindow)
        self.actionOpen_Project.setObjectName(u"actionOpen_Project")
        self.action_vol = QAction(MainWindow)
        self.action_vol.setObjectName(u"action_vol")
        self.action_vol.setEnabled(True)
        self.actionToggle2D = QAction(MainWindow)
        self.actionToggle2D.setObjectName(u"actionToggle2D")
        self.actionToggle2D.setCheckable(True)
        self.actionToggle2D.setChecked(True)
        self.actionToggle2D.setEnabled(True)
        self.actionToggle3D = QAction(MainWindow)
        self.actionToggle3D.setObjectName(u"actionToggle3D")
        self.actionToggle3D.setCheckable(True)
        self.actionToggle3D.setChecked(True)
        self.actionToogleToolbox = QAction(MainWindow)
        self.actionToogleToolbox.setObjectName(u"actionToogleToolbox")
        self.actionToogleToolbox.setCheckable(True)
        self.actionToogleToolbox.setChecked(True)
        self.actionUndo = QAction(MainWindow)
        self.actionUndo.setObjectName(u"actionUndo")
        self.actionUndo.setCheckable(False)
        self.actionUndo.setEnabled(True)
        icon = QIcon()
        icon.addFile(
            u":/icons/icons/baseline-undo-24px.svg", QSize(), QIcon.Normal, QIcon.Off
        )
        self.actionUndo.setIcon(icon)
        self.actionRedo = QAction(MainWindow)
        self.actionRedo.setObjectName(u"actionRedo")
        icon1 = QIcon()
        icon1.addFile(
            u":/icons/icons/baseline-redo-24px.svg", QSize(), QIcon.Normal, QIcon.Off
        )
        self.actionRedo.setIcon(icon1)
        self.action_cfp = QAction(MainWindow)
        self.action_cfp.setObjectName(u"action_cfp")
        self.actionExport = QAction(MainWindow)
        self.actionExport.setObjectName(u"actionExport")
        self.actionImportVol = QAction(MainWindow)
        self.actionImportVol.setObjectName(u"actionImportVol")
        self.actionImportCfp = QAction(MainWindow)
        self.actionImportCfp.setObjectName(u"actionImportCfp")
        self.actionSave = QAction(MainWindow)
        self.actionSave.setObjectName(u"actionSave")
        self.actionImportHEXML = QAction(MainWindow)
        self.actionImportHEXML.setObjectName(u"actionImportHEXML")
        self.actionImportBSFolder = QAction(MainWindow)
        self.actionImportBSFolder.setObjectName(u"actionImportBSFolder")
        self.actionLayerAnnotationGuide = QAction(MainWindow)
        self.actionLayerAnnotationGuide.setObjectName(u"actionLayerAnnotationGuide")
        self.actionAreaAnnotationGuide = QAction(MainWindow)
        self.actionAreaAnnotationGuide.setObjectName(u"actionAreaAnnotationGuide")
        self.actionRegistrationGuide = QAction(MainWindow)
        self.actionRegistrationGuide.setObjectName(u"actionRegistrationGuide")
        self.actionShortcutSheet = QAction(MainWindow)
        self.actionShortcutSheet.setObjectName(u"actionShortcutSheet")
        self.actionImportNir = QAction(MainWindow)
        self.actionImportNir.setObjectName(u"actionImportNir")
        self.actionIntroduction = QAction(MainWindow)
        self.actionIntroduction.setObjectName(u"actionIntroduction")
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
        self.menuEdit = QMenu(self.menubar)
        self.menuEdit.setObjectName(u"menuEdit")
        self.menuEdit.setEnabled(False)
        self.menuEdit.setTearOffEnabled(False)
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.menuUpload.menuAction())
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addSeparator()
        self.menuUpload.addAction(self.actionImportVol)
        self.menuUpload.addAction(self.actionImportHEXML)
        self.menuUpload.addSeparator()
        self.menuUpload.addAction(self.actionImportBSFolder)
        self.menuEdit.addAction(self.actionUndo)
        self.menuEdit.addAction(self.actionRedo)
        self.menuHelp.addAction(self.actionIntroduction)
        self.menuHelp.addAction(self.actionLayerAnnotationGuide)
        self.menuHelp.addAction(self.actionAreaAnnotationGuide)
        self.menuHelp.addAction(self.actionRegistrationGuide)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionShortcutSheet)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            QCoreApplication.translate("MainWindow", u"EyeLab", None)
        )
        self.actionSave_as.setText(
            QCoreApplication.translate("MainWindow", u"Save as", None)
        )
        self.actionOpen_Project.setText(
            QCoreApplication.translate("MainWindow", u"Open Project", None)
        )
        self.action_vol.setText(
            QCoreApplication.translate("MainWindow", u"HE raw Export (.vol )", None)
        )
        self.actionToggle2D.setText(
            QCoreApplication.translate("MainWindow", u"2D Viewer", None)
        )
        self.actionToggle3D.setText(
            QCoreApplication.translate("MainWindow", u"3D Viewer", None)
        )
        self.actionToogleToolbox.setText(
            QCoreApplication.translate("MainWindow", u"Toolbox", None)
        )
        self.actionUndo.setText(QCoreApplication.translate("MainWindow", u"Undo", None))
        # if QT_CONFIG(shortcut)
        self.actionUndo.setShortcut(
            QCoreApplication.translate("MainWindow", u"Ctrl+Z", None)
        )
        # endif // QT_CONFIG(shortcut)
        self.actionRedo.setText(QCoreApplication.translate("MainWindow", u"Redo", None))
        # if QT_CONFIG(shortcut)
        self.actionRedo.setShortcut(
            QCoreApplication.translate("MainWindow", u"Ctrl+Y", None)
        )
        # endif // QT_CONFIG(shortcut)
        self.action_cfp.setText(
            QCoreApplication.translate("MainWindow", u"CFP (.bmp/.tif/.jpg)", None)
        )
        self.actionExport.setText(
            QCoreApplication.translate("MainWindow", u"Export", None)
        )
        self.actionImportVol.setText(
            QCoreApplication.translate("MainWindow", u"Heyex Raw (.vol)", None)
        )
        self.actionImportCfp.setText(
            QCoreApplication.translate("MainWindow", u"CFP", None)
        )
        self.actionSave.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.actionImportHEXML.setText(
            QCoreApplication.translate("MainWindow", u"Heyex XML (.xml)", None)
        )
        self.actionImportBSFolder.setText(
            QCoreApplication.translate("MainWindow", u"B-Scans from folder", None)
        )
        self.actionLayerAnnotationGuide.setText(
            QCoreApplication.translate("MainWindow", u"Layer Annotation Guide", None)
        )
        self.actionAreaAnnotationGuide.setText(
            QCoreApplication.translate("MainWindow", u"Area Annotation Guide", None)
        )
        self.actionRegistrationGuide.setText(
            QCoreApplication.translate("MainWindow", u"Registration Guide", None)
        )
        self.actionShortcutSheet.setText(
            QCoreApplication.translate("MainWindow", u"Shortcut Sheet", None)
        )
        self.actionImportNir.setText(
            QCoreApplication.translate("MainWindow", u"NIR", None)
        )
        self.actionIntroduction.setText(
            QCoreApplication.translate("MainWindow", u"Introduction", None)
        )
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuUpload.setTitle(
            QCoreApplication.translate("MainWindow", u"Import", None)
        )
        self.menuEdit.setTitle("")
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))

    # retranslateUi
