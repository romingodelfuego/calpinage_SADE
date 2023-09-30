from tkinter import *
from math import *
import json

WIDTH = 400
HEIGHT = 400
CANVAS_MID_X = WIDTH / 2
CANVAS_MID_Y = HEIGHT / 2
SIDE = WIDTH / 4

root = Tk()
canvas = Canvas(root, bg="black", height=HEIGHT, width=WIDTH)
canvas.pack()


def translate(figures):
    coords=[]
    for value in figures.values():
        coords.append(value["coords"])
    return coords
def change(figures, new_coords):
    i=0
    for value in figures.values():
        value["coords"]=new_coords[i]
        i+=1
    return figures

def rotatebis(figures, angle, center):

    coords =translate(figures)
    angle = radians(angle)
    cos_val = cos(angle)
    sin_val = sin(angle)
    cx, cy = center
    new_coords = []
    for points in coords:
        new_points = []
        for i in range(len(points)//2):
            x_old, y_old = points[2 * i : 2 * (i + 1)]
            x_old -= cx
            y_old -= cy
            x_new = x_old * cos_val - y_old * sin_val
            y_new = x_old * sin_val + y_old * cos_val
            new_points.append(x_new + cx)
            new_points.append(y_new + cy)
        new_coords.append(new_points)
    return change(figures,new_coords)


def constructor(construct):
    for data in construct.values():
        if data["type"]=="cercle":
            ##Centre cercle
            xc0,yc0= data["coords"][0]-data["radius"],data["coords"][1]-data["radius"]
            xc1,yc1= data["coords"][0]+data["radius"],data["coords"][1]+data["radius"]
            data["object"]=canvas.create_oval(xc0,yc0,xc1,yc1, fill=data["color"]) ##For click event
            canvas.create_oval(xc0,yc0,xc1,yc1, fill=data["color"])
        if data["type"]=="line":
            data["object"]=canvas.create_line(data["coords"], fill=data["color"])
            canvas.create_line(data["coords"], fill=data["color"])

center = (CANVAS_MID_X, CANVAS_MID_Y)
base_test2 ={   "cercle":{"color":"red",
                        "radius":50,
                        "coords":(100,100)  #Centre
                        },
                "line":{"color":"green",
                        "coords":(0,0,300,300)}
                        }

x0, y0, x1, y1,angle_deg = 150, 150, 350, 350, 20
angle_rad=angle_deg * (pi / 180)
rayon=abs(y0 - y1) / 2
center_x, center_y=(x0 + x1) / 2, (y0 + y1) / 2

ensemble_piece = {  
                "Cercle de limitation de pièce":{
                                            "type": "cercle",
                                            "radius" : rayon,
                                            "coords": (center_x,center_y),
                                            "color":'green'},
                    "Cercle centre de la figure":{
                                            "type":"cercle",
                                            "radius": 2,
                                            "coords" : (center_x,center_y),
                                            "color" : "black"},
                    "Vecteur Connexion 1":{ "type" : "line",
                                            "color":"red",
                                            "coords":(center_x, center_y, center_x-rayon, center_y)},
                    "Vecteur Connexion 2":{ "type":"line",
                                            "color":"red",
                                            "coords":(center_x, center_y, center_x+rayon*cos(angle_rad), center_y-rayon*sin(angle_rad))},
                    "Point de connexion 1":{
                                            "type":"cercle",
                                            "radius": 5,
                                            "coords" : (x0, center_y, x0, center_y),
                                            "color" : "purple"},     
                    "Point de connexion 2":{
                                            "type": "cercle",
                                            "radius": 5,
                                            "coords" : (center_x + rayon * cos(angle_rad), center_y - rayon * sin(angle_rad), center_x + rayon * cos(angle_rad), center_y - rayon * sin(angle_rad)),
                                            "color" : "purple"},                   
                                         }
#constructor(base_test2)
#print("Old Figure:", base_test2)
#new_figures = rotatebis(base_test2, 180, center)
#print("New Figure:", new_figures)
#constructor(new_figures)
#print(translate(base_test2))
constructor(ensemble_piece)
constructor(rotatebis(ensemble_piece,180,center))
mainloop()