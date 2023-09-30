import tkinter as tk
from gui.menuBar.bind import * 
from tests import nameOfFunctionCalled as tst
from utils import variables
from gui.gui import tkinterObject
print('INIT FAIT')
@tst.show_function_name
def initialize():
    mainWindow = tkinterObject.mainWindow
    leftFrame= tkinterObject.leftFrame
    infoPieceFrame= tkinterObject.infoPieceFrame
    middleFrame= tkinterObject.middleFrame
    bottomFrame= tkinterObject.bottomFrame
    selectorFrame= tkinterObject.selectorFrame
    buttonFrame= tkinterObject.buttonFrame

    sharedVar= variables

    menu_bar = tk.Menu(mainWindow)
    menu_file = tk.Menu(menu_bar, tearoff=0)
    menu_file.add_command(label="New", underline=0, accelerator="CTRL+N", command=lambda:new_document(mainWindow,leftFrame,infoPieceFrame,middleFrame,bottomFrame,selectorFrame,buttonFrame,sharedVar))
    menu_file.add_separator()
    menu_file.add_command(label="Open...", underline=0, accelerator="CTRL+O", command=lambda:open_file(mainWindow,leftFrame,infoPieceFrame,middleFrame,bottomFrame,selectorFrame,buttonFrame,sharedVar))
    menu_file.add_command(label="Save", underline=0, accelerator="CTRL+S", command=lambda:save_document(sharedVar))
    menu_file.add_command(label="Save as", underline=0, accelerator="CTRL+SHIFT+S", command=lambda:save_as_document(sharedVar))
    menu_file.add_separator()
    menu_file.add_command(label="Import DataBase", accelerator="CTRL+SHIFT+I",underline=0, command=lambda:import_database(sharedVar))
    menu_file.add_separator()
    menu_file.add_command(label="Export Project", accelerator="CTRL+SHIFT+E",underline=0, command=None)
    menu_file.add_separator()
    menu_file.add_command(label="Exit", underline=1, command=quit)

    menu_bar.add_cascade(label="File", underline=0, menu=menu_file)

    mainWindow.bind_all("<Control-n>", lambda x: new_document())
    mainWindow.bind_all("<Control-o>", lambda x: open_file())
    mainWindow.bind_all("<Control-s>", lambda x: save_document())

    #menu_edit = tk.Menu(menu_bar, tearoff=0)
    #menu_edit.add_command(label="Undo", command=do_something)
    #menu_edit.add_separator()
    #menu_edit.add_command(label="Copy", command=do_something)
    #menu_edit.add_command(label="Cut", command=do_something)
    #menu_edit.add_command(label="Paste", command=do_something)

    #menu_bar.add_cascade(label="Edit", underline=0, menu=menu_edit)

    menu_help = tk.Menu(menu_bar, tearoff=0)
    menu_help.add_command(label="About...", command=do_about)

    menu_bar.add_cascade(label="Help", underline=0, menu=menu_help)

    mainWindow.config(menu=menu_bar)
    


    
