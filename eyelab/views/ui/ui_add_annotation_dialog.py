# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_add_annotation_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.1.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore

from . import resources_rc


class Ui_AddAnnotationDialog(object):
    def setupUi(self, AddAnnotationDialog):
        if not AddAnnotationDialog.objectName():
            AddAnnotationDialog.setObjectName(u"AddAnnotationDialog")
        AddAnnotationDialog.resize(400, 112)
        self.verticalLayout = QVBoxLayout(AddAnnotationDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.nameLabel = QLabel(AddAnnotationDialog)
        self.nameLabel.setObjectName(u"nameLabel")
        font = QFont()
        font.setBold(True)
        self.nameLabel.setFont(font)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.nameLabel)

        self.nameEdit = QLineEdit(AddAnnotationDialog)
        self.nameEdit.setObjectName(u"nameEdit")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.nameEdit)

        self.typeLabel = QLabel(AddAnnotationDialog)
        self.typeLabel.setObjectName(u"typeLabel")
        self.typeLabel.setFont(font)

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.typeLabel)

        self.typeBox = QComboBox(AddAnnotationDialog)
        self.typeBox.setObjectName(u"typeBox")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.typeBox)

        self.verticalLayout.addLayout(self.formLayout)

        self.buttonBox = QDialogButtonBox(AddAnnotationDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setEnabled(True)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)

        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(AddAnnotationDialog)
        self.buttonBox.accepted.connect(AddAnnotationDialog.accept)
        self.buttonBox.rejected.connect(AddAnnotationDialog.reject)

        QMetaObject.connectSlotsByName(AddAnnotationDialog)

    # setupUi

    def retranslateUi(self, AddAnnotationDialog):
        AddAnnotationDialog.setWindowTitle(
            QCoreApplication.translate("AddAnnotationDialog", u"Dialog", None)
        )
        self.nameLabel.setText(
            QCoreApplication.translate("AddAnnotationDialog", u"Name:", None)
        )
        self.nameEdit.setText(
            QCoreApplication.translate("AddAnnotationDialog", u"New Annotation", None)
        )
        self.typeLabel.setText(
            QCoreApplication.translate("AddAnnotationDialog", u"Type:", None)
        )

    # retranslateUi
