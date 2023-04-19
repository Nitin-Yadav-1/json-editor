
import sys
import os 

from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QMessageBox
)

from ui import UI
from model import Model

# GLOBALS
CURR_DIR = os.path.dirname(os.path.realpath(__file__))


class CaseEditor:
    def __init__(self):
        self._createProperties()
        self._createConnections()
        
    def _createProperties(self):
        self.app = QApplication([])
        self.model = Model()
        self.ui = UI()

    def run(self):
        sys.exit(self.app.exec())

    def _createConnections(self):
        self.ui.tabList.tabCloseRequested.connect(self.tabClose)

        # fileMenu actions
        self.ui.newAction.triggered.connect(self.newActionHandler)
        self.ui.openAction.triggered.connect(self.openActionHandler)
        self.ui.saveAction.triggered.connect(self.saveActionHandler)
        self.ui.saveAsAction.triggered.connect(self.saveAsActionHandler)
        self.ui.closeAction.triggered.connect(self.closeActionHandler)

        # editMenu actions
        self.ui.deleteAction.triggered.connect(self.deleteActionHandler)
        self.ui.insertAction.triggered.connect(self.insertActionHandler)
        self.ui.replaceAction.triggered.connect(self.replaceActionHandler)

        # toolbar actions
        self.ui.selectAllAction.triggered.connect(self.selectAllActionHandler)
        self.ui.unselectAllAction.triggered.connect(self.unselectAllActionHandler)
        self.ui.collapseAllAction.triggered.connect(self.collapseAllActionHandler)
        self.ui.expandAllAction.triggered.connect(self.expandAllActionHandler)

    def deleteActionHandler(self):
        currIndex = self.ui.tabList.currentIndex()
        if( currIndex < 0 ):
            return
        deletionCount = self.ui.deleteCurrentSelectedItems()
        if( deletionCount > 0 ):
            self.model.setChangesSaved(False, currIndex)

    def insertActionHandler(self):
        currIndex = self.ui.tabList.currentIndex()
        if( currIndex < 0 ):
            return
        insertionCount = self.ui.insertCurrentSelectedItems()
        if( insertionCount > 0 ):
            self.model.setChangesSaved(False, currIndex)

    def replaceActionHandler(self):
        currIndex = self.ui.tabList.currentIndex()
        if( currIndex < 0 ):
            return
        replaceCount = self.ui.replaceCurrentSelectedItems()
        if( replaceCount > 0 ):
            self.model.setChangesSaved(False, currIndex)

    def selectAllActionHandler(self):
        self.ui.setCheckedAllCurrentItems(True)

    def unselectAllActionHandler(self):
        self.ui.setCheckedAllCurrentItems(False)

    def collapseAllActionHandler(self):
        self.ui.setExpandedAllCurrentItems(False)

    def expandAllActionHandler(self):
        self.ui.setExpandedAllCurrentItems(True)

    def tabClose(self, index):
        if( self.model.isUntitledFile(index) ):
            dlg = QMessageBox(self.ui)
            dlg.setWindowTitle("Unsaved Files")
            dlg.setText("All progress made in unsaved files will be lost!")
            dlg.setStandardButtons(QMessageBox.Cancel | QMessageBox.Discard)
            dlg.setIcon(QMessageBox.Warning)
            button = dlg.exec()

            if( button == QMessageBox.Discard ):
                self.model.closeFile(index)
                self.ui.tabList.removeTab(index)
        else:
            self.model.saveFile(index, self.ui.tabToDict(index))
            self.model.closeFile(index)
            self.ui.tabList.removeTab(index)

    def newActionHandler(self):
        self.model.newFile()
        self.ui.createTab("untitled", {})

    def openActionHandler(self):
        filePath, _ = QFileDialog.getOpenFileName(
            self.ui, 
            "Open Case File", 
            CURR_DIR, 
            "Text files ( *.json )",
        )

        if( filePath != "" ):
            tabName = filePath.split("/")[-1]
            tabData = self.model.openFile(filePath)
            self.ui.createTab(tabName, tabData)

    def saveActionHandler(self):
        currIndex = self.ui.tabList.currentIndex()
        if( currIndex == -1 ):
            return

        if( self.model.isUntitledFile(currIndex) ):
            self.saveAsActionHandler()
        else:
            self.model.saveFile(currIndex, self.ui.tabToDict(currIndex))

    def saveAsActionHandler(self):
        currIndex = self.ui.tabList.currentIndex()
        if( currIndex == -1 ):
            return

        filePath, _ = QFileDialog.getSaveFileName(
            self.ui,
            CURR_DIR,
            "",
            "Text Files(*.json)"
        )
        
        if( filePath != "" ):
            currIndex = self.ui.tabList.currentIndex()
            dataDict = self.ui.tabToDict(currIndex)
            self.model.saveAsFile(currIndex, dataDict, filePath)
            self.ui.setTabName(currIndex, filePath.split("/")[-1])

    def closeActionHandler(self):
        self.ui.close()
        # # maybe we can attempt to save and close all files before closing

        # # check for updated file
        # unsavedFilesExist = False
        # closeWindow = True

        # for tab in self.model.tabDataList:
        #     if( tab.isChanged ):
        #         unsavedFilesExist = True
        #         break

        # if( unsavedFilesExist ):
        #     dlg = QMessageBox(self.ui)
        #     dlg.setWindowTitle("Unsaved Files")
        #     dlg.setText("All progress made in unsaved files will be lost!")
        #     dlg.setStandardButtons(QMessageBox.Cancel | QMessageBox.Discard)
        #     dlg.setIcon(QMessageBox.Warning)
        #     button = dlg.exec()

        #     if( button == QMessageBox.Cancel ):
        #         closeWindow = False

        # # close window
        # if( closeWindow ):
        #     self.ui.close()


if __name__ == "__main__":
    editor = CaseEditor()
    editor.run()