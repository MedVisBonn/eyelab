from PySide6 import QtCore, QtGui, QtWidgets


class PaintPreview(QtWidgets.QGraphicsItem):
    def __init__(self, settings_widget, parent=None):
        super().__init__(parent)
        self.settings_widget = settings_widget
        self.init_preview()

    def init_preview(self):
        pass

    def boundingRect(self) -> QtCore.QRectF:
        return QtCore.QRectF(0.0, 0.0, 0.0, 0.0)

    def paint(
        self, painter: QtGui.QPainter, option: "QStyleOptionGraphicsItem", widget
    ) -> None:
        return None


class Inspection(object):
    def __init__(self):
        """ """
        self.name = "inspection"
        self.cursor = self.get_cursor()
        self.button = self.get_tool_button()
        self.hot_key = None
        self.options_widget = QtWidgets.QWidget()
        self.paint_preview = PaintPreview(self.options_widget)

    def get_tool_button(self):
        button = QtWidgets.QToolButton()
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(":/icons/icons/navigation.svg"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        button.setIcon(icon)
        button.setIconSize(QtCore.QSize(24, 24))
        button.setCheckable(True)
        button.setObjectName("inspectionButton")
        button.setToolTip("Inspection Tool")
        return button

    def enable(self):
        pass

    def disable(self):
        pass

    def get_cursor(self):
        return QtGui.QCursor(
            QtGui.QPixmap(":/cursors/cursors/navigation_cursor.svg"), hotX=0, hotY=0
        )

    @staticmethod
    def mouse_move_handler(gitem, event):
        pass

    @staticmethod
    def mouse_press_handler(gitem, event):
        pass

    @staticmethod
    def mouse_doubleclick_handler(gitem, event):
        pass

    @staticmethod
    def mouse_release_handler(gitem, event):
        pass

    @staticmethod
    def mouse_release_handler(gitem, event):
        pass

    @staticmethod
    def key_press_handler(gitem, event):
        pass

    @staticmethod
    def key_release_handler(gitem, event):
        pass
