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
        CardWidget.resize(463, 152)
        self.gridLayout = QtWidgets.QGridLayout(CardWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.splitter = QtWidgets.QSplitter(CardWidget)
        self.splitter.setStyleSheet("background-color: #fafafa;")
        self.splitter.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.icon = QtWidgets.QLabel(self.splitter)
        self.icon.setObjectName("icon")
        self.variablesView = QtWidgets.QTableView(self.splitter)
        self.variablesView.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.variablesView.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.variablesView.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.variablesView.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.variablesView.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.variablesView.setShowGrid(False)
        self.variablesView.setObjectName("variablesView")
        self.variablesView.horizontalHeader().setHighlightSections(False)
        self.variablesView.horizontalHeader().setStretchLastSection(True)
        self.variablesView.verticalHeader().setVisible(False)
        self.variablesView.verticalHeader().setDefaultSectionSize(20)
        self.variablesView.verticalHeader().setMinimumSectionSize(15)
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
