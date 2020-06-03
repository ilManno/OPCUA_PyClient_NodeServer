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
        ConnectionDialog.resize(387, 283)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("uawidgets/icons/property.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ConnectionDialog.setWindowIcon(icon)
        self.gridLayout = QtWidgets.QGridLayout(ConnectionDialog)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.modeLabel = QtWidgets.QLabel(ConnectionDialog)
        self.modeLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.modeLabel.setObjectName("modeLabel")
        self.gridLayout.addWidget(self.modeLabel, 0, 1, 1, 1)
        self.connectButton = QtWidgets.QPushButton(ConnectionDialog)
        self.connectButton.setObjectName("connectButton")
        self.gridLayout.addWidget(self.connectButton, 5, 2, 1, 1)
        self.privateKeyButton = QtWidgets.QPushButton(ConnectionDialog)
        self.privateKeyButton.setObjectName("privateKeyButton")
        self.gridLayout.addWidget(self.privateKeyButton, 3, 2, 1, 2)
        self.cancelButton = QtWidgets.QPushButton(ConnectionDialog)
        self.cancelButton.setObjectName("cancelButton")
        self.gridLayout.addWidget(self.cancelButton, 5, 3, 1, 1)
        self.certificateButton = QtWidgets.QPushButton(ConnectionDialog)
        self.certificateButton.setObjectName("certificateButton")
        self.gridLayout.addWidget(self.certificateButton, 2, 2, 1, 2)
        self.policyComboBox = QtWidgets.QComboBox(ConnectionDialog)
        self.policyComboBox.setObjectName("policyComboBox")
        self.gridLayout.addWidget(self.policyComboBox, 1, 2, 1, 2)
        spacerItem = QtWidgets.QSpacerItem(25, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 0, 2, 1)
        self.modeComboBox = QtWidgets.QComboBox(ConnectionDialog)
        self.modeComboBox.setObjectName("modeComboBox")
        self.gridLayout.addWidget(self.modeComboBox, 0, 2, 1, 2)
        self.policyLabel = QtWidgets.QLabel(ConnectionDialog)
        self.policyLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.policyLabel.setObjectName("policyLabel")
        self.gridLayout.addWidget(self.policyLabel, 1, 1, 1, 1)
        self.privateKeyLabel = QtWidgets.QLabel(ConnectionDialog)
        font = QtGui.QFont()
        font.setItalic(True)
        self.privateKeyLabel.setFont(font)
        self.privateKeyLabel.setText("")
        self.privateKeyLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.privateKeyLabel.setObjectName("privateKeyLabel")
        self.gridLayout.addWidget(self.privateKeyLabel, 3, 0, 1, 2)
        self.certificateLabel = QtWidgets.QLabel(ConnectionDialog)
        font = QtGui.QFont()
        font.setItalic(True)
        self.certificateLabel.setFont(font)
        self.certificateLabel.setText("")
        self.certificateLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.certificateLabel.setObjectName("certificateLabel")
        self.gridLayout.addWidget(self.certificateLabel, 2, 0, 1, 2)
        spacerItem1 = QtWidgets.QSpacerItem(20, 25, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem1, 4, 0, 1, 4)

        self.retranslateUi(ConnectionDialog)
        QtCore.QMetaObject.connectSlotsByName(ConnectionDialog)

    def retranslateUi(self, ConnectionDialog):
        _translate = QtCore.QCoreApplication.translate
        ConnectionDialog.setWindowTitle(_translate("ConnectionDialog", "Connection Options"))
        self.modeLabel.setText(_translate("ConnectionDialog", "Message Security Mode"))
        self.connectButton.setText(_translate("ConnectionDialog", "Connect"))
        self.privateKeyButton.setToolTip(_translate("ConnectionDialog", "Select PEM File"))
        self.privateKeyButton.setText(_translate("ConnectionDialog", "Select private key"))
        self.cancelButton.setText(_translate("ConnectionDialog", "Cancel"))
        self.certificateButton.setToolTip(_translate("ConnectionDialog", "Select DER File"))
        self.certificateButton.setText(_translate("ConnectionDialog", "Select certificate"))
        self.policyLabel.setText(_translate("ConnectionDialog", "Security Policy"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ConnectionDialog = QtWidgets.QDialog()
    ui = Ui_ConnectionDialog()
    ui.setupUi(ConnectionDialog)
    ConnectionDialog.show()
    sys.exit(app.exec_())
