# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_pen_options.ui'
##
## Created by: Qt User Interface Compiler version 6.1.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore


class Ui_penOptions(object):
    def setupUi(self, penOptions):
        if not penOptions.objectName():
            penOptions.setObjectName(u"penOptions")
        penOptions.resize(126, 56)
        self.verticalLayout = QVBoxLayout(penOptions)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(2, 2, 2, 2)
        self.label = QLabel(penOptions)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(8)
        font.setBold(True)
        self.label.setFont(font)

        self.verticalLayout.addWidget(self.label)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setHorizontalSpacing(2)
        self.formLayout.setVerticalSpacing(2)
        self.formLayout.setContentsMargins(5, -1, -1, -1)
        self.sizeLabel = QLabel(penOptions)
        self.sizeLabel.setObjectName(u"sizeLabel")
        font1 = QFont()
        font1.setPointSize(8)
        self.sizeLabel.setFont(font1)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.sizeLabel)

        self.sizeSlider = QSlider(penOptions)
        self.sizeSlider.setObjectName(u"sizeSlider")
        self.sizeSlider.setMinimum(1)
        self.sizeSlider.setMaximum(100)
        self.sizeSlider.setValue(5)
        self.sizeSlider.setOrientation(Qt.Horizontal)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.sizeSlider)

        self.verticalLayout.addLayout(self.formLayout)

        self.verticalSpacer = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.verticalLayout.addItem(self.verticalSpacer)

        self.retranslateUi(penOptions)

        QMetaObject.connectSlotsByName(penOptions)

    # setupUi

    def retranslateUi(self, penOptions):
        penOptions.setWindowTitle("")
        self.label.setText(QCoreApplication.translate("penOptions", u"Pen:", None))
        self.sizeLabel.setText(QCoreApplication.translate("penOptions", u"Size:", None))

    # retranslateUi
