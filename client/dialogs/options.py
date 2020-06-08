from pathlib import Path
import subprocess

from PyQt5.QtWidgets import QDialog, QFileDialog, QMessageBox

from dialogs.options_ui import Ui_OptionsDialog
from utils import trycatchslot


class OptionsDialog(QDialog):
    def __init__(self, endpoints_dict, security_mode, security_policy, certificate_path, private_key_path):
        super().__init__()
        self.ui = Ui_OptionsDialog()
        self.ui.setupUi(self)

        self.endpoints_dict = endpoints_dict
        self.certificate_path = certificate_path
        self.private_key_path = private_key_path

        self._init_fields(security_mode, security_policy)

        self.ui.modeComboBox.currentTextChanged.connect(self._change_policies)
        self.ui.certificateButton.clicked.connect(self.select_certificate)
        self.ui.privateKeyButton.clicked.connect(self.select_private_key)
        self.ui.generateButton.clicked.connect(self.generate_certificate)
        self.ui.connectButton.clicked.connect(self.accept)
        self.ui.cancelButton.clicked.connect(self.reject)

    @trycatchslot
    def _init_fields(self, security_mode, security_policy):
        self.ui.modeComboBox.clear()
        self.ui.policyComboBox.clear()

        self.ui.modeComboBox.addItems(self.endpoints_dict.keys())
        self.ui.modeComboBox.setCurrentText(security_mode)
        current_mode = self.ui.modeComboBox.currentText()
        self.ui.policyComboBox.addItems(self.endpoints_dict[current_mode])
        self.ui.policyComboBox.setCurrentText(security_policy)

        self.ui.certificateLabel.setText(Path(self.certificate_path).name)
        self.ui.privateKeyLabel.setText(Path(self.private_key_path).name)

        self._toggle_security_fields(current_mode)

    def _change_policies(self, mode):
        self.ui.policyComboBox.clear()
        self.ui.policyComboBox.addItems(self.endpoints_dict[mode])
        self._toggle_security_fields(mode)

    def _toggle_security_fields(self, mode):
        if mode == "None_":
            self.ui.certificateButton.setEnabled(False)
            self.ui.certificateLabel.hide()
            self.ui.privateKeyButton.setEnabled(False)
            self.ui.privateKeyLabel.hide()
            self.ui.generateButton.setEnabled(False)
            self.ui.connectButton.setEnabled(True)
        else:
            self.ui.certificateButton.setEnabled(True)
            self.ui.certificateLabel.show()
            self.ui.privateKeyButton.setEnabled(True)
            self.ui.privateKeyLabel.show()
            self.ui.generateButton.setEnabled(True)
            if self.certificate_path and self.private_key_path:
                self.ui.connectButton.setEnabled(True)
            else:
                self.ui.connectButton.setEnabled(False)

    def select_certificate(self):
        path = QFileDialog.getOpenFileName(self, "Select certificate", self.certificate_path, "Certificate (*.der)")[0]
        if path:
            self.certificate_path = path
            self.ui.certificateLabel.setText(Path(path).name)
            if self.private_key_path:
                self.ui.connectButton.setEnabled(True)

    def select_private_key(self):
        path = QFileDialog.getOpenFileName(self, "Select private key", self.private_key_path, "Private key (*.pem)")[0]
        if path:
            self.private_key_path = path
            self.ui.privateKeyLabel.setText(Path(path).name)
            if self.certificate_path:
                self.ui.connectButton.setEnabled(True)

    def generate_certificate(self):
        private_key_path = QFileDialog.getSaveFileName(self, "Save private key file", "my_private_key.pem", "Private key (*.pem)")[0]
        if private_key_path:
            private_key_ext = Path(private_key_path).suffix
            if private_key_ext != ".pem":
                private_key_path += ".pem"
            path = Path(private_key_path).parent
            certificate_path = QFileDialog.getSaveFileName(self, "Save certificate file", str(path.joinpath("my_cert.der")), "Certificate (*.der)")[0]
            if certificate_path:
                certificate_ext = Path(certificate_path).suffix
                if certificate_ext != ".der":
                    certificate_path += ".der"
                return_code = subprocess.call(
                    f"""openssl req -x509 -newkey rsa:2048 \
                    -keyout {private_key_path} -nodes \
                    -outform der -out {certificate_path} \
                    -subj '/C=IT/ST=Catania/O=UniCT' \
                    -addext 'subjectAltName = URI:urn:example.org:OpcUa:python-client'""",
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
                )
                if return_code == 0:
                    QMessageBox.information(self, "Success", "Certificate generated successfully")
                    self.certificate_path = certificate_path
                    self.ui.certificateLabel.setText(Path(certificate_path).name)
                    self.private_key_path = private_key_path
                    self.ui.privateKeyLabel.setText(Path(private_key_path).name)
                    self.ui.connectButton.setEnabled(True)
                else:
                    QMessageBox.warning(self, "Error", "Unable to generate certificate")

    def get_selected_options(self):
        return self.ui.modeComboBox.currentText(), self.ui.policyComboBox.currentText(), self.certificate_path, self.private_key_path
