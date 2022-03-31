from PySide6 import QtWidgets

from eyelab.views.ui.ui_text_window import Ui_TextWindow


class HelpWindow(QtWidgets.QDialog, Ui_TextWindow):
    def __init__(self, md_str, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.textEdit.setMarkdown(md_str)
