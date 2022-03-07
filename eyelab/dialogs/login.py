import logging
from pathlib import Path

import pandas as pd
import requests
from PySide6 import QtWidgets, QtCore

from oat import config
from oat.core.security import get_fernet
from oat.views.ui.ui_login_dialog import Ui_LoginDialog

logger = logging.getLogger(__name__)


class LoginDialog(QtWidgets.QDialog, Ui_LoginDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        logger.info("Login dialog initialization.")
        _translate = QtCore.QCoreApplication.translate

        self.db_dict = {
            "Default DB": "http://localhost/api/v1",
            "UKB": "http://131.220.28.177/api/v1",
            "Informatik": "http://demeljoch/api/v1",
        }

        self.setupUi(self)

        for i, key in enumerate(self.db_dict.keys()):
            self.dbDropdown.addItem(key)

        self.buttonBox.accepted.connect(self.handleLogin)
        self.buttonBox.rejected.connect(self.close)

    def handleLogin(self):
        # query selected DB for user:
        db_key = self.dbDropdown.currentText()
        try:
            api_server = self.db_dict[db_key]
        except:
            api_server = "http://" + db_key + "/api/v1"

        login_data = {
            "username": self.username.text(),
            "password": self.password.text(),
        }

        # login_data = {
        #    "username": "oli4morelle@gmail.com",
        #    "password": "testpw",
        # }

        r = requests.post(f"{api_server}/login/access-token", data=login_data)

        if r.status_code != 200:
            msg = "Wrong username or password"
            logger.warning(msg)
            QtWidgets.QMessageBox.warning(self, "Error", msg)
        else:
            response = r.json()
            auth_token = response["access_token"]
            config.auth_header = {"Authorization": f"Bearer {auth_token}"}
            logging.info("Authentication token received")
            config.api_server = api_server
            config.local_patient_info_file = (
                Path.home() / ".oat" / f"{login_data['username']}_patients.csv"
            )
            config.fernet = get_fernet(login_data["password"])

            # Create local patients info if not existing
            if not config.local_patient_info_file.exists():
                columns = ["pseudonym"]
                patients_info = pd.DataFrame(columns=columns)
                with open(config.local_patient_info_file, "wb") as myfile:
                    myfile.write(
                        config.fernet.encrypt(
                            patients_info.to_csv(index=False).encode("utf8")
                        )
                    )
                logging.info(
                    f"Local patient info created for user " f"{login_data['username']}"
                )

            self.accept()
