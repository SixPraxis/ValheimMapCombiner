from vmcUtils import loadSaveFile
from vmcUtils import writeSaveFile
from vmcUtils import backupSaveFile

class VmcSaveData:
    def __init__(self, saveFileData):
        self.data1 = saveFileData[0]
        self.worldCount = saveFileData[1]
        self.worlds = [VmcWorld(world) for world in saveFileData[2]]
        self.data2 = saveFileData[3]

class VmcWorld:
    def __init__(self, world):
        self.worldKey = world[0]
        self.worldData1 = world[1]
        self.mapDataBool = world[2]
        self.mapDataLength = world[3]
        self.mapData = VmcMapData(world[4])

class VmcMapData:
    def __init__(self, mapData):
        self.num1 = mapData[0]
        self.num2 = mapData[1]
        self.explored = mapData[2]
        self.pinCount = mapData[3]
        self.pins = mapData[4]
        self.publicRef = None
        if self.num1 >= 4:
            self.publicRef = mapData[5]

def createSaveData(path):
    saveData = None
    saveFileData = loadSaveFile(path)
    if saveFileData != None:
        saveData = VmcSaveData(saveFileData)
    return saveData

def writeSaveDataFile(saveData, path):
    backupSaveFile(path)
    writeSaveFile(saveData, path)
