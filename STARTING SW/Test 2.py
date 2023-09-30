import tkinter as tk
from PIL import Image, ImageTk

class MenuPieces:
    def __init__(self, window, piece_menus_labels):
        self.window = window
        self.piece_menus_labels = piece_menus_labels
        self.menu_box = tk.PanedWindow(bd=4)
        self.menu_box.pack(fill="x", expand=0)

    def create_menu(self, labels):
        for items in labels:
            menu_label = tk.Menubutton(self.menu_box, text=str(items))
            menu_label.menu = tk.Menu(menu_label)
            menu_label["menu"] = menu_label.menu
            self.menu_box.add(menu_label)
            for sm_items in labels[str(items)]:
                menu_label.menu.add_cascade(label=str(sm_items),
                                            command=lambda items=items, sm_items=sm_items: self.display_piece(items, sm_items))
        frame = tk.Frame(self.menu_box)
        self.menu_box.add(frame)

    def display_piece(self, items, selected_piece):
        print("Catégorie sélectionnée: ", items, " | Pièce sélectionnée: ", selected_piece)
        image_path = self.piece_menus_labels[str(items)][str(selected_piece)]
        print(image_path)
        image = Image.open(image_path)
        image = image.resize((100, 100))
        photo_image = ImageTk.PhotoImage(image)

        piece = Piece(self.window, photo_image)
        piece.display()

class Piece:
    def __init__(self, window, image):
        self.window = window
        self.image = image
        self.label = None
        self.selected = False

    def display(self):
        self.label = tk.Label(self.window, image=self.image)
        self.label.image = self.image
        self.window.bind("<Button-1>", self.check_piece_press)
        self.label.bind("<B1-Motion>", self.update_position)
        self.label.pack()

    def update_position(self, event):
        if self.selected:
            x = self.label.winfo_x() + event.x - self.offset_x
            y = self.label.winfo_y() + event.y - self.offset_y
            self.label.place(x=x, y=y)

    def check_piece_press(self,event):
        if self.label.winfo_containing(event.x_root, event.y_root) == self.label:
            print("Le curseur est sur l'image.")
            self.offset_x = event.x
            self.offset_y = event.y
            self.select_piece(event)
        else:
            print("Le curseur n'est pas sur l'image.") 
            self.deselect_piece()
    def select_piece(self, event):
        #self.check_piece_press(event)
            self.selected = True
            self.label.configure(relief="solid")

    def deselect_piece(self):
        self.selected = False
        self.label.configure(relief="flat")

# Création de la fenêtre principale
window = tk.Tk()

# Données de menu de pièces
piece_menus_labels = {
    "Catégorie 1": {
        "Pièce 1": "DN100.png",
        "Pièce 2": "DN100.png"
    },
    "Catégorie 2": {
        "Pièce 3": "DN100.png",
        "Pièce 4": "DN100.png"
    }
}

# Création de l'instance de menu de pièces
menu_pieces = MenuPieces(window, piece_menus_labels)

# Création du menu de pièces
menu_pieces.create_menu(piece_menus_labels)

# Lancement de la boucle principale
window.mainloop()
