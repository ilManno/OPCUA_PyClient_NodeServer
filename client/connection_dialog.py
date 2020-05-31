from pathlib import Path

from PyQt5.QtWidgets import QDialog, QFileDialog

from connection_ui import Ui_ConnectionDialog
from uawidgets.utils import trycatchslot


class ConnectionDialog(QDialog):
    def __init__(self, parent, uri):
        super().__init__()
        self.ui = Ui_ConnectionDialog()
        self.ui.setupUi(self)

        self.uaclient = parent.uaclient
        self.uri = uri
        self.parent = parent

        # Fill comboboxes
        self.query()

        self.ui.closeButton.clicked.connect(self.accept)
        self.ui.certificateButton.clicked.connect(self.get_certificate)
        self.ui.privateKeyButton.clicked.connect(self.get_private_key)

    @trycatchslot
    # Fill comboboxs
    def query(self):
        self.ui.modeComboBox.clear()
        self.ui.policyComboBox.clear()
        endpoints = self.parent.uaclient.get_endpoints(self.uri)
        modes = []
        policies = []
        for edp in endpoints:
            mode = edp.SecurityMode.name
            if mode not in modes:
                self.ui.modeComboBox.addItem(mode)
                modes.append(mode)
            policy = edp.SecurityPolicyUri.split("#")[1]
            if policy not in policies:
                self.ui.policyComboBox.addItem(policy)
                policies.append(policy)

    @property
    def security_mode(self):
        text = self.ui.modeComboBox.currentText()
        if text == "None":
            return None
        return text

    @security_mode.setter
    def security_mode(self, value):
        self.ui.modeComboBox.setCurrentText(value)

    @property
    def security_policy(self):
        text = self.ui.policyComboBox.currentText()
        if text == "None":
            return None
        return text

    @security_policy.setter
    def security_policy(self, value):
        self.ui.policyComboBox.setCurrentText(value)

    @property
    def certificate_path(self):
        return self.ui.certificateLabel.text()

    @certificate_path.setter
    def certificate_path(self, value):
        self.ui.certificateLabel.setText(value)

    @property
    def private_key_path(self):
        return self.ui.privateKeyLabel.text()

    @private_key_path.setter
    def private_key_path(self, value):
        self.ui.privateKeyLabel.setText(value)

    def get_certificate(self):
        path = QFileDialog.getOpenFileName(self, "Select certificate", self.certificate_path, "Certificate (*.der)")[0]
        if path:
            self.ui.certificateLabel.setText(Path(path).name)

    def get_private_key(self):
        path = QFileDialog.getOpenFileName(self, "Select private key", self.private_key_path, "Private key (*.pem)")[0]
        if path:
            self.ui.privateKeyLabel.setText(Path(path).name)
