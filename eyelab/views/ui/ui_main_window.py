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
        self.actionImportVol = QAction(MainWindow)
        self.actionImportVol.setObjectName(u"actionImportVol")
        self.actionSaveAnnotations = QAction(MainWindow)
        self.actionSaveAnnotations.setObjectName(u"actionSaveAnnotations")
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
        self.actionIntroduction = QAction(MainWindow)
        self.actionIntroduction.setObjectName(u"actionIntroduction")
        self.actionImportRETOUCH = QAction(MainWindow)
        self.actionImportRETOUCH.setObjectName(u"actionImportRETOUCH")
        self.actionImportDuke = QAction(MainWindow)
        self.actionImportDuke.setObjectName(u"actionImportDuke")
        self.actionImportHEXML = QAction(MainWindow)
        self.actionImportHEXML.setObjectName(u"actionImportHEXML")
        self.actionLoadAnnotations = QAction(MainWindow)
        self.actionLoadAnnotations.setObjectName(u"actionLoadAnnotations")
        self.actionSaveAnnotationsAs = QAction(MainWindow)
        self.actionSaveAnnotationsAs.setObjectName(u"actionSaveAnnotationsAs")
        self.actionOpen = QAction(MainWindow)
        self.actionOpen.setObjectName(u"actionOpen")
        self.actionSave = QAction(MainWindow)
        self.actionSave.setObjectName(u"actionSave")
        self.actionSave_As = QAction(MainWindow)
        self.actionSave_As.setObjectName(u"actionSave_As")
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
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_As)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.menuUpload.menuAction())
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.menuAnnotations.menuAction())
        self.menuUpload.addAction(self.actionImportVol)
        self.menuUpload.addAction(self.actionImportHEXML)
        self.menuUpload.addSeparator()
        self.menuUpload.addAction(self.actionImportRETOUCH)
        self.menuUpload.addAction(self.actionImportDuke)
        self.menuUpload.addSeparator()
        self.menuUpload.addAction(self.actionImportBSFolder)
        self.menuAnnotations.addAction(self.actionLoadAnnotations)
        self.menuAnnotations.addSeparator()
        self.menuAnnotations.addAction(self.actionSaveAnnotations)
        self.menuAnnotations.addAction(self.actionSaveAnnotationsAs)
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
        self.actionImportVol.setText(
            QCoreApplication.translate("MainWindow", u"Heyex Raw (.vol)", None)
        )
        self.actionSaveAnnotations.setText(
            QCoreApplication.translate("MainWindow", u"Save", None)
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
        self.actionIntroduction.setText(
            QCoreApplication.translate("MainWindow", u"Introduction", None)
        )
        self.actionImportRETOUCH.setText(
            QCoreApplication.translate("MainWindow", u"RETOUCH", None)
        )
        self.actionImportDuke.setText(
            QCoreApplication.translate("MainWindow", u"Duke (Farsiu 2014)", None)
        )
        self.actionImportHEXML.setText(
            QCoreApplication.translate("MainWindow", u"Heyex XML (.xml)", None)
        )
        self.actionLoadAnnotations.setText(
            QCoreApplication.translate("MainWindow", u"Load", None)
        )
        self.actionSaveAnnotationsAs.setText(
            QCoreApplication.translate("MainWindow", u"Save As", None)
        )
        self.actionOpen.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        self.actionSave.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.actionSave_As.setText(
            QCoreApplication.translate("MainWindow", u"Save As", None)
        )
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuUpload.setTitle(
            QCoreApplication.translate("MainWindow", u"Import", None)
        )
        self.menuAnnotations.setTitle(
            QCoreApplication.translate("MainWindow", u"Annotations", None)
        )
        self.menuEdit.setTitle("")
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))

    # retranslateUi
