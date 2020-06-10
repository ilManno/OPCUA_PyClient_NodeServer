# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mi_options_ui.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MiOptionsDialog(object):
    def setupUi(self, MiOptionsDialog):
        MiOptionsDialog.setObjectName("MiOptionsDialog")
        MiOptionsDialog.resize(339, 319)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/property.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MiOptionsDialog.setWindowIcon(icon)
        self.gridLayout = QtWidgets.QGridLayout(MiOptionsDialog)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.samplingInterval = QtWidgets.QDoubleSpinBox(MiOptionsDialog)
        self.samplingInterval.setMaximum(9999.0)
        self.samplingInterval.setSingleStep(100.0)
        self.samplingInterval.setObjectName("samplingInterval")
        self.gridLayout.addWidget(self.samplingInterval, 0, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(MiOptionsDialog)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 1, 1, 1)
        self.deadbandValue = QtWidgets.QDoubleSpinBox(MiOptionsDialog)
        self.deadbandValue.setMaximum(9999.0)
        self.deadbandValue.setObjectName("deadbandValue")
        self.gridLayout.addWidget(self.deadbandValue, 7, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(MiOptionsDialog)
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 1, 1, 1)
        self.saveButton = QtWidgets.QPushButton(MiOptionsDialog)
        self.saveButton.setObjectName("saveButton")
        self.gridLayout.addWidget(self.saveButton, 9, 2, 1, 1)
        self.deadbandType = QtWidgets.QComboBox(MiOptionsDialog)
        self.deadbandType.setObjectName("deadbandType")
        self.gridLayout.addWidget(self.deadbandType, 6, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 25, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem, 8, 1, 1, 2)
        self.label_5 = QtWidgets.QLabel(MiOptionsDialog)
        self.label_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 6, 1, 1, 1)
        self.dataChangeTrigger = QtWidgets.QComboBox(MiOptionsDialog)
        self.dataChangeTrigger.setObjectName("dataChangeTrigger")
        self.gridLayout.addWidget(self.dataChangeTrigger, 5, 2, 1, 1)
        self.queueSize = QtWidgets.QSpinBox(MiOptionsDialog)
        self.queueSize.setMaximum(100)
        self.queueSize.setObjectName("queueSize")
        self.gridLayout.addWidget(self.queueSize, 1, 2, 1, 1)
        self.label_6 = QtWidgets.QLabel(MiOptionsDialog)
        self.label_6.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 7, 1, 1, 1)
        self.discardOldest = QtWidgets.QCheckBox(MiOptionsDialog)
        self.discardOldest.setObjectName("discardOldest")
        self.gridLayout.addWidget(self.discardOldest, 2, 2, 1, 1)
        self.label_4 = QtWidgets.QLabel(MiOptionsDialog)
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 5, 1, 1, 1)
        self.label = QtWidgets.QLabel(MiOptionsDialog)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)
        self.dataChangeFilter = QtWidgets.QCheckBox(MiOptionsDialog)
        self.dataChangeFilter.setObjectName("dataChangeFilter")
        self.gridLayout.addWidget(self.dataChangeFilter, 4, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem1, 3, 1, 1, 2)

        self.retranslateUi(MiOptionsDialog)
        QtCore.QMetaObject.connectSlotsByName(MiOptionsDialog)

    def retranslateUi(self, MiOptionsDialog):
        _translate = QtCore.QCoreApplication.translate
        MiOptionsDialog.setWindowTitle(_translate("MiOptionsDialog", "Monitored Items Options"))
        self.label_2.setText(_translate("MiOptionsDialog", "Queue Size"))
        self.label_3.setText(_translate("MiOptionsDialog", "Discard Oldest"))
        self.saveButton.setText(_translate("MiOptionsDialog", "Save"))
        self.label_5.setText(_translate("MiOptionsDialog", "Deadband Type"))
        self.label_6.setText(_translate("MiOptionsDialog", "Deadband Value"))
        self.label_4.setText(_translate("MiOptionsDialog", "Data Change Trigger"))
        self.label.setText(_translate("MiOptionsDialog", "Sampling Interval"))
        self.dataChangeFilter.setText(_translate("MiOptionsDialog", "Data Change Filter"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MiOptionsDialog = QtWidgets.QDialog()
    ui = Ui_MiOptionsDialog()
    ui.setupUi(MiOptionsDialog)
    MiOptionsDialog.show()
    sys.exit(app.exec_())
