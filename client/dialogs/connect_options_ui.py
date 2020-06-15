# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'connect_options_ui.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ConnectOptionsDialog(object):
    def setupUi(self, ConnectOptionsDialog):
        ConnectOptionsDialog.setObjectName("ConnectOptionsDialog")
        ConnectOptionsDialog.resize(1312, 387)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/property.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ConnectOptionsDialog.setWindowIcon(icon)
        self.gridLayout = QtWidgets.QGridLayout(ConnectOptionsDialog)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 25, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem, 6, 1, 1, 4)
        spacerItem1 = QtWidgets.QSpacerItem(25, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 1, 2, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 25, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem2, 4, 1, 1, 4)
        self.policyLabel = QtWidgets.QLabel(ConnectOptionsDialog)
        self.policyLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.policyLabel.setObjectName("policyLabel")
        self.gridLayout.addWidget(self.policyLabel, 1, 2, 1, 1)
        self.connectButton = QtWidgets.QPushButton(ConnectOptionsDialog)
        self.connectButton.setObjectName("connectButton")
        self.gridLayout.addWidget(self.connectButton, 7, 3, 1, 1)
        self.modeLabel = QtWidgets.QLabel(ConnectOptionsDialog)
        self.modeLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.modeLabel.setObjectName("modeLabel")
        self.gridLayout.addWidget(self.modeLabel, 0, 2, 1, 1)
        self.modeComboBox = QtWidgets.QComboBox(ConnectOptionsDialog)
        self.modeComboBox.setObjectName("modeComboBox")
        self.gridLayout.addWidget(self.modeComboBox, 0, 3, 1, 2)
        self.generateButton = QtWidgets.QPushButton(ConnectOptionsDialog)
        self.generateButton.setObjectName("generateButton")
        self.gridLayout.addWidget(self.generateButton, 5, 3, 1, 2)
        self.certificateButton = QtWidgets.QPushButton(ConnectOptionsDialog)
        self.certificateButton.setObjectName("certificateButton")
        self.gridLayout.addWidget(self.certificateButton, 2, 3, 1, 2)
        self.policyComboBox = QtWidgets.QComboBox(ConnectOptionsDialog)
        self.policyComboBox.setObjectName("policyComboBox")
        self.gridLayout.addWidget(self.policyComboBox, 1, 3, 1, 2)
        self.privateKeyButton = QtWidgets.QPushButton(ConnectOptionsDialog)
        self.privateKeyButton.setObjectName("privateKeyButton")
        self.gridLayout.addWidget(self.privateKeyButton, 3, 3, 1, 2)
        self.privateKeyLabel = QtWidgets.QLabel(ConnectOptionsDialog)
        font = QtGui.QFont()
        font.setItalic(True)
        self.privateKeyLabel.setFont(font)
        self.privateKeyLabel.setText("")
        self.privateKeyLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.privateKeyLabel.setObjectName("privateKeyLabel")
        self.gridLayout.addWidget(self.privateKeyLabel, 3, 1, 1, 2)
        self.certificateLabel = QtWidgets.QLabel(ConnectOptionsDialog)
        font = QtGui.QFont()
        font.setItalic(True)
        self.certificateLabel.setFont(font)
        self.certificateLabel.setText("")
        self.certificateLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.certificateLabel.setObjectName("certificateLabel")
        self.gridLayout.addWidget(self.certificateLabel, 2, 1, 1, 2)
        self.cancelButton = QtWidgets.QPushButton(ConnectOptionsDialog)
        self.cancelButton.setObjectName("cancelButton")
        self.gridLayout.addWidget(self.cancelButton, 7, 4, 1, 1)
        self.endpointsView = QtWidgets.QTableView(ConnectOptionsDialog)
        self.endpointsView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.endpointsView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.endpointsView.setObjectName("endpointsView")
        self.endpointsView.horizontalHeader().setStretchLastSection(True)
        self.gridLayout.addWidget(self.endpointsView, 0, 0, 8, 1)

        self.retranslateUi(ConnectOptionsDialog)
        QtCore.QMetaObject.connectSlotsByName(ConnectOptionsDialog)

    def retranslateUi(self, ConnectOptionsDialog):
        _translate = QtCore.QCoreApplication.translate
        ConnectOptionsDialog.setWindowTitle(_translate("ConnectOptionsDialog", "Connection Options"))
        self.policyLabel.setText(_translate("ConnectOptionsDialog", "Security Policy"))
        self.connectButton.setText(_translate("ConnectOptionsDialog", "Connect"))
        self.modeLabel.setText(_translate("ConnectOptionsDialog", "Message Security Mode"))
        self.generateButton.setText(_translate("ConnectOptionsDialog", "Generate valid certificate"))
        self.certificateButton.setToolTip(_translate("ConnectOptionsDialog", "Select DER File"))
        self.certificateButton.setText(_translate("ConnectOptionsDialog", "Select certificate"))
        self.privateKeyButton.setToolTip(_translate("ConnectOptionsDialog", "Select PEM File"))
        self.privateKeyButton.setText(_translate("ConnectOptionsDialog", "Select private key"))
        self.cancelButton.setText(_translate("ConnectOptionsDialog", "Cancel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ConnectOptionsDialog = QtWidgets.QDialog()
    ui = Ui_ConnectOptionsDialog()
    ui.setupUi(ConnectOptionsDialog)
    ConnectOptionsDialog.show()
    sys.exit(app.exec_())
