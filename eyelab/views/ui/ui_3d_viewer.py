# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_3d_viewer.ui'
##
## Created by: Qt User Interface Compiler version 6.1.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from oat.views.custom import CustomGraphicsView
from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore


class Ui_Viewer3D(object):
    def setupUi(self, Viewer3D):
        if not Viewer3D.objectName():
            Viewer3D.setObjectName(u"Viewer3D")
        Viewer3D.resize(400, 300)
        self.verticalLayout_2 = QVBoxLayout(Viewer3D)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.graphicsView3D = CustomGraphicsView(Viewer3D)
        self.graphicsView3D.setObjectName(u"graphicsView3D")
        self.graphicsView3D.setMinimumSize(QSize(400, 400))
        self.graphicsView3D.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphicsView3D.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.verticalLayout_2.addWidget(self.graphicsView3D)

        self.spinBox = QSpinBox(Viewer3D)
        self.spinBox.setObjectName(u"spinBox")

        self.verticalLayout_2.addWidget(self.spinBox)

        self.retranslateUi(Viewer3D)

        QMetaObject.connectSlotsByName(Viewer3D)

    # setupUi

    def retranslateUi(self, Viewer3D):
        Viewer3D.setWindowTitle(QCoreApplication.translate("Viewer3D", u"Form", None))

    # retranslateUi
