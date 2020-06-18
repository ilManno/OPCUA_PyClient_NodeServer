# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sub_settings_ui.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SubSettingsDialog(object):
    def setupUi(self, SubSettingsDialog):
        SubSettingsDialog.setObjectName("SubSettingsDialog")
        SubSettingsDialog.resize(301, 271)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/property.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        SubSettingsDialog.setWindowIcon(icon)
        self.gridLayout = QtWidgets.QGridLayout(SubSettingsDialog)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.label_4 = QtWidgets.QLabel(SubSettingsDialog)
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 2)
        self.requestedMaxKeepAliveCount = QtWidgets.QSpinBox(SubSettingsDialog)
        self.requestedMaxKeepAliveCount.setMinimum(1)
        self.requestedMaxKeepAliveCount.setMaximum(715827882)
        self.requestedMaxKeepAliveCount.setObjectName("requestedMaxKeepAliveCount")
        self.gridLayout.addWidget(self.requestedMaxKeepAliveCount, 1, 2, 1, 1)
        self.label = QtWidgets.QLabel(SubSettingsDialog)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)
        self.label_3 = QtWidgets.QLabel(SubSettingsDialog)
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 2)
        self.maxNotificationsPerPublish = QtWidgets.QSpinBox(SubSettingsDialog)
        self.maxNotificationsPerPublish.setMaximum(2147483647)
        self.maxNotificationsPerPublish.setObjectName("maxNotificationsPerPublish")
        self.gridLayout.addWidget(self.maxNotificationsPerPublish, 3, 2, 1, 1)
        self.requestedLifeTimeCount = QtWidgets.QSpinBox(SubSettingsDialog)
        self.requestedLifeTimeCount.setMinimum(3)
        self.requestedLifeTimeCount.setMaximum(2147483646)
        self.requestedLifeTimeCount.setObjectName("requestedLifeTimeCount")
        self.gridLayout.addWidget(self.requestedLifeTimeCount, 2, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 25, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem, 5, 0, 1, 3)
        self.label_2 = QtWidgets.QLabel(SubSettingsDialog)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 2)
        self.requestedPublishInterval = QtWidgets.QSpinBox(SubSettingsDialog)
        self.requestedPublishInterval.setMaximum(50000)
        self.requestedPublishInterval.setSingleStep(100)
        self.requestedPublishInterval.setObjectName("requestedPublishInterval")
        self.gridLayout.addWidget(self.requestedPublishInterval, 0, 2, 1, 1)
        self.priority = QtWidgets.QSpinBox(SubSettingsDialog)
        self.priority.setMaximum(255)
        self.priority.setObjectName("priority")
        self.gridLayout.addWidget(self.priority, 4, 2, 1, 1)
        self.label_5 = QtWidgets.QLabel(SubSettingsDialog)
        self.label_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 2)
        self.cancelButton = QtWidgets.QPushButton(SubSettingsDialog)
        self.cancelButton.setObjectName("cancelButton")
        self.gridLayout.addWidget(self.cancelButton, 6, 2, 1, 1)
        self.createButton = QtWidgets.QPushButton(SubSettingsDialog)
        self.createButton.setObjectName("createButton")
        self.gridLayout.addWidget(self.createButton, 6, 1, 1, 1)

        self.retranslateUi(SubSettingsDialog)
        QtCore.QMetaObject.connectSlotsByName(SubSettingsDialog)

    def retranslateUi(self, SubSettingsDialog):
        _translate = QtCore.QCoreApplication.translate
        SubSettingsDialog.setWindowTitle(_translate("SubSettingsDialog", "Subscription Settings"))
        self.label_4.setText(_translate("SubSettingsDialog", "Max Notifications per Publish"))
        self.label.setText(_translate("SubSettingsDialog", "Requested Publishing Interval"))
        self.label_3.setText(_translate("SubSettingsDialog", "Requested LifeTime Count"))
        self.label_2.setText(_translate("SubSettingsDialog", "Requested Max Keep-Alive Count"))
        self.label_5.setText(_translate("SubSettingsDialog", "Priority"))
        self.cancelButton.setText(_translate("SubSettingsDialog", "Cancel"))
        self.createButton.setText(_translate("SubSettingsDialog", "Create"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    SubSettingsDialog = QtWidgets.QDialog()
    ui = Ui_SubSettingsDialog()
    ui.setupUi(SubSettingsDialog)
    SubSettingsDialog.show()
    sys.exit(app.exec_())
