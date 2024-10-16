from fltk import *
import time
from random import randrange
from tetrilib import *


#### constantes et variables globales ####

largeurFenetre = 1000
hauteurFenetre = largeurFenetre
yMargin = int(0.15*hauteurFenetre)

# constante
numYSquare = 20
numXSquare = 10
sizeSquareGrid = int(0.65*hauteurFenetre/numYSquare)

# on definit les variables pour les differentes pièce 
a = 1
b = 2
c = 3
d = 4
e = 5
f = 6
g = 7

squareColors = ["white", "red", "blue", "yellow", "green", "orange", "pink", ]

# structure de donnée pour représenter la grille de jeu
# la grille de jeu fait du 10 par 20 
# mais comme les pièces apparaissent au dessus des 20 de hauteur 
# on doit rajouter 4 cases sur les y
grid = []

for i in range(numYSquare + 4):
    grid.append([])
    for j in range(numXSquare):
        grid[i].append(0)

# variables globales pour chaque pièce 



def main():

    cree_fenetre(largeurFenetre, hauteurFenetre)

    #cadrillage

    yGrid = 0
    xGrid = 0
    for i in range(numYSquare):

        yGrid = hauteurFenetre - yMargin - i* sizeSquareGrid
        for j in range(numXSquare):
                
            xGrid = largeurFenetre/2 - sizeSquareGrid*numXSquare/2 + j*sizeSquareGrid
            rectangle(xGrid, yGrid, xGrid + sizeSquareGrid, yGrid - sizeSquareGrid, "gray",)
                

    x = 4
    y = 3
    ori = 0

    # grille dynamique en fonction de la taille de la fenêtre 

    # ligne basse de la grille
    ligne(largeurFenetre/2 - sizeSquareGrid*numXSquare/2, hauteurFenetre - yMargin, largeurFenetre/2 + sizeSquareGrid*numXSquare/2, hauteurFenetre - yMargin, "black", 4)

    #ligne gauche
    ligne(largeurFenetre/2 - sizeSquareGrid*numXSquare/2, hauteurFenetre - yMargin, largeurFenetre/2 - sizeSquareGrid*numXSquare/2, hauteurFenetre - yMargin - sizeSquareGrid*numYSquare, "black", 4)

    #ligne droit
    ligne(largeurFenetre/2 + sizeSquareGrid*numXSquare/2, hauteurFenetre - yMargin, largeurFenetre/2 + sizeSquareGrid*numXSquare/2, hauteurFenetre - yMargin - sizeSquareGrid*numYSquare, "black", 4)

    pieceActivated = 1

    change = 1

    while True:

        # si la dernière piece a été déposé 
        if pieceActivated == 0:

            # on génère aléatoirement numéro de la nouvelle pièce 
            n=randrange(a, g+1)

            # on fait apparaitre un pièce aléatoirement 
            # avec la fonction spawnPiece() qui prend en argument le numéro de la piece que l'on génère aléatoirement 
            spawnPiece(n=n) 

            # on initialise les coordonnées par défaut de la prièce 
            #x = 4 
            #y = 3

            # orientation par défaut de la pièce en degré
            #ori = 0

            pieceActivated = 1
        else:
            pass
        
        # il faut redessiner la grille uniquemnt si elle a changé avec le flag 'change'
        if change == 1:
            drawGrid()

            change = 0

        # il faut mettre à jour pour pouvoir afficher le cadrillage et mettre les touches en attente 
        mise_a_jour()

        #### on gère les touches ####
        
        # on enregiste l'évenement en attente le plus ancien
        ev = attend_ev()
        
        # si une touche  bien été pressé 
        if ev is not None:
            
            key = type_ev(ev)
            
            # si l'utilisateur appuis pour sur la croix ou alt + f4 pour fermer la fenêtre
            if key == 'Quitte':
                ferme_fenetre()
                break
            elif key == 'Touche':
                key = touche(ev)

                # si la touche est utile pour le jeu
                if key == 'space' or key == 'Up' or key == 'Down' or key == 'Right' or key == 'Left':
                    x, y, ori, change = keyPressed(key, x, y, ori, change)
                    printGrid()
                    

           
                


            else:
                print(key)
            






if __name__ == "__main__":
    main()