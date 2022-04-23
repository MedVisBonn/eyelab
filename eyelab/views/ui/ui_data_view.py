# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_data_view.ui'
##
## Created by: Qt User Interface Compiler version 6.1.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore

from eyelab.views.enface_view import EnfaceView
from eyelab.views.volume_view import VolumeView

from . import resources_rc


class Ui_DataView(object):
    def setupUi(self, DataView):
        if not DataView.objectName():
            DataView.setObjectName(u"DataView")
        DataView.resize(670, 200)
        sizePolicy = QSizePolicy(
            QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding
        )
        sizePolicy.setHorizontalStretch(5)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(DataView.sizePolicy().hasHeightForWidth())
        DataView.setSizePolicy(sizePolicy)
        self.horizontalLayout = QHBoxLayout(DataView)
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.graphicsViewLocalizer = EnfaceView(DataView)
        self.graphicsViewLocalizer.setObjectName(u"graphicsViewLocalizer")
        sizePolicy1 = QSizePolicy(
            QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding
        )
        sizePolicy1.setHorizontalStretch(2)
        sizePolicy1.setVerticalStretch(2)
        sizePolicy1.setHeightForWidth(
            self.graphicsViewLocalizer.sizePolicy().hasHeightForWidth()
        )
        self.graphicsViewLocalizer.setSizePolicy(sizePolicy1)
        self.graphicsViewLocalizer.setMinimumSize(QSize(200, 200))

        self.horizontalLayout.addWidget(self.graphicsViewLocalizer)

        self.horizontalSpacer_3 = QSpacerItem(
            2, 20, QSizePolicy.Preferred, QSizePolicy.Minimum
        )

        self.horizontalLayout.addItem(self.horizontalSpacer_3)

        self.graphicsViewVolume = VolumeView(DataView)
        self.graphicsViewVolume.setObjectName(u"graphicsViewVolume")
        sizePolicy2 = QSizePolicy(
            QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding
        )
        sizePolicy2.setHorizontalStretch(4)
        sizePolicy2.setVerticalStretch(2)
        sizePolicy2.setHeightForWidth(
            self.graphicsViewVolume.sizePolicy().hasHeightForWidth()
        )
        self.graphicsViewVolume.setSizePolicy(sizePolicy2)
        self.graphicsViewVolume.setMinimumSize(QSize(400, 200))

        self.horizontalLayout.addWidget(self.graphicsViewVolume)

        self.retranslateUi(DataView)

        QMetaObject.connectSlotsByName(DataView)

    # setupUi

    def retranslateUi(self, DataView):
        DataView.setWindowTitle(QCoreApplication.translate("DataView", u"Form", None))

    # retranslateUi
