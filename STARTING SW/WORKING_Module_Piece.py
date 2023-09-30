from tkinter import *
from math import *
from time import *
WIDTH = 400
HEIGHT =400
class Piece:
    def __init__(self, canvas, x0, y0, x1, y1, angle_deg):
        self.canvas = canvas
        self.x0, self.y0, self.x1, self.y1 = x0, y0, x1, y1
        self.angle_deg = angle_deg
        self.angle_rad = angle_deg * (pi / 180)
        self.rayon = abs(y0 - y1) / 2
        self.center_x, self.center_y = (x0 + x1) / 2, (y0 + y1) / 2

        self.detection_radius = 100 +self.rayon # Rayon de détection en pixels
        self.detection_circle = self.canvas.create_oval(0, 0, 0, 0, outline="blue", width=2)  # Cercle de détection initial

        self.ensemble_piece = {  
                                "Shape" :{  "type": "cercle",
                                            "radius" : self.rayon,
                                            "coords": (self.center_x,self.center_y),
                                            "color":'green'},
         "Cercle centre de la figure"   :{  "type":"cercle",
                                            "radius": 2,
                                            "coords" : (self.center_x,self.center_y),
                                            "color" : "black"},
                "Vecteur Connexion 1"   :{  "type" : "line",
                                            "color":"red",
                                            "coords":(self.center_x, self.center_y, self.center_x-self.rayon, self.center_y)},
                "Vecteur Connexion 2"   :{  "type":"line",
                                            "color":"red",
                                            "coords":(self.center_x, self.center_y, self.center_x+self.rayon*cos(self.angle_rad), self.center_y-self.rayon*sin(self.angle_rad))},
                "Point de connexion 1"  :{  "type":"cercle",
                                            "radius": 5,
                                            "coords" : (x0, self.center_y, x0, self.center_y),
                                            "color" : "purple"},     
                "Point de connexion 2"  :{  "type": "cercle",
                                            "radius": 5,
                                            "coords" : (self.center_x + self.rayon * cos(self.angle_rad), self.center_y - self.rayon * sin(self.angle_rad), self.center_x + self.rayon * cos(self.angle_rad), self.center_y - self.rayon * sin(self.angle_rad)),
                                            "color" : "purple"},                   
                                         }
        self.constructor(self.ensemble_piece)
        
        self.is_dragging = False
        self.prev_x, self.prev_y = 0, 0

        self.detection_radius = 100  # Rayon de détection en pixels
        self.detection_circle = None

        # Gestion des événements pour le déplacement de la pièce
        self.canvas.tag_bind(self.ensemble_piece["Shape"]["object"], "<ButtonPress-1>", self.on_click)
        self.canvas.tag_bind(self.ensemble_piece["Shape"]["object"], "<B1-Motion>", self.on_drag)
        self.canvas.tag_bind(self.ensemble_piece["Shape"]["object"], "<ButtonRelease-1>", self.on_release)

    def on_release(self,event):
        self.is_dragging = False
    def on_click(self, event):
        self.is_dragging = True
        self.prev_x, self.prev_y = event.x, event.y
    def on_drag(self, event):

        if self.is_dragging:
            dx = event.x - self.prev_x
            dy = event.y - self.prev_y
            for piece in self.ensemble_piece.values():
                self.canvas.move(piece["object"],dx,dy)
            self.prev_x, self.prev_y = event.x, event.y
    
    def check_collision(self, other_piece):
        x1, y1 = self.center_x, self.center_y
        x2, y2 = other_piece.center_x, other_piece.center_y
        distance = sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        return distance <= self.detection_radius + other_piece.detection_radius

    def highlight_connection_points(self,pieces):
        self.canvas.itemconfig(self.point_conn1, width=4)
        self.canvas.itemconfig(self.point_conn2, width=4)

        collision_detected = False  # Indicateur de collision détectée

        for piece in pieces:
            self.canvas.itemconfig(piece.point_conn1, width=4)
            self.canvas.itemconfig(piece.point_conn2, width=4)
            if piece is not self and self.check_collision(piece):
                self.canvas.itemconfig(self.point_conn1, width=10)
                self.canvas.itemconfig(self.point_conn2, width=10)
                self.canvas.itemconfig(piece.point_conn1, width=10)
                self.canvas.itemconfig(piece.point_conn2, width=10)
                collision_detected = True  # Collision détectée
                break
    def constructor(self,construct):
        for data in construct.values():
            if data["type"]=="cercle":
                ##Centre cercle
                xc0,yc0= data["coords"][0]-data["radius"],data["coords"][1]-data["radius"]
                xc1,yc1= data["coords"][0]+data["radius"],data["coords"][1]+data["radius"]
                data["object"]=self.canvas.create_oval(xc0,yc0,xc1,yc1, fill=data["color"])
            if data["type"]=="line":
                data["object"]=self.canvas.create_line(data["coords"], fill=data["color"])
            if data["type"]=="rectangle":
                data["object"]=self.canvas.create_rectangle(data["coords"], fill=data["color"])