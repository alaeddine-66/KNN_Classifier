"""
Visualisations de l'algorithm de Graham Scan ET minimum bounding Box
"""

import tkinter as tk
import random
from Graham import *

# Création d'une fenêtre Tkinter
root = tk.Tk()
root.title("Visualisation de l'algorithme de Graham")

# Taille de la fenêtre
canvas_width = 600
canvas_height = 400

# Création du canevas
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="white")
canvas.pack()

# Fonction pour dessiner les points
def draw_points(points):
    for point in points:
        x, y = point
        canvas.create_oval(x-2, y-2, x+2, y+2, fill="black")

# Fonction pour dessiner une ligne entre deux points
def draw_line(p1, p2):
    canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill="blue")

# Fonction pour dessiner le contour convexe
def draw_convex_hull(convex_hull , color='black'):
    for i in range(len(convex_hull)):
        canvas.create_line(convex_hull[i], convex_hull[(i+1)%len(convex_hull)] , fill=color)

# Fonction de visualisation de l'algorithme de Graham
def visualize_graham_scan():
    canvas.delete('all')
    # Génération aléatoire de points
    num_points = 20
    points = [(random.randint(50, canvas_width-50), random.randint(50, canvas_height-50)) for _ in range(num_points)]
    # Dessiner les points initiaux
    draw_points(points)

    # Appliquer l'algorithme de Graham
    convex_hull = graham_scan(points)

    #appliquer minimum box bondries
    mbox = minimum_bounding_box(points)
    vertices = mbox['vertices']

    # Dessiner le contour convexe
    draw_convex_hull(convex_hull)

    # dessiner le minimum box
    draw_convex_hull(vertices, 'red')

# Bouton pour lancer la visualisation
start_button = tk.Button(root, text="Visualiser Graham Scan", command=visualize_graham_scan)
start_button.pack()

# Lancement de la boucle principale Tkinter
root.mainloop()
