from constants import *
from utilsTk import *

class Graph:
    def __init__(self, canvas, samples):
        self.canvas = canvas
        self.samples = samples
        
        # Marge pour la taille du graphique
        self.margin = GRAPH_SIZE * 0.1
        
        # Coordonnées du point dynamique et de l'échantillon le plus proche
        self.DynamicPoint = [min_width(self.samples), min_height(self.samples)]
        self.indexNearestSamples = 0
        
        # Limites des données et limites des pixels
        self.defaultDataBounds = self.getDataBounds()
        self.pixelBounds = self.pixelBoundes()
        self.dataBounds = self.getDataBounds()
        
        # Pas pour le zoom
        self.step = 0.02
        
        # Transformation des données (zoom et décalage)
        self.datatrans = {'offset': [0, 0], 'scale': 1}
        
        # Informations pour le déplacement
        self.dragInfo = {'start': [0, 0], 'end': [0, 0], 'offset': [0, 0], 'dragging': False}
        
        # Point survolé et correspondance classe/image
        self.hovered_point = None
        self.classes = {0: "Car", 1: "Fish", 2: "House", 3: "Tree", 4: "Bycicle", 5: "Guitar", 6: "Pencil", 7: "Clock"}
        #self.images = {0: '🚗', 1: "🐟", 2: "🏠", 3: "🌳", 4: "🚲", 5: "🎸", 6: "✏️", 7: "🕗"} 
        self.emojis = getEmojis(self.canvas) 
        
        self.draw()
        
    def showDynamicPoint(self , features , indexNearestSamples):
        # Affiche le point dynamique et met à jour l'index de l'échantillon le plus proche
        self.DynamicPoint = features
        self.indexNearestSamples = indexNearestSamples
        self.draw()

    def pixelBoundes(self):
        pixelBounds = {
            'left' : self.margin , 
            'right' : GRAPH_SIZE - self.margin,
            'top' : self.margin  ,
            'bottom' : GRAPH_SIZE - self.margin
        }
        return pixelBounds
    
    def getDataBounds(self):
            min_X = min_width(self.samples)
            max_X = max_width(self.samples)
            min_Y = min_height(self.samples)
            max_Y = max_height(self.samples)
            dataBounds = {
                'left': min_X,
                'right': max_X,
                'top': max_Y,
                'bottom': min_Y
            }
            return dataBounds
 
    def draw_Axes(self):
        #afficher les titres
        draw_text(self.canvas,'width', self.pixelBounds['right']  , self.pixelBounds['right'] +25, 'black'  , size=25)
        draw_text(self.canvas,'height', self.pixelBounds['left']   ,self.pixelBounds['top'] - 25, 'black'  , size=25)

        #afficher les axes
        self.canvas.create_line( self.pixelBounds['left'] , self.pixelBounds['top'] ,self.pixelBounds['left'] , self.pixelBounds['bottom'] , fill='black')
        self.canvas.create_line( self.pixelBounds['left'] , self.pixelBounds['bottom'] ,self.pixelBounds['right'] , self.pixelBounds['bottom'] , fill = 'black')

        data_min = remapPoint(self.pixelBounds , self.dataBounds , [self.pixelBounds['left'] , self.pixelBounds['bottom']])
        draw_text(self.canvas,f'{data_min[0]:.2f}', self.pixelBounds['left'] , self.pixelBounds['bottom'] + 20 , 'black'  , size=25) 
        draw_text(self.canvas,f'{data_min[1]:.2f}', self.pixelBounds['left'] -20 , self.pixelBounds['bottom']-15 , 'black'  , size=25) 

        data_max = remapPoint(self.pixelBounds , self.dataBounds , [self.pixelBounds['right'] , self.pixelBounds['top']])
        draw_text(self.canvas,f'{data_max[0]:.2f}', self.pixelBounds['right'] , self.pixelBounds['right'] + 5 , 'black'  , size=25)   
        draw_text(self.canvas,f'{data_max[1]:.2f}', self.pixelBounds['left'] - 25  , self.pixelBounds['top'] , 'black'  , size=25)  

    def draw_Samples(self):
        # Dessine les échantillons sur le graphique
        id = 0
        for sample in self.samples :
            pixelLoc = remapPoint(self.dataBounds , self.pixelBounds , sample)
            self.canvas.create_image(pixelLoc[0], pixelLoc[1], anchor=tk.NW, image=self.emojis[id%8])
            #draw_text(self.canvas , self.images[id%8] , pixelLoc[0], pixelLoc[1] , size=10)
            id +=1

    def draw(self):
        self.canvas.delete('all') 
        self.draw_Samples()

        #dessiner le DynamycPoint (notre Araignée)
        pixelLoc = remapPoint(self.dataBounds , self.pixelBounds , self.DynamicPoint)
        cercle(self.canvas , pixelLoc[0] , pixelLoc[1] , 5 , 5 , 'black')
        # Dessiner les lignes qui attache notre desin avec les autres dessin (les membres de l'Araignée)
        if self.indexNearestSamples !=0 :
            for indexNearestSample in self.indexNearestSamples :
                # on enléve 1 à indexNearestSample parceque features id commences par 1 tandis que le premier label dans self.label (car) commence par 0
                # on utulise cette ligne quand on travail avec des emojis 
                #self.canvas.create_line(pixelLoc, remapPoint(self.dataBounds , self.pixelBounds , self.samples[indexNearestSample - 1] ) ,fill='black' )
                #on travail avec cette ligne quand on travail avec les emojis qui sont dans le répertoire emojis 
                self.canvas.create_line(pixelLoc, add(remapPoint(self.dataBounds , self.pixelBounds , self.samples[indexNearestSample - 1] ) , (10,10) ) ,fill='black' )

        self.draw_Axes()     

    def getmouse(self, event):
        # Récupère les coordonnées de la souris
        pixelLoc = [
            event.x - GRAPH_X - 400,
            event.y - GRAPH_Y
        ]
        dataLoc = remapPoint(
                self.pixelBounds,
                self.defaultDataBounds, 
                pixelLoc
            )
        return dataLoc

    def updateDataBounds(self, offset , scale):
        # Met à jour les limites des données en fonction du zoom et du décalage

        self.dataBounds['left'] = self.defaultDataBounds['left'] + offset[0]
        self.dataBounds['right'] = self.defaultDataBounds['right'] + offset[0]
        self.dataBounds['top'] = self.defaultDataBounds['top'] + offset[1]
        self.dataBounds['bottom'] = self.defaultDataBounds['bottom'] + offset[1]
        
        center = [
            (self.dataBounds['left'] + self.dataBounds['right'] )/2 , 
            (self.dataBounds['top'] + self.dataBounds['bottom'] )/2
        ]
        self.dataBounds['right'] = lerp(center[0] , self.dataBounds['right'] , scale**2)
        self.dataBounds['left'] = lerp(center[0] , self.dataBounds['left'] , scale**2)
        self.dataBounds['top'] = lerp(center[1] , self.dataBounds['top'] , scale**2)
        self.dataBounds['bottom'] = lerp(center[1] , self.dataBounds['bottom'] , scale**2)

    def on_button_press(self, event):
        # Lorsqu'un bouton de la souris est enfoncé, démarre le déplacement
        data_loc = self.getmouse(event)
        self.dragInfo['start'] = data_loc
        self.dragInfo['dragging'] = True

    def on_mouse_wheel(self, event):
        # Gère le zoom avec la molette de la souris
        delta = event.delta
        if event.num == 5 or delta < 0:
            # Scroll vers le haut ou delta négatif
            self.datatrans['scale'] += self.step
        elif event.num == 4 or delta > 0:
            # Scroll vers le bas ou delta positif
            self.datatrans['scale'] -= self.step
        self.datatrans['scale'] = max(self.step, min(2, self.datatrans['scale']))
        self.updateDataBounds(self.datatrans['offset'], self.datatrans['scale'])
        self.draw()
   

    def on_button_move(self, event):
        # Déplace les données lorsque la souris est déplacée
        if self.dragInfo['dragging']:
            data_loc = self.getmouse(event)
            self.dragInfo['end'] = data_loc
            self.dragInfo['offset'] = scale(
                substract(self.dragInfo['start'], self.dragInfo['end']),
                self.datatrans['scale'])
            new_offset = add(self.dragInfo['offset'], self.datatrans['offset'])
            self.updateDataBounds(new_offset, self.datatrans['scale'])
            self.draw()
            
    def on_button_release(self , event):
        # Fin du déplacement
        self.datatrans['offset'] = add(self.dragInfo['offset'], self.datatrans['offset'])
        self.dragInfo['dragging'] = False        

    def check_hover(self, pos):
        # Vérifie si la souris survole un échantillon
        min_dist = dist = distance(pos, remapPoint(self.dataBounds, self.pixelBounds, self.samples[0]))
        min_index = 0
        for i  in range(1,len(self.samples)):
            pixelLoc = remapPoint(self.dataBounds, self.pixelBounds, self.samples[i])
            dist = distance(pos, pixelLoc)
            if dist < min_dist:
                min_dist = dist
                min_index = i
        if min_dist < 5 :
            return min_index
        else :
            return None

    def draw_hover_info(self , event):
         # Dessine des informations supplémentaires lorsqu'un échantillon est survolé
        self.hovered_point = self.check_hover((event.x, event.y))
        if self.hovered_point is not None:
            # Dessiner le texte
            class_name = self.classes[self.hovered_point % 8]
            draw_text(self.canvas,f"{self.hovered_point+1}:{class_name}" , GRAPH_Y+ GRAPH_SIZE/2 - 50 , GRAPH_Y - 30 , 'black', size=32) 

        else:
            self.draw()