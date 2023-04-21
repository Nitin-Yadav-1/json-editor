
import json


class TabData:
    def __init__(self, filePath=""):
        self.filePath = filePath
        self.areChangesSaved = True


class Model:
    def __init__(self):
        self.tabDataList = []

    def newFile(self) -> None:
        self.tabDataList.append(TabData(""))

    def openFile(self, filePath : str) -> dict:
        with open(filePath) as f:
            text = f.read()
        fileDataDict = json.loads(text)
        self.tabDataList.append(TabData(filePath))
        return fileDataDict

    def saveFile(self, index : int, dataDict : dict) -> None:
        with open(self.tabDataList[index].filePath, "w") as f:
            f.write(json.dumps(dataDict, indent=4))
        self.setChangesSaved(True, index)

    def saveAsFile(self, index : int, dataDict : dict, filePath : str) -> None:
        with open(filePath, "w") as f:
            f.write(json.dumps(dataDict, indent=4))
        if( self.isUntitledFile(index) ):
            self.tabDataList[index].filePath = filePath
            self.setChangesSaved(True, index)

    def isUntitledFile(self, index : int) -> bool:
        return ( self.tabDataList[index].filePath == "" )

    def setChangesSaved(self, changesSaved : bool, index : int) -> None:
        self.tabDataList[index].areChangesSaved = changesSaved

    def areChangesSaved(self, index : int) -> bool:
        return self.tabDataList[index].areChangesSaved

    def filePath(self, index : int) -> str:
        return self.tabDataList[index].filePath

    def isFileOpen(self, filePath : str) -> bool:
        for tabData in self.tabDataList:
            if( tabData.filePath == filePath ):
                return True
        return False

    def closeFile(self, index : int) -> None:
        self.tabDataList.pop(index)