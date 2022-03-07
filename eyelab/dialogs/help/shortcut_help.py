from oat.modules.dialogs.help.help_dialog import HelpWindow

help_text = """
# Shortcut Sheet

## Annotation

+ Ctrl + X: toggle linked navigation
+ Ctrl + A: toggle all annotations
+ Ctrl + 1: switch to tool 1 (always inspection)
+ Ctrl + 2: switch to tool 2 (depends on current annotation type)

## Registration

### Feature table navigation
+ W: Last feature pair (one row up)
+ S: Next feature pair (one row down)
+ A: Last feature (previous column)
+ D: Next feature (next column)
"""


class ShortcutHelp(HelpWindow):
    def __init__(self, parent):
        super().__init__(help_text, parent)
