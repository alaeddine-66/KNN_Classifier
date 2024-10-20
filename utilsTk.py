import tkinter as tk
from math import sqrt

def draw_text(window, text, x, y, color = 'black', size=32):
    font = ("Arial", size)
    window.create_text(x, y, text=text, fill=color, font=font)

def draw_paths(window , paths):
    # Dessine tous les chemins dans la liste de chemins
    for path in paths :
        # Dessine une ligne sur le canevas à partir d'une liste de points
        for i in range(len(path) - 1):
            last_pos = (path[i][0], path[i][1])
            current_pos = (path[i + 1][0], path[i + 1][1])
            window.create_line(last_pos, current_pos, fill="black", width=5)

def getEmojis(canvas):
    # Récupérer les emojis dans le répertoire emojis 
    images = [f"emojis/{i}.png" for i in range(1, 9)]
    canvas_images = []
    for image_file in images:
        # Charger l'image avec PhotoImage
        image = tk.PhotoImage(file=image_file, master=canvas)
        canvas_images.append(image)
    return canvas_images

######### 
#   Récupérer les données du fichier features dans path
########            
def position(ch, car):
    for i in range(1 , len(ch)-1):
        if ch[i] == car:
            return i

def slice(chaine):
    list = []
    while chaine != '':
        pos = position(chaine , ',')
        if pos == None :
            list.append(float(chaine))
            chaine = ''
        else :    
            list.append(float(chaine[:pos]))
            chaine = chaine[pos+1:]
    return list    

def ChaineTodict():
    #Tourner les informations dans le fichier features en un dictionnaire
    dico = dict()
    file = open("path/features.txt" , 'r')
    for line in file:
        deux_points = position(line, ":")
        id = line[:deux_points]
        features = slice(line[deux_points+1:-1])
        dico[int(id)] = features
    file.close()        
    #dict contient {id : [width , height , roundness , élongation]} 
    return dico

def featuresToList():
    #Tourner les coordonnées dans le fichier features en une liste
    list = []
    samples  = ChaineTodict()
    for k in samples.values() :
        list.append(k)
    return list

##################

def flat(list):
    points = []
    for sous_list in list :
        for couple in sous_list :
            points.append(couple)
    return points      

def distance(p1,p2):
    # on fait une boucle pour que la fonction fonctionne meme avec dans 3D ou nD
    sqrdist = 0
    for i in range(len(p1)):
        sqrdist+=(p1[i]-p2[i])**2
    return sqrt(sqrdist)

def width(list):
    #calculer le largeur du dessin
    min = list[0][0][0]
    max =list[0][0][0]
    for L in list :
        for couple in L :
            (x,y) = couple
            if x < min :
                min = x
            if x > max :
                max = x
    return distance((min , 0) , (max , 0))   

def height(list):
    #calculer le hauteur du dessin 
    min = list[0][0][1]
    max =list[0][0][1]
    for L in list :
        for couple in L :
            (x,y) = couple
            if y < min :
                min = y
            if y > max :
                max = y
    return distance((0 , min) , (0 , max))   

def min_width(list):
    #calculer le minimum des largeurs du tous les dessins   
    min_val = list[0][0]
    for couple in list:
        if couple[0] < min_val:
            min_val = couple[0]
    return min_val   

def max_width(list):
    #calculer le max des largeurs du tous les dessins      
    max_val= list[0][0]
    for couple in list :
        if couple[0] > max_val :
            max_val = couple[0]
    return max_val

def min_height(lst):
    #calculer le minimum des hauteurs du tous les dessins  
    min_val = lst[0][1]
    for couple in lst:
        if couple[1] < min_val:
            min_val = couple[1]
    return min_val   

def max_height(list):
    #calculer le maximum des hauteurs du tous les dessins      
    max_val = list[0][1]
    for couple in list :
        if couple[1] > max_val :
            max_val = couple[1]
    return max_val              

def lerp(a, b, t):
    """
    Interpolation linéaire entre les valeurs a et b en fonction du coefficient t (entre 0 et 1)
    Elle retourne une valeur entre a et b 
    """
    return a + (b - a) * t

def invLerp(a, b, v):
    """
    L'inverse de l'interpolation linéaire
    Calcule le coefficient d'interpolation `t` entre les valeurs `a` et `b`
    """
    return (v - a) / (b - a)

def remap(oldA, oldB, newA, newB, v):
    """
    Remappe la valeur `v` de l'ancienne plage [oldA, oldB] à la nouvelle plage [newA, newB].
    """
    return lerp(newA, newB, invLerp(oldA, oldB, v))

def remapPoint(oldBounds, newBounds, point):
    """
    Remappe un point de l'ancienne plage de bornes à la nouvelle plage de bornes.
    """
    return [
        remap(oldBounds['left'], oldBounds['right'], newBounds['left'], newBounds['right'], point[0]),
        remap(oldBounds['top'], oldBounds['bottom'], newBounds['top'], newBounds['bottom'], point[1])
    ]

def add(p1, p2):
    """
    Ajoute deux vecteurs p1 et p2.
    """
    return [
        p1[0] + p2[0],
        p1[1] + p2[1]
    ]

def substract(p1, p2):
    """
    Soustrait deux vecteurs p2 de p1.
    """
    return [
        p1[0] - p2[0],
        p1[1] - p2[1]
    ]

def scale(p, scaler):
    """
    Multiplie un vecteur p par un scalaire.
    """
    return [
        p[0] * scaler,
        p[1] * scaler
    ]

def cercle(surface, x, y, rayon, épaisseur, couleur):
    p1 = (x - rayon, y - rayon)
    p2 = (x + rayon, y + rayon)
    (w, c) = (épaisseur, couleur)
    surface.create_oval(p1, p2, width=w, outline=c)

# K Nearest Neighbour

def distance_to_loc(point, loc):
    """
    Calcule la distance entre un point et une position donnée.
    """
    return distance(loc, point["val"])

def custom_sorted(obj, loc):
    """
    Trie une liste d'objets en fonction de leur distance à une position donnée.
    """
    for i in range(len(obj)):
        for j in range(i + 1, len(obj)):
            if distance_to_loc(obj[i], loc) > distance_to_loc(obj[j], loc):
                obj[i], obj[j] = obj[j], obj[i]

def getNearest(loc, points, k=1):
    """
    Retourne les indices des k points les plus proches d'une position donnée.
    """
    obj = [{"ind": key, "val": points[key]} for key in points]
    custom_sorted(obj, loc)
    indices = [obj["ind"] for obj in obj]
    return indices[:k]

#Classification :

def Classify(indices , labels):
    """Cette fonction détermine le label le plus proche des features donnés"""
    nearestLabels = [labels[(i - 1) % len(labels)] for i in indices]
    counts = dict()
    for label in nearestLabels:
        if label in counts:
            counts[label] += 1
        else:
            counts[label] = 1
    max_count = 0
    nearest_label = None
    for label in counts:
        if counts[label] > max_count:
            max_count = counts[label]
            nearest_label = label  
    return nearest_label   

def accurency(labels , samples , k):
    import time
    # Calcule l'exactitude en fonction de k
    acc = 0
    print('RUNNING CLASSIFICATION ...')
    for coord in samples:
        #affichage de progrés
        progress = f"{acc/len(samples)*100:.2f}%"
        print("\r" + "ACCURACY : " + progress, end="")
        time.sleep(0.1)  # Simuler un téléchargement en attente

        #l'algorithme
        indices = getNearest(samples[coord], samples, k)
        nearest_label = Classify(indices , labels) 
        if nearest_label == labels[(coord - 1) % len(labels)]:
            acc += 1 
    print("\nDONE!")           
    return acc  

# normalisation 
"""
On utilise la normalisation par ce que les valeurs de largeur et hauteurs sont tros grandees (plus grand que 100)
Tandis que les valeurs de rondness sont entre 0 et 1 et ceux de l'élongations sont inférieurs à 10 
d'ou quand on fait la distance avec ces valeurs le poids de la roundness et l'elongation est négligeable devant les autres
d'ou grace a la normalisation on peut rendre tous les facteurs entre 0 et 1 d'où ils auront le meme poids pour la classification
"""

def normalizePoints(points , Min=None , Max=None):
    dimension = len(points[0])
    if Min and Max :
        val_min = Min
        val_max = Max
    else :    
        val_min = points[0][:]
        val_max = points[0][:]
        for i in range(1, len(points)):
            for j in range(dimension):
                val_min[j] = min(val_min[j], points[i][j])
                val_max[j] = max(val_max[j], points[i][j])
    for i in range(len(points)):
        for j in range(dimension):
            points[i][j] = invLerp(val_min[j], val_max[j], points[i][j])
    return val_min , val_max , points