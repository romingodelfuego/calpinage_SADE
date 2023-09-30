from tkinter import *
from math import *
from time import *
from TEST_Module_Piece import *

WIDTH = 400
HEIGHT =400

# Création de la fenêtre
Fenetre = Tk()
Fenetre.title("Détection de pièces")

# Création du canvas
canvas = Canvas(Fenetre, width=WIDTH, height=HEIGHT, bg="white", bd=8)
canvas.pack()

## Création des pièces
figures = []
figure1 = Piece(canvas, 150, 150, 350, 350, 30)
figure2 = Piece(canvas, 400, 100, 500, 200, 45)
figure3 = Piece(canvas, 300, 100, 400, 200, 45)
figures.extend([figure1, figure2, figure3])

# Démarrage de la boucle Tkinter
Fenetre.mainloop()

