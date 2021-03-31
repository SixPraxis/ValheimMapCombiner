import struct
from hashlib import sha512
from shutil import copyfile
from time import time_ns

def loadSaveFile(path):
    saveFileData = None
    with open(path, 'rb') as file:
        saveFileData = readSaveFile(file)
    return saveFileData


def readSaveFile(file):
    file.read(4) #File length in bytes, without SHA512 hash
    data1 = file.read(20)
    worldCount = file.read(4)
    worlds = []

    for __ in range(int.from_bytes(worldCount, 'little')):
        worldKey = file.read(8)
        worldData1 = file.read(51)
        mapDataBool = file.read(1)
        mapDataLength = file.read(4)
        mapData = file.read(int.from_bytes(mapDataLength, 'little'))

        mapData = parseMapData(mapData)
        
        worldData = [worldKey, worldData1, mapDataBool, mapDataLength, mapData]
        worlds.append(worldData)

    data2 = file.read()
    data2 = data2[:-64] #Remove SHA512 hash from end of data

    saveFileData = [data1, worldCount, worlds, data2]
    return saveFileData

def parseMapData(mapData):
    num, num2 = struct.unpack_from('<II', mapData, 0)
    mapSize = num2 * num2
    offset = struct.calcsize('<II')
    mapGrid = struct.unpack_from(str(mapSize) + 's', mapData, offset)[0]
    offset += struct.calcsize(str(mapSize) + 's')
    pinCount = struct.unpack_from('<I', mapData, offset)[0]
    offset += struct.calcsize('<I')
    pinArray = []
    for __ in range(0, pinCount):
        formatString = '<'
        formatString = addStringToFormat(formatString, mapData, offset)
        formatString += 'fffI?'
        pinName, posX, posY, posZ, pinType, isChecked = struct.unpack_from(formatString, mapData, offset)
        pin = [pinName[1::].decode(), posX, posY, posZ, pinType, isChecked]
        pinArray.append(pin)
        offset += struct.calcsize(formatString)

    if num >= 4:
        publicReference = struct.unpack_from('<?', mapData, offset)[0]
        mapDataArray = [num, num2, mapGrid, pinCount, pinArray, publicReference]
    else:
        mapDataArray = [num, num2, mapGrid, pinCount, pinArray]

    return mapDataArray

def addStringToFormat(formatString, buffer, offset):
    stringLength = int.from_bytes(buffer[offset:offset + 1], 'little')
    formatString += str(stringLength + 1) + 's'
    return formatString

def stringEncoder(string):
    length = len(string)
    pattern = 'B' + str(int(length)) + 's'
    string = string.encode('utf-8')
    return pattern, length, string

def backupSaveFile(path):
    copyPath = path + '.' + str(time_ns()) + '.BACKUP'
    copyfile(path, copyPath)

def writeSaveFile(saveData, path):
    data1 = saveData.data1
    worldCount = saveData.worldCount

    worldByteArray = bytearray()
    for world in saveData.worlds:
        worldKey = world.worldKey
        worldData2 = struct.pack('<II', world.mapData.num1, world.mapData.num2)
        worldData3 = world.mapData.explored
        worldData4 = struct.pack('<I', len(world.mapData.pins))
        worldData5 = bytearray()
        for pin in world.mapData.pins:
            pinNamePattern, pinNameInt, pinName = stringEncoder(pin[0])
            worldData5 += struct.pack('<' + pinNamePattern + 'fffI?', pinNameInt, pinName, pin[1], pin[2], pin[3], pin[4], pin[5])
        pubRef = world.mapData.publicRef
        worldData6 = b''
        if world.mapData.num1 >= 4:
            worldData6 = struct.pack('<?', pubRef)
        world.mapDataLength = len(worldData2 + worldData3 + worldData4 + worldData5 + worldData6)
        worldData0 = struct.pack('<?I', world.mapDataBool, world.mapDataLength)
        worldByteArray += worldKey + world.worldData1 + worldData0 + worldData2 + worldData3 + worldData4 + worldData5 + worldData6

        data2 = saveData.data2

    opener = struct.pack('<I', len(data1 + worldCount + worldByteArray + data2))
    h = sha512()
    h.update(data1 + worldCount + worldByteArray + data2)
    sha512hash = h.hexdigest().encode('utf-8')
    
    with open(path, 'wb') as file:
        file.write(opener)
        file.write(data1)
        file.write(worldCount)
        file.write(worldByteArray)
        file.write(data2)
        file.write(struct.pack('<I', 64))
        file.write(sha512hash)
