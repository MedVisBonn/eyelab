import logging

import eyepy as ep
from PySide6 import QtCore, QtWidgets

from eyelab.views.graphicsview import CustomGraphicsView
from eyelab.views.ui.ui_data_view import Ui_DataView

logger = logging.getLogger("eyelab.workspace.dataview")


class DataView(QtWidgets.QWidget, Ui_DataView):
    cursorPosChanged = QtCore.Signal(QtCore.QPointF, CustomGraphicsView)

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.setupUi(self)

        self.graphicsViewVolume.cursorPosChanged.connect(self.emit_volume_pos)
        self.graphicsViewLocalizer.cursorPosChanged.connect(self.emit_localizer_pos)

        self.graphicsViewLocalizer.hide()
        self.graphicsViewVolume.hide()

        self.data = None

    def set_data(self, data: ep.EyeVolume):
        logger.debug("DataView: set_data")
        self.data = data
        self.graphicsViewVolume.set_data(self.data, name="Volume")
        self.graphicsViewLocalizer.set_data(self.data.localizer, name="Enface")

        self.graphicsViewLocalizer.show()
        self.graphicsViewVolume.show()

    def emit_volume_pos(self, pos, sender):
        # The position coming from the volume is in the localizer space.
        # Since other views can only map from the localizer to their space
        # replace the sender here.
        self.cursorPosChanged.emit(pos, self.graphicsViewLocalizer)
        self.graphicsViewLocalizer.set_fake_cursor(pos)

    def emit_localizer_pos(self, pos, sender):
        self.graphicsViewVolume.set_fake_cursor(pos, sender)
        self.cursorPosChanged.emit(pos, sender)

    def set_fake_cursor(self, pos, sender):
        pos = self.graphicsViewLocalizer.map_from_sender(pos, sender)
        self.graphicsViewLocalizer.set_fake_cursor(pos, self.graphicsViewLocalizer)
        self.graphicsViewVolume.set_fake_cursor(pos, self.graphicsViewLocalizer)
