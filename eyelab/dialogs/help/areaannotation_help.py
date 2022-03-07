from oat.modules.dialogs.help.help_dialog import HelpWindow

help_text = """
# Area Annotation Guide
"""


class AreaAnnotationHelp(HelpWindow):
    def __init__(self, parent):
        super().__init__(help_text, parent)
