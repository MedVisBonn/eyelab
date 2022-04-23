# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_proceed_diaolog.ui'
##
## Created by: Qt User Interface Compiler version 6.1.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore


class Ui_ProceedDialog(object):
    def setupUi(self, ProceedDialog):
        if not ProceedDialog.objectName():
            ProceedDialog.setObjectName(u"ProceedDialog")
        ProceedDialog.resize(297, 136)
        self.verticalLayout = QVBoxLayout(ProceedDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.messageLabel = QLabel(ProceedDialog)
        self.messageLabel.setObjectName(u"messageLabel")
        self.messageLabel.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)
        self.messageLabel.setWordWrap(True)
        self.messageLabel.setMargin(5)

        self.verticalLayout.addWidget(self.messageLabel)

        self.buttonBox = QDialogButtonBox(ProceedDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.No | QDialogButtonBox.Yes)

        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(ProceedDialog)
        self.buttonBox.accepted.connect(ProceedDialog.accept)
        self.buttonBox.rejected.connect(ProceedDialog.reject)

        QMetaObject.connectSlotsByName(ProceedDialog)

    # setupUi

    def retranslateUi(self, ProceedDialog):
        ProceedDialog.setWindowTitle(
            QCoreApplication.translate("ProceedDialog", u"Notification", None)
        )
        self.messageLabel.setText("")

    # retranslateUi
