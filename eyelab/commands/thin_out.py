import logging

import eyepy as ep
import numpy as np
from PySide6.QtGui import QUndoCommand

logger = logging.getLogger(__name__)


class ThinOut(QUndoCommand):
    def __init__(self, data: ep.EyeVolume, n, region=(0, 1), parent=None):
        self.data = data
        self.indices = self._get_sparse_indices(n, region)
        self.old_disabled = [m["disabled"] for m in self.data.meta["bscan_meta"]]
        self.disabled = self._get_disabled()

        super().__init__(parent)
        self.setText("Thin out volume")

    def _get_sparse_indices(self, n, region=(0, 1)):
        n_bscans = len(self.data)

        start_index = int(round(region[0] * n_bscans))
        stop_index = int(round(region[1] * n_bscans))
        indices = np.rint(np.linspace(start_index, stop_index, n)).astype(int)
        return indices

    def _get_disabled(self):
        n_bscans = len(self.data.meta["bscan_meta"])
        disabled = [True for _ in range(n_bscans)]

        for i in self.indices:
            disabled[i] = False

        return disabled

    def redo(self):
        logger.debug(f"Redo: {self.text()}")
        for i, bscan in enumerate(self.data.meta["bscan_meta"]):
            bscan["disabled"] = self.disabled[i]

    def undo(self):
        logger.debug(f"Undo: {self.text()}")
        for i, bscan in enumerate(self.data.meta["bscan_meta"]):
            bscan["disabled"] = self.old_disabled[i]
