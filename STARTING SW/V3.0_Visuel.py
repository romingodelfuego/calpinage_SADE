import tkinter as tk
import WORKING_V4_COMPTABILISER as br

class Cortex(tk.Tk):
    def __init__(self,piece_names,*listMotMontage) -> None:
        super().__init__()
        self.title("Interface utilisateur")
        window_width = self.winfo_screenwidth() // 2
        window_height = self.winfo_screenheight()
        self.geometry(f"{window_width-50}x{window_height}+0+0")
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


class LeftFrame:
    def __init__(self, cortex_instance) -> None:
        self.cortex_instance = cortex_instance

        self.left_frame = tk.Frame(self.cortex_instance)
        self.left_frame.pack(fill='y',side=tk.LEFT, padx=20, pady=20)

        self.buttonArea = None
        self.piece_names=self.cortex_instance.piece_names
        self.selectMenu = tk.Frame(self.left_frame)
        self.selectMenu.pack(side=tk.TOP)
        
        self.current_index = tk.IntVar()
        self.current_index.set(0)  # Index initial sélectionné
        self.cat_selected = tk.StringVar()
        self.cat_selected.set(self.cortex_instance.all_cat[self.current_index.get()])  # Pièce initialement sélectionnée

        # Label pour afficher la pièce sélectionnée
        tk.Label(self.selectMenu, textvariable=self.cat_selected, width=20).pack(pady=10)
        # Bouton pour sélectionner la pièce précédente
        tk.Button(self.selectMenu, text="<", command=self.select_previous, width=5).pack(side=tk.LEFT)
        # Bouton pour sélectionner la pièce suivante
        tk.Button(self.selectMenu, text=">", command=self.select_next, width=5).pack(side=tk.RIGHT)
        self.refreshButton()

    def refreshButton(self):
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
                print("REFRESHED")

    def addToSeriesEltSelec(self,pieceName,rowSelected):
            ##Il faut ajouter a la liste l'elt cliqué
            copyListMotMontage=self.cortex_instance.listMotMontage[rowSelected]
            copyListMotMontage.append(pieceName)
            if rowSelected is not None:
                if br.BRAIN.constructor(copyListMotMontage):
                    self.cortex_instance.listMotMontage[rowSelected].append(pieceName)
            elif len(copyListMotMontage)<1:
                self.cortex_instance.listMotMontageappend([pieceName])
            
            MiddleFrame(self.cortex_instance)

    # Fonctions pour gérer la sélection
    def select_previous(self):
        self.current_index.set((self.current_index.get() - 1) % len(self.cortex_instance.all_cat))
        self.cat_selected.set(self.cortex_instance.all_cat[self.current_index.get()])
        self.refreshButton()

    def select_next(self):
        self.current_index.set((self.current_index.get() + 1) % len(self.cortex_instance.all_cat))
        self.cat_selected.set(self.cortex_instance.all_cat[self.current_index.get()])
        self.refreshButton()
            
class MiddleFrame:
    def __init__(self,cortex_instance) -> None:
        self.cortex_instance = cortex_instance
        self.middle_frame=self.cortex_instance.middle_frame
        # Groupe de cellules sélectionnables
        self.cell_names = self.cortex_instance.listMotMontage
        self.labels = []  # Liste pour stocker les labels de tous les groupes
        self.labels_rows = []  # Liste pour stocker les labels de chaque ligne

        self.refreshCells()

    def on_row_click(self,event):
        row = event.widget.grid_info()['row']
        self.cortex_instance.rowSelected=row
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
    
    def refreshCells(self):
        try:
            if self.middle_frame:
                self.middle_frame.destroy()
        except UnboundLocalError:
            pass
        self.middle_frame = tk.Frame(self.cortex_instance)
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

class BottomFrame:
    def __init__(self) -> None:
        pass
def main():
    general= ["BE","VANNE","BU","TÉ EMBOITEMENT","TÉ BRIDE","TUYAUX M-F","TUYAUX M-M","COUDE EMBOITEMENT","COUDE BRIDE","CONE EMBOITEMENT","CONE BRIDE","PLAQUE PLEINE","BRANCHEMENT","MANCHON","MANCHON TRANSITION","ADAPTATEUR DE BRIDE"]
    app = Cortex(general,["TUYAUX M-M","TUYAUX M-F","TÉ EMBOITEMENT","BU","VANNE"])
    app.mainloop()

if __name__ == "__main__":
    main()