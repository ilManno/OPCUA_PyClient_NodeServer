# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'connect_settings_ui.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ConnectSettingsDialog(object):
    def setupUi(self, ConnectSettingsDialog):
        ConnectSettingsDialog.setObjectName("ConnectSettingsDialog")
        ConnectSettingsDialog.resize(1312, 387)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/property.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ConnectSettingsDialog.setWindowIcon(icon)
        self.gridLayout = QtWidgets.QGridLayout(ConnectSettingsDialog)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 25, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem, 6, 1, 1, 4)
        spacerItem1 = QtWidgets.QSpacerItem(25, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 1, 2, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 25, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem2, 4, 1, 1, 4)
        self.policyLabel = QtWidgets.QLabel(ConnectSettingsDialog)
        self.policyLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.policyLabel.setObjectName("policyLabel")
        self.gridLayout.addWidget(self.policyLabel, 1, 2, 1, 1)
        self.connectButton = QtWidgets.QPushButton(ConnectSettingsDialog)
        self.connectButton.setObjectName("connectButton")
        self.gridLayout.addWidget(self.connectButton, 7, 3, 1, 1)
        self.modeLabel = QtWidgets.QLabel(ConnectSettingsDialog)
        self.modeLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.modeLabel.setObjectName("modeLabel")
        self.gridLayout.addWidget(self.modeLabel, 0, 2, 1, 1)
        self.modeComboBox = QtWidgets.QComboBox(ConnectSettingsDialog)
        self.modeComboBox.setObjectName("modeComboBox")
        self.gridLayout.addWidget(self.modeComboBox, 0, 3, 1, 2)
        self.generateButton = QtWidgets.QPushButton(ConnectSettingsDialog)
        self.generateButton.setObjectName("generateButton")
        self.gridLayout.addWidget(self.generateButton, 5, 3, 1, 2)
        self.certificateButton = QtWidgets.QPushButton(ConnectSettingsDialog)
        self.certificateButton.setObjectName("certificateButton")
        self.gridLayout.addWidget(self.certificateButton, 2, 3, 1, 2)
        self.policyComboBox = QtWidgets.QComboBox(ConnectSettingsDialog)
        self.policyComboBox.setObjectName("policyComboBox")
        self.gridLayout.addWidget(self.policyComboBox, 1, 3, 1, 2)
        self.privateKeyButton = QtWidgets.QPushButton(ConnectSettingsDialog)
        self.privateKeyButton.setObjectName("privateKeyButton")
        self.gridLayout.addWidget(self.privateKeyButton, 3, 3, 1, 2)
        self.privateKeyLabel = QtWidgets.QLabel(ConnectSettingsDialog)
        font = QtGui.QFont()
        font.setItalic(True)
        self.privateKeyLabel.setFont(font)
        self.privateKeyLabel.setText("")
        self.privateKeyLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.privateKeyLabel.setObjectName("privateKeyLabel")
        self.gridLayout.addWidget(self.privateKeyLabel, 3, 1, 1, 2)
        self.certificateLabel = QtWidgets.QLabel(ConnectSettingsDialog)
        font = QtGui.QFont()
        font.setItalic(True)
        self.certificateLabel.setFont(font)
        self.certificateLabel.setText("")
        self.certificateLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.certificateLabel.setObjectName("certificateLabel")
        self.gridLayout.addWidget(self.certificateLabel, 2, 1, 1, 2)
        self.cancelButton = QtWidgets.QPushButton(ConnectSettingsDialog)
        self.cancelButton.setObjectName("cancelButton")
        self.gridLayout.addWidget(self.cancelButton, 7, 4, 1, 1)
        self.endpointsView = QtWidgets.QTableView(ConnectSettingsDialog)
        self.endpointsView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.endpointsView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.endpointsView.setObjectName("endpointsView")
        self.endpointsView.horizontalHeader().setStretchLastSection(True)
        self.gridLayout.addWidget(self.endpointsView, 0, 0, 8, 1)

        self.retranslateUi(ConnectSettingsDialog)
        QtCore.QMetaObject.connectSlotsByName(ConnectSettingsDialog)

    def retranslateUi(self, ConnectSettingsDialog):
        _translate = QtCore.QCoreApplication.translate
        ConnectSettingsDialog.setWindowTitle(_translate("ConnectSettingsDialog", "Connection Settings"))
        self.policyLabel.setText(_translate("ConnectSettingsDialog", "Security Policy"))
        self.connectButton.setText(_translate("ConnectSettingsDialog", "Connect"))
        self.modeLabel.setText(_translate("ConnectSettingsDialog", "Message Security Mode"))
        self.generateButton.setText(_translate("ConnectSettingsDialog", "Generate valid certificate"))
        self.certificateButton.setToolTip(_translate("ConnectSettingsDialog", "Select DER File"))
        self.certificateButton.setText(_translate("ConnectSettingsDialog", "Select certificate"))
        self.privateKeyButton.setToolTip(_translate("ConnectSettingsDialog", "Select PEM File"))
        self.privateKeyButton.setText(_translate("ConnectSettingsDialog", "Select private key"))
        self.cancelButton.setText(_translate("ConnectSettingsDialog", "Cancel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ConnectSettingsDialog = QtWidgets.QDialog()
    ui = Ui_ConnectSettingsDialog()
    ui.setupUi(ConnectSettingsDialog)
    ConnectSettingsDialog.show()
    sys.exit(app.exec_())
