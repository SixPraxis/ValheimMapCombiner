def combineMaps(combinePins, removeOverlappingPins, targetWorldKey, saveDataList):
    explored = bytearray([0] * 4194304)
    pinArray = []
    worldInSaveDict = {}
    for save in saveDataList:
        worldFound = False
        for world in save.worlds:
            if targetWorldKey.to_bytes(8, 'little') == world.worldKey:
                worldInSaveDict[save] = world
                worldFound = True
                break

        if not worldFound:
            return False, 'World ID ' + str(targetWorldKey) + ' not found in save file!'

    for index in range(0, len(explored) - 1):
        for saveData in worldInSaveDict:
            if worldInSaveDict[saveData].mapData.explored[index] != 0:
                explored[index] = True

    if combinePins:
        if removeOverlappingPins:
            for save in saveDataList:
                for world in save.worlds:
                    if targetWorldKey.to_bytes(8, 'little') == world.worldKey:
                        for pin in world.mapData.pins:
                            collisions = 0
                            for arrayPin in pinArray:
                                if abs(pin[1] - arrayPin[1]) < 6 and abs(pin[2] - arrayPin[2]) < 6:
                                    collisions += 1
                            if collisions == 0:
                                pinArray.append(pin)
        else:
            for save in saveDataList:
                for world in save.worlds:
                    if targetWorldKey.to_bytes(8, 'little') == world.worldKey:
                        for pin in world.mapData.pins:
                            pinArray.append(pin)

    for save in saveDataList:
        for world in save.worlds:
            if targetWorldKey.to_bytes(8, 'little') == world.worldKey:
                world.mapData.explored = explored
                world.mapData.pins = pinArray

    return True, 'Maps updated!'
