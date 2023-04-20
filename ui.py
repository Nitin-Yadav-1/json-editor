
from PySide6.QtWidgets import (
    QMainWindow,
    QTabWidget,
    QMenu,
    QTreeWidget,
    QTreeWidgetItem,
    QTreeWidgetItemIterator,
    QCheckBox,
    QDialog,
    QDialogButtonBox,
    QVBoxLayout,
    QGridLayout,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QFontDialog
)

from PySide6.QtGui import (
    QFont,
    QAction
)


class UI(QMainWindow):
    def __init__(self):
        super().__init__()
        self._createProperties()
        self._setupMenuBar()
        self._setupToolBar()
        self.setWindowTitle("OpenFoam Case Editor")
        self.setGeometry(100,100,1000,500)
        self.setCentralWidget(self.tabList)
        self.tabList.setTabsClosable(True)
        self.show()

    def _createProperties(self):
        self.mainFont = self.font()
        self.tabFont = self.font()

        self.fileMenu = None
        self.editMenu = None
        self.viewMenu = None
        self.menuBar = self.menuBar()
        self.toolBar = self.addToolBar("")
        self.statusBar = self.statusBar()
        self.tabList = QTabWidget()
        
        # file menu actions
        self.newAction = QAction("&New", self)
        self.openAction = QAction("&Open", self)
        self.saveAction = QAction("&Save", self)
        self.saveAsAction = QAction("S&ave As", self)
        self.closeAction = QAction("&Close", self)

        # edit menu actions
        self.deleteAction = QAction("&Delete", self)
        self.insertAction = QAction("&Insert", self)
        self.replaceAction = QAction("&Replace", self)

        # view menu actions
        self.setMenuBarFontAction = QAction("Set &Menu Font", self)
        self.setBodyFontAction = QAction("Set &Body Font", self)

        # toolbar actions
        self.selectAllAction = QAction("Select All", self)
        self.unselectAllAction = QAction("Unselect All", self)
        self.collapseAllAction = QAction("Collapse All", self)
        self.expandAllAction = QAction("Expand All", self)

    def _setupMenuBar(self):
        # create 'File' menu
        self.fileMenu = self.menuBar.addMenu("&File")
        self.fileMenu.addAction(self.newAction)
        self.fileMenu.addAction(self.openAction)
        self.fileMenu.addAction(self.saveAction)
        self.fileMenu.addAction(self.saveAsAction)
        self.fileMenu.addAction(self.closeAction)
        
        # create 'Edit' menu
        self.editMenu = self.menuBar.addMenu("&Edit")
        self.editMenu.addAction(self.deleteAction)
        self.editMenu.addAction(self.insertAction)
        self.editMenu.addAction(self.replaceAction)
        
        # create 'View' menu
        self.viewMenu = self.menuBar.addMenu("&View")
        self.viewMenu.addAction(self.setMenuBarFontAction)
        self.viewMenu.addAction(self.setBodyFontAction)
        self.setMenuBarFontAction.triggered.connect(self.setMenuBarFontActionHandler)
        self.setBodyFontAction.triggered.connect(self.setBodyFontActionHandler)

    def _setupToolBar(self):
        self.toolBar.setMovable(False)
        self.toolBar.setFloatable(False)

        selectAllButton = QPushButton("Select All")
        self.selectAllAction.triggered.connect(self.selectAllActionHandler)
        selectAllButton.clicked.connect(self.selectAllAction.trigger)
        self.toolBar.addWidget(selectAllButton)
        self.toolBar.addSeparator()

        unselectAllButton = QPushButton("Unselect All")
        self.unselectAllAction.triggered.connect(self.unselectAllActionHandler)
        unselectAllButton.clicked.connect(self.unselectAllAction.trigger)
        self.toolBar.addWidget(unselectAllButton)
        self.toolBar.addSeparator()

        collapseAllButton = QPushButton("Collapse All")
        self.collapseAllAction.triggered.connect(self.collapseAllActionHandler)
        collapseAllButton.clicked.connect(self.collapseAllAction.trigger)
        self.toolBar.addWidget(collapseAllButton)
        self.toolBar.addSeparator()

        expandAllButton = QPushButton("Expand All")
        self.expandAllAction.triggered.connect(self.expandAllActionHandler)
        expandAllButton.clicked.connect(self.expandAllAction.trigger)
        self.toolBar.addWidget(expandAllButton)
        self.toolBar.addSeparator()

    def setMenuBarFontActionHandler(self) -> None:
        _, font = QFontDialog.getFont(self.mainFont, self, "Choose Font")
        self.mainFont = font
        self.setFont(self.mainFont)
        self.fileMenu.setFont(self.mainFont)
        self.editMenu.setFont(self.mainFont)
        self.viewMenu.setFont(self.mainFont)
        self.tabList.setFont(self.tabFont)

    def setBodyFontActionHandler(self) -> None:
        _, font = QFontDialog.getFont(self.tabFont, self, "Choose Font")
        self.tabFont = font
        self.tabList.setFont(self.tabFont)

    def selectAllActionHandler(self) -> None:
        self.setCheckedAllCurrentItems(True)

    def unselectAllActionHandler(self) -> None:
        self.setCheckedAllCurrentItems(False)

    def collapseAllActionHandler(self) -> None:
        self.setExpandedAllCurrentItems(False)

    def expandAllActionHandler(self) -> None:
        self.setExpandedAllCurrentItems(True)

    def getCurrentSelectedItems(self) -> list:
        selectedItems = []
        tree = self.tabList.currentWidget()
        itr = QTreeWidgetItemIterator(tree)
        while( itr.value() is not None ):
            item = itr.value()
            checkbox = tree.itemWidget(item,0)
            if( checkbox.isChecked() ):
                selectedItems.append(item)
            itr += 1
        return selectedItems

    def deleteCurrentSelectedItems(self) -> int:
        '''
        Delete selected items in the current tab.
        Returns the count of deleted items.
        '''
        tree = self.tabList.currentWidget()
        toDelete = self.getCurrentSelectedItems()
        
        if( len(toDelete) == 0 ):
            return 0

        # show confirm checkbox
        deletionAllowed = Dialog.deleteConfirmDialog(self, len(toDelete))

        if( not deletionAllowed ):
            return 0

        # delete in reverse so that child is deleted before parent
        root = tree.invisibleRootItem()
        for item in reversed(toDelete):
            ( item.parent() or root ).removeChild(item)

        return len(toDelete)

    def insertCurrentSelectedItems(self) -> int:
        '''
        Insert under selected items in current tab. If no item is selected insert at top-level.
        Return the count of new elements.
        '''
        if( self.tabList.count() == 0 ):
            return 0

        tree = self.tabList.currentWidget()
        selectedItems = self.getCurrentSelectedItems()
        if( len(selectedItems) == 0 ):
            selectedItems.append(tree.invisibleRootItem())

        # give multiple place insertion warning
        insertionAllowed = True
        if( len(selectedItems) > 1 ):
            insertionAllowed = Dialog.insertConfirmDialog(self, len(selectedItems))

        if( not insertionAllowed ):
            return 0

        # show dialog box for insertion
        pairs = Dialog.insertDialog(self)

        # insert into tree widget
        for item in selectedItems:
            item.setText(1,"")
            for pair in pairs:
                key,val = pair
                widget = QTreeWidgetItem()
                widget.setText(1,val)
                item.addChild(widget)
                checkbox = QCheckBox(key)
                checkbox.setAutoFillBackground(True)
                tree.setItemWidget(widget, 0, checkbox)

        return len(selectedItems) * len(pairs)

    def replaceCurrentSelectedItems(self) -> int:
        '''
        Replace the selected items in current tab.
        Return the count of items replaced.
        '''
        if( self.tabList.count() == 0 ):
            return 0

        tree = self.tabList.currentWidget()
        selected = self.getCurrentSelectedItems()
        if( len(selected) == 0 ):
            return 0

        # see staticmethod Dialog.replaceDialog for format of 'data'
        data = [0 for i in range(len(selected))]
        for index,item in enumerate(selected):
            if( item.childCount() == 0 ):
                keyText = tree.itemWidget(item,0).text()
                valText = item.text(1)
                data[index] = [keyText,valText,True]
            else:
                keyText = tree.itemWidget(item,0).text()
                data[index] = [keyText,"",False]

        Dialog.replaceDialog(self, data)
        for index,item in enumerate(selected):
            tree.itemWidget(item,0).setText(data[index][0])
            item.setText(1, data[index][1])

        return len(selected)

    def setCheckedAllCurrentItems(self, checked : bool) -> None:
        if( self.tabList.count() == 0 ):
            return

        tree = self.tabList.currentWidget()
        itr = QTreeWidgetItemIterator(tree)
        while( itr.value() is not None ):
            checkbox = tree.itemWidget(itr.value(),0)
            checkbox.setChecked(checked)
            itr += 1

    def setExpandedAllCurrentItems(self, expand : bool) -> None:
        if( self.tabList.count() == 0 ):
            return

        tree = self.tabList.currentWidget()
        itr = QTreeWidgetItemIterator(tree)
        while( itr.value() is not None ):
            item = itr.value()
            item.setExpanded(expand)
            itr += 1

    def createTab(self, tabName : str, tabData : dict) -> None:

        def recursive_build(treeWidget, curr, parent):
            if( type(curr) is not dict ):
                text = None
                if( type(curr) is list ):
                    text = ", ".join(map(str,curr))
                else:
                    text = str(curr)
                parent.setText(1,text)
                return

            for key, val in curr.items():
                w = QTreeWidgetItem([key])
                parent.addChild(w)
                recursive_build(treeWidget, val, w)
                
                checkbox = QCheckBox(key)
                checkbox.setAutoFillBackground(True)
                treeWidget.setItemWidget(w, 0, checkbox)

        treeWidget = QTreeWidget()
        treeWidget.setColumnCount(2)
        treeWidget.setHeaderLabels(["",""])

        for key,val in tabData.items():
            # create structure
            top = QTreeWidgetItem([key])
            treeWidget.addTopLevelItem(top)
            recursive_build(treeWidget, val, top)

            # create actual widget
            checkbox = QCheckBox(key)
            checkbox.setAutoFillBackground(True)
            treeWidget.setItemWidget(top, 0, checkbox)
            treeWidget.expandItem(top)

        self.tabList.addTab(treeWidget, tabName)

    def tabToDict(self, index : int) -> dict:

        def treeToDict(tree : QTreeWidget, currWidgetItem : QTreeWidgetItem) -> dict:
            resDict = {}

            for i in range(currWidgetItem.childCount()):
                child = currWidgetItem.child(i)
                key = tree.itemWidget(child, 0).text()
                val = None
                if( child.childCount() == 0 ):
                    val = child.text(1)
                else:
                    val = treeToDict(tree,child)
                resDict[key] = val

            return resDict

        tree = self.tabList.widget(index)
        return treeToDict(tree, tree.invisibleRootItem())

    def setTabName(self, index : int, tabName : str) -> None:
        self.tabList.setTabText(index, tabName)


class Dialog():
    @staticmethod
    def insertDialog(parent : UI) -> list:

        def acceptHandler():
            for row in range(1,grid.rowCount()):
                keyText = grid.itemAtPosition(row,0).widget().text()
                valText = grid.itemAtPosition(row,1).widget().text()
                if( keyText == "" or valText == ""):
                    continue
                pairs.append((keyText,valText))
            dlg.accept()

        def addField():
            row = grid.rowCount()
            grid.addWidget(QLineEdit(), row, 0)
            grid.addWidget(QLineEdit(), row, 1)

        pairs = []
        dlg = QDialog(parent)
        dlgLayout = QVBoxLayout(dlg)
        dlg.setWindowTitle("Insert")

        # create text edit fields
        grid = QGridLayout()
        addFieldButton = QPushButton("+")
        addFieldButton.clicked.connect(addField)
        grid.addWidget(addFieldButton, 0, 0, 1, 2)
        grid.addWidget(QLineEdit(), 1, 0)
        grid.addWidget(QLineEdit(), 1, 1)
        grid.addWidget(QLineEdit(), 2, 0)
        grid.addWidget(QLineEdit(), 2, 1)
        dlgLayout.addLayout(grid)

        # create buttons
        buttons = QDialogButtonBox()
        buttons.setStandardButtons(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(acceptHandler)
        buttons.rejected.connect(dlg.reject)
        dlgLayout.addWidget(buttons)

        dlg.setLayout(dlgLayout)
        dlg.exec()
        return pairs

    @staticmethod
    def replaceDialog(parent : UI, data : list) -> None:

        # data = [ [key,val,bool], [key,val,bool], ... ]
        # key = keyText
        # val = valText
        # bool = True(show both key-val pair), False(show only key) in dialog

        def acceptHandler():
            for row in range(grid.rowCount()):
                keyItem = grid.itemAtPosition(row,0)
                data[row][0] = keyItem.widget().text()
                
                valItem = grid.itemAtPosition(row,1)
                if( valItem is not None ):
                    data[row][1] = valItem.widget().text()

            dlg.accept()

        dlg = QDialog(parent)
        dlg.setWindowTitle("Replace Items")
        dlgLayout = QVBoxLayout()

        # create fields
        grid = QGridLayout()
        for index,itemData in enumerate(data):
            grid.addWidget(QLineEdit(itemData[0]), index, 0)
            if( itemData[2] ):
                grid.addWidget(QLineEdit(itemData[1]), index, 1)
        dlgLayout.addLayout(grid)

        # create buttons
        buttons = QDialogButtonBox()
        buttons.setStandardButtons(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(acceptHandler)
        buttons.rejected.connect(dlg.reject)
        dlgLayout.addWidget(buttons)

        dlg.setLayout(dlgLayout)
        dlg.exec()

    @staticmethod
    def deleteConfirmDialog(parent : UI, count : int) -> bool:
        selectedButton = QMessageBox.warning(
            parent,
            "Confirm Delete",
            f"{count} items and their sub-items will be deleted!",
            (QMessageBox.Ok | QMessageBox.Cancel),
            QMessageBox.Cancel
        )

        return (selectedButton == QMessageBox.Ok)

    @staticmethod
    def insertConfirmDialog(parent : UI, count : int) -> bool:
        selectedButton = QMessageBox.warning(
            parent,
            "Multiple Insert",
            f"New items will be inserted under {count} items!",
            (QMessageBox.Ok | QMessageBox.Cancel),
            (QMessageBox.Cancel)
        )

        return (selectedButton == QMessageBox.Ok)