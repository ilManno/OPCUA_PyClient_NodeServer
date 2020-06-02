from PyQt5.QtWidgets import QDialog, QFileDialog

from connection_ui import Ui_ConnectionDialog
from uawidgets.utils import trycatchslot


class ConnectionDialog(QDialog):
    def __init__(self, parent, endpoints_dict, security_mode, security_policy, certificate_path, private_key_path):
        super().__init__()
        self.ui = Ui_ConnectionDialog()
        self.ui.setupUi(self)

        self.uaclient = parent.uaclient
        self.parent = parent

        self.endpoints_dict = endpoints_dict

        # Fill comboboxes
        self._init_fields(security_mode, security_policy, certificate_path, private_key_path)
        self.ui.modeComboBox.currentTextChanged.connect(self._change_policies)

        self.ui.closeButton.clicked.connect(self.accept)
        self.ui.certificateButton.clicked.connect(self.select_certificate)
        self.ui.privateKeyButton.clicked.connect(self.select_private_key)

    @trycatchslot
    # Fill comboboxes
    def _init_fields(self, security_mode, security_policy, certificate_path, private_key_path):
        self.ui.modeComboBox.clear()
        self.ui.policyComboBox.clear()

        self.ui.modeComboBox.addItems(self.endpoints_dict.keys())
        self.ui.modeComboBox.setCurrentText(security_mode)
        current_mode = self.ui.modeComboBox.currentText()
        self.ui.policyComboBox.addItems(self.endpoints_dict[current_mode])
        self.ui.policyComboBox.setCurrentText(security_policy)

        self._toggle_security_fields(current_mode)

        self.ui.certificateLabel.setText(certificate_path)
        self.ui.privateKeyLabel.setText(private_key_path)

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
        else:
            self.ui.certificateButton.setEnabled(True)
            self.ui.certificateLabel.show()
            self.ui.privateKeyButton.setEnabled(True)
            self.ui.privateKeyLabel.show()

    def get_selected_options(self):
        return self.ui.modeComboBox.currentText(), self.ui.policyComboBox.currentText(), self.ui.certificateLabel.text(), self.ui.privateKeyLabel.text()

    def select_certificate(self):
        path = QFileDialog.getOpenFileName(self, "Select certificate", self.ui.certificateLabel.text(), "Certificate (*.der)")[0]
        if path:
            self.ui.certificateLabel.setText(path)

    def select_private_key(self):
        path = QFileDialog.getOpenFileName(self, "Select private key", self.ui.privateKeyLabel.text(), "Private key (*.pem)")[0]
        if path:
            self.ui.privateKeyLabel.setText(path)
