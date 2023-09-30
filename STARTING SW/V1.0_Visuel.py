import tkinter as tk
from WORKING_V4_COMPTABILISER import *

class InterfaceUtilisateur(tk.Tk):
    def __init__(self,piece_names,*listMotMontage):
        super().__init__()
        self.title("Interface utilisateur")
        self.montage=listMotMontage

        self.rowSelected=None
        self.columSelected=None
        # Taille et position de la fenêtre
        window_width = self.winfo_screenwidth() // 2
        window_height = self.winfo_screenheight()
        self.geometry(f"{window_width-50}x{window_height}+0+0")
        all_cat=["EMBOITEMENT","BRIDE","AUTRES"]

        self.create_left_frame(piece_names,all_cat)
        self.create_middle_frame(self.montage)
        self.create_bottom_frame()


    def create_left_frame(self,piece_names,all_cat):
        left_frame = tk.Frame(self)
        left_frame.pack(fill='y',side=tk.LEFT, padx=20, pady=20)
        buttonArea = None

        def addToSeriesEltSelec(pieceName,rowSelected):
            ##Il faut ajouter a la liste l'elt cliqué
            if rowSelected is not None:
                print(pieceName)
                self.montage[rowSelected].append(pieceName)
                print(self.montage[rowSelected])

        def refreshButton():
            nonlocal buttonArea  # Utilisez nonlocal pour indiquer que vous utilisez la variable déclarée à l'extérieur
            try:
                if buttonArea:
                    buttonArea.destroy()
            except UnboundLocalError:
                pass
            buttonArea = tk.Frame(left_frame,width=20)  # Recréez le cadre buttonArea avec les nouveaux boutons
            buttonArea.pack(side=tk.TOP,expand=False)
            for pieceName in piece_names:
                if CORTEX.searchPiece(pieceName, db_Connexions)[1][0] == cat_selected.get():
                    tk.Button(buttonArea, text=pieceName,command=lambda pieceNameLambda=pieceName:addToSeriesEltSelec(pieceNameLambda,self.rowSelected)).pack(pady=10,expand=False) 
                    print("REFRESHED")
            

            
        
        selectMenu = tk.Frame(left_frame)
        selectMenu.pack(side=tk.TOP)

        current_index = tk.IntVar()
        current_index.set(0)  # Index initial sélectionné
        cat_selected = tk.StringVar()
        cat_selected.set(all_cat[current_index.get()])  # Pièce initialement sélectionnée

        # Fonctions pour gérer la sélection
        def select_previous():
            nonlocal current_index
            if current_index.get() > 0:
                current_index.set(current_index.get() - 1)
                cat_selected.set(all_cat[current_index.get()])
                refreshButton()

        def select_next():
            nonlocal current_index
            if current_index.get() < len(all_cat) - 1:
                current_index.set(current_index.get() + 1)
                cat_selected.set(all_cat[current_index.get()])
                refreshButton()
        # Label pour afficher la pièce sélectionnée
        labecat_selected = tk.Label(selectMenu, textvariable=cat_selected, width=20)
        labecat_selected.pack(pady=10)
        # Bouton pour sélectionner la pièce précédente
        tk.Button(selectMenu, text="<", command=select_previous, width=5).pack(side=tk.LEFT)
        # Bouton pour sélectionner la pièce suivante
        tk.Button(selectMenu, text=">", command=select_next, width=5).pack(side=tk.RIGHT)
        refreshButton()
        
    def create_middle_frame(self,*listMotMontage):
        middle_frame = tk.Frame(self)  # Couleur de fond du cadre middle_frame
        middle_frame.pack(expand=True, fill=tk.BOTH)

        # Groupe de cellules sélectionnables
        cell_names = listMotMontage[0] 
        self.labels = []  # Liste pour stocker les labels de tous les groupes
        self.labels_rows = []  # Liste pour stocker les labels de chaque ligne

        def on_row_click(event):
            row = event.widget.grid_info()['row']
            self.rowSelected=row
            for row_labels in self.labels_rows:
                for label in row_labels:
                    label.config(relief=tk.RIDGE,borderwidth=2,bg='white')

            for label in self.labels_rows[row]:
                label.config(relief=tk.SOLID, borderwidth=2)

        def on_label_double_click(event):
            label = event.widget
            print("event \n",event)
            print("event widget \n",event.widget)
            label.config(bg='blue')  # Définir la couleur de fond du label sur bleu
        def refreshCells():
            for i, row in enumerate(cell_names):
                row_labels = []  # Liste pour stocker les labels de chaque ligne
                for j, cell_name in enumerate(row):
                    label = tk.Label(middle_frame, text=cell_name, relief=tk.RIDGE, width=15, height=5)
                    label.grid(row=i, column=j, pady=(10, 0))
                    row_labels.append(label)
                    self.labels.append(label)
                    # Liaison du clic sur le label avec la fonction on_row_click
                    label.bind('<Button-1>', on_row_click)
                    label.bind('<Double-Button-1>', on_label_double_click)
                self.labels_rows.append(row_labels)
        refreshCells()

    def create_bottom_frame(self):
        bottom_frame = tk.Frame(self)
        bottom_frame.pack(side=tk.BOTTOM, padx=20, pady=20)

        self.pieces_selected = tk.Listbox(bottom_frame, width=30, height=10)
        self.pieces_selected.pack()

def main():
    general= ["BE","VANNE","BU","TÉ EMBOITEMENT","TÉ BRIDE","TUYAUX M-F","TUYAUX M-M","COUDE EMBOITEMENT","COUDE BRIDE","CONE EMBOITEMENT","CONE BRIDE","PLAQUE PLEINE","BRANCHEMENT","MANCHON","MANCHON TRANSITION","ADAPTATEUR DE BRIDE"]
    app = InterfaceUtilisateur(general,["TUYAUX M-M","TUYAUX M-F","TÉ EMBOITEMENT","BU","VANNE"],["VANNE","BU","BE"])
    app.mainloop()

if __name__ == "__main__":
    main()
