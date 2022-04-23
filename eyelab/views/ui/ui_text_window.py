# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_text_window.ui'
##
## Created by: Qt User Interface Compiler version 6.1.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore


class Ui_TextWindow(object):
    def setupUi(self, TextWindow):
        if not TextWindow.objectName():
            TextWindow.setObjectName(u"TextWindow")
        TextWindow.resize(400, 300)
        self.horizontalLayout = QHBoxLayout(TextWindow)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.textEdit = QTextEdit(TextWindow)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setReadOnly(True)

        self.horizontalLayout.addWidget(self.textEdit)

        self.retranslateUi(TextWindow)

        QMetaObject.connectSlotsByName(TextWindow)

    # setupUi

    def retranslateUi(self, TextWindow):
        TextWindow.setWindowTitle(
            QCoreApplication.translate("TextWindow", u"Help", None)
        )
        self.textEdit.setHtml(
            QCoreApplication.translate(
                "TextWindow",
                u'<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">\n'
                '<html><head><meta name="qrichtext" content="1" /><style type="text/css">\n'
                "p, li { white-space: pre-wrap; }\n"
                "</style></head><body style=\" font-family:'Ubuntu'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
                '<p style="-qt-paragraph-type:empty; margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><br /></p></body></html>',
                None,
            )
        )

    # retranslateUi
