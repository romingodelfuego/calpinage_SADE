import tkinter as tk
import V5_COMPTABILISER as br


class Cortex(tk.Tk):
    def __init__(self,piece_names,*listMotMontage:list) -> None:
        super().__init__()

        self.piece_names=piece_names
        self.all_cat=["EMBOITEMENT","BRIDE","AUTRES"]
        self.listMotMontage=listMotMontage
       #self.listPieceMontage = br.BRAIN.constructor(listMotMontage)
        self.rowSelected=None

        self.middle_frame=None

        self.refreshAll()

    def refreshAll(self):
        LeftFrame(self)
        MiddleFrame(self)
        self.UserNeeded("What inside my bag",["Nothing","Phone","LipStick","Uoh","Essaie","Livre","NoWay"])

    def UserNeeded(self,question,repPossible):
        PopUpUser(self,question,repPossible)

class PopUpUser:
    def __init__(self,cortex_instance,question,repPossible):
        self.cortex_instance = cortex_instance
        popUpWindow=tk.Toplevel(self.cortex_instance)
        popUpWindow.geometry(f"300x{len(repPossible)*35}+0+0")
        popUpWindow.resizable(False,False)
        tk.Label(popUpWindow, text=question,height=2).pack(side=tk.TOP)
        for rep in repPossible:
            button=tk.Button(popUpWindow,text=rep,command=None,height=1)
            button.pack()









class MainFrame(tk.Tk):
        def __init__(self):
            super().__init__()
            nom_fichier="Fichier test" ##A gerer avec le import plus tard
            self.title(f"Interface fichier: {nom_fichier}")
            window_width = self.winfo_screenwidth() // 2
            window_height = self.winfo_screenheight()
            self.geometry(f"{window_width-50}x{window_height}+0+0")
            return self
        
class LeftFrame:#piece_names,all_cat
    def __init__(self,main,piece_names,all_cat,rowSelected) -> None:

        
        self.current_index = tk.IntVar()
        self.current_index.set(0)  # Index initial sélectionné
        self.cat_selected = tk.StringVar()
        self.cat_selected.set(all_cat[self.current_index.get()])  # Pièce initialement sélectionnée
        #self.updateButtons()
        self.construct(main)

    def construct(self,main):
        ##Container
        self.leftFrame = tk.Frame(main)
        self.leftFrame.pack(fill='y',side=tk.LEFT, padx=20, pady=20)
        ##Menu
        self.selectMenu = tk.Frame(self.leftFrame)
        self.selectMenu.pack(side=tk.TOP)
        tk.Label(self.selectMenu, textvariable=main.cat_selected, width=20).pack(pady=10)
        tk.Button(self.selectMenu, text="<", command=self.select_previous, width=5).pack(side=tk.LEFT)        # Bouton pour sélectionner la pièce précédente
        tk.Button(self.selectMenu, text=">", command=self.select_next, width=5).pack(side=tk.RIGHT)        # Bouton pour sélectionner la pièce suivante
        ##Boutons
        self.buttonArea = tk.Frame(self.leftFrame,width=20)  
        self.buttonArea.pack(side=tk.TOP,expand=False)
        return self.leftFrame,self.selectMenu,self.buttonArea
    

    def updateButtons(self):
        try:
            if self.buttonArea:
                self.buttonArea.destroy()
        except UnboundLocalError:
            pass
        self.buttonArea = tk.Frame(self.left_frame,width=20)  # Recréez le cadre buttonArea avec les nouveaux boutons
        self.buttonArea.pack(side=tk.TOP,expand=False)
        for pieceName in self.piece_names:
            if br.BRAIN.searchPiece(pieceName, br.db_Connexions)[1][0] == self.cat_selected.get():
                tk.Button(self.buttonArea, text=pieceName,command=lambda pieceNameLambda=pieceName: self.addToSeriesEltSelec(pieceNameLambda,self.cortex_instance.rowSelected)).pack(pady=10,expand=False) 

    # Fonctions pour gérer la sélection
    def select_previous(self):
        self.current_index.set((self.current_index.get() - 1) % len(self.cortex_instance.all_cat))
        self.cat_selected.set(self.cortex_instance.all_cat[self.current_index.get()])
        self.updateButtons()

    def select_next(self):
        self.current_index.set((self.current_index.get() + 1) % len(self.cortex_instance.all_cat))
        self.cat_selected.set(self.cortex_instance.all_cat[self.current_index.get()])
        self.updateButtons()
            
class MiddleFrame: #Utilises listMotMontage,rowSelected,
    def __init__(self,main) -> None:
        # Groupe de cellules sélectionnables
        self.thereIsCells = False
        self.cell_names = main.listMotMontage
        self.labels = []  # Liste pour stocker les labels de tous les groupes
        self.labels_rows = []  # Liste pour stocker les labels de chaque ligne

        self.updateCells()

    def on_row_click(self,event):
        row = event.widget.grid_info()['row']
        main.rowSelected=row
        for row_labels in self.labels_rows:
            for label in row_labels:
                label.config(relief=tk.RIDGE,borderwidth=2,bg='white')
        for label in self.labels_rows[row]:
            label.config(relief=tk.SOLID, borderwidth=2)

    def on_label_double_click(self,event):
        label = event.widget
        print("event \n",event)
        print("event widget \n",event.widget)
        label.config(bg='blue')  # Définir la couleur de fond du label sur bleu 
    
    def updateCells(self):
        try:
            if self.middle_frame:
                self.middle_frame.destroy()
        except UnboundLocalError:
            pass
        self.middle_frame = tk.Frame(main)
        self.middle_frame.pack(expand=True, fill=tk.BOTH)
        for i, row in enumerate(self.cell_names):
            row_labels = []  # Liste pour stocker les labels de chaque ligne
            for j, cell_name in enumerate(row):
                label = tk.Label(self.middle_frame, text=cell_name, relief=tk.RIDGE, width=15, height=5,bg='white')
                label.grid(row=i, column=j, pady=(10, 0))
                row_labels.append(label)
                self.labels.append(label)
                # Liaison du clic sur le label avec la fonction on_row_click
                label.bind('<Button-1>', self.on_row_click)
                label.bind('<Double-Button-1>', self.on_label_double_click)
            self.labels_rows.append(row_labels)
        self.cortex_instance.middle_frame=self.middle_frame


def main():
    general= ["BE","VANNE","BU","TÉ EMBOITEMENT","TÉ BRIDE","TUYAUX M-F","TUYAUX M-M","COUDE EMBOITEMENT","COUDE BRIDE","CONE EMBOITEMENT","CONE BRIDE","PLAQUE PLEINE","BRANCHEMENT","MANCHON","MANCHON TRANSITION","ADAPTATEUR DE BRIDE"]
    app = Cortex(general)
    app.mainloop()

if __name__ == "__main__":
    main()
