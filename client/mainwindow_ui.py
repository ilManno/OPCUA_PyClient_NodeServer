# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow_ui.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(922, 879)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/client.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.centralWidget)
        self.gridLayout_8.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_8.setSpacing(6)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.subWidget = QtWidgets.QDockWidget(self.centralWidget)
        self.subWidget.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)
        self.subWidget.setObjectName("subWidget")
        self.dockWidgetContents_7 = QtWidgets.QWidget()
        self.dockWidgetContents_7.setObjectName("dockWidgetContents_7")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.dockWidgetContents_7)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 7)
        self.gridLayout_2.setSpacing(6)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.tabWidget = QtWidgets.QTabWidget(self.dockWidgetContents_7)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setObjectName("tabWidget")
        self.addSubTab = QtWidgets.QWidget()
        self.addSubTab.setObjectName("addSubTab")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.addSubTab)
        self.gridLayout_7.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_7.setSpacing(6)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.noSubLabel = QtWidgets.QLabel(self.addSubTab)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.noSubLabel.setFont(font)
        self.noSubLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.noSubLabel.setObjectName("noSubLabel")
        self.gridLayout_7.addWidget(self.noSubLabel, 0, 0, 1, 1)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icons/add.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.addSubTab, icon1, "")
        self.gridLayout_2.addWidget(self.tabWidget, 0, 0, 1, 1)
        self.subWidget.setWidget(self.dockWidgetContents_7)
        self.gridLayout_8.addWidget(self.subWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 922, 21))
        self.menuBar.setObjectName("menuBar")
        self.menuView = QtWidgets.QMenu(self.menuBar)
        self.menuView.setObjectName("menuView")
        MainWindow.setMenuBar(self.menuBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.attrDockWidget = QtWidgets.QDockWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.attrDockWidget.sizePolicy().hasHeightForWidth())
        self.attrDockWidget.setSizePolicy(sizePolicy)
        self.attrDockWidget.setMinimumSize(QtCore.QSize(400, 170))
        self.attrDockWidget.setObjectName("attrDockWidget")
        self.dockWidgetContents = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dockWidgetContents.sizePolicy().hasHeightForWidth())
        self.dockWidgetContents.setSizePolicy(sizePolicy)
        self.dockWidgetContents.setMinimumSize(QtCore.QSize(100, 0))
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.dockWidgetContents)
        self.gridLayout_4.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_4.setSpacing(6)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.attrView = QtWidgets.QTreeView(self.dockWidgetContents)
        self.attrView.setEditTriggers(QtWidgets.QAbstractItemView.AllEditTriggers)
        self.attrView.setProperty("showDropIndicator", False)
        self.attrView.setTextElideMode(QtCore.Qt.ElideNone)
        self.attrView.setAutoExpandDelay(-1)
        self.attrView.setIndentation(18)
        self.attrView.setSortingEnabled(True)
        self.attrView.setWordWrap(True)
        self.attrView.setObjectName("attrView")
        self.gridLayout_4.addWidget(self.attrView, 0, 0, 1, 2)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem, 1, 0, 1, 1)
        self.attrRefreshButton = QtWidgets.QPushButton(self.dockWidgetContents)
        self.attrRefreshButton.setObjectName("attrRefreshButton")
        self.gridLayout_4.addWidget(self.attrRefreshButton, 1, 1, 1, 1)
        self.attrDockWidget.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.attrDockWidget)
        self.addrDockWidget = QtWidgets.QDockWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addrDockWidget.sizePolicy().hasHeightForWidth())
        self.addrDockWidget.setSizePolicy(sizePolicy)
        self.addrDockWidget.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)
        self.addrDockWidget.setAllowedAreas(QtCore.Qt.TopDockWidgetArea)
        self.addrDockWidget.setObjectName("addrDockWidget")
        self.dockWidgetContents_2 = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dockWidgetContents_2.sizePolicy().hasHeightForWidth())
        self.dockWidgetContents_2.setSizePolicy(sizePolicy)
        self.dockWidgetContents_2.setObjectName("dockWidgetContents_2")
        self.gridLayout = QtWidgets.QGridLayout(self.dockWidgetContents_2)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.settingsButton = QtWidgets.QPushButton(self.dockWidgetContents_2)
        self.settingsButton.setObjectName("settingsButton")
        self.gridLayout.addWidget(self.settingsButton, 1, 4, 1, 1)
        self.addrComboBox = QtWidgets.QComboBox(self.dockWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addrComboBox.sizePolicy().hasHeightForWidth())
        self.addrComboBox.setSizePolicy(sizePolicy)
        self.addrComboBox.setEditable(True)
        self.addrComboBox.setInsertPolicy(QtWidgets.QComboBox.InsertAtTop)
        self.addrComboBox.setObjectName("addrComboBox")
        self.gridLayout.addWidget(self.addrComboBox, 1, 2, 1, 1)
        self.connectButton = QtWidgets.QPushButton(self.dockWidgetContents_2)
        self.connectButton.setObjectName("connectButton")
        self.gridLayout.addWidget(self.connectButton, 1, 3, 1, 1)
        self.addrDockWidget.setWidget(self.dockWidgetContents_2)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(4), self.addrDockWidget)
        self.refDockWidget = QtWidgets.QDockWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.refDockWidget.sizePolicy().hasHeightForWidth())
        self.refDockWidget.setSizePolicy(sizePolicy)
        self.refDockWidget.setObjectName("refDockWidget")
        self.dockWidgetContents_4 = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dockWidgetContents_4.sizePolicy().hasHeightForWidth())
        self.dockWidgetContents_4.setSizePolicy(sizePolicy)
        self.dockWidgetContents_4.setObjectName("dockWidgetContents_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.dockWidgetContents_4)
        self.verticalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.refView = QtWidgets.QTableView(self.dockWidgetContents_4)
        self.refView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.refView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.refView.setObjectName("refView")
        self.refView.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout_2.addWidget(self.refView)
        self.refDockWidget.setWidget(self.dockWidgetContents_4)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.refDockWidget)
        self.treeDockWidget = QtWidgets.QDockWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.treeDockWidget.sizePolicy().hasHeightForWidth())
        self.treeDockWidget.setSizePolicy(sizePolicy)
        self.treeDockWidget.setObjectName("treeDockWidget")
        self.dockWidgetContents_5 = QtWidgets.QWidget()
        self.dockWidgetContents_5.setObjectName("dockWidgetContents_5")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.dockWidgetContents_5)
        self.gridLayout_5.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_5.setSpacing(6)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.treeView = QtWidgets.QTreeView(self.dockWidgetContents_5)
        self.treeView.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.treeView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.treeView.setDragEnabled(True)
        self.treeView.setDragDropMode(QtWidgets.QAbstractItemView.DragOnly)
        self.treeView.setObjectName("treeView")
        self.gridLayout_5.addWidget(self.treeView, 0, 0, 1, 1)
        self.treeDockWidget.setWidget(self.dockWidgetContents_5)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.treeDockWidget)
        self.logDockWidget = QtWidgets.QDockWidget(MainWindow)
        self.logDockWidget.setObjectName("logDockWidget")
        self.dockWidgetContents_6 = QtWidgets.QWidget()
        self.dockWidgetContents_6.setObjectName("dockWidgetContents_6")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.dockWidgetContents_6)
        self.gridLayout_6.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_6.setSpacing(6)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.logTextEdit = QtWidgets.QTextEdit(self.dockWidgetContents_6)
        self.logTextEdit.setObjectName("logTextEdit")
        self.gridLayout_6.addWidget(self.logTextEdit, 0, 0, 1, 1)
        self.logDockWidget.setWidget(self.dockWidgetContents_6)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(8), self.logDockWidget)
        self.actionAddMonitoredItem = QtWidgets.QAction(MainWindow)
        self.actionAddMonitoredItem.setObjectName("actionAddMonitoredItem")
        self.actionDeleteMonitoredItem = QtWidgets.QAction(MainWindow)
        self.actionDeleteMonitoredItem.setObjectName("actionDeleteMonitoredItem")
        self.actionCopyPath = QtWidgets.QAction(MainWindow)
        self.actionCopyPath.setObjectName("actionCopyPath")
        self.actionCopyNodeId = QtWidgets.QAction(MainWindow)
        self.actionCopyNodeId.setObjectName("actionCopyNodeId")
        self.actionCall = QtWidgets.QAction(MainWindow)
        self.actionCall.setObjectName("actionCall")
        self.actionReload = QtWidgets.QAction(MainWindow)
        self.actionReload.setObjectName("actionReload")
        self.menuBar.addAction(self.menuView.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.addrComboBox, self.connectButton)
        MainWindow.setTabOrder(self.connectButton, self.settingsButton)
        MainWindow.setTabOrder(self.settingsButton, self.treeView)
        MainWindow.setTabOrder(self.treeView, self.tabWidget)
        MainWindow.setTabOrder(self.tabWidget, self.attrView)
        MainWindow.setTabOrder(self.attrView, self.attrRefreshButton)
        MainWindow.setTabOrder(self.attrRefreshButton, self.refView)
        MainWindow.setTabOrder(self.refView, self.logTextEdit)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "OPC UA Client"))
        self.subWidget.setWindowTitle(_translate("MainWindow", "Subscriptions"))
        self.noSubLabel.setText(_translate("MainWindow", "No Subscription"))
        self.tabWidget.setTabToolTip(self.tabWidget.indexOf(self.addSubTab), _translate("MainWindow", "Click to create a new subscription"))
        self.menuView.setTitle(_translate("MainWindow", "View"))
        self.attrDockWidget.setWindowTitle(_translate("MainWindow", "Attributes"))
        self.attrRefreshButton.setText(_translate("MainWindow", "Refresh"))
        self.settingsButton.setText(_translate("MainWindow", "Settings..."))
        self.connectButton.setText(_translate("MainWindow", "Connect"))
        self.refDockWidget.setWindowTitle(_translate("MainWindow", "References"))
        self.treeDockWidget.setWindowTitle(_translate("MainWindow", "Address Space"))
        self.logDockWidget.setWindowTitle(_translate("MainWindow", "Logs"))
        self.actionAddMonitoredItem.setText(_translate("MainWindow", "Add Monitored Item to Subscription"))
        self.actionAddMonitoredItem.setToolTip(_translate("MainWindow", "Add selected node to monitored items for current subscription"))
        self.actionDeleteMonitoredItem.setText(_translate("MainWindow", "Delete Monitored Item from Subscription"))
        self.actionDeleteMonitoredItem.setToolTip(_translate("MainWindow", "Delete selected node from monitored items for current subscription"))
        self.actionCopyPath.setText(_translate("MainWindow", "Copy Path"))
        self.actionCopyPath.setToolTip(_translate("MainWindow", "Copy path to node to clipboard"))
        self.actionCopyNodeId.setText(_translate("MainWindow", "Copy NodeId"))
        self.actionCopyNodeId.setToolTip(_translate("MainWindow", "Copy NodeId to clipboard"))
        self.actionCall.setText(_translate("MainWindow", "Call Method"))
        self.actionCall.setToolTip(_translate("MainWindow", "Call Ua Method"))
        self.actionReload.setText(_translate("MainWindow", "Reload"))
        self.actionReload.setToolTip(_translate("MainWindow", "Reload address space"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
