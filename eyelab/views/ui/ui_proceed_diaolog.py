# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_proceed_diaolog.ui'
##
## Created by: Qt User Interface Compiler version 6.2.4
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
from PySide6.QtWidgets import (
    QAbstractButton,
    QApplication,
    QDialog,
    QDialogButtonBox,
    QLabel,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


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
