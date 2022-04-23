# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_scene_tab.ui'
##
## Created by: Qt User Interface Compiler version 6.1.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore

from . import resources_rc


class Ui_SceneTab(object):
    def setupUi(self, SceneTab):
        if not SceneTab.objectName():
            SceneTab.setObjectName(u"SceneTab")
        SceneTab.resize(166, 386)
        self.verticalLayout = QVBoxLayout(SceneTab)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.opacityLayout = QHBoxLayout()
        self.opacityLayout.setObjectName(u"opacityLayout")
        self.opacitySliderLabel = QLabel(SceneTab)
        self.opacitySliderLabel.setObjectName(u"opacitySliderLabel")
        font = QFont()
        font.setPointSize(7)
        font.setBold(True)
        self.opacitySliderLabel.setFont(font)

        self.opacityLayout.addWidget(self.opacitySliderLabel)

        self.opacitySlider = QSlider(SceneTab)
        self.opacitySlider.setObjectName(u"opacitySlider")
        self.opacitySlider.setMaximum(100)
        self.opacitySlider.setPageStep(10)
        self.opacitySlider.setValue(100)
        self.opacitySlider.setSliderPosition(100)
        self.opacitySlider.setOrientation(Qt.Horizontal)
        self.opacitySlider.setInvertedAppearance(False)
        self.opacitySlider.setInvertedControls(False)

        self.opacityLayout.addWidget(self.opacitySlider)

        self.verticalLayout.addLayout(self.opacityLayout)

        self.imageTreeView = QTreeView(SceneTab)
        self.imageTreeView.setObjectName(u"imageTreeView")
        self.imageTreeView.setSelectionMode(QAbstractItemView.SingleSelection)
        self.imageTreeView.setIndentation(5)

        self.verticalLayout.addWidget(self.imageTreeView)

        self.buttonsLayout = QHBoxLayout()
        self.buttonsLayout.setObjectName(u"buttonsLayout")
        self.addButton = QToolButton(SceneTab)
        self.addButton.setObjectName(u"addButton")
        icon = QIcon()
        icon.addFile(
            u":/icons/icons/baseline-add_circle-24px.svg",
            QSize(),
            QIcon.Normal,
            QIcon.Off,
        )
        self.addButton.setIcon(icon)
        self.addButton.setIconSize(QSize(24, 24))

        self.buttonsLayout.addWidget(self.addButton)

        self.upButton = QToolButton(SceneTab)
        self.upButton.setObjectName(u"upButton")
        self.upButton.setEnabled(True)
        icon1 = QIcon()
        icon1.addFile(
            u":/icons/icons/baseline-arrow_upward-24px.svg",
            QSize(),
            QIcon.Normal,
            QIcon.Off,
        )
        self.upButton.setIcon(icon1)
        self.upButton.setIconSize(QSize(24, 24))

        self.buttonsLayout.addWidget(self.upButton)

        self.downButton = QToolButton(SceneTab)
        self.downButton.setObjectName(u"downButton")
        icon2 = QIcon()
        icon2.addFile(
            u":/icons/icons/baseline-arrow_downward-24px.svg",
            QSize(),
            QIcon.Normal,
            QIcon.Off,
        )
        self.downButton.setIcon(icon2)
        self.downButton.setIconSize(QSize(24, 24))

        self.buttonsLayout.addWidget(self.downButton)

        self.deleteButton = QToolButton(SceneTab)
        self.deleteButton.setObjectName(u"deleteButton")
        icon3 = QIcon()
        icon3.addFile(
            u":/icons/icons/baseline-delete-24px.svg", QSize(), QIcon.Normal, QIcon.Off
        )
        self.deleteButton.setIcon(icon3)
        self.deleteButton.setIconSize(QSize(24, 24))

        self.buttonsLayout.addWidget(self.deleteButton)

        self.verticalLayout.addLayout(self.buttonsLayout)

        self.line = QFrame(SceneTab)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.toolboxWidget = QWidget(SceneTab)
        self.toolboxWidget.setObjectName(u"toolboxWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(100)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.toolboxWidget.sizePolicy().hasHeightForWidth()
        )
        self.toolboxWidget.setSizePolicy(sizePolicy)
        self.verticalLayout_7 = QVBoxLayout(self.toolboxWidget)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.toolsLabel = QLabel(self.toolboxWidget)
        self.toolsLabel.setObjectName(u"toolsLabel")
        self.toolsLabel.setMinimumSize(QSize(0, 0))
        font1 = QFont()
        font1.setPointSize(10)
        font1.setBold(True)
        self.toolsLabel.setFont(font1)
        self.toolsLabel.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)

        self.verticalLayout_7.addWidget(self.toolsLabel)

        self.toolsWidget = QWidget(self.toolboxWidget)
        self.toolsWidget.setObjectName(u"toolsWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.toolsWidget.sizePolicy().hasHeightForWidth())
        self.toolsWidget.setSizePolicy(sizePolicy1)
        self.gridLayout = QGridLayout(self.toolsWidget)
        self.gridLayout.setObjectName(u"gridLayout")

        self.verticalLayout_7.addWidget(self.toolsWidget)

        self.line_2 = QFrame(self.toolboxWidget)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_7.addWidget(self.line_2)

        self.optionsLabel = QLabel(self.toolboxWidget)
        self.optionsLabel.setObjectName(u"optionsLabel")
        self.optionsLabel.setMinimumSize(QSize(0, 0))
        self.optionsLabel.setFont(font1)
        self.optionsLabel.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)

        self.verticalLayout_7.addWidget(self.optionsLabel)

        self.optionsWidget = QWidget(self.toolboxWidget)
        self.optionsWidget.setObjectName(u"optionsWidget")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(1)
        sizePolicy2.setHeightForWidth(
            self.optionsWidget.sizePolicy().hasHeightForWidth()
        )
        self.optionsWidget.setSizePolicy(sizePolicy2)
        self.verticalLayout_2 = QVBoxLayout(self.optionsWidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")

        self.verticalLayout_7.addWidget(self.optionsWidget)

        self.verticalLayout.addWidget(self.toolboxWidget)

        self.verticalSpacer = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.verticalLayout.addItem(self.verticalSpacer)

        self.retranslateUi(SceneTab)

        QMetaObject.connectSlotsByName(SceneTab)

    # setupUi

    def retranslateUi(self, SceneTab):
        SceneTab.setWindowTitle(QCoreApplication.translate("SceneTab", u"Form", None))
        self.opacitySliderLabel.setText(
            QCoreApplication.translate("SceneTab", u"Opacity", None)
        )
        # if QT_CONFIG(tooltip)
        self.opacitySlider.setToolTip(
            QCoreApplication.translate(
                "SceneTab", u"Change the opacity for all annotations", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(tooltip)
        self.addButton.setToolTip(
            QCoreApplication.translate("SceneTab", u"Add new Annotation Layers", None)
        )
        # endif // QT_CONFIG(tooltip)
        self.addButton.setText(QCoreApplication.translate("SceneTab", u"...", None))
        # if QT_CONFIG(tooltip)
        self.upButton.setToolTip(
            QCoreApplication.translate("SceneTab", u"Move selected layer up", None)
        )
        # endif // QT_CONFIG(tooltip)
        self.upButton.setText(QCoreApplication.translate("SceneTab", u"...", None))
        # if QT_CONFIG(tooltip)
        self.downButton.setToolTip(
            QCoreApplication.translate("SceneTab", u"Move selected layer down", None)
        )
        # endif // QT_CONFIG(tooltip)
        self.downButton.setText(QCoreApplication.translate("SceneTab", u"...", None))
        # if QT_CONFIG(tooltip)
        self.deleteButton.setToolTip(
            QCoreApplication.translate("SceneTab", u"Delete selected layer", None)
        )
        # endif // QT_CONFIG(tooltip)
        self.deleteButton.setText(QCoreApplication.translate("SceneTab", u"...", None))
        self.toolsLabel.setText(QCoreApplication.translate("SceneTab", u"Tools:", None))
        self.optionsLabel.setText(
            QCoreApplication.translate("SceneTab", u"Options:", None)
        )

    # retranslateUi
