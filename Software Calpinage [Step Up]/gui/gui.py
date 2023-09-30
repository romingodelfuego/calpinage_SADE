import tkinter as tk
class GUI:
    def __init__(self,windowName)->tk:
        self.mainWindow=self.create(windowName)
        self.tkinterObjects={"mainWindow":self.mainWindow}

    def create(self,windowName):
        mainWindow=tk.Tk()
        mainWindow.title(f"SADE - CALPINAGE - {windowName}")
        window_width = mainWindow.winfo_screenwidth()
        window_height = mainWindow.winfo_screenheight()
        mainWindow.geometry(f"{window_width}x{window_height}+0+0")
        return mainWindow
    
    class BIND:
        def function(self,):
            pass
    def refresh(self,):
        pass

    def addToArborescence(self,child_name:str,child_value:tk):
        self.tkinterObjects[str(child_name)]=child_value