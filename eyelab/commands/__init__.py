from PySide6.QtGui import QUndoStack

_undo_stacks = {}


def get_undo_stack(name, parent=None):
    if name in _undo_stacks:
        return _undo_stacks[name]
    else:
        _undo_stacks[name] = QUndoStack(parent)
        return _undo_stacks[name]
