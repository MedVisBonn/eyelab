from PySide6 import QtGui, QtWidgets, QtCore, Qt
from eyelab.views.ui.ui_spline_options import Ui_splineOptions

# from oat.modules.annotation.models.treeview.lineitem import TreeLineItemBase


class SplineWidget(QtWidgets.QWidget, Ui_splineOptions):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        # self.showCheckBox.setChecked()
        self.showCheckBox.stateChanged.connect(self.change_controlpoints)

    def change_controlpoints(self):
        scenetab = self.parentWidget().parentWidget()
        model_index = scenetab.ImageTreeView.selectionModel().currentIndex()
        item = scenetab.model.getItem(model_index)
        if self.showCheckBox.isChecked():
            item.show_control_points()
        else:
            item.hide_control_points()


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


class Spline(object):
    def __init__(self):
        """ """
        self.name = "spline"
        self.cursor = self.get_cursor()
        self.button = self.get_tool_button()
        self.hot_key = None
        self.options_widget = self.get_options_widget()
        self.paint_preview = PaintPreview(self.options_widget)

    def get_options_widget(self):
        widget = SplineWidget()
        return widget

    def enable(self):
        pass

    def disable(self):
        pass

    def get_tool_button(self):
        button = QtWidgets.QToolButton()
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(":/icons/icons/path-tool.svg"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        button.setIcon(icon)
        button.setIconSize(QtCore.QSize(24, 24))
        button.setCheckable(True)
        button.setObjectName("inspectionButton")
        button.setToolTip("Curve Tool")
        return button

    def get_cursor(self):
        return QtGui.QCursor(
            QtGui.QPixmap(":/cursors/cursors/path_cursor.svg"), hotX=0, hotY=0
        )

    def mouse_move_handler(self, gitem, event):
        pass

    def mouse_press_handler(self, gitem, event):
        pass

    def mouse_doubleclick_handler(self, gitem, event):
        pos = gitem.mapToScene(event.pos())
        gitem.add_knot(pos)

    def mouse_release_handler(self, gitem, event):
        pass

    def mouse_release_handler(self, gitem, event):
        pass

    def key_press_handler(self, gitem, event):
        pass

    def key_release_handler(self, gitem, event):
        pass
