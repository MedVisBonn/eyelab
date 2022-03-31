# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_layer_entry.ui'
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
    Qt,
    QTime,
    QUrl,
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
    QApplication,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QToolButton,
    QWidget,
)

from . import resources_rc


class Ui_LayerEntry(object):
    def setupUi(self, LayerEntry):
        if not LayerEntry.objectName():
            LayerEntry.setObjectName(u"LayerEntry")
        LayerEntry.resize(150, 30)
        LayerEntry.setMinimumSize(QSize(150, 30))
        LayerEntry.setMaximumSize(QSize(300, 30))
        LayerEntry.setContextMenuPolicy(Qt.ActionsContextMenu)
        LayerEntry.setAutoFillBackground(False)
        LayerEntry.setStyleSheet(u"background-color: white")
        self.horizontalLayout = QHBoxLayout(LayerEntry)
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(2, 2, 2, 2)
        self.hideButton = QToolButton(LayerEntry)
        self.hideButton.setObjectName(u"hideButton")
        self.hideButton.setMinimumSize(QSize(26, 26))
        self.hideButton.setMaximumSize(QSize(26, 26))
        self.hideButton.setContextMenuPolicy(Qt.NoContextMenu)
        self.hideButton.setStyleSheet(u"background-color: white")
        icon = QIcon()
        icon.addFile(
            u":/icons/icons/baseline-visibility-24px.svg",
            QSize(),
            QIcon.Normal,
            QIcon.Off,
        )
        self.hideButton.setIcon(icon)
        self.hideButton.setIconSize(QSize(24, 24))

        self.horizontalLayout.addWidget(self.hideButton)

        self.colorButton = QToolButton(LayerEntry)
        self.colorButton.setObjectName(u"colorButton")
        self.colorButton.setMinimumSize(QSize(26, 26))
        self.colorButton.setContextMenuPolicy(Qt.NoContextMenu)
        self.colorButton.setAutoFillBackground(False)
        self.colorButton.setStyleSheet(u"background-color: white")

        self.horizontalLayout.addWidget(self.colorButton)

        self.label = QLabel(LayerEntry)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(8)
        self.label.setFont(font)
        self.label.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.label.setAutoFillBackground(False)
        self.label.setStyleSheet(u"")
        self.label.setScaledContents(False)
        self.label.setWordWrap(False)

        self.horizontalLayout.addWidget(self.label)

        self.retranslateUi(LayerEntry)

        QMetaObject.connectSlotsByName(LayerEntry)

    # setupUi

    def retranslateUi(self, LayerEntry):
        LayerEntry.setWindowTitle(
            QCoreApplication.translate("LayerEntry", u"Form", None)
        )
        self.hideButton.setText(QCoreApplication.translate("LayerEntry", u"...", None))
        self.colorButton.setText("")
        self.label.setText(
            QCoreApplication.translate("LayerEntry", u"Layer Name", None)
        )

    # retranslateUi
