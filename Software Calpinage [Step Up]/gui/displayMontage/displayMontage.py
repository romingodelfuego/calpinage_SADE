from gui.gui import GUI 
from tkinter import ttk
import tkinter as tk
from utils import variables as sharedVar
from tests import nameOfFunctionCalled as tst


class DISPLAYMONTAGE:
    def __init__(self) -> None:
        self.displayMontage=self.create()
        GUI.addToArborescence()
    def create(self,):

        notebook=ttk.Notebook(GUI.mainWindow)
        notebook.pack(expand=True, fill=tk.BOTH)

        onglet = ttk.Frame(notebook)
        onglet.pack(fill='both', expand=True,padx=0,pady=0)

        notebook.add(onglet, text='Raccord 1')

        notebook.add(tk.Frame(notebook),text="+")
        notebook.bind("<<NotebookTabChanged>>", lambda event: self.BIND.on_tab_changed(event, notebook))

        return notebook
    
    class BIND:
        def __init__(self):
            self.bottomFrame=GUI.tkinterObjects["bottomFrame"]
            self.infoPieceFrame=GUI.tkinterObjects["infoPieceFrame"]
        def on_tab_changed(self,event,notebook):
            ##On supprime ce qui existe deja sur le frame
            for child in notebook.winfo_children():
                if isinstance(child, tk.Label):
                    child.destroy()
            # Obtient l'index de l'onglet sélectionné
            next_selected_raccord=event.widget.index("current")
            # Si l'onglet "+" est sélectionné, ajoute un nouvel onglet "Raccord X"
            if next_selected_raccord == len(notebook.tabs()) - 1:
                self.newRaccord(next_selected_raccord)
            elif next_selected_raccord != sharedVar.raccordSelected:
                self.changeRaccord(next_selected_raccord)
            sharedVar.set_variable("rowSelect",0)

            GUI.refresh.refreshPromptPiece(notebook,self.infoPieceFrame,self.bottomFrame)
            GUI.refresh.refreshTree(self.bottomFrame)
        
        @tst.show_function_name
        def newRaccord(self,next_selected_raccord):
            ## On crée l'onglet sur le notebook
            onglet_num = len(self.self.tabs()) - 2
            new_frame = ttk.Frame(self.self, width=400, height=280)
            self.self.insert(next_selected_raccord, new_frame, text="Raccord " + str(onglet_num + 2))
            self.self.select(next_selected_raccord)  # Sélectionne le nouvel onglet ajouté
            
            #On sauvegarde les anciennes données
            sharedVar.montageForRaccord[sharedVar.raccordSelected]={"suiteMontageActuel":sharedVar.suiteMontageActuel,"paramMontageActuel":sharedVar.paramMontageActuel}
            # Créer le contenu du nouvel onglet en utilisant grid
            label = tk.Label(new_frame)
            label.grid(row=0, column=0, padx=10, pady=10)  # Utilisez grid pour placer le contenu
            sharedVar.montageForRaccord.append({})  #On ajoute un endroit pour stocker le montage de ce raccord
            sharedVar.set_variable("montageForRaccord",sharedVar.montageForRaccord)
            sharedVar.set_variable("raccordSelected",next_selected_raccord)
            sharedVar.set_variable("suiteMontageActuel",[])
            sharedVar.set_variable("paramMontageActuel",[])

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