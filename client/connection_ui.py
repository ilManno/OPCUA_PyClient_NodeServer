# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'connection_ui.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ConnectionDialog(object):
    def setupUi(self, ConnectionDialog):
        ConnectionDialog.setObjectName("ConnectionDialog")
        ConnectionDialog.resize(400, 300)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("uawidgets/icons/property.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ConnectionDialog.setWindowIcon(icon)
        self.gridLayout = QtWidgets.QGridLayout(ConnectionDialog)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.policyLabel = QtWidgets.QLabel(ConnectionDialog)
        self.policyLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.policyLabel.setObjectName("policyLabel")
        self.gridLayout.addWidget(self.policyLabel, 1, 0, 1, 1)
        self.privateKeyLabel = QtWidgets.QLabel(ConnectionDialog)
        font = QtGui.QFont()
        font.setItalic(True)
        self.privateKeyLabel.setFont(font)
        self.privateKeyLabel.setText("")
        self.privateKeyLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.privateKeyLabel.setObjectName("privateKeyLabel")
        self.gridLayout.addWidget(self.privateKeyLabel, 3, 0, 1, 1)
        self.connectButton = QtWidgets.QPushButton(ConnectionDialog)
        self.connectButton.setObjectName("connectButton")
        self.gridLayout.addWidget(self.connectButton, 4, 2, 1, 1)
        self.modeComboBox = QtWidgets.QComboBox(ConnectionDialog)
        self.modeComboBox.setObjectName("modeComboBox")
        self.gridLayout.addWidget(self.modeComboBox, 0, 1, 1, 2)
        self.modeLabel = QtWidgets.QLabel(ConnectionDialog)
        self.modeLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.modeLabel.setObjectName("modeLabel")
        self.gridLayout.addWidget(self.modeLabel, 0, 0, 1, 1)
        self.privateKeyButton = QtWidgets.QPushButton(ConnectionDialog)
        self.privateKeyButton.setObjectName("privateKeyButton")
        self.gridLayout.addWidget(self.privateKeyButton, 3, 1, 1, 2)
        self.certificateButton = QtWidgets.QPushButton(ConnectionDialog)
        self.certificateButton.setObjectName("certificateButton")
        self.gridLayout.addWidget(self.certificateButton, 2, 1, 1, 2)
        self.certificateLabel = QtWidgets.QLabel(ConnectionDialog)
        font = QtGui.QFont()
        font.setItalic(True)
        self.certificateLabel.setFont(font)
        self.certificateLabel.setText("")
        self.certificateLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.certificateLabel.setObjectName("certificateLabel")
        self.gridLayout.addWidget(self.certificateLabel, 2, 0, 1, 1)
        self.policyComboBox = QtWidgets.QComboBox(ConnectionDialog)
        self.policyComboBox.setObjectName("policyComboBox")
        self.gridLayout.addWidget(self.policyComboBox, 1, 1, 1, 2)

        self.retranslateUi(ConnectionDialog)
        QtCore.QMetaObject.connectSlotsByName(ConnectionDialog)

    def retranslateUi(self, ConnectionDialog):
        _translate = QtCore.QCoreApplication.translate
        ConnectionDialog.setWindowTitle(_translate("ConnectionDialog", "Connection Options"))
        self.policyLabel.setText(_translate("ConnectionDialog", "Security Policy"))
        self.connectButton.setText(_translate("ConnectionDialog", "Connect"))
        self.modeLabel.setText(_translate("ConnectionDialog", "Message Security Mode"))
        self.privateKeyButton.setToolTip(_translate("ConnectionDialog", "Select PEM File"))
        self.privateKeyButton.setText(_translate("ConnectionDialog", "Select private key"))
        self.certificateButton.setToolTip(_translate("ConnectionDialog", "Select DER File"))
        self.certificateButton.setText(_translate("ConnectionDialog", "Select certificate"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ConnectionDialog = QtWidgets.QDialog()
    ui = Ui_ConnectionDialog()
    ui.setupUi(ConnectionDialog)
    ConnectionDialog.show()
    sys.exit(app.exec_())
