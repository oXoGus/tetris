from fltk import *
import time
from random import randrange
from copy import copy


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

squareColors = ["white", "red", "blue", "yellow", "green", "orange", "pink"]

# structure de donnée pour représenter la grille de jeu
# la grille de jeu fait du 10 par 20 
# mais comme les pièces apparaissent au dessus des 20 de hauteur 
# on doit rajouter 4 cases sur les y
grid = []

for i in range(numYSquare + 4):
    grid.append([])
    for j in range(numXSquare):
        grid[i].append(0)

# on génére les polyomino pour la partie







def main():

    # les variables locales, on ne peut pas utiliser de variables globales en les définissant hors de la fonction son accessible qu'en lecture exeption faite au liste 

    pieceActivated = 0

    change = 1


    ### création de la fenêtre ###
    cree_fenetre(largeurFenetre, hauteurFenetre)


    ### création du cadrillage ###
    yGrid = 0
    xGrid = 0
    for i in range(numYSquare):

        yGrid = hauteurFenetre - yMargin - i* sizeSquareGrid
        for j in range(numXSquare):
                
            xGrid = largeurFenetre/2 - sizeSquareGrid*numXSquare/2 + j*sizeSquareGrid
            rectangle(xGrid, yGrid, xGrid + sizeSquareGrid, yGrid - sizeSquareGrid, "gray",)
                

    # grille dynamique en fonction de la taille de la fenêtre 

    # ligne basse de la grille
    ligne(largeurFenetre/2 - sizeSquareGrid*numXSquare/2, hauteurFenetre - yMargin, largeurFenetre/2 + sizeSquareGrid*numXSquare/2, hauteurFenetre - yMargin, "black", 4)

    #ligne de gauche
    ligne(largeurFenetre/2 - sizeSquareGrid*numXSquare/2, hauteurFenetre - yMargin, largeurFenetre/2 - sizeSquareGrid*numXSquare/2, hauteurFenetre - yMargin - sizeSquareGrid*numYSquare, "black", 4)

    #ligne de droite
    ligne(largeurFenetre/2 + sizeSquareGrid*numXSquare/2, hauteurFenetre - yMargin, largeurFenetre/2 + sizeSquareGrid*numXSquare/2, hauteurFenetre - yMargin - sizeSquareGrid*numYSquare, "black", 4)

    
    # au début du jeu on génére dans une liste toutes les polyomino de taille n 
    # dans une autre liste, a l'index de la piece on insert une autre liste contenant toute les rotation de cette piece


    # TODO : menu
    while True:

        # si la dernière piece a été déposé 
        if pieceActivated == 0:

            # on génère aléatoirement numéro de la nouvelle pièce 
            n=randrange(a, g+1)

            # on fait apparaitre un pièce aléatoirement 
            # avec la fonction spawnPiece() qui prend en argument le numéro de la piece que l'on génère aléatoirement 
            spawnPiece(grid, n=n) 

            # on initialise les coordonnées par défaut de la prièce 
            xPGrid = 3
            yPGrid = 4
            
            # orientation par défaut de la pièce en degré
            oriPiece = 0

            pieceActivated = 1
        else:
            pass
        
        # il faut redessiner la grille uniquemnt si elle a changé avec le flag 'change'
        if change == 1:
            drawGrid(grid)

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
                    xPGrid, yPGrid, oriPiece, change = keyPressed(key, xPGrid, yPGrid, oriPiece, change)
            else:
                print(key)
            



def drawGrid(grid):
    yGrid = 0
    xGrid = 0
    for i in range(len(grid)):

        yGrid = hauteurFenetre - yMargin - sizeSquareGrid*(numYSquare + 4) + i* sizeSquareGrid
        for j in range(len(grid[0])):

             # on enregistre la couleur de la case
            n = grid[i][j]

            xGrid = largeurFenetre/2 - sizeSquareGrid*numXSquare/2 + j*sizeSquareGrid

            # si on est dans les 4 première ligne
            if i < 4:
                # on affiche que les pièce, pas la grille
                if n == 0:
                    pass
                else:
                    rectangle(xGrid, yGrid, xGrid + sizeSquareGrid, yGrid + sizeSquareGrid, squareColors[n], squareColors[n])
            
            else:
                if n == 0:
                    rectangle(xGrid, yGrid, xGrid + sizeSquareGrid, yGrid + sizeSquareGrid, "gray", "white")
                else:
                    rectangle(xGrid, yGrid, xGrid + sizeSquareGrid, yGrid + sizeSquareGrid, squareColors[n], squareColors[n])

 





def genPolyominoLst(n):
    """génère une liste de tous les polyomino unique et unilatérale de taille n """

    lstPolyomino = []

    # selon la page wikipedia des polyomino il existe 7 polyomino de forme unilatérale de taille 4
    
    lenLstMaxPolyomino = [1, 1, 2, 7, 18, 60, 196, 704, 2500]

    # tant qu'on a pas dans cette liste tout les polyomino de forme unilatératle de taille n 
    while len(lstPolyomino) < lenLstMaxPolyomino[n-1]:
        
        polyomino = genPolyomino(n)

        # TODO : faire une comparaison plus poussé a l'aide des différentes rotations d'une même pièce 

        # si le polyomino généré n'est pas déja dans la liste on l'ajoute
        if polyomino in lstPolyomino:
            pass
        else:
            lstPolyomino.append(polyomino)

    # on identifi chaque pièce par son index
    for k in range(len(lstPolyomino)):
        
        # on remplace le n par i

        polyomino = lstPolyomino[k]
        for i in range(len(polyomino)):
            for j in range(len(polyomino)):
                if polyomino[i][j] == n:
                    polyomino[i][j] = k + 1

    return lstPolyomino
    
def genPolyomino(n):
    """génere aléatoirement un polyomino de taille n"""

    # on créer le matrice n par n 
    pGrid = [[0] * n for i in range(n)]

    # carré de base 
    pGrid[0][0] = n 

    # liste contenant les coordonnée des carré deja posé 
    coordsSquare = [[0, 0]]

    # variable pour compter le nombre de carré posé dans pGrid
    numSquare = 1

    # tant qu'il n'y a pas de n carré dans pGrid
    while numSquare < n:

        # on part de un des carrés déja posé 
        coords = coordsSquare[randrange(0, len(coordsSquare))]
        xSquare = coords[0]
        ySquare = coords[1]
        
        # on génère un nombre aléatoire entre 0 et 3 qui représentera la prochaine position du carré
        nextPose = randrange(0, 4)

        # a gauche
        if nextPose == 0:

            # si on peut poser le carré sur une case vide de la matrice
            if xSquare - 1 >= 0 and pGrid[xSquare - 1][ySquare] == 0:
                
                # on pose le carré
                xSquare -= 1
                ySquare = ySquare

                pGrid[xSquare][ySquare] = n

                # on enregistre ce carré dans la listes des carré posé
                coordsSquare.append([xSquare, ySquare])

                numSquare += 1

        # a droite
        elif nextPose == 1:
            
            # si on peut poser le carré sur une case vide de la matrice
            if xSquare + 1 < len(pGrid) and pGrid[xSquare + 1][ySquare] == 0:
                
                # on pose le carré
                xSquare += 1
                ySquare = ySquare

                pGrid[xSquare][ySquare] = n

                # on enregistre ce carré dans la listes des carré posé
                coordsSquare.append([xSquare, ySquare])

                numSquare += 1

        # en bas
        elif nextPose == 2:
            
            # si on peut poser le carré sur une case vide de la matrice
            if ySquare + 1 < len(pGrid) and pGrid[xSquare][ySquare + 1] == 0:
                
                # on pose le carré
                xSquare = xSquare
                ySquare += 1

                pGrid[xSquare][ySquare] = n

                # on enregistre ce carré dans la listes des carré posé
                coordsSquare.append([xSquare, ySquare])

                numSquare += 1

        # en haut
        elif nextPose == 3:
            
            # si on peut poser le carré sur une case vide de la matrice
            if ySquare - 1 >= 0 and pGrid[xSquare][ySquare - 1] == 0:
                
                # on pose le carré
                xSquare = xSquare
                ySquare -= 1

                pGrid[xSquare][ySquare] = n

                # on enregistre ce carré dans la listes des carré posé
                coordsSquare.append([xSquare, ySquare])

                numSquare += 1
    
    return pGrid
        

def genPolyRoationLst(n):
    """génère une liste contenant toutes les rotation un polyomino de taille n"""
    
    # on génère un polyomino de taille n aléatoire
    poly = genPolyomino(n)

    printPgrid(poly)

    polyRoationLst = []

    # on tourne la piece 4 fois
    for i in range(4):

        # on tourne la pièce
        poly = rotatePoly(poly)

        print()
        printPgrid(poly)

        cleanPoly = polyCleanUp(poly)

        print()
        printPgrid(cleanPoly)

        polyRoationLst.append(cleanPoly)

    return polyRoationLst



    

        
def rotatePoly(poly):
    """tourne d'un quart vers la droite"""

    nPoly = []

    for i in range(len(poly)):

        nPoly.append([])
        for j in range(len(poly)):
            nPoly[i].append(poly[len(poly) - 1 - j][i])

    return nPoly


def polyCleanUp(poly : list):
    """renvoie la plus petite matrice pouvant contenir le polyomino pour pouvoir comparer les polyomino
    
    """

    # il ne faut pas modifier la liste de base donc on en fait la copie
    nPoly = []

    for i in range(len(poly)):
        nPoly.append([])
        for j in range(len(poly)):
            nPoly[i].append(poly[i][j])
    
    # pour la hauteur 
    # si a que des 0 on la supprime 

    for i in range(len(nPoly) - 1, -1, -1):
        if nPoly[i] == [0]*len(nPoly[0]):
            nPoly.pop(i)

    # pour la largeur 
    # si dans une colone on a que des 0 on la supprime

    for j in range(len(nPoly[0]) - 1, -1, -1):
        colCount = 0

        for i in range(len(nPoly)):

            # on compte le nombre de 0 dans la colone 
            if nPoly[i][j] == 0:
                colCount += 1
        
        # si le nombre de 0 est égale a len(poly) on supprime la colone
        if colCount == len(nPoly):
            for i in range(len(nPoly)):
                nPoly[i].pop(j)
        
    return nPoly



def printGrid(grid):
    """affiche la grille de jeu pour débuggé"""
    for y in range(len(grid)):
        print(grid[y])
    return


def printPgrid(pGrid):
    """on affiche la grille de la pièce active pour débuggé"""
    for i in range(len(pGrid)):
        print(pGrid[i])



        


def drawPiece(grid, n, x, y, ori):
    """dessine sur la grille la pièce active, gestion des colision"""
    
    

        

def erasePiece(grid, n, x, y, ori):
    """efface la prièce active""" 

    

def spawnPiece(grid, n):
    """on dessine une piece n aux coordonnées par défaut (x = 4 et y = 3)"""
    drawPiece(grid, n=n, x=4, y=3, ori = 0)
        
                
def rotatePiece(grid, n, x, y, ori):
    """tourne la pièce active de 90° puis la dessine"""

    # on efface l'ancienne piece 
    erasePiece(grid, n, x, y, ori)

    # on tourne la pièce 
    ori += 90
    if ori == 360:
        ori = 0

    # on redessine la pièce avec sa nouvelle orientation 
    drawPiece(grid, n, x, y, ori)

    return x, y, ori


def keyPressed(key, xPGrid, yPGrid, oriPiece, change):
    """prends en argument la touche pressée et appelle differentes fonction selon la touche pressée"""
    
    #debug 
    print(key)

    # pour touner la pièce d'1/4 vers la droite
    if key == 'Up':
        x, y, ori = rotatePiece(grid, n, pGrid, x, y, ori)

        change = 1
        return x, y, ori, change, pGrid

    # pour déplacer la pièce de une case vers la gauche
    if key == 'Left':
        return x, y, ori, change, pGrid


    # pour déplacer la pièce de une case vers la gauche
    elif key == 'Right':

        return x, y, ori, change, pGrid

    
    # pour placer intantanément la pièce 
    elif key == 'space':
        return x, y, ori, change, pGrid


    # 'down' pour baisser la pièce plus rapidement 
    else:

        return x, y, ori, change, pGrid


if __name__ == "__main__":
    polyLst = genPolyRoationLst(n=4)
    for i in range(len(polyLst)):
        print()
        printPgrid(polyLst[i])

    #main()