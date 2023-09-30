import tkinter as tk


class InterfaceUtilisateur(tk.Tk):
    def __init__(self, piece_names, *listMotMontage):
        from MAIN import EXCEL_DATA
        super().__init__()
        self.title("Interface utilisateur")
        self.montage = listMotMontage

        self.rowSelected = None
        self.columSelected = None
        # Taille et position de la fenêtre
        window_width = self.winfo_screenwidth() // 2
        window_height = self.winfo_screenheight()
        self.geometry(f"{window_width-50}x{window_height}+0+0")
        self.all_cat = ["EMBOITEMENT", "BRIDE", "AUTRES"]
        self.piece_names = piece_names
        self.data=EXCEL_DATA()
        #self.methodConstructor=Constructor()


        self.refreshAll()

    def refreshAll(self):
        LeftFrame(self, self.piece_names, self.all_cat)  # Pass self as the master
        MiddleFrame(self, self.montage)  # Pass self as the master
        #BottomFrame(self)  # Pass self as the master


class LeftFrame(tk.Frame):  # Inherit from tk.Frame
    def __init__(self, master, piece_names, all_cat):
        super().__init__(master)  # Call the constructor of tk.Frame with the provided master
        self.left_frame = tk.Frame(self)
        self.left_frame.pack(fill='y', side=tk.LEFT, padx=20, pady=20)
        self.buttonArea = None
        self.piece_names = piece_names
        self.selectMenu = tk.Frame(self.left_frame)
        self.selectMenu.pack(side=tk.TOP)

        self.current_index = tk.IntVar()
        self.current_index.set(0)  # Index initial sélectionné
        self.cat_selected = tk.StringVar()
        self.cat_selected.set(all_cat[self.current_index.get()])  # Pièce initialement sélectionnée

        # Label pour afficher la pièce sélectionnée
        tk.Label(self.selectMenu, textvariable=self.cat_selected, width=20).pack(pady=10)
        # Bouton pour sélectionner la pièce précédente
        tk.Button(self.selectMenu, text="<", command=self.select_previous, width=5).pack(side=tk.LEFT)
        # Bouton pour sélectionner la pièce suivante
        tk.Button(self.selectMenu, text=">", command=self.select_next, width=5).pack(side=tk.RIGHT)
        self.refreshButton(master)

    def refreshButton(self,master):
        try:
            if self.buttonArea:
                self.buttonArea.destroy()
        except UnboundLocalError:
            pass
        self.buttonArea = tk.Frame(self.left_frame,width=20)  # Recréez le cadre buttonArea avec les nouveaux boutons
        self.buttonArea.pack(side=tk.TOP,expand=False)
        for pieceName in self.piece_names:
            if master.methodConstructor.searchPiece(pieceName, master.data.db_Connexions)[1][0] == self.cat_selected.get():
                button=tk.Button(self.buttonArea, text=pieceName,command=lambda pieceNameLambda=pieceName: self.addToSeriesEltSelec(pieceNameLambda,self.rowSelected))
                button.pack(pady=10,expand=False) 
                print("REFRESHED")
        
    def addToSeriesEltSelec(self,pieceName,rowSelected):
            ##Il faut ajouter a la liste l'elt cliqué
            if rowSelected is not None:
                print(pieceName)
                self.montage[rowSelected].append(pieceName) ## PAS SELF MONTAGE
                print(self.montage[rowSelected])
                self.refreshCells()
    # Fonctions pour gérer la sélection
    def select_previous(self):
        if self.current_index.get() > 0:
            self.current_index.set(self.current_index.get() - 1)
            self.cat_selected.set(self.all_cat[self.current_index.get()])
            self.refreshButton()

    def select_next(self):
        if self.current_index.get() < len(self.all_cat) - 1:
            self.current_index.set(self.current_index.get() + 1)
            self.cat_selected.set(self.all_cat[self.current_index.get()])
            self.refreshButton()

    
class MiddleFrame(tk.Frame):
    def __init__(self, master, *listMotMontage):
        super().__init__(master)  # Call the constructor of tk.Frame with the provided master
        self.middle_frame = tk.Frame(self, bg='white')  # Couleur de fond du cadre middle_frame
        self.middle_frame.pack(expand=True, fill=tk.BOTH)

        # Groupe de cellules sélectionnables
        self.cell_names = listMotMontage[0]
        self.labels = []  # Liste pour stocker les labels de tous les groupes
        self.labels_rows = []  # Liste pour stocker les labels de chaque ligne

    def on_row_click(self, event):
        row = event.widget.grid_info()['row']
        self.rowSelected = row
        for row_labels in self.labels_rows:
            for label in row_labels:
                label.config(relief=tk.RIDGE, borderwidth=2)

        for label in self.labels_rows[row]:
            label.config(relief=tk.SOLID, borderwidth=2)

    def on_label_double_click(self, event):
        label = event.widget
        label.config(bg='blue')  # Définir la couleur de fond du label sur bleu

    def refreshCells(self):
        for label in self.labels:
            label.grid_forget()
            label.destroy()

        self.labels = []  # Réinitialiser la liste des labels
        self.labels_rows = []  # Réinitialiser la liste des labels de chaque ligne

        for i, row in enumerate(self.cell_names):
            row_labels = []  # Liste pour stocker les labels de chaque ligne
            for j, cell_name in enumerate(row):
                label = tk.Label(self.middle_frame, text=cell_name, relief=tk.RIDGE, width=15, height=5, bg='white')
                label.grid(row=i, column=j, pady=(10, 0))
                row_labels.append(label)
                self.labels.append(label)

                # Liaison du clic sur le label avec la fonction on_row_click
                label.bind('<Button-1>', self.on_row_click)
                label.bind('<Double-Button-1>', self.on_label_double_click)
            self.labels_rows.append(row_labels)

class BottomFrame():
    pass


general= ["BE","VANNE","BU","TÉ EMBOITEMENT","TÉ BRIDE","TUYAUX M-F","TUYAUX M-M","COUDE EMBOITEMENT","COUDE BRIDE","CONE EMBOITEMENT","CONE BRIDE","PLAQUE PLEINE","BRANCHEMENT","MANCHON","MANCHON TRANSITION","ADAPTATEUR DE BRIDE"]
InterfaceUtilisateur(general,[]).mainloop()