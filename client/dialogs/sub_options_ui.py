# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sub_options_ui.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SubOptionsDialog(object):
    def setupUi(self, SubOptionsDialog):
        SubOptionsDialog.setObjectName("SubOptionsDialog")
        SubOptionsDialog.resize(301, 232)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/property.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        SubOptionsDialog.setWindowIcon(icon)
        self.gridLayout = QtWidgets.QGridLayout(SubOptionsDialog)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.maxNotificationsPerPublish = QtWidgets.QSpinBox(SubOptionsDialog)
        self.maxNotificationsPerPublish.setMaximum(999999999)
        self.maxNotificationsPerPublish.setObjectName("maxNotificationsPerPublish")
        self.gridLayout.addWidget(self.maxNotificationsPerPublish, 3, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(SubOptionsDialog)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 2)
        self.label_3 = QtWidgets.QLabel(SubOptionsDialog)
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 2)
        self.label = QtWidgets.QLabel(SubOptionsDialog)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)
        self.saveButton = QtWidgets.QPushButton(SubOptionsDialog)
        self.saveButton.setObjectName("saveButton")
        self.gridLayout.addWidget(self.saveButton, 5, 2, 1, 1)
        self.label_4 = QtWidgets.QLabel(SubOptionsDialog)
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 2)
        self.requestedMaxKeepAliveCount = QtWidgets.QSpinBox(SubOptionsDialog)
        self.requestedMaxKeepAliveCount.setMinimum(1)
        self.requestedMaxKeepAliveCount.setMaximum(999999999)
        self.requestedMaxKeepAliveCount.setObjectName("requestedMaxKeepAliveCount")
        self.gridLayout.addWidget(self.requestedMaxKeepAliveCount, 1, 2, 1, 1)
        self.requestedLifeTimeCount = QtWidgets.QSpinBox(SubOptionsDialog)
        self.requestedLifeTimeCount.setMinimum(1)
        self.requestedLifeTimeCount.setMaximum(999999999)
        self.requestedLifeTimeCount.setObjectName("requestedLifeTimeCount")
        self.gridLayout.addWidget(self.requestedLifeTimeCount, 2, 2, 1, 1)
        self.requestedPublishInterval = QtWidgets.QSpinBox(SubOptionsDialog)
        self.requestedPublishInterval.setMaximum(9999)
        self.requestedPublishInterval.setSingleStep(100)
        self.requestedPublishInterval.setObjectName("requestedPublishInterval")
        self.gridLayout.addWidget(self.requestedPublishInterval, 0, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 25, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem, 4, 0, 1, 3)

        self.retranslateUi(SubOptionsDialog)
        QtCore.QMetaObject.connectSlotsByName(SubOptionsDialog)

    def retranslateUi(self, SubOptionsDialog):
        _translate = QtCore.QCoreApplication.translate
        SubOptionsDialog.setWindowTitle(_translate("SubOptionsDialog", "Subscription Options"))
        self.label_2.setText(_translate("SubOptionsDialog", "Requested Max Keep-Alive Count"))
        self.label_3.setText(_translate("SubOptionsDialog", "Requested LifeTime Count"))
        self.label.setText(_translate("SubOptionsDialog", "Requested Publishing Interval"))
        self.saveButton.setText(_translate("SubOptionsDialog", "Save"))
        self.label_4.setText(_translate("SubOptionsDialog", "Max Notifications per Publish"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    SubOptionsDialog = QtWidgets.QDialog()
    ui = Ui_SubOptionsDialog()
    ui.setupUi(SubOptionsDialog)
    SubOptionsDialog.show()
    sys.exit(app.exec_())
