"""from tkinter import *
from tkinter import filedialog
from PyPDF2 import PdfReader

def charger_pdf():
    filepath = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if filepath:
        pdf = PdfReader(open(filepath, "rb"))
        # Faites ce que vous voulez avec le fichier PDF chargé, par exemple :
        print("Nombre de pages du PDF :", len(pdf.pages))

# Création de la fenêtre principale
fenetre = Tk()
fenetre.title("Charger un PDF")

# Création du bouton de chargement
btn_charger = Button(fenetre, text="Charger un PDF", command=charger_pdf)
btn_charger.pack(pady=20)

# Lancement de la boucle principale
fenetre.mainloop()


"""
"""
from tkinter import *
from tkinter import filedialog
from PyPDF2 import PdfReader

def charger_pdf():
    filepath = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if filepath:
        pdf = PdfReader(open(filepath, "rb"))
        num_pages = len(pdf.pages)
        text_content = ""

        for page_num in range(num_pages):
            page = pdf.pages[page_num]
            text_content += page.extract_text()

        # Création de la fenêtre d'affichage du contenu du PDF
        fenetre_contenu = Toplevel(fenetre)
        fenetre_contenu.title("Contenu du PDF")

        # Création du widget Text pour afficher le contenu
        txt_contenu = Text(fenetre_contenu)
        txt_contenu.insert(END, text_content)
        txt_contenu.pack()

# Création de la fenêtre principale
fenetre = Tk()
fenetre.title("Charger un PDF")

# Création du bouton de chargement
btn_charger = Button(fenetre, text="Charger un PDF", command=charger_pdf)
btn_charger.pack(pady=20)

# Lancement de la boucle principale
fenetre.mainloop()
"""
from pdf2image import convert_from_path
from tkinter import *
from tkinter import filedialog

class PDFViewer:
    def __init__(self, fenetre):
        self.fenetre = fenetre
        self.pages = []
        self.current_page = 0
        self.canvas = None
        self.image_on_canvas = None
        self.start_x = 0
        self.start_y = 0

        # Création de la fenêtre principale
        self.fenetre.title("Charger un PDF")

        # Création du bouton de chargement
        self.btn_charger = Button(self.fenetre, text="Charger un PDF", command=self.charger_pdf)
        self.btn_charger.pack(pady=20)

    def charger_pdf(self):
        filepath = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if filepath:
            self.pages = convert_from_path(filepath, dpi=200)  # Convertir le PDF en images
            self.afficher_page()

    def afficher_page(self):
        # Création de la fenêtre d'affichage du contenu du PDF
        self.fenetre_contenu = Toplevel(self.fenetre)
        self.fenetre_contenu.title("Contenu du PDF")

        # Création du canevas pour afficher la page
        self.canvas = Canvas(self.fenetre_contenu, width=self.pages[self.current_page].width,
                             height=self.pages[self.current_page].height)
        self.canvas.pack()

        # Affichage de la page sur le canevas
        self.image_on_canvas = self.canvas.create_image(0, 0, anchor=NW, image=self.pages[self.current_page])

        # Configuration des événements de la souris
        self.canvas.bind("<ButtonPress-1>", self.on_mouse_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_release)

    def on_mouse_press(self, event):
        # Enregistre la position de départ lors du clic de souris
        self.start_x = event.x
        self.start_y = event.y

    def on_mouse_drag(self, event):
        # Fait défiler le canevas en fonction du mouvement de la souris
        delta_x = event.x - self.start_x
        delta_y = event.y - self.start_y
        self.canvas.xview_scroll(-delta_x, "units")
        self.canvas.yview_scroll(-delta_y, "units")
        self.start_x = event.x
        self.start_y = event.y

    def on_mouse_release(self, event):
        # Réinitialise la position de départ lorsque le bouton de souris est relâché
        self.start_x = 0
        self.start_y = 0


# Création de la fenêtre principale
fenetre = Tk()

# Création de l'instance du visualiseur PDF
viewer = PDFViewer(fenetre)

# Lancement de la boucle principale
fenetre.mainloop()
