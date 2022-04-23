# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_notification_diaolog.ui'
##
## Created by: Qt User Interface Compiler version 6.1.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore


class Ui_NotificationDialog(object):
    def setupUi(self, NotificationDialog):
        if not NotificationDialog.objectName():
            NotificationDialog.setObjectName(u"NotificationDialog")
        NotificationDialog.resize(297, 136)
        self.verticalLayout = QVBoxLayout(NotificationDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.messageLabel = QLabel(NotificationDialog)
        self.messageLabel.setObjectName(u"messageLabel")
        self.messageLabel.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)
        self.messageLabel.setWordWrap(True)
        self.messageLabel.setMargin(5)

        self.verticalLayout.addWidget(self.messageLabel)

        self.buttonBox = QDialogButtonBox(NotificationDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(NotificationDialog)
        self.buttonBox.accepted.connect(NotificationDialog.accept)
        self.buttonBox.rejected.connect(NotificationDialog.reject)

        QMetaObject.connectSlotsByName(NotificationDialog)

    # setupUi

    def retranslateUi(self, NotificationDialog):
        NotificationDialog.setWindowTitle(
            QCoreApplication.translate("NotificationDialog", u"Notification", None)
        )
        self.messageLabel.setText("")

    # retranslateUi
