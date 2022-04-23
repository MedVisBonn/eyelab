# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_volumelocalizer_view.ui'
##
## Created by: Qt User Interface Compiler version 6.1.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from oat.modules.annotation.views.enface_view import EnfaceView
from oat.modules.annotation.views.volume_view import VolumeView
from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore

from . import resources_rc


class Ui_VolumeLocalizerView(object):
    def setupUi(self, VolumeLocalizerView):
        if not VolumeLocalizerView.objectName():
            VolumeLocalizerView.setObjectName(u"VolumeLocalizerView")
        VolumeLocalizerView.resize(670, 200)
        sizePolicy = QSizePolicy(
            QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding
        )
        sizePolicy.setHorizontalStretch(5)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(
            VolumeLocalizerView.sizePolicy().hasHeightForWidth()
        )
        VolumeLocalizerView.setSizePolicy(sizePolicy)
        self.horizontalLayout = QHBoxLayout(VolumeLocalizerView)
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.graphicsViewLocalizer = EnfaceView(VolumeLocalizerView)
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

        self.graphicsViewVolume = VolumeView(VolumeLocalizerView)
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

        self.retranslateUi(VolumeLocalizerView)

        QMetaObject.connectSlotsByName(VolumeLocalizerView)

    # setupUi

    def retranslateUi(self, VolumeLocalizerView):
        VolumeLocalizerView.setWindowTitle(
            QCoreApplication.translate("VolumeLocalizerView", u"Form", None)
        )

    # retranslateUi
