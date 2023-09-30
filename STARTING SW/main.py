import tkinter as tk
from tkPDFViewer import tkPDFViewer as pdf
from PIL import ImageTk, Image
from pdf2image import convert_from_path


"""--------------------ASSETS-------------------"""
pieceMenus_labels = { "Réseaux":{ "DN100":"DN100.png",
                                "DN60":"DN60.png"},
                    "Raccordements":{   "Ø100":"Ø100.png",
                                        "Ø60":"Ø60p.ng"}}
"""--------------------------------------------------------------"""
"""--------------------CREATION PAGE PRINCIPALE-------------------"""
class Main_Window(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.create_menu_bar()
        #Fill the content of the window
        self.geometry("1000x800")
        self.title("SADE")

    def create_menu_bar(self):
        menu_bar = tk.Menu(self)

        menu_file = tk.Menu(menu_bar, tearoff=0)
        menu_file.add_command(label="New", command=self.do_something)
        menu_file.add_command(label="Open", command=self.open_file)
        menu_file.add_command(label="Save", command=self.do_something)
        menu_file.add_separator()
        menu_file.add_command(label="Exit", command=self.quit)
        menu_bar.add_cascade(label="File", menu=menu_file)

        menu_edit = tk.Menu(menu_bar, tearoff=0)
        menu_edit.add_command(label="Undo", command=self.do_something)
        menu_edit.add_separator()
        menu_edit.add_command(label="Copy", command=self.do_something)
        menu_edit.add_command(label="Cut", command=self.do_something)
        menu_edit.add_command(label="Paste", command=self.do_something)
        menu_bar.add_cascade(label="Edit", menu=menu_edit)

        menu_help = tk.Menu(menu_bar, tearoff=0)
        menu_help.add_command(label="About", command=self.do_about)
        menu_bar.add_cascade(label="Help", menu=menu_help)

        self.config(menu=menu_bar)

    def open_file(self):
        file = tk.askopenfilename(title="Choose the file to open",
                               filetypes=[("PNG image", ".png"), ("GIF image", ".gif"), ("All files", ".*")])
        print(file)

    def do_something(self):
        print("Menu clicked")

    def do_about(self):
        tk.messagebox.showinfo("My title", "My message")
"""--------------------------------------------------------------"""
"""--------------------CREATION MENU PIECE-------------------"""
class PieceMenu:
    def __init__(self, window, piece_menus_labels):
        self.window = window
        self.piece_menus_labels = piece_menus_labels
        self.menu_box = tk.PanedWindow(bd=4)
        self.menu_box.pack(fill="x", expand=0)
        self.selected_piece_label=None

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

        label = tk.Label(self.window, image=photo_image)
        label.image = photo_image

        def update_position(event):
            label_width = label.winfo_width()
            label_height = label.winfo_height()
            x = event.x_root - label_width // 2
            y = event.y_root - label_height // 2
            label.place(x=x, y=y)

        self.window.bind("<Motion>", update_position)

        def destroy_label(event):
            label.destroy()
            self.window.unbind("<Motion>")
            label.unbind("<Button-1>")

        label.bind("<Button-1>", destroy_label)
"""--------------------------------------------------------------"""
"""--------------------CREATION PDFViewer-------------------"""
def PDFViewer():
    pdfView_box = tk.PanedWindow(bd=4,bg='red')
    pdfView_box.pack(fill='both',expand=1)
    v1 = pdf.ShowPdf()
  
    # Adding pdf location and width and height.
    v2 = v1.pdf_view(pdfView_box,
                    pdf_location = r"02_Plan-des-ouvrages-projetés.pdf",
                 width = 100, height = 50)
    v2.pack()
"""--------------------------------------------------------------"""

window = Main_Window()
#create_menu(pieceMenus_labels)
PieceMenu(window,pieceMenus_labels).create_menu(pieceMenus_labels)

PDFViewer()
window.mainloop()