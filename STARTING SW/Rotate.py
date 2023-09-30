from tkinter import *
from math import*

WIDTH = 400
HEIGHT = 400
CANVAS_MID_X = WIDTH/2
CANVAS_MID_Y = HEIGHT/2
SIDE = WIDTH/4
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
        self.vect2 = self.canvas.create_line(self.center_x, self.center_y, x1, self.center_y - (x1 - self.center_x) * tan(self.angle_rad), fill="red", width=2)

        self.point_conn1 = self.canvas.create_oval(x0, self.center_y, x0, self.center_y, fill="purple", width=10)
        self.point_conn2 = self.canvas.create_oval(self.center_x + self.rayon * cos(self.angle_rad), self.center_y - self.rayon * sin(self.angle_rad), self.center_x + self.rayon * cos(self.angle_rad), self.center_y - self.rayon * sin(self.angle_rad), fill="purple", width=10)

        self.detection_radius = 100 +self.rayon # Rayon de détection en pixels
        self.detection_circle = self.canvas.create_oval(0, 0, 0, 0, outline="blue", width=2)  # Cercle de détection initial

            
        self.is_dragging = False
        self.prev_x = 0
        self.prev_y = 0
root = Tk()
canvas = Canvas(root, bg="black", height=HEIGHT, width=WIDTH)
canvas.pack()

vertices = [
    [CANVAS_MID_X - SIDE/2, CANVAS_MID_Y - SIDE/2],
    [CANVAS_MID_X + SIDE/2, CANVAS_MID_Y - SIDE/2],
    [CANVAS_MID_X + SIDE/2, CANVAS_MID_Y + SIDE/2],
    [CANVAS_MID_X - SIDE/2, CANVAS_MID_Y + SIDE/2],
]

def rotatebis(figures, angle, center):
    angle = radians(angle)
    cos_val = cos(angle)
    sin_val = sin(angle)
    cx, cy = center
    new_figures=[]
    for points in figures:
        new_points = []
        for i in range(2):
            x_old, y_old=points[2*i:2*(i+1)]
            x_old -= cx
            y_old -= cy
            x_new = x_old * cos_val - y_old * sin_val
            y_new = x_old * sin_val + y_old * cos_val
            new_points.append(x_new + cx)
            new_points.append(y_new + cy)
        new_figures.append(new_points)
    return new_figures

def constructor(points,construct):
    type = [construct[i][0] for i in range(len(construct))]
    color = [construct[i][1] for i in range(len(construct))]
    
    for i in range(len(construct)):
        if (type[i]=="cercle"):
           canvas.create_oval(points[i],fill=color[i]) 
        elif(type[i]=="line"):
            canvas.create_line(points[i],fill=color[i])


base_test=[(200,200,300,300),(0,0,WIDTH,HEIGHT)],[["cercle","red"],["line","green"]]
center = (CANVAS_MID_X, CANVAS_MID_Y)

constructor(base_test[0],base_test[1])
print("Old Figure: ",base_test[0])
new_figures=rotatebis(base_test[0],50,center)
print("New Figure: ",new_figures)
constructor(new_figures,base_test[1])

#new_square = rotate(vertices, 30, center)
#print("basique: ",trait,"rotate: ",rotate(trait,40,center))
#canvas.create_line(rotate(trait,90,center),fill='green')

#draw_square(new_square)

mainloop()