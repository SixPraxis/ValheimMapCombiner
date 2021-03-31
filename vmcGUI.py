import PySimpleGUI as gui
from vmcSaveData import createSaveData
from vmcSaveData import writeSaveDataFile
from vmcCombiner import combineMaps

title = 'Valheim Map Combiner'
version = '1.0.0'
gui.theme('LightGrey3')

layout = [[gui.Text('Valheim Map Combiner', font=('Helvetica', 20), justification="center", auto_size_text=True)],
        [gui.Text('1.', size=(2, 1)), gui.Input(key='input1Key'), gui.FileBrowse()],
        [gui.Text('2.', size=(2, 1)), gui.Input(key='input2Key'), gui.FileBrowse()],
        [gui.Text('3.', size=(2, 1)), gui.Input(key='input3Key'), gui.FileBrowse()],
        [gui.Text('4.', size=(2, 1)), gui.Input(key='input4Key'), gui.FileBrowse()],
        [gui.Text('5.', size=(2, 1)), gui.Input(key='input5Key'), gui.FileBrowse()],
        [gui.Text('6.', size=(2, 1)), gui.Input(key='input6Key'), gui.FileBrowse()],
        [gui.Text('7.', size=(2, 1)), gui.Input(key='input7Key'), gui.FileBrowse()],
        [gui.Text('8.', size=(2, 1)), gui.Input(key='input8Key'), gui.FileBrowse()],
        [gui.Text('9.', size=(2, 1)), gui.Input(key='input9Key'), gui.FileBrowse()],
        [gui.Text('10.', size=(2, 1)), gui.Input(key='input10Key'), gui.FileBrowse()],
        [gui.Text('World ID:'), gui.Combo('', size=(24, 1), key='worldIDKey'), gui.Button('Find Common IDs', key='findCommonKey')],
        [gui.Checkbox('Combine Pins', enable_events = True, key='combinePinsKey')],
        [gui.Checkbox('Remove Overlapping Pins', disabled = True, enable_events = True, key='removeOverlapKey')],
        [gui.Submit('Submit')],
]

keyArray = ['input1Key', 'input2Key', 'input3Key', 'input4Key',
    'input5Key', 'input6Key', 'input7Key', 'input8Key', 
    'input9Key', 'input10Key']

def startGUI():
    window = gui.Window(title + ' ' + version, layout, margins=(10,10), finalize=True)
    saves = []

    while True:
        event, values = window.read()
        
        if event == 'findCommonKey':
            window['worldIDKey'].update(values=getCommonIDs(loadSaves(values)))

        if event == 'combinePinsKey':
            window['removeOverlapKey'].update(disabled = False)

        if event == 'Submit':
            saves = loadSaves(values)
            out, message = combineMaps(values['combinePinsKey'], values['removeOverlapKey'], values['worldIDKey'], saves)
            if out:
                writeSaves(saves, values)
                gui.popup_ok(message)
            else:
                errorPopup(message)
        if event == gui.WIN_CLOSED or event == 'Exit':
            break

def loadSaves(values):
    saveDataArray = []
    
    for key in keyArray:
        if values[key] != '':
            saveData = createSaveData(values[key])
            if saveData != None:
                saveDataArray.append(saveData)

    return saveDataArray

def writeSaves(saves, values):
    index = 0
    for save in saves:
        writeSaveDataFile(save, values[keyArray[index]])
        index += 1

def getCommonIDs(saveDataArray):
    worldKeys = {}
    for saveData in saveDataArray:
        for world in saveData.worlds:
            try:
                worldKeys[world.worldKey] += 1
            except:
                worldKeys[world.worldKey] = 1

    commonKeys = [int.from_bytes(key, 'little') for key in worldKeys if worldKeys[key] == len(saveDataArray)]
    if len(commonKeys) == 0:
        errorPopup('No common world IDs were found!')

    return commonKeys

def errorPopup(errorMessage):
    gui.popup_error(customError(errorMessage))

class customError(Exception):
    def __init__(self, message):
        if message:
            self.message = message
        else:
            self.message = "Error"
    
    def __str__(self):
        return self.message
