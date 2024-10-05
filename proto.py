from fltk import *
import time
from random import randrange


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
            

def drawGrid():
    yGrid = 0
    xGrid = 0
    for i in range(numYSquare):

        yGrid = hauteurFenetre - yMargin - sizeSquareGrid*numYSquare + i* sizeSquareGrid
        for j in range(numXSquare):
            
            # on enregistre la couleur de la case
            n = grid[i][j]

            xGrid = largeurFenetre/2 - sizeSquareGrid*numXSquare/2 + j*sizeSquareGrid

            if n == 0:
                rectangle(xGrid, yGrid, xGrid + sizeSquareGrid, yGrid + sizeSquareGrid, "gray", "white")
            else:
                rectangle(xGrid, yGrid, xGrid + sizeSquareGrid, yGrid + sizeSquareGrid, squareColors[n], squareColors[n])

                
def printGrid():
    """affiche la grille de jeu pour débuggé"""
    for y in range(len(grid)):
        print(grid[y])
    return


def keyPressed(key, x, y, ori, change):
    """prends en argument la touche pressée et appelle differentes fonction selon la touche pressée"""
    print(key)

    # pour touner la pièce d'1/4 vers la droite
    if key == 'Up':
        x, y, ori = rotatePiece(1, x, y, ori)

        change = 1
        return x, y, ori, change

    # pour déplacer la pièce de une case vers la gauche
    if key == 'Left':
        return x, y, ori, change


    # pour déplacer la pièce de une case vers la gauche
    elif key == 'Right':

        return x, y, ori, change

    
    # pour placer intantanément la pièce 
    elif key == 'space':
        return x, y, ori, change


    # 'down' pour baisser la pièce plus rapidement 
    else:

        return x, y, ori, change
        


def drawPiece(n, x, y, ori):
    """dessine la pièce a sur la gille avec comme coordonné x, y du pixel réference 
    (le pixel le plus en bas de la pièce dans son orientation par défaut) et son orientation  
    ATTENTION il n'y a pas de verification a ce que la pièce rentre dans la grille"""
    
    if n == a:
        drawPieceA(x, y, ori)    
    elif n == b:
        drawPieceB(x, y, ori)  

       

def drawPieceA(x, y, ori, erase=0):
    """
    toutes les positions 
    0 0 0 0 0 0
    0 0 1 1 0 0
    0 1 1 1 1 0
    0 1 1 1 1 0
    0 0 1 1 0 0
    0 0 0 0 0 0

    les pixels de réference sont les 4 pixels du milieu


    position à 0°
    0 0 0 0 0 0
    0 0 1 0 0 0
    0 0 1 0 0 0
    0 0'1'0 0 0
    0 0 1 0 0 0
    0 0 0 0 0 0

    position à 90° 
    0 0 0 0 0 0
    0 0 0 0 0 0
    0 1 1'1'1 0
    0 0 0 0 0 0
    0 0 0 0 0 0
    0 0 0 0 0 0

    position à 90°
    0 0 0 0 0 0 
    0 0 0 1 0 0 
    0 0 0 1 0 0 
    0 0 0'1'0 0 
    0 0 0 1 0 0 
    0 0 0 0 0 0 

    position à 270° 
    0 0 0 0 0 0
    0 0 0 0 0 0
    0 0 0 0 0 0
    0 1 1'1'1 0
    0 0 0 0 0 0
    0 0 0 0 0 0
    

    """

    if erase == 1:
        val = 0
    else:
        val = a
        print(f"x = {x}, y = {y}, ori = {ori}, n = {a}")


    if ori == 0:
        grid[y+1][x] = val
        grid[y][x] = val
        grid[y-1][x] = val
        grid[y-2][x] = val

    # si la pièce est orienté horizontalement 
    elif ori == 90:
        # on déplace le pixel de réference 

        grid[y][x+1] = val
        grid[y][x] = val
        grid[y][x-1] = val
        grid[y][x-2] = val

    elif ori == 180:
        # on déplace le pixel de réference 
        

        grid[y+1][x] = val
        grid[y][x] = val
        grid[y-1][x] = val
        grid[y-2][x] = val

    elif ori == 270:
        # on déplace le pixel de réference 

        grid[y][x+1] = val
        grid[y][x] = val
        grid[y][x-1] = val
        grid[y][x-2] = val



# on pourrait rassembler les pièce b et c dans une meme fonction mais ca compliquerait le code plus qu'autre chose 
def drawPieceB(x, y, ori, erase=0):
    """
    les x et y en argument sont les coordonnées du pixel qui sera toujour plein quel que soit l'orientation de la pièce

    position à 0° 
    0 0 0 0 0
    0 0 2 2 0 
    0 0 2 0 0
    0 0 2 0 0 
    0 0 0 0 0

    position à 90°
    0 0 0 0 0
    0 0 0 0 0 
    0 2 2 2 0
    0 0 0 2 0 
    0 0 0 0 0

    position à 180° 
    0 0 0 0 0
    0 0 2 0 0 
    0 0 2 0 0
    0 2 2 0 0 
    0 0 0 0 0

    position à 270°
    0 0 0 0 0
    0 2 0 0 0 
    0 2 2 2 0
    0 0 0 0 0 
    0 0 0 0 0
    

    """

    if erase == 1:
        val = 0
    else:
        val = b

    print(ori)
    
    # pixel de réference
    grid[y][x] = val

    if ori == 0:
        # on dessine la pièce b à la posstion 0°

        grid[y-1][x] = val
        grid[y+1][x] = val
        grid[y-1][x+1] = val

    # si la pièce est orienté horizontalement 
    elif ori == 90:
        # on dessine la pièce b à la posstion 90°

        grid[y][x-1] = val
        grid[y][x+1] = val
        grid[y+1][x+1] = val

    elif ori == 180:
        # on dessine la pièce b à la posstion 180°

        grid[y+1][x] = val
        grid[y-1][x] = val
        grid[y+1][x-1] = val
    
    elif ori == 270:
        # on dessine la pièce b à la posstion 270°

        grid[y][x+1] = val
        grid[y][x-1] = val
        grid[y-1][x-1] = val

        

def erasePiece(n, x, y, ori):

    if n == a:
        drawPieceA(x, y, ori, erase=1)
    elif n == b:
        drawPieceB(x, y, ori, erase=1)

def spawnPiece(n):
    """on dessine une piece n aux coordonnées par défaut (x = 4 et y = 3)"""
    drawPiece(n=n, x=4, y=3, ori = 0)
        
                
def rotatePiece(n, x, y, ori):
    """tourne la pièce active de 90°"""

    # on efface l'ancienne piece 
    erasePiece(n, x, y, ori)

    ori += 90
    if ori == 360:
        ori = 0

    # si la piece à tourner est la 'a' on modifit son picel de réference
    if n == a:
        if ori == 0:
            # ori était avant de 270° 
            x -= 1 
        elif ori == 90:
            # ori était avant de 0°
            x += 1
            y -= 1
        elif ori == 180:
            y += 1
        elif ori == 270:
            pass

    
    drawPiece(n, x, y, ori)

    

    return x, y, ori




if __name__ == "__main__":
    main()