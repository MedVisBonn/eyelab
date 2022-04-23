# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_spline_options.ui'
##
## Created by: Qt User Interface Compiler version 6.1.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore


class Ui_splineOptions(object):
    def setupUi(self, splineOptions):
        if not splineOptions.objectName():
            splineOptions.setObjectName(u"splineOptions")
        splineOptions.resize(139, 109)
        self.verticalLayout = QVBoxLayout(splineOptions)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(2, 2, 2, 2)
        self.label = QLabel(splineOptions)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(8)
        font.setBold(True)
        self.label.setFont(font)

        self.verticalLayout.addWidget(self.label)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(5, -1, -1, -1)
        self.showCheckBox = QCheckBox(splineOptions)
        self.showCheckBox.setObjectName(u"showCheckBox")
        font1 = QFont()
        font1.setPointSize(8)
        self.showCheckBox.setFont(font1)
        self.showCheckBox.setChecked(True)

        self.verticalLayout_2.addWidget(self.showCheckBox)

        self.strengthCheckBox = QCheckBox(splineOptions)
        self.strengthCheckBox.setObjectName(u"strengthCheckBox")
        self.strengthCheckBox.setFont(font1)
        self.strengthCheckBox.setChecked(True)

        self.verticalLayout_2.addWidget(self.strengthCheckBox)

        self.slopeCheckBox = QCheckBox(splineOptions)
        self.slopeCheckBox.setObjectName(u"slopeCheckBox")
        self.slopeCheckBox.setFont(font1)
        self.slopeCheckBox.setChecked(True)

        self.verticalLayout_2.addWidget(self.slopeCheckBox)

        self.neighbourCheckBox = QCheckBox(splineOptions)
        self.neighbourCheckBox.setObjectName(u"neighbourCheckBox")
        self.neighbourCheckBox.setFont(font1)
        self.neighbourCheckBox.setChecked(True)

        self.verticalLayout_2.addWidget(self.neighbourCheckBox)

        self.verticalLayout.addLayout(self.verticalLayout_2)

        self.verticalSpacer = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.verticalLayout.addItem(self.verticalSpacer)

        self.retranslateUi(splineOptions)

        QMetaObject.connectSlotsByName(splineOptions)

    # setupUi

    def retranslateUi(self, splineOptions):
        splineOptions.setWindowTitle("")
        self.label.setText(
            QCoreApplication.translate("splineOptions", u"Control points:", None)
        )
        # if QT_CONFIG(tooltip)
        self.showCheckBox.setToolTip(
            QCoreApplication.translate(
                "splineOptions", u"Hide the blue control points", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.showCheckBox.setText(
            QCoreApplication.translate("splineOptions", u"Show", None)
        )
        # if QT_CONFIG(tooltip)
        self.strengthCheckBox.setToolTip(
            QCoreApplication.translate(
                "splineOptions",
                u"Optimize control point position when moving a knot",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.strengthCheckBox.setText(
            QCoreApplication.translate("splineOptions", u"Optimize strength", None)
        )
        self.slopeCheckBox.setText(
            QCoreApplication.translate("splineOptions", u"Optimize slope", None)
        )
        self.neighbourCheckBox.setText(
            QCoreApplication.translate("splineOptions", u"Optimize neighbours", None)
        )

    # retranslateUi
