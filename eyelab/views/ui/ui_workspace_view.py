# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_workspace_view.ui'
##
## Created by: Qt User Interface Compiler version 6.1.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore

from . import resources_rc


class Ui_WorkspaceView(object):
    def setupUi(self, WorkspaceView):
        if not WorkspaceView.objectName():
            WorkspaceView.setObjectName(u"WorkspaceView")
        WorkspaceView.resize(856, 489)
        self.horizontalLayout = QHBoxLayout(WorkspaceView)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.data_widget = QWidget(WorkspaceView)
        self.data_widget.setObjectName(u"data_widget")
        sizePolicy = QSizePolicy(
            QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding
        )
        sizePolicy.setHorizontalStretch(200)
        sizePolicy.setVerticalStretch(200)
        sizePolicy.setHeightForWidth(self.data_widget.sizePolicy().hasHeightForWidth())
        self.data_widget.setSizePolicy(sizePolicy)
        self.data_widget.setAutoFillBackground(False)
        self.data_widget.setStyleSheet(u"")
        self.verticalLayout_3 = QVBoxLayout(self.data_widget)
        self.verticalLayout_3.setSpacing(2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)

        self.horizontalLayout.addWidget(self.data_widget)

        self.widget_2 = QWidget(WorkspaceView)
        self.widget_2.setObjectName(u"widget_2")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(1)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy1)
        self.verticalLayout_2 = QVBoxLayout(self.widget_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.layerOverview = QTabWidget(self.widget_2)
        self.layerOverview.setObjectName(u"layerOverview")
        sizePolicy1.setHeightForWidth(
            self.layerOverview.sizePolicy().hasHeightForWidth()
        )
        self.layerOverview.setSizePolicy(sizePolicy1)
        self.layerOverview.setMinimumSize(QSize(170, 250))
        self.layerOverview.setElideMode(Qt.ElideNone)

        self.verticalLayout_2.addWidget(self.layerOverview)

        self.horizontalLayout.addWidget(self.widget_2)

        self.retranslateUi(WorkspaceView)

        self.layerOverview.setCurrentIndex(-1)

        QMetaObject.connectSlotsByName(WorkspaceView)

    # setupUi

    def retranslateUi(self, WorkspaceView):
        WorkspaceView.setWindowTitle(
            QCoreApplication.translate("WorkspaceView", u"Workspace", None)
        )

    # retranslateUi
