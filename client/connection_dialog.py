from PyQt5.QtWidgets import QDialog, QFileDialog

from connection_ui import Ui_ConnectionDialog
from uawidgets.utils import trycatchslot


class ConnectionDialog(QDialog):
    def __init__(self, parent, endpoints, security_policy, security_mode, certificate_path, private_key_path):
        super().__init__()
        self.ui = Ui_ConnectionDialog()
        self.ui.setupUi(self)

        self.uaclient = parent.uaclient
        self.parent = parent

        # Fill comboboxes
        self.fill_fields(endpoints, security_policy, security_mode, certificate_path, private_key_path)

        self.ui.closeButton.clicked.connect(self.accept)
        self.ui.certificateButton.clicked.connect(self.get_certificate)
        self.ui.privateKeyButton.clicked.connect(self.get_private_key)

    @trycatchslot
    # Fill comboboxes
    def fill_fields(self, endpoints, security_policy, security_mode, certificate_path, private_key_path):
        self.ui.modeComboBox.clear()
        self.ui.policyComboBox.clear()
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
        self.ui.policyComboBox.setCurrentText(security_policy)
        self.ui.modeComboBox.setCurrentText(security_mode)
        self.ui.certificateLabel.setText(certificate_path)
        self.ui.privateKeyLabel.setText(private_key_path)

    def get_selected_options(self):
        return self.ui.policyComboBox.currentText(), self.ui.modeComboBox.currentText(), self.ui.certificateLabel.text(), self.ui.privateKeyLabel.text()

    def get_certificate(self):
        path = QFileDialog.getOpenFileName(self, "Select certificate", self.certificate_path, "Certificate (*.der)")[0]
        if path:
            self.ui.certificateLabel.setText(path)

    def get_private_key(self):
        path = QFileDialog.getOpenFileName(self, "Select private key", self.private_key_path, "Private key (*.pem)")[0]
        if path:
            self.ui.privateKeyLabel.setText(path)
