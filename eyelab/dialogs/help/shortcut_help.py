from eyelab.dialogs.help.help_dialog import HelpWindow

help_text = """
# Shortcut Sheet

## Annotation

+ Ctrl + X: toggle linked navigation
"""


class ShortcutHelp(HelpWindow):
    def __init__(self, parent):
        super().__init__(help_text, parent)
