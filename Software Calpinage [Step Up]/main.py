#from gui import interface,selectorButton,buttonCommand,menuBar
from gui.gui import GUI
from utils import variables
from tests import nameOfFunctionCalled as tst
import datetime

class Main:
    def __init__(self):
        pass

    def create(self):
        classSharedVariable = variables.SharedVariables()
        classSharedVariable.filePath = "data/BackUp.sade"
        classSharedVariable.fileName = self.generate_default_filename()

        return GUI(classSharedVariable.fileName).mainWindow

    def generate_default_filename(self):
        now = datetime.datetime.now()
        formatted_date = now.strftime("%d.%m.%Y_%H.%M")
        return formatted_date

if __name__ == "__main__":
    app = Main().create()  # Appelez la méthode create() de l'instance
    app.mainloop()
    

    
