# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'card.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CardWidget(object):
    def setupUi(self, CardWidget):
        CardWidget.setObjectName("CardWidget")
        CardWidget.resize(513, 208)
        self.gridLayout = QtWidgets.QGridLayout(CardWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.splitter = QtWidgets.QSplitter(CardWidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.label = QtWidgets.QLabel(self.splitter)
        self.label.setObjectName("label")
        self.listWidget = QtWidgets.QListWidget(self.splitter)
        self.listWidget.setObjectName("listWidget")
        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 1)

        self.retranslateUi(CardWidget)
        QtCore.QMetaObject.connectSlotsByName(CardWidget)

    def retranslateUi(self, CardWidget):
        _translate = QtCore.QCoreApplication.translate
        CardWidget.setWindowTitle(_translate("CardWidget", "Form"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    CardWidget = QtWidgets.QWidget()
    ui = Ui_CardWidget()
    ui.setupUi(CardWidget)
    CardWidget.show()
    sys.exit(app.exec_())
