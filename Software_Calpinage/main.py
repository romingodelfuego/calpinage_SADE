from gui import interface,selectorButton,buttonCommand
from gui.menu import menu
from utils import variables
from tests import nameOfFunctionCalled as tst
import sys
import os

#https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def main():
    classSharedVariable = variables.SharedVariables()
    varSetMethod = classSharedVariable.set_variable

    mainWindow=interface.createMainWindow(classSharedVariable.fileName)
    leftFrame,infoPieceFrame,middleFrame,bottomFrame=interface.separateMainWindow(mainWindow,classSharedVariable)
    selectorFrame = interface.createSelectorFrame(leftFrame)
    
    buttonFrame = interface.createBoutonFrame(leftFrame)
    selectorButton.createSelector(selectorFrame,middleFrame,bottomFrame,infoPieceFrame,classSharedVariable,varSetMethod,buttonFrame,buttonCommand.command)
    menu.createMenu(mainWindow,leftFrame,infoPieceFrame,middleFrame,bottomFrame,selectorFrame,buttonFrame,classSharedVariable)
    classSharedVariable.tkinterObject["mainWindow"]=mainWindow
    classSharedVariable.tkinterObject["leftFrame"]=leftFrame
    classSharedVariable.tkinterObject["infoPieceFrame"]=infoPieceFrame
    classSharedVariable.tkinterObject["middleFrame"]=middleFrame
    classSharedVariable.tkinterObject["bottomFrame"]=bottomFrame
    classSharedVariable.tkinterObject["selectorFrame"]=selectorFrame
    classSharedVariable.tkinterObject["buttonFrame"]=buttonFrame
    return mainWindow

if __name__ == "__main__":
    app=main()
    app.mainloop()
    

    
