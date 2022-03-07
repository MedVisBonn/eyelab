import logging

import requests
from PySide6 import QtWidgets

from oat import config
from oat.views.ui.ui_add_collection_dialog import Ui_AddCollectionDialog

logger = logging.getLogger(__name__)


class AddCollectionDialog(QtWidgets.QDialog, Ui_AddCollectionDialog):
    def __init__(self, patient_id, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.patient_id = patient_id

        self.buttonBox.accepted.connect(self.add_collection)
        self.buttonBox.rejected.connect(self.close)

        self.button_group = QtWidgets.QButtonGroup(self)
        self.button_group.setExclusive(True)
        self.button_group.addButton(self.od_button)
        self.button_group.addButton(self.os_button)
        self.button_group.addButton(self.na_button)

    def add_collection(self):
        laterality = self.button_group.checkedButton().text()

        data = {"name": self.nameEdit.text(), "laterality": laterality}

        data = {**{"patient_id": self.patient_id}, **data}
        # Only pseudonym is uploaded
        r = requests.post(
            f"{config.api_server}/collections/", headers=config.auth_header, json=data
        )

        if r.status_code != 200:
            print(r.json())
            try:
                QtWidgets.QMessageBox.warning(self, "Error", r.json()["detail"])
            except:
                QtWidgets.QMessageBox.warning(
                    self, "Error", "Patient could not be added to the database"
                )
            self.accept()
