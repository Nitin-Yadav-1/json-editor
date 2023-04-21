
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
TEMP_MSG_TIMEOUT = 3000


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

    def deleteActionHandler(self):
        currIndex = self.ui.tabList.currentIndex()
        if( currIndex < 0 ):
            return
        deletionCount = self.ui.deleteCurrentSelectedItems()
        if( deletionCount > 0 ):
            self.model.setChangesSaved(False, currIndex)
        self.ui.statusBar.showMessage(f"{deletionCount} items deleted.", TEMP_MSG_TIMEOUT)

    def insertActionHandler(self):
        currIndex = self.ui.tabList.currentIndex()
        if( currIndex < 0 ):
            return
        insertionCount = self.ui.insertCurrentSelectedItems()
        if( insertionCount > 0 ):
            self.model.setChangesSaved(False, currIndex)
        self.ui.statusBar.showMessage(f"{insertionCount} items inserted.", TEMP_MSG_TIMEOUT)

    def replaceActionHandler(self):
        currIndex = self.ui.tabList.currentIndex()
        if( currIndex < 0 ):
            return
        replaceCount = self.ui.replaceCurrentSelectedItems()
        if( replaceCount > 0 ):
            self.model.setChangesSaved(False, currIndex)
        self.ui.statusBar.showMessage(f"{replaceCount} items replaced.", TEMP_MSG_TIMEOUT)

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
            if( not self.model.areChangesSaved(index) ):
                selected = QMessageBox.warning(
                    self.ui,
                    "Save changes",
                    "Save changes before closing the file?",
                    (QMessageBox.Ok | QMessageBox.Cancel | QMessageBox.Discard),
                    QMessageBox.Cancel
                )
                if( selected == QMessageBox.Cancel):
                    return
                if( selected == QMessageBox.Ok):
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

        if( filePath == "" ):
            return

        if( self.model.isFileOpen(filePath) ):
            return
    
        tabName = filePath.split("/")[-1]
        tabData = self.model.openFile(filePath)
        self.ui.createTab(tabName, tabData)
        self.ui.statusBar.showMessage(f"File opened : {filePath}", TEMP_MSG_TIMEOUT)

    def saveActionHandler(self):
        currIndex = self.ui.tabList.currentIndex()
        if( currIndex == -1 ):
            return

        if( self.model.isUntitledFile(currIndex) ):
            self.saveAsActionHandler()
        else:
            self.model.saveFile(currIndex, self.ui.tabToDict(currIndex))
            filePath = self.model.filePath(currIndex)
            self.ui.statusBar.showMessage(f"File saved : {filePath}", TEMP_MSG_TIMEOUT)

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

        if( filePath == "" ):
            return

        if( self.model.isUntitledFile(currIndex) ):
            self.ui.setTabName(currIndex, filePath.split("/")[-1])
            
        dataDict = self.ui.tabToDict(currIndex)
        self.model.saveAsFile(currIndex, dataDict, filePath)
        self.ui.statusBar.showMessage(f"File Saved As : {filePath}", TEMP_MSG_TIMEOUT)

    def closeActionHandler(self):
        self.ui.close()


if __name__ == "__main__":
    editor = CaseEditor()
    editor.run()