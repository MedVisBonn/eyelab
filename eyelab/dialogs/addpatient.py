import logging

import requests
from PySide6 import QtWidgets, QtCore

from oat import config
from oat.core.security import get_local_patient_info
from oat.views.ui.ui_add_patient_dialog import Ui_AddPatientDialog

logger = logging.getLogger(__name__)


class AddPatientDialog(QtWidgets.QDialog, Ui_AddPatientDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.buttonBox.accepted.connect(self.add_patient)
        self.buttonBox.rejected.connect(self.close)

    def add_patient(self):
        pseudonym = {"pseudonym": self.pseudonymEdit.text()}

        # Only pseudonym is uploaded
        r = requests.post(
            "{}/patients/".format(config.api_server),
            headers=config.auth_header,
            json=pseudonym,
        )

        if r.status_code != 200:
            print(r.json())
            try:
                QtWidgets.QMessageBox.warning(self, "Error", r.json()["detail"])
            except:
                QtWidgets.QMessageBox.warning(
                    self, "Error", "Patient could not be added to the database"
                )
        else:
            # Save additional information to local patients file
            pd = {
                "pseudonym": self.pseudonymEdit.text(),
                "gender": self.genderBox.currentText().lower(),
                "birthday": self.birthdayEdit.date().toString(QtCore.Qt.ISODate),
            }
            patient_data = {key: pd[key] for key in pd if pd[key]}

            self.add_local_patient_info(patient_data)
            self.accept()

    def add_local_patient_info(self, patient_data: dict):
        try:
            patients_info = get_local_patient_info(
                config.local_patient_info_file, config.fernet
            )
        except Exception as e:
            raise e

        if patient_data["pseudonym"] not in patients_info.pseudonym:
            patients_info = patients_info.append(patient_data, ignore_index=True)
            with open(config.local_patient_info_file, "wb") as myfile:
                myfile.write(
                    config.fernet.encrypt(
                        patients_info.to_csv(index=False).encode("utf8")
                    )
                )
