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

from eyelab.views.data_view import DataView

from . import resources_rc


class Ui_WorkspaceView(object):
    def setupUi(self, WorkspaceView):
        if not WorkspaceView.objectName():
            WorkspaceView.setObjectName(u"WorkspaceView")
        WorkspaceView.resize(856, 489)
        self.horizontalLayout = QHBoxLayout(WorkspaceView)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.data_view = DataView(WorkspaceView)
        self.data_view.setObjectName(u"data_view")
        sizePolicy = QSizePolicy(
            QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding
        )
        sizePolicy.setHorizontalStretch(200)
        sizePolicy.setVerticalStretch(200)
        sizePolicy.setHeightForWidth(self.data_view.sizePolicy().hasHeightForWidth())
        self.data_view.setSizePolicy(sizePolicy)
        self.data_view.setAutoFillBackground(False)
        self.data_view.setStyleSheet(u"")

        self.horizontalLayout.addWidget(self.data_view)

        self.layer_overview = QTabWidget(WorkspaceView)
        self.layer_overview.setObjectName(u"layer_overview")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(1)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(
            self.layer_overview.sizePolicy().hasHeightForWidth()
        )
        self.layer_overview.setSizePolicy(sizePolicy1)
        self.layer_overview.setMinimumSize(QSize(170, 250))
        self.layer_overview.setElideMode(Qt.ElideNone)

        self.horizontalLayout.addWidget(self.layer_overview)

        self.retranslateUi(WorkspaceView)

        self.layer_overview.setCurrentIndex(-1)

        QMetaObject.connectSlotsByName(WorkspaceView)

    # setupUi

    def retranslateUi(self, WorkspaceView):
        WorkspaceView.setWindowTitle(
            QCoreApplication.translate("WorkspaceView", u"Workspace", None)
        )

    # retranslateUi
