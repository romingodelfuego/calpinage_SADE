import tkinter as tk
from PIL import Image, ImageTk


class MenuPieces:
    def __init__(self, window, piece_menus_labels):
        self.window = window
        self.piece_menus_labels = piece_menus_labels
        self.menu_box = tk.PanedWindow(bd=4)
        self.menu_box.pack(fill="x", expand=0)
        self.selected_piece = None

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
        print("Catégorie sélectionnée:", items, "| Pièce sélectionnée:", selected_piece)
        image_path = self.piece_menus_labels[str(items)][str(selected_piece)]
        print(image_path)
        if self.selected_piece:
            self.selected_piece.unselect()
        self.selected_piece = Piece(self.window, image_path)
        self.selected_piece.select()
        self.selected_piece.attach_to_window()

class Piece:
    def __init__(self, window, image_path):
        self.window = window
        self.image_path = image_path
        self.label = None
        self.is_selected = False
        self.dragging = False
        self.offset_x = 0
        self.offset_y = 0

    def select(self):
        self.is_selected = True

    def unselect(self):
        self.is_selected = False

    def attach_to_window(self):
        image = Image.open(self.image_path)
        image = image.resize((100, 100))
        photo_image = ImageTk.PhotoImage(image)

        self.label = tk.Label(self.window, image=photo_image)
        self.label.image = photo_image
        self.window.bind("<ButtonPress-1>", self.start_drag)
        self.label.bind("<ButtonRelease-1>", self.stop_drag)
        self.label.pack()

        if self.is_selected:
            self.label.bind("<B1-Motion>", self.drag)

    
    def start_drag(self, event):
        self.dragging = True
        self.offset_x = event.x
        self.offset_y = event.y
        self.label.configure(relief="solid")


    def stop_drag(self, event):
        self.dragging = False
        self.label.configure(relief="flat")


    def drag(self, event):
        x = self.label.winfo_x() + event.x - self.offset_x
        y = self.label.winfo_y() + event.y - self.offset_y
        self.label.place(x=x, y=y)


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

# Création de l'instance du menu de pièces
menu_pieces = MenuPieces(window, piece_menus_labels)

# Création du menu de pièces
menu_pieces.create_menu(piece_menus_labels)

# Lancement de la boucle principale
window.mainloop()
