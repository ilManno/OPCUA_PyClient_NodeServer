from pathlib import Path

from PyQt5.QtWidgets import QDialog, QFileDialog

from connection_ui import Ui_ConnectionDialog
from uawidgets.utils import trycatchslot


class ConnectionDialog(QDialog):
    def __init__(self, endpoints_dict, security_mode, security_policy, certificate_path, private_key_path):
        super().__init__()
        self.ui = Ui_ConnectionDialog()
        self.ui.setupUi(self)

        self.endpoints_dict = endpoints_dict
        self.certificate_path = certificate_path
        self.private_key_path = private_key_path

        self._init_fields(security_mode, security_policy)

        self.ui.modeComboBox.currentTextChanged.connect(self._change_policies)
        self.ui.certificateButton.clicked.connect(self.select_certificate)
        self.ui.privateKeyButton.clicked.connect(self.select_private_key)
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
            self.ui.connectButton.setEnabled(True)
        else:
            self.ui.certificateButton.setEnabled(True)
            self.ui.certificateLabel.show()
            self.ui.privateKeyButton.setEnabled(True)
            self.ui.privateKeyLabel.show()
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

    def get_selected_options(self):
        return self.ui.modeComboBox.currentText(), self.ui.policyComboBox.currentText(), self.certificate_path, self.private_key_path
