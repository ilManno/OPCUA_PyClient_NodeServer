# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'connection_ui.ui'
#
# Created by: PyQt5 UI code generator 5.14.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ConnectionDialog(object):
    def setupUi(self, ConnectionDialog):
        ConnectionDialog.setObjectName("ConnectionDialog")
        ConnectionDialog.resize(400, 300)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("uawidgets/resources/property.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ConnectionDialog.setWindowIcon(icon)
        self.gridLayout = QtWidgets.QGridLayout(ConnectionDialog)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.certificateLabel = QtWidgets.QLabel(ConnectionDialog)
        font = QtGui.QFont()
        font.setItalic(True)
        self.certificateLabel.setFont(font)
        self.certificateLabel.setText("")
        self.certificateLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.certificateLabel.setObjectName("certificateLabel")
        self.gridLayout.addWidget(self.certificateLabel, 2, 0, 1, 1)
        self.label = QtWidgets.QLabel(ConnectionDialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(ConnectionDialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.modeComboBox = QtWidgets.QComboBox(ConnectionDialog)
        self.modeComboBox.setObjectName("modeComboBox")
        self.gridLayout.addWidget(self.modeComboBox, 1, 1, 1, 2)
        self.policyComboBox = QtWidgets.QComboBox(ConnectionDialog)
        self.policyComboBox.setObjectName("policyComboBox")
        self.gridLayout.addWidget(self.policyComboBox, 0, 1, 1, 2)
        self.privateKeyLabel = QtWidgets.QLabel(ConnectionDialog)
        font = QtGui.QFont()
        font.setItalic(True)
        self.privateKeyLabel.setFont(font)
        self.privateKeyLabel.setText("")
        self.privateKeyLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.privateKeyLabel.setObjectName("privateKeyLabel")
        self.gridLayout.addWidget(self.privateKeyLabel, 3, 0, 1, 1)
        self.certificateButton = QtWidgets.QPushButton(ConnectionDialog)
        self.certificateButton.setObjectName("certificateButton")
        self.gridLayout.addWidget(self.certificateButton, 2, 1, 1, 2)
        self.privateKeyButton = QtWidgets.QPushButton(ConnectionDialog)
        self.privateKeyButton.setObjectName("privateKeyButton")
        self.gridLayout.addWidget(self.privateKeyButton, 3, 1, 1, 2)
        self.closeButton = QtWidgets.QPushButton(ConnectionDialog)
        self.closeButton.setObjectName("closeButton")
        self.gridLayout.addWidget(self.closeButton, 4, 2, 1, 1)

        self.retranslateUi(ConnectionDialog)
        QtCore.QMetaObject.connectSlotsByName(ConnectionDialog)

    def retranslateUi(self, ConnectionDialog):
        _translate = QtCore.QCoreApplication.translate
        ConnectionDialog.setWindowTitle(_translate("ConnectionDialog", "Connection Options"))
        self.label.setText(_translate("ConnectionDialog", "Security Policy"))
        self.label_2.setText(_translate("ConnectionDialog", "Message Security Mode"))
        self.certificateButton.setToolTip(_translate("ConnectionDialog", "Select DER File"))
        self.certificateButton.setText(_translate("ConnectionDialog", "Select certificate"))
        self.privateKeyButton.setToolTip(_translate("ConnectionDialog", "Select PEM File"))
        self.privateKeyButton.setText(_translate("ConnectionDialog", "Select private key"))
        self.closeButton.setText(_translate("ConnectionDialog", "Connect"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ConnectionDialog = QtWidgets.QDialog()
    ui = Ui_ConnectionDialog()
    ui.setupUi(ConnectionDialog)
    ConnectionDialog.show()
    sys.exit(app.exec_())
