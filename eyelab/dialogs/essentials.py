import logging

from PySide6 import QtWidgets, QtCore
from typing import List, Tuple

from eyelab.views.ui.ui_proceed_diaolog import Ui_ProceedDialog
from eyelab.views.ui.ui_notification_diaolog import Ui_NotificationDialog
import json

logger = logging.getLogger(__name__)


class ProceedDialog(QtWidgets.QDialog, Ui_ProceedDialog):
    def __init__(self, message, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.messageLabel.setText(message)


class NotificationDialog(QtWidgets.QDialog, Ui_NotificationDialog):
    def __init__(self, message, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.messageLabel.setText(message)
