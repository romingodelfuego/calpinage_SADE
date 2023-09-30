from tkinter import *
from math import *


class Piece:
    def __init__(self, canvas, x0, y0, x1, y1, angle_deg):
        self.canvas = canvas
        self.x0, self.y0, self.x1, self.y1 = x0, y0, x1, y1
        self.angle_deg = angle_deg
        self.angle_rad = angle_deg * (pi / 180)
        self.rayon = abs(y0 - y1) / 2
        self.center_x, self.center_y = (x0 + x1) / 2, (y0 + y1) / 2

        self.cercle = self.canvas.create_oval(x0, y0, x1, y1, width=4)
        self.centre_cercle = self.canvas.create_oval(self.center_x, self.center_y, self.center_x, self.center_y, width=4, fill='black')
        self.vect1 = self.canvas.create_line(0, self.center_y, self.center_x, self.center_y, fill="red", width=2)
        self.vect2 = self.canvas.create_line(self.center_x, self.center_y, x_max, self.center_y - (x_max - self.center_x) * tan(self.angle_rad), fill="red", width=2)

        self.point_conn1 = self.canvas.create_oval(x0, self.center_y, x0, self.center_y, fill="purple", width=10)
        self.point_conn2 = self.canvas.create_oval(self.center_x + self.rayon * cos(self.angle_rad), self.center_y - self.rayon * sin(self.angle_rad), self.center_x + self.rayon * cos(self.angle_rad), self.center_y - self.rayon * sin(self.angle_rad), fill="purple", width=10)

        self.is_dragging = False
        self.prev_x, self.prev_y = 0, 0

        self.detection_radius = 100  # Rayon de détection en pixels
        self.detection_circle = None

        # Gestion des événements pour le déplacement de la pièce
        self.canvas.tag_bind(self.cercle, "<ButtonPress-1>", self.on_click)
        self.canvas.tag_bind(self.cercle, "<B1-Motion>", self.on_drag)
        self.canvas.tag_bind(self.cercle, "<ButtonRelease-1>", self.on_release)


    def on_click(self, event):
        self.is_dragging = True
        self.prev_x, self.prev_y = event.x, event.y

    def on_drag(self, event):
        if self.is_dragging:
            dx = event.x - self.prev_x
            dy = event.y - self.prev_y
            self.canvas.move(self.cercle, dx, dy)
            self.canvas.move(self.centre_cercle, dx, dy)
            self.canvas.move(self.vect1, dx, dy)
            self.canvas.move(self.vect2, dx, dy)
            self.canvas.move(self.point_conn1, dx, dy)
            self.canvas.move(self.point_conn2, dx, dy)
            self.prev_x, self.prev_y = event.x, event.y

            # Vérification du rayon après le déplacement de la pièce
            check_radius()

    def on_release(self, event):
        self.is_dragging = False

    def is_in_radius(self, other_piece, radius):
        distance = sqrt((self.center_x - other_piece.center_x) ** 2 + (self.center_y - other_piece.center_y) ** 2)
        return distance <= radius

    def highlight_connection_points(self, highlight=True):
        fill_color = "white" if highlight else "black"
        self.canvas.itemconfigure(self.point_conn1, fill=fill_color)
        self.canvas.itemconfigure(self.point_conn2, fill=fill_color)


# Création de la fenêtre et du canvas
Fenetre = Tk()
(x_max, y_max) = (1000, 1000)
canvas = Canvas(Fenetre, width=x_max, height=y_max, bg="white", bd=8)
canvas.pack()

# Création des pièces
piece1 = Piece(canvas, 150, 150, 350, 350, 30)
piece2 = Piece(canvas, 250, 250, 450, 450, 45)

# Fonction pour vérifier si une pièce est dans le rayon autour d'une autre pièce
def check_radius():
    radius = 300  # Rayon en pixels

    if piece1.is_in_radius(piece2, radius):
        piece1.highlight_connection_points(highlight=True)
        piece2.highlight_connection_points(highlight=True)
    else:
        piece1.highlight_connection_points(highlight=False)
        piece2.highlight_connection_points(highlight=False)

# Gestionnaire d'événements pour la souris pour vérifier le rayon au démarrage
canvas.bind("<ButtonRelease-1>", lambda event: check_radius())

# Démarrage de la boucle Tkinter
Fenetre.mainloop()
