# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_2d_viewer.ui'
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
from PySide6.QtWidgets import QApplication, QSizePolicy, QVBoxLayout, QWidget

from oat.views import CustomGraphicsView


class Ui_Viewer2D(object):
    def setupUi(self, Viewer2D):
        if not Viewer2D.objectName():
            Viewer2D.setObjectName(u"Viewer2D")
        Viewer2D.resize(400, 400)
        Viewer2D.setMinimumSize(QSize(400, 400))
        self.verticalLayout = QVBoxLayout(Viewer2D)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.graphicsView2D = CustomGraphicsView(Viewer2D)
        self.graphicsView2D.setObjectName(u"graphicsView2D")
        self.graphicsView2D.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphicsView2D.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.verticalLayout.addWidget(self.graphicsView2D)

        self.retranslateUi(Viewer2D)

        QMetaObject.connectSlotsByName(Viewer2D)

    # setupUi

    def retranslateUi(self, Viewer2D):
        Viewer2D.setWindowTitle(QCoreApplication.translate("Viewer2D", u"Form", None))

    # retranslateUi
