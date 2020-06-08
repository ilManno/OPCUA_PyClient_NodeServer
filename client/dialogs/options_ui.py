# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'options_ui.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_OptionsDialog(object):
    def setupUi(self, OptionsDialog):
        OptionsDialog.setObjectName("OptionsDialog")
        OptionsDialog.resize(408, 307)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/property.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        OptionsDialog.setWindowIcon(icon)
        self.gridLayout = QtWidgets.QGridLayout(OptionsDialog)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 25, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem, 6, 0, 1, 4)
        self.generateButton = QtWidgets.QPushButton(OptionsDialog)
        self.generateButton.setObjectName("generateButton")
        self.gridLayout.addWidget(self.generateButton, 5, 2, 1, 2)
        self.connectButton = QtWidgets.QPushButton(OptionsDialog)
        self.connectButton.setObjectName("connectButton")
        self.gridLayout.addWidget(self.connectButton, 7, 2, 1, 1)
        self.privateKeyButton = QtWidgets.QPushButton(OptionsDialog)
        self.privateKeyButton.setObjectName("privateKeyButton")
        self.gridLayout.addWidget(self.privateKeyButton, 3, 2, 1, 2)
        self.certificateLabel = QtWidgets.QLabel(OptionsDialog)
        font = QtGui.QFont()
        font.setItalic(True)
        self.certificateLabel.setFont(font)
        self.certificateLabel.setText("")
        self.certificateLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.certificateLabel.setObjectName("certificateLabel")
        self.gridLayout.addWidget(self.certificateLabel, 2, 0, 1, 2)
        self.cancelButton = QtWidgets.QPushButton(OptionsDialog)
        self.cancelButton.setObjectName("cancelButton")
        self.gridLayout.addWidget(self.cancelButton, 7, 3, 1, 1)
        self.modeComboBox = QtWidgets.QComboBox(OptionsDialog)
        self.modeComboBox.setObjectName("modeComboBox")
        self.gridLayout.addWidget(self.modeComboBox, 0, 2, 1, 2)
        self.policyLabel = QtWidgets.QLabel(OptionsDialog)
        self.policyLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.policyLabel.setObjectName("policyLabel")
        self.gridLayout.addWidget(self.policyLabel, 1, 1, 1, 1)
        self.certificateButton = QtWidgets.QPushButton(OptionsDialog)
        self.certificateButton.setObjectName("certificateButton")
        self.gridLayout.addWidget(self.certificateButton, 2, 2, 1, 2)
        spacerItem1 = QtWidgets.QSpacerItem(25, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 0, 2, 1)
        self.privateKeyLabel = QtWidgets.QLabel(OptionsDialog)
        font = QtGui.QFont()
        font.setItalic(True)
        self.privateKeyLabel.setFont(font)
        self.privateKeyLabel.setText("")
        self.privateKeyLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.privateKeyLabel.setObjectName("privateKeyLabel")
        self.gridLayout.addWidget(self.privateKeyLabel, 3, 0, 1, 2)
        self.modeLabel = QtWidgets.QLabel(OptionsDialog)
        self.modeLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.modeLabel.setObjectName("modeLabel")
        self.gridLayout.addWidget(self.modeLabel, 0, 1, 1, 1)
        self.policyComboBox = QtWidgets.QComboBox(OptionsDialog)
        self.policyComboBox.setObjectName("policyComboBox")
        self.gridLayout.addWidget(self.policyComboBox, 1, 2, 1, 2)
        spacerItem2 = QtWidgets.QSpacerItem(20, 25, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem2, 4, 0, 1, 4)

        self.retranslateUi(OptionsDialog)
        QtCore.QMetaObject.connectSlotsByName(OptionsDialog)

    def retranslateUi(self, OptionsDialog):
        _translate = QtCore.QCoreApplication.translate
        OptionsDialog.setWindowTitle(_translate("OptionsDialog", "Connection Options"))
        self.generateButton.setText(_translate("OptionsDialog", "Generate valid certificate"))
        self.connectButton.setText(_translate("OptionsDialog", "Connect"))
        self.privateKeyButton.setToolTip(_translate("OptionsDialog", "Select PEM File"))
        self.privateKeyButton.setText(_translate("OptionsDialog", "Select private key"))
        self.cancelButton.setText(_translate("OptionsDialog", "Cancel"))
        self.policyLabel.setText(_translate("OptionsDialog", "Security Policy"))
        self.certificateButton.setToolTip(_translate("OptionsDialog", "Select DER File"))
        self.certificateButton.setText(_translate("OptionsDialog", "Select certificate"))
        self.modeLabel.setText(_translate("OptionsDialog", "Message Security Mode"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    OptionsDialog = QtWidgets.QDialog()
    ui = Ui_OptionsDialog()
    ui.setupUi(OptionsDialog)
    OptionsDialog.show()
    sys.exit(app.exec_())
