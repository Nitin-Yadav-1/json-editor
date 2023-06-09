
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
    QFontDialog,
    QWidget,
    QHBoxLayout,
    QLabel
)

from PySide6.QtGui import (
    QFont,
    QAction,
    QKeySequence
)

import parser


class UI(QMainWindow):
    def __init__(self):
        super().__init__()
        self._createProperties()
        self._setShortcuts()
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
        self.shortcutsAction = QAction("Shortcuts", self)

        # edit menu actions
        self.deleteAction = QAction("&Delete", self)
        self.insertAction = QAction("&Insert", self)
        self.replaceAction = QAction("&Replace", self)

        # view menu actions
        self.setMenuBarFontAction = QAction("Set &Menu Font", self)
        self.setBodyFontAction = QAction("Set &Body Font", self)
        self.hideValuesAction = QAction("&Hide Values", self)
        self.showValuesAction = QAction("&Show Values", self)

        # toolbar actions
        self.selectAllAction = QAction("Select All", self)
        self.unselectAllAction = QAction("Unselect All", self)
        self.collapseAllAction = QAction("Collapse All", self)
        self.expandAllAction = QAction("Expand All", self)

    def _setShortcuts(self):
        self.newAction.setShortcut(QKeySequence.New) # Ctrl+N
        self.openAction.setShortcut(QKeySequence.Open) # Ctrl+O 
        self.saveAction.setShortcut(QKeySequence.Save) # Ctrl+S
        self.saveAsAction.setShortcut(QKeySequence.SaveAs) # Ctrl+Shift+S

        self.deleteAction.setShortcut(QKeySequence.Delete) # del, Ctrl+D
        self.insertAction.setShortcut(QKeySequence("Ctrl+I"))
        self.replaceAction.setShortcut(QKeySequence("Ctrl+R"))

        self.selectAllAction.setShortcut(QKeySequence.SelectAll) # Ctrl+A
        self.unselectAllAction.setShortcut(QKeySequence("Ctrl+Shift+A"))
        self.collapseAllAction.setShortcut(QKeySequence("Ctrl+Tab"))
        self.expandAllAction.setShortcut(QKeySequence("Ctrl+Shift+Tab"))

        self.hideValuesAction.setShortcut(QKeySequence("Ctrl+Shift+V"))
        self.showValuesAction.setShortcut(QKeySequence("Ctrl+Shift+B"))

    def _setupMenuBar(self):
        # create 'File' menu
        self.fileMenu = self.menuBar.addMenu("&File")
        self.fileMenu.addAction(self.newAction)
        self.fileMenu.addAction(self.openAction)
        self.fileMenu.addAction(self.saveAction)
        self.fileMenu.addAction(self.saveAsAction)
        self.fileMenu.addAction(self.shortcutsAction)
        self.fileMenu.addAction(self.closeAction)
        self.shortcutsAction.triggered.connect(self.shortcutsActionHandler)
        
        # create 'Edit' menu
        self.editMenu = self.menuBar.addMenu("&Edit")
        self.editMenu.addAction(self.deleteAction)
        self.editMenu.addAction(self.insertAction)
        self.editMenu.addAction(self.replaceAction)
        
        # create 'View' menu
        self.viewMenu = self.menuBar.addMenu("&View")
        self.viewMenu.addAction(self.setMenuBarFontAction)
        self.viewMenu.addAction(self.setBodyFontAction)
        self.viewMenu.addAction(self.hideValuesAction)
        self.viewMenu.addAction(self.showValuesAction)
        self.setMenuBarFontAction.triggered.connect(self.setMenuBarFontActionHandler)
        self.setBodyFontAction.triggered.connect(self.setBodyFontActionHandler)
        self.hideValuesAction.triggered.connect(self.hideValuesActionHandler)
        self.showValuesAction.triggered.connect(self.showValuesActionHandler)

    def _setupToolBar(self):
        self.toolBar.setMovable(False)
        self.toolBar.setFloatable(False)

        self.toolBar.addAction(self.selectAllAction)
        self.selectAllAction.triggered.connect(self.selectAllActionHandler)
        self.toolBar.addSeparator()

        self.toolBar.addAction(self.unselectAllAction)
        self.unselectAllAction.triggered.connect(self.unselectAllActionHandler)
        self.toolBar.addSeparator()

        self.toolBar.addAction(self.collapseAllAction)
        self.collapseAllAction.triggered.connect(self.collapseAllActionHandler)
        self.toolBar.addSeparator()

        self.toolBar.addAction(self.expandAllAction)
        self.expandAllAction.triggered.connect(self.expandAllActionHandler)

    def shortcutsActionHandler(self) -> None:
        Dialog.showShortcuts(self)

    def hideValuesActionHandler(self) -> None:
        self.setCurrentValuesVisibility(False)

    def showValuesActionHandler(self) -> None:
        self.setCurrentValuesVisibility(True)

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
            tree.removeItemWidget(item, 1)
            for pair in pairs:
                key,val = pair
                widget = QTreeWidgetItem()
                item.addChild(widget)

                keyWidget = QCheckBox(key)
                tree.setItemWidget(widget, 0, keyWidget)

                valWidget = QWidget()
                label = QLabel(val)
                layout = QHBoxLayout(valWidget)
                layout.setContentsMargins(0,0,0,0)
                layout.addWidget(label)
                tree.setItemWidget(widget, 1, valWidget)

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
                valText = tree.itemWidget(item,1).layout().itemAt(0).widget().text()
                data[index] = [keyText,valText,True]
            else:
                keyText = tree.itemWidget(item,0).text()
                data[index] = [keyText,"",False]

        Dialog.replaceDialog(self, data)
        for index,item in enumerate(selected):
            tree.itemWidget(item,0).setText(data[index][0])
            if( item.childCount() == 0 ):
                tree.itemWidget(item,1).layout().itemAt(0).widget().setText(data[index][1])

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

    def setCurrentValuesVisibility(self, visible : bool) -> None:
        if( self.tabList.count() == 0 ):
            return

        tree = self.tabList.currentWidget()
        itr = QTreeWidgetItemIterator(tree)
        while( itr.value() is not None ):
            item = itr.value()
            if( item.childCount() != 0 ):
                itr += 1
                continue

            valLabel = tree.itemWidget(item,1).layout().itemAt(0).widget()
            if( visible ):
                valLabel.show()
            else:
                valLabel.hide()
            itr += 1

    def createTab(self, tabName : str, tabData : dict) -> None:

        def recursiveBuild(root : QTreeWidgetItem, data : dict) -> None:
            for key,val in data.items():
                item = QTreeWidgetItem()
                root.addChild(item)
                if( type(val) is dict ):
                    recursiveBuild(item, val)
                else:
                    text = parser.toText(val)
                    container = QWidget()
                    layout = QHBoxLayout(container)
                    layout.setContentsMargins(0,0,0,0)
                    valLabel = QLabel(text)
                    layout.addWidget(valLabel)
                    tree.setItemWidget(item, 1, container)

                tree.setItemWidget(item, 0, QCheckBox(key))
                item.setExpanded(True)
        
        tree = QTreeWidget()
        tree.setColumnCount(2)
        tree.setHeaderLabels(["",""])
        root = tree.invisibleRootItem()
        recursiveBuild(root, tabData)

        self.tabList.addTab(tree, tabName)

    def tabToDict(self, index : int) -> dict:

        def treeToDict(tree : QTreeWidget, currWidgetItem : QTreeWidgetItem) -> dict:
            resDict = {}

            for i in range(currWidgetItem.childCount()):
                child = currWidgetItem.child(i)
                key = tree.itemWidget(child, 0).text()
                val = None
                if( child.childCount() == 0 ):
                    val = tree.itemWidget(child,1).layout().itemAt(0).widget().text()
                    val = parser.toJSONValue(val)
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

    @staticmethod
    def showShortcuts(parent : UI) -> None:
        dlg = QDialog(parent)
        dlg.setWindowTitle("Shortcuts")
        dlg.setGeometry(400,400,300,100)
        layout = QGridLayout(dlg)
        
        shortcuts = [
            ("New", "Ctrl + N"),
            ("Open", "Ctrl + O"),
            ("Save", "Ctrl + S"),
            ("Save As", "Ctrl + Shift + S"),
            ("Delete", "del"),
            ("Insert", "Ctrl + I"),
            ("Replace", "Ctrl + R"),
            ("Select All", "Ctrl + A"),
            ("Unselect All", "Ctrl + Shift + A"),
            ("Collapse All", "Ctrl + Tab"),
            ("Expand All", "Ctrl + Shift + Tab"),
            ("Hide Values", "Ctrl + Shift + V"),
            ("Show Values", "Ctrl + Shift + B")
        ]

        for row,item in enumerate(shortcuts):
            layout.addWidget(QLabel(item[0]), row, 0)
            layout.addWidget(QLabel(item[1]), row, 1)

        dlg.exec()