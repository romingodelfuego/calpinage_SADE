import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename 
from tkinter.filedialog import asksaveasfilename 
#from utils import refresh   
import pickle
import os

from modules.pieces import PIECE
from tests import nameOfFunctionCalled as tst

##Il faut reussir a stocker les données dans sharedVar et a actualiser les données 
@tst.show_function_name
def new_document(mainWindow,leftFrame,infoPieceFrame,middleFrame,bottomFrame,selectorFrame,buttonFrame,sharedVar):
    #sauvegarder l'ancien doc
    response = messagebox.askyesnocancel("Confirmation", "Voulez-vous sauvegarder les modifications avant de créer un nouveau fichier?")
    print(response)
    if response is None:
        pass #Cancel
    elif response:
        ##On sauvegarde ici
        save_document(sharedVar)
    ##Créer un backup files. ?
    # Creer un nouveau fichier ?   
    ## Reinitialiser toutes les variables
    sharedVar.__init__()
    refresh.refreshAll(mainWindow,leftFrame,infoPieceFrame,middleFrame,bottomFrame,selectorFrame,buttonFrame,sharedVar)
  
@tst.show_function_name
def open_file(mainWindow,leftFrame,infoPieceFrame,middleFrame,bottomFrame,selectorFrame,buttonFrame,sharedVar):
    file_path = askopenfilename(filetypes=[("Sade Files", "*.sade"), ("All files", "*.*")])

    if file_path:
        with open(file_path, "rb") as file:
            data = pickle.load(file)
            sharedVar.__dict__.update(data)
            refresh.refreshAll(mainWindow,leftFrame,infoPieceFrame,middleFrame,bottomFrame,selectorFrame,buttonFrame,sharedVar)
            sharedVar.set_variable("filePath",file_path)
            file_name=os.path.basename(file_path)
            sharedVar.set_variable("fileName",file_name)

@tst.show_function_name
def save_document(sharedVar):
    if sharedVar.filePath is None:
        save_as_document(sharedVar)
        return
    elif not sharedVar.filePath.endswith(".sade"): ##Si le path name ne finis pas par .sade
        sharedVar.filePath += ".sade"   #On le force a finir par sade
    with open(sharedVar.filePath, "wb") as file:
        pickle.dump(sharedVar.dict_savable_variable(), file)
        print(f"Fichier sauvegardé avec succès a l'adresse {sharedVar.filePath}")
    
@tst.show_function_name
def save_as_document(sharedVar):
    file_path = asksaveasfilename(defaultextension=".sade", filetypes=[("Sade Files", "*.sade"), ("All files", "*.*")])

    if file_path:
        if not file_path.endswith(".sade"):
            file_path += ".sade"
        sharedVar.filePath = file_path
        save_document(sharedVar)

def do_about():
    messagebox.showinfo("My title", "")
 


@tst.show_function_name
def import_database(sharedVar):
    paramWindow = tk.Toplevel()
    paramWindow.title("GESTION: BASE DE DONNÉE")
    paramWindow.geometry("800x400")

    paramFrame = tk.Frame(paramWindow)
    paramFrame.pack(fill='x', expand=True)
    buttonFrame=tk.Frame(paramWindow,bg="yellow")
    buttonFrame.pack(fill='x',expand=False,side=tk.BOTTOM)
    paramFrame.grid_columnconfigure(0, weight=2)
    paramFrame.grid_columnconfigure(1, weight=3)
    paramFrame.grid_columnconfigure(2, weight=1)

    filePath_db=sharedVar.filePath_db.copy()
    # CREATION LABEL
    labelResume = tk.Label(paramFrame, text="Resume",bg="blue")
    labelResume.grid(row=0, column=0)

    labelJonctions = tk.Label(paramFrame, text="Jonctions")
    labelJonctions.grid(row=1, column=0)

    labelPieces = tk.Label(paramFrame, text="Pieces")
    labelPieces.grid(row=2, column=0)

    # CREATION Text
    def refreshLabel_db():
        for widget in paramFrame.grid_slaves(column=1):
            widget.grid_remove()
        textResume = tk.Label(paramFrame, height=1,text=filePath_db["Resume"],bg="red")
        textResume.grid(row=0, column=1, sticky="e")

        textJonctions = tk.Label(paramFrame, height=1,text=filePath_db["Jonctions"])
        textJonctions.grid(row=1, column=1, sticky="e")
        textPieces = tk.Label(paramFrame, height=1,text=filePath_db["Pieces"])
        textPieces.grid(row=2, column=1, sticky="e")

    refreshLabel_db()
    # CREATION Bouton
    buttonResume = tk.Button(paramFrame, text="...",command=lambda:open_path("Resume"))
    buttonResume.grid(row=0, column=2)

    buttonJonctions = tk.Button(paramFrame, text="...",command=lambda:open_path("Jonctions"))
    buttonJonctions.grid(row=1, column=2)

    buttonPieces = tk.Button(paramFrame, text="...",command=lambda:open_path("Pieces"))
    buttonPieces.grid(row=2, column=2)

    def open_path(name_db):
        file_path = askopenfilename(filetypes=[("Excel Files", "*.xlsx"), ("All files", "*.*")]) 
        if file_path:
            filePath_db[str(name_db)]=file_path
            refreshLabel_db()
            
    buttonSave=tk.Button(buttonFrame,text="SAVE",command=lambda :save_changes(sharedVar))
    buttonSave.pack(pady=(0,5))

    def save_changes(sharedVar):
        for widget in buttonFrame.winfo_children():
            if isinstance(widget,tk.Label):
                widget.destroy()
        sharedVar.set_variable("filePath_db",filePath_db)
        confirmation_save = tk.Label(buttonFrame,text="All changes saved",fg="green",height=1)
        confirmation_save.pack(side=tk.BOTTOM)

