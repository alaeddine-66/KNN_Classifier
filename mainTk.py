"""
Main programme
"""

import tkinter as tk
from constants import *
from graph import Graph
from utilsTk import *
from Graham import *

root = tk.Tk()
root.title("Drawing App")
Dessin = tk.Canvas(root,height=WINDOW_HEIGHT,width=WINDOW_WIDTH,bg=BLEUE_CIEL)
Dessin.pack()

class Etat:
    def __init__(self, root, Dessin):
        self.root = root
        self.Dessin = Dessin
        
        # Liste des étiquettes
        self.labels = ["car", "fish", "house", "tree", "bicycle", "guitar", "pencil", "clock"]
        
        # Echantillons et coordonnées des échantillons
        # dict contient {id : [width , height , roundness , élongation]} 
        self.samples = ChaineTodict()
        self.samples_coord = featuresToList()

        # Echantillons et coordonnées des échantillons normalizer 
        self.val_min, self.val_max, self.samples_coord = normalizePoints(self.samples_coord)
        for i in range(len(self.samples_coord)):
            self.samples[i+1] = self.samples_coord[i]
                
        # Label le plus proche et valeur k pour la classification
        self.nearest_label = None
        self.k = 5

        # Echantillons valides
        #décommentez le ligne d'aprés si vous voulez changer le k mais il vas prendre du temps 
        # pour le calculer , et décommentez le texte en affichage 
        #self.ValidSamples = accurency(self.labels , self.samples , self.k)
        #resultat : "204/272 (75.00%)" pour k = 6

        # Création du canevas pour dessiner par-dessus avec fond blanc
        self.canvas = tk.Canvas(self.root, width=CANVAS_SIZE, height=CANVAS_SIZE, bg="white")
        self.canvas.place(x=CANVAS_X, y=CANVAS_Y)

        # Initialise une liste vide pour stocker les chemins dessinés 
        self.paths = []
        self.drawing = False

        # Création du canevas pour le graphique
        self.chart = tk.Canvas(self.root, width=GRAPH_SIZE, height=GRAPH_SIZE, bg='white')
        self.chart.place(x=GRAPH_X, y=GRAPH_Y)

        # Initialisation du graphique et association des événements
        self.graph = Graph(self.chart, self.samples_coord)

        # Affichage initial
        self.affichage()

    def affichage(self):
        # Affichage des informations
        self.Dessin.delete('all')
        draw_text(self.Dessin, "Drawing App", WINDOW_WIDTH // 2, 30, color='black', size=32)
        if self.nearest_label and self.paths :
            text = "Is it a " + self.nearest_label
            draw_text(self.Dessin, text, CANVAS_X + CANVAS_SIZE / 2, CANVAS_Y - 20, size=32)   
        else:
            text = "                Please draw something from the list:\n" + str(self.labels)
            draw_text(self.Dessin, text, CANVAS_X + CANVAS_SIZE / 2, CANVAS_Y - 20, size=15)       
        
        # Exactitude
        draw_text(self.Dessin, "ACCURACY", WINDOW_WIDTH * 5 // 6, 30, color='black', size=20) 
        #draw_text(self.Dessin, f"{self.ValidSamples}/{len(self.samples_coord)} ({self.ValidSamples / len(self.samples_coord) * 100:.2f}%)", WINDOW_WIDTH * 5 // 6, 50, color='black', size=20)  
        draw_text(self.Dessin, "204/272 (75.00%)", WINDOW_WIDTH * 5 // 6, 50, color='black', size=20)  
        
        # Efface le canevas et redessine tous les chemins
        self.canvas.delete('all')
        draw_paths(self.canvas , self.paths)
        
        # Si une fonction de mise à jour est définie et qu'il y a des chemins à mettre à jour, appelle la fonction de mise à jour
        if self.paths:
            self.onDrawingUpdate(self.paths) 

    def onDrawingUpdate(self, path):
        # Mise à jour après dessin
        points = flat(path)
        features = [width(path), height(path) , roundness(points) , getElongation(points)]
        _ , _ , features = normalizePoints([features] , self.val_min , self.val_max)
        features = flat(features)
        indices = getNearest(features, self.samples, self.k)
        self.nearest_label = Classify(indices , self.labels)          
        self.graph.showDynamicPoint(features, indices)  

état = Etat(root , Dessin) # On initialise l'état

def on_button_press(event):
    # Lorsqu'un bouton de la souris est enfoncé, commence le dessin en initialisant un nouveau chemin
    état.drawing = True
    état.paths.append([(event.x, event.y)])  # Ajoute le premier point du nouveau chemin

def draw(event):
    # Dessine lorsqu'un mouvement de la souris est détecté
    if état.drawing:
        last_path = état.paths[len(état.paths) - 1]  # Récupère le dernier chemin dessiné
        last_path.append((event.x, event.y))  # Ajoute le point actuel à ce chemin
        état.affichage()  # Redessine pour afficher la nouvelle ligne

def stop_drawing(event):
    # Lorsqu'un bouton de la souris est relâché, arrête le dessin en désactivant le drapeau de dessin
    état.drawing = False
    
def undo():
    # Annule la dernière action de dessin en retirant le dernier chemin de la liste des chemins et redessine
    if état.paths:
        état.paths.pop()
        état.affichage()

# association des événements du Sketchpad
état.canvas.bind("<ButtonPress-1>", on_button_press)
état.canvas.bind("<B1-Motion>", draw)
état.canvas.bind("<ButtonRelease-1>", stop_drawing)
undoButton = tk.Button(root,text="Undo",command=undo,width=9)
undoButton.place(x=CANVAS_X + CANVAS_SIZE / 2 - 50 , y=CANVAS_Y + CANVAS_SIZE + 20)

# Initialisation du graphique et association des événements
état.chart.bind("<ButtonPress-1>", état.graph.on_button_press)
état.chart.bind("<B1-Motion>", état.graph.on_button_move)
état.chart.bind("<ButtonRelease-1>", état.graph.on_button_release)
état.chart.bind("<Motion>", état.graph.draw_hover_info)
# Bind mouse wheel event
état.chart.bind("<MouseWheel>", état.graph.on_mouse_wheel)  # por le macOS
état.chart.bind("<Button-4>", état.graph.on_mouse_wheel)
état.chart.bind("<Button-5>", état.graph.on_mouse_wheel)
root.mainloop()

