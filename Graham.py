from math import pi , sqrt
from utilsTk import distance

#lancer visualisation.py pour comprendre l'algorithme

############################################
##                                        ##
##          Graham Scan Algorithm         ## 
##                                        ## 
############################################


""" Trouve un point avec la position verticale la plus basse (le plus à gauche en cas d'égalité)"""
def lowest_point(points):
    lowest = points[0]
    for point in points[1:]:
        if point[1] < lowest[1]:
            lowest = point
        elif point[1] == lowest[1] and point[0] < lowest[0]:
            lowest = point
    return lowest

def distance_squared(p1, p2):
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    return dx * dx + dy * dy

def get_orientation(p1, p2, p3):
    # Calcul du produit vectoriel entre les vecteurs (p2 - p1) et (p3 - p1)
    cross_product = (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])

    if cross_product == 0:
        return 0  # Les points sont colinéaires
    elif cross_product > 0:
        return 1  # Orientation horaire
    else:
        return -1  # Orientation anti-horaire

def compare(origin , p1, p2):
        # Comparaison des produits vectoriels pour déterminer l'orientation
        cross = get_orientation(origin, p1, p2)
        if cross == 0:
            # Si les points sont colinéaires, choisir le plus proche
            return distance_squared(origin, p1) - distance_squared(origin, p2)
        return -cross

def sort_points(origin ,points):
    # Tri des points en utilisant l'algorithme de tri de sélection avec la fonction de comparaison personnalisée
    n = len(points)
    for i in range(n - 1):
        min_index = i
        for j in range(i + 1, n):
            if compare(origin ,points[j], points[min_index]) < 0:
                min_index = j
        points[i], points[min_index] = points[min_index], points[i]
    
    return points

def graham_scan(points):
    the_lowest_point = lowest_point(points)
    sorted_points = sort_points(the_lowest_point, points)

    # Initialisation de la pile avec les trois premiers points
    stack = [sorted_points[0], sorted_points[1], sorted_points[2]]

    # Itération sur les points restants
    for i in range(3, len(sorted_points)):
        top = len(stack) - 1
        # Exclure les points à partir de la fin
        # jusqu'à ce qu'ajouter un nouveau point ne cause pas de concavité
        # de sorte que le polygone résultant sera convexe
        while top > 0 and get_orientation(stack[top - 1], stack[top], sorted_points[i]) <= 0:
            stack.pop()
            top -= 1
        # Ajouter le point
        stack.append(sorted_points[i])

    return stack

def coincident_box(hull, i, j):
    # Fonction pour calculer la différence entre deux points (vecteur les connectant)
    def diff(a, b):
        return [a[0] - b[0], a[1] - b[1]]
    
    # Produit scalaire de deux vecteurs
    def dot(a, b):
        return a[0] * b[0] + a[1] * b[1]
    
    # Longueur d'un vecteur
    def length(a):
        return (a[0] ** 2 + a[1] ** 2) ** 0.5
    
    # Addition de deux vecteurs
    def add(a, b):
        return [a[0] + b[0], a[1] + b[1]]
    
    # Multiplication d'un vecteur par une magnitude donnée
    def mult(a, n):
        return [a[0] * n, a[1] * n]
    
    # Division d'un vecteur par une magnitude donnée
    def div(a, n):
        return [a[0] / n, a[1] / n]
    
    # Crée un vecteur unitaire (de longueur 1) avec la même direction qu'un vecteur donné
    def unit(a):
        l = length(a)
        if l == 0:
            return [0, 0]  # ou une autre valeur appropriée
        return div(a, l)

    origin = hull[i]
    # Construit les vecteurs de base pour un nouveau système de coordonnées
    # où l'axe x est coincident avec le bord i-j
    base_x = unit(diff(hull[j], origin))
    # et l'axe y est orthogonal (rotation de 90 degrés dans le sens antihoraire)
    base_y = [base_x[1], -base_x[0]]

    left = right = top = bottom = 0
    # Pour chaque point d'une coque convexe
    for p in hull:
        # Calcule la position par rapport à l'origine
        n = [p[0] - origin[0], p[1] - origin[1]]
        # Calcule la position dans le nouveau système d'axes (rotation)
        v = [dot(base_x, n), dot(base_y, n)]
        # Applique une logique triviale pour calculer la boîte englobante
        # car la rotation n'est pas prise en compte à ce stade
        left = min(v[0], left)
        top = min(v[1], top)
        right = max(v[0], right)
        bottom = max(v[1], bottom)

    # Calcule les sommets de la boîte englobante dans l'espace d'écran original
    vertices = [
        add(add(mult(base_x, left), mult(base_y, top)), origin),
        add(add(mult(base_x, left), mult(base_y, bottom)), origin),
        add(add(mult(base_x, right), mult(base_y, bottom)), origin),
        add(add(mult(base_x, right), mult(base_y, top)), origin)
    ]

    return {
        'vertices': vertices,
        'width': right - left,
        'height': bottom - top
    }

def minimum_bounding_box(points, hull=None):
    if len(points) < 3:
        return {
            'width': 0,
            'height': 0,
            'vertices': points,
            'hull': points
        }
    
    hull = hull or graham_scan(points)

    min_area = float('inf')
    result = None
    for i in range(len(hull)):
        cbox = coincident_box(hull, i, (i + 1) % len(hull))
        vertices, width, height = cbox['vertices'] , cbox['width'] , cbox['height']
        area = width * height
        if area < min_area:
            min_area = area
            result = {'vertices': vertices, 'width': width, 'height': height, 'hull': hull}
    
    return result

##############################
##                          ##
##         Roundness        ##
##                          ##
############################## 

def roundness(polygon):
    bbox = minimum_bounding_box(polygon)
    points = bbox['hull']
    length = calculate_length(points)
    area = calculate_area(points)
    R = length / (pi * 2)
    circle_area = pi * R ** 2
    roundness = area / circle_area if circle_area != 0 else 0
    return roundness

def calculate_length(polygon):
    length = 0
    for i in range(len(polygon)):
        next_i = (i + 1) % len(polygon)
        length += distance(polygon[i], polygon[next_i])
    return length

def calculate_area(polygon):
    area = 0
    A = polygon[0]
    for i in range(1, len(polygon) - 1):
        B = polygon[i]
        C = polygon[i + 1]
        area += triangle_area(A, B, C)
    return area

def triangle_area(A, B, C):
    a = distance(B, C)
    b = distance(A, C)
    c = distance(A, B)

    p = (a + b + c) / 2
    area = sqrt(p * abs((p - a)) * abs((p - b)) * abs((p - c)))
    return area

##############################
##                          ##
##        Elongation        ##
##                          ##
############################## 

def getElongation(paths):
    mbox =  minimum_bounding_box(paths)
    width ,height = mbox['width'] , mbox['height']
    # on fait +1 pour éviter le cas de division par 0
    return ( max(width, height) +1) / ( min(width, height)+1)
