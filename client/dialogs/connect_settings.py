from pathlib import Path
import subprocess

from PyQt5.QtCore import Qt, QItemSelection, QSignalBlocker
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QBrush, QColor
from PyQt5.QtWidgets import QDialog, QFileDialog, QMessageBox

from dialogs.connect_settings_ui import Ui_ConnectSettingsDialog
from utils import trycatchslot


class ConnectSettingsDialog(QDialog):
    def __init__(self, endpoints, security_mode, security_policy, certificate_path, private_key_path):
        super().__init__()
        self.ui = Ui_ConnectSettingsDialog()
        self.ui.setupUi(self)

        self.endpoints_model = QStandardItemModel()
        self.ui.endpointsView.setModel(self.endpoints_model)
        self.endpoints_model.setHorizontalHeaderLabels(["Endpoint URL", "Security Mode", "Security Policy", "Transport Profile URI"])
        self.ui.endpointsView.setColumnWidth(0, 300)
        self.ui.endpointsView.selectionModel().selectionChanged.connect(self.select_security)

        # Dict of endpoints with security modes as keys and security policies as values
        self.endpoints_dict = {"None": [], "Sign": [], "SignAndEncrypt": []}
        self.certificate_path = certificate_path
        self.private_key_path = private_key_path

        self._init_fields(endpoints, security_mode, security_policy)

        self.ui.modeComboBox.currentTextChanged.connect(self._change_policies)
        self.ui.policyComboBox.currentTextChanged.connect(self._select_endpoint)
        self.ui.certificateButton.clicked.connect(self.select_certificate)
        self.ui.privateKeyButton.clicked.connect(self.select_private_key)
        self.ui.generateButton.clicked.connect(self.generate_certificate)
        self.ui.connectButton.clicked.connect(self.accept)
        self.ui.cancelButton.clicked.connect(self.reject)

    @trycatchslot
    def _init_fields(self, endpoints, security_mode, security_policy):
        for edp in endpoints:
            mode = edp.SecurityMode.name
            if mode == "None_":
                mode = "None"
            policy = edp.SecurityPolicyUri.split("#")[1]
            transport_profile = edp.TransportProfileUri
            row = [QStandardItem(edp.EndpointUrl), QStandardItem(mode), QStandardItem(policy), QStandardItem(transport_profile)]
            if transport_profile == "http://opcfoundation.org/UA-Profile/Transport/uatcp-uasc-uabinary":
                # Endpoint supported
                self.endpoints_dict[mode].append(policy)
            else:
                # Endpoint not supported
                for col in row:
                    col.setData(QBrush(QColor(255, 183, 183)), Qt.BackgroundRole)
            self.endpoints_model.appendRow(row)

        self.ui.modeComboBox.clear()
        self.ui.policyComboBox.clear()

        self.ui.modeComboBox.addItems(self.endpoints_dict.keys())
        self.ui.modeComboBox.setCurrentText(security_mode)
        current_mode = self.ui.modeComboBox.currentText()
        self.ui.policyComboBox.addItems(self.endpoints_dict[current_mode])
        self.ui.policyComboBox.setCurrentText(security_policy)

        self._select_endpoint(security_policy)

        self.ui.certificateLabel.setText(Path(self.certificate_path).name)
        self.ui.privateKeyLabel.setText(Path(self.private_key_path).name)

        self._toggle_security_fields(current_mode)

    def _change_policies(self, mode):
        self.ui.policyComboBox.clear()
        self.ui.policyComboBox.addItems(self.endpoints_dict[mode])
        self._toggle_security_fields(mode)

    def _toggle_security_fields(self, mode):
        if mode == "None":
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

    def _select_endpoint(self, policy):
        if policy:
            mode = self.ui.modeComboBox.currentText()
            # Get indices of supported endpoints
            idxlist = self.endpoints_model.match(self.endpoints_model.index(0, 3), Qt.DisplayRole, "http://opcfoundation.org/UA-Profile/Transport/uatcp-uasc-uabinary", -1, Qt.MatchExactly)
            for idx in idxlist:
                if self.endpoints_model.data(idx.siblingAtColumn(1)) == mode and self.endpoints_model.data(idx.siblingAtColumn(2)) == policy and idx.row() != self.ui.endpointsView.currentIndex().row():
                    self.ui.endpointsView.setCurrentIndex(idx)

    def select_security(self, selection):
        if isinstance(selection, QItemSelection):
            if not selection.indexes():  # no selection
                return
        idx = self.ui.endpointsView.currentIndex()
        transport_profile_uri = self.endpoints_model.data(idx.siblingAtColumn(3))
        if transport_profile_uri != "http://opcfoundation.org/UA-Profile/Transport/uatcp-uasc-uabinary":
            blocker = QSignalBlocker(self.ui.endpointsView.selectionModel())
            self.ui.endpointsView.selectionModel().clearSelection()
        else:
            security_mode = self.endpoints_model.data(idx.siblingAtColumn(1))
            security_policy = self.endpoints_model.data(idx.siblingAtColumn(2))
            self.ui.modeComboBox.setCurrentText(security_mode)
            self.ui.policyComboBox.setCurrentText(security_policy)

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
