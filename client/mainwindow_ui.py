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
        icon.addPixmap(QtGui.QPixmap("uawidgets/icons/client.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.centralWidget)
        self.gridLayout_7.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_7.setSpacing(6)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.splitter = QtWidgets.QSplitter(self.centralWidget)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.subDockWidget = QtWidgets.QDockWidget(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.subDockWidget.sizePolicy().hasHeightForWidth())
        self.subDockWidget.setSizePolicy(sizePolicy)
        self.subDockWidget.setFeatures(QtWidgets.QDockWidget.DockWidgetClosable|QtWidgets.QDockWidget.DockWidgetMovable)
        self.subDockWidget.setObjectName("subDockWidget")
        self.dockWidgetContents_7 = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dockWidgetContents_7.sizePolicy().hasHeightForWidth())
        self.dockWidgetContents_7.setSizePolicy(sizePolicy)
        self.dockWidgetContents_7.setObjectName("dockWidgetContents_7")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.dockWidgetContents_7)
        self.gridLayout_3.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_3.setSpacing(6)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.subView = QtWidgets.QTableView(self.dockWidgetContents_7)
        self.subView.setAcceptDrops(True)
        self.subView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.subView.setDragDropOverwriteMode(False)
        self.subView.setDragDropMode(QtWidgets.QAbstractItemView.DropOnly)
        self.subView.setObjectName("subView")
        self.subView.horizontalHeader().setStretchLastSection(True)
        self.gridLayout_3.addWidget(self.subView, 0, 0, 1, 1)
        self.subDockWidget.setWidget(self.dockWidgetContents_7)
        self.evDockWidget = QtWidgets.QDockWidget(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.evDockWidget.sizePolicy().hasHeightForWidth())
        self.evDockWidget.setSizePolicy(sizePolicy)
        self.evDockWidget.setFeatures(QtWidgets.QDockWidget.DockWidgetClosable|QtWidgets.QDockWidget.DockWidgetMovable)
        self.evDockWidget.setObjectName("evDockWidget")
        self.dockWidgetContents_8 = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dockWidgetContents_8.sizePolicy().hasHeightForWidth())
        self.dockWidgetContents_8.setSizePolicy(sizePolicy)
        self.dockWidgetContents_8.setObjectName("dockWidgetContents_8")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.dockWidgetContents_8)
        self.gridLayout_2.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_2.setSpacing(6)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.evView = QtWidgets.QListView(self.dockWidgetContents_8)
        self.evView.setAcceptDrops(True)
        self.evView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.evView.setDragDropMode(QtWidgets.QAbstractItemView.DropOnly)
        self.evView.setObjectName("evView")
        self.gridLayout_2.addWidget(self.evView, 0, 0, 1, 1)
        self.evDockWidget.setWidget(self.dockWidgetContents_8)
        self.gridLayout_7.addWidget(self.splitter, 0, 0, 1, 1)
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
        self.attrDockWidget.setFeatures(QtWidgets.QDockWidget.DockWidgetClosable|QtWidgets.QDockWidget.DockWidgetMovable)
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
        self.optionsButton = QtWidgets.QPushButton(self.dockWidgetContents_2)
        self.optionsButton.setObjectName("optionsButton")
        self.gridLayout.addWidget(self.optionsButton, 1, 4, 1, 1)
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
        self.refDockWidget.setFeatures(QtWidgets.QDockWidget.DockWidgetClosable|QtWidgets.QDockWidget.DockWidgetMovable)
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
        self.treeDockWidget.setFeatures(QtWidgets.QDockWidget.DockWidgetClosable|QtWidgets.QDockWidget.DockWidgetMovable)
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
        self.logDockWidget.setFeatures(QtWidgets.QDockWidget.DockWidgetClosable|QtWidgets.QDockWidget.DockWidgetMovable)
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
        self.actionSubscribeDataChange = QtWidgets.QAction(MainWindow)
        self.actionSubscribeDataChange.setObjectName("actionSubscribeDataChange")
        self.actionUnsubscribeDataChange = QtWidgets.QAction(MainWindow)
        self.actionUnsubscribeDataChange.setObjectName("actionUnsubscribeDataChange")
        self.actionSubscribeEvent = QtWidgets.QAction(MainWindow)
        self.actionSubscribeEvent.setObjectName("actionSubscribeEvent")
        self.actionUnsubscribeEvents = QtWidgets.QAction(MainWindow)
        self.actionUnsubscribeEvents.setObjectName("actionUnsubscribeEvents")
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

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "OPC UA Client"))
        self.subDockWidget.setWindowTitle(_translate("MainWindow", "Subscriptions"))
        self.evDockWidget.setWindowTitle(_translate("MainWindow", "Events"))
        self.menuView.setTitle(_translate("MainWindow", "View"))
        self.attrDockWidget.setWindowTitle(_translate("MainWindow", "Attributes"))
        self.attrRefreshButton.setText(_translate("MainWindow", "Refresh"))
        self.optionsButton.setText(_translate("MainWindow", "Options..."))
        self.connectButton.setText(_translate("MainWindow", "Connect"))
        self.refDockWidget.setWindowTitle(_translate("MainWindow", "References"))
        self.treeDockWidget.setWindowTitle(_translate("MainWindow", "Address Space"))
        self.logDockWidget.setWindowTitle(_translate("MainWindow", "Logs"))
        self.actionSubscribeDataChange.setText(_translate("MainWindow", "Subscribe to DataChange"))
        self.actionSubscribeDataChange.setToolTip(_translate("MainWindow", "Subscribe to data change from selected node"))
        self.actionUnsubscribeDataChange.setText(_translate("MainWindow", "Unsubscribe to DataChange"))
        self.actionUnsubscribeDataChange.setToolTip(_translate("MainWindow", "Unsubscribe to DataChange for current node"))
        self.actionSubscribeEvent.setText(_translate("MainWindow", "Subscribe to Events"))
        self.actionSubscribeEvent.setToolTip(_translate("MainWindow", "Subscribe to events from selected node"))
        self.actionUnsubscribeEvents.setText(_translate("MainWindow", "Unsubscribe to Events"))
        self.actionUnsubscribeEvents.setToolTip(_translate("MainWindow", "Unsubscribe to Events from current node"))
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
