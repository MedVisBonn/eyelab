# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_layergroup_entry.ui'
##
## Created by: Qt User Interface Compiler version 6.1.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore

from . import resources_rc


class Ui_LayerGroupEntry(object):
    def setupUi(self, LayerGroupEntry):
        if not LayerGroupEntry.objectName():
            LayerGroupEntry.setObjectName(u"LayerGroupEntry")
        LayerGroupEntry.resize(200, 30)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(LayerGroupEntry.sizePolicy().hasHeightForWidth())
        LayerGroupEntry.setSizePolicy(sizePolicy)
        LayerGroupEntry.setMinimumSize(QSize(200, 30))
        LayerGroupEntry.setMaximumSize(QSize(350, 30))
        font = QFont()
        font.setPointSize(10)
        LayerGroupEntry.setFont(font)
        LayerGroupEntry.setContextMenuPolicy(Qt.PreventContextMenu)
        LayerGroupEntry.setAutoFillBackground(True)
        self.horizontalLayout_2 = QHBoxLayout(LayerGroupEntry)
        self.horizontalLayout_2.setSpacing(2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(2, 2, 2, 2)
        self.hideButton = QToolButton(LayerGroupEntry)
        self.hideButton.setObjectName(u"hideButton")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.hideButton.sizePolicy().hasHeightForWidth())
        self.hideButton.setSizePolicy(sizePolicy1)
        self.hideButton.setMinimumSize(QSize(26, 26))
        self.hideButton.setMaximumSize(QSize(26, 26))
        self.hideButton.setContextMenuPolicy(Qt.NoContextMenu)
        self.hideButton.setAutoFillBackground(False)
        icon = QIcon()
        icon.addFile(
            u":/icons/icons/baseline-visibility-24px.svg",
            QSize(),
            QIcon.Normal,
            QIcon.Off,
        )
        self.hideButton.setIcon(icon)
        self.hideButton.setIconSize(QSize(24, 24))

        self.horizontalLayout_2.addWidget(self.hideButton)

        self.label = QLabel(LayerGroupEntry)
        self.label.setObjectName(u"label")

        self.horizontalLayout_2.addWidget(self.label)

        self.retranslateUi(LayerGroupEntry)

        QMetaObject.connectSlotsByName(LayerGroupEntry)

    # setupUi

    def retranslateUi(self, LayerGroupEntry):
        LayerGroupEntry.setWindowTitle(
            QCoreApplication.translate("LayerGroupEntry", u"Form", None)
        )
        self.hideButton.setText(
            QCoreApplication.translate("LayerGroupEntry", u"...", None)
        )
        self.label.setText("")

    # retranslateUi
