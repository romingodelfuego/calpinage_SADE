import tkinter as tk
from tkinter import ttk
from tests import nameOfFunctionCalled as tst
from utils import refresh 

@tst.show_function_name
def createMainWindow(windowName):
    mainWindow=tk.Tk()
    mainWindow.title(f"SADE - CALPINAGE - {windowName}")
    window_width = mainWindow.winfo_screenwidth()
    window_height = mainWindow.winfo_screenheight()
    mainWindow.geometry(f"{window_width}x{window_height}+0+0")
    return mainWindow

@tst.show_function_name
def separateMainWindow(mainWindow,sharedVar):
    bottomFrame = tk.Frame(mainWindow)
    bottomFrame.pack(side=tk.BOTTOM,fill="both")

    createButtonSelection(bottomFrame,sharedVar)

    leftFrame = tk.Frame(mainWindow,width=350)
    leftFrame.pack(fill='y', side=tk.LEFT, padx=20, pady=20)
    leftFrame.propagate(False)
    infoPieceFrame = tk.Frame(leftFrame)
    infoPieceFrame.pack(fill='y',side=tk.BOTTOM)

    middleFrame=ttk.Notebook(mainWindow)
    middleFrame.pack(expand=True, fill=tk.BOTH)

    onglet = tk.Canvas(middleFrame,background="#ffffff")
    pieceFrame=tk.Frame(onglet,background="#ffffff")
    pieceFrame.pack(side='left',fill=tk.BOTH)
    sbX = ttk.Scrollbar(middleFrame, orient = 'horizontal',command=onglet.xview)
    sbY = ttk.Scrollbar(middleFrame, orient="vertical",command=onglet.yview)
    sbX.pack(side="bottom",fill="x")
    sbY.pack(side="right",fill="y")    
    onglet.configure(xscrollcommand=sbX.set, yscrollcommand=sbY.set)        
    onglet.pack(fill='both', expand=True,padx=0,pady=0)

    middleFrame.add(onglet, text='Raccord 1')

    middleFrame.add(tk.Frame(middleFrame),text="+")
    middleFrame.bind("<<NotebookTabChanged>>", lambda event: on_tab_changed(event, middleFrame,bottomFrame,infoPieceFrame,sharedVar))
    pieceFrame.bind("<Configure>", lambda event,onglet=onglet: onglet.configure(scrollregion=onglet.bbox("all")))

    sharedVar.tkinterObject["pieceFrame"]=pieceFrame
    return leftFrame,infoPieceFrame,middleFrame,bottomFrame

@tst.show_function_name
def createButtonSelection(bottomFrame:tk,sharedVar):
    #Une journée sans y parvenir
    #C'est pour selectionner soit les piece soit les liaisons soit les deux #relou
    buttonContainer=tk.Frame(bottomFrame)
    for nom in sharedVar.stateOfButtons.keys():
        button = tk.Button(buttonContainer, text=nom,command=lambda nom=nom:toggle(nom))
        button.pack(side=tk.LEFT)
    buttonContainer.pack(side=tk.TOP)
    def toggle(nom):
        state = sharedVar.stateOfButtons[str(nom)]  

        for key in sharedVar.stateOfButtons.keys():
            sharedVar.stateOfButtons[key]=False

        sharedVar.stateOfButtons[str(nom)] = not state
        bottomFrame=sharedVar.tkinterObject["bottomFrame"]
        sharedVar.set_variable("stateOfButtons",sharedVar.stateOfButtons)
        refresh.refreshTree(bottomFrame,sharedVar)

def on_tab_changed(event, middleFrame:tk,bottomFrame:tk,infoPieceFrame:tk, sharedVar):
    ##On supprime ce qui existe deja sur le frame
    for child in middleFrame.winfo_children():
        if isinstance(child, tk.Label):
            child.destroy()
    # Obtient l'index de l'onglet sélectionné
    next_selected_raccord=event.widget.index("current")
    # Si l'onglet "+" est sélectionné, ajoute un nouvel onglet "Raccord X"
    if next_selected_raccord == len(middleFrame.tabs()) - 1:
        newRaccord(middleFrame,sharedVar,next_selected_raccord)
    elif next_selected_raccord != sharedVar.raccordSelected:
        changeRaccord(sharedVar,next_selected_raccord)
    sharedVar.set_variable("rowSelect",0)
    sharedVar.set_variable("indexSelect",None)

    refresh.refreshPromptPiece(middleFrame,infoPieceFrame,bottomFrame,sharedVar)
    refresh.refreshTree(bottomFrame,sharedVar)

@tst.show_function_name
def newRaccord(middleFrame, sharedVar,next_selected_raccord):
    ## On crée l'onglet sur le notebook
    onglet_num = len(middleFrame.tabs()) - 2
    new_onglet = tk.Canvas(middleFrame,background="#ffffff")
    middleFrame.insert(next_selected_raccord, new_onglet, text="Raccord " + str(onglet_num + 2))
    middleFrame.select(next_selected_raccord)  # Sélectionne le nouvel onglet ajouté
    
    #On sauvegarde les anciennes données
    sharedVar.montageForRaccord[sharedVar.raccordSelected]={"suiteMontageActuel":sharedVar.suiteMontageActuel,"paramMontageActuel":sharedVar.paramMontageActuel}
    # Créer le contenu du nouvel onglet en utilisant grid
    pieceFrame=tk.Frame(new_onglet,background="#ffffff")
    pieceFrame.pack(side='left',fill=tk.BOTH)
    sharedVar.montageForRaccord.append({})  #On ajoute un endroit pour stocker le montage de ce raccord
    sharedVar.set_variable("montageForRaccord",sharedVar.montageForRaccord)
    sharedVar.set_variable("raccordSelected",next_selected_raccord)
    sharedVar.set_variable("suiteMontageActuel",[])
    sharedVar.set_variable("paramMontageActuel",[])
    
    pieceFrameAppend=sharedVar.tkinterObject["pieceFrame"].append(pieceFrame)
    sharedVar.tkinterObject["pieceFrame"]=pieceFrameAppend
    
@tst.show_function_name
def changeRaccord(sharedVar,next_selected_raccord):
    ##On stocke les anciennes données
    sharedVar.montageForRaccord[sharedVar.raccordSelected]["suiteMontageActuel"]=sharedVar.suiteMontageActuel
    sharedVar.montageForRaccord[sharedVar.raccordSelected]["paramMontageActuel"]=sharedVar.paramMontageActuel
    sharedVar.set_variable("montageForRaccord",sharedVar.montageForRaccord)
    ##On va chercher les données stockées pour ce raccord
    copyMontageActuel=sharedVar.montageForRaccord[next_selected_raccord]["suiteMontageActuel"]
    copyParamMontageActuel=sharedVar.montageForRaccord[next_selected_raccord]["paramMontageActuel"]
    sharedVar.set_variable("suiteMontageActuel",copyMontageActuel)
    sharedVar.set_variable("paramMontageActuel",copyParamMontageActuel)
    sharedVar.set_variable("raccordSelected",next_selected_raccord)
    

@tst.show_function_name
def createBoutonFrame(leftFrame):
    buttonFrame = tk.Frame(leftFrame,width=10)
    buttonFrame.pack(side=tk.TOP,expand=False)
    print("Button frame created")
    return buttonFrame

@tst.show_function_name
def createSelectorFrame(leftFrame):
    selectorFrame = tk.Frame(leftFrame)
    selectorFrame.pack(side=tk.TOP)
    return selectorFrame
