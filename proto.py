from fltk import *
import time
from random import randrange



def main():
    
    



    ### création de la fenêtre ###
    cree_fenetre(largeurFenetre, hauteurFenetre)
    
    # grille du haut contenant les id des carrées pour pouvoir les supprimer 

    # structure de donnée pour représenter la grille de jeu
    # la grille de jeu fait du 10 par 20 
    # mais comme les pièces apparaissent au dessus des 20 de hauteur 
    # on doit rajouter 4 cases sur les y
    grid = []

    for i in range(numYSquare + 4):
        grid.append([])
        for j in range(numXSquare):
            grid[i].append(0)

    
    

    # les variables locales, on ne peut pas utiliser de variables globales en les définissant hors de la fonction son accessible qu'en lecture exeption faite au liste 
    pieceActivated = 0

    # on initialise la variable qui va contenir le poly que le joueur va jouer, celui qui apparaitera a la droite de la grille
    nextPoly = None

    change = 1

    timer = 0

    maxY = len(grid)

    # TODO : menu
    while True:


        # il faut mettre à jour pour pouvoir afficher le cadrillage et mettre les touches en attente 
        mise_a_jour()


        # si la dernière piece a été déposé 
        if pieceActivated == 0:


            # si c'est la première pièce de la partie 
            if nextPoly == None:
                
                # on génère les deux poly

                # on choisit aléatoirement la nouvelle pièce 
                poly = polyLst[randrange(0, len(polyLst))]

                # on choisit aléatoirement le prochaine pièce
                nextPoly = polyLst[randrange(0, len(polyLst))]

            # sinon
            else : 
                
                # la pièce suivante devient la pièce active et on génère la pièce suivante 
                poly = nextPoly

                # on choisit aléatoirement la nouvelle pièce 
                nextPoly = polyLst[randrange(0, len(polyLst))]

            # on initialise l'oriantation de la pièce a 0
            ori = 0

            # condition de défaite
            # si le maxY de la dernière pièce qui vient d'être posé va se supperposer avec le nouveau poly généré
            if len(poly[ori]) - 1 >= maxY:
                break

            

            # on fait apparaitre un pièce aléatoirement 
            # avec la fonction spawnPiece() qui prend en argument le numéro de la piece que l'on génère aléatoirement 
            grid, poly, prevX, prevY, x, y, ori, change, maxY = spawnPiece(grid, poly, ori, change)

            printGrid(grid)

            pieceActivated = 1

            desactivateCounter = 0


        # timer pour descendre la pièce de une case toute les une secondes
        if timer == 0:
            timer = time.perf_counter()
        #print(time.perf_counter() - timer)
        # 1000 ms 
        if time.perf_counter() - timer > 1:

            

            # gestion du délais pour desactiver la piece

            if isPolyMaxY(grid, poly, x, y, ori) == True:
                desactivateCounter += 1
            
            # on reinitialise la compteur dès qu'il y a de l'espace sous la pièce active
            else:
                desactivateCounter = 0

            if desactivateCounter > 3:

                # on desactive la pièce pour en faire spawn une autre
                pieceActivated = 0
                
            # print(desactivateCounter)

            y += 1
            
            grid, poly, prevX, prevY, x, y, ori, change, maxY = drawPiece(grid, poly, prevX, prevY, x, y, ori, change, maxY)

            #print(y)
            
            # on reset le timer pour déclancher le if dans la prochaine itération
            timer = 0

            #printGrid(grid)


        

        # il faut redessiner la grille uniquemnt si elle a changé avec le flag 'change'
        if change == 1:
            drawGrid(grid, nextPoly)

            change = 0

        

        #### on gère les touches ####
        
        # on enregiste l'évenement en attente le plus ancien
        ev = donne_ev()
        
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
                    grid, poly, prevX, prevY, x, y, ori, change, maxY, pieceActivated = keyPressed(key, grid, poly, prevX, prevY, x, y, ori, change, maxY, pieceActivated)
            else:
                print(key)

    # TODO : délais pour afficher le texte de défaite
    time.sleep(1)


def genColorRGBLst(len):
    """génére une liste de couleurs RGB contenant une couleur par pièces avec 0 a l'index 0 une case vide"""

    lst = [0]

    for i in range(len):
        lst.append(genColorRGB())
    
    lst.append("#b2b7bf")
    return lst

def genColorRGB():
    # composante rouge verte et bleu aléatoire
    return '#' + toHex(randrange(0, 256)) + toHex(randrange(0, 256)) + toHex(randrange(0, 256))

def toHex(n):
    if n < 16:
        return "0" + hex(n)[2:]
    return hex(n)[2:]    

def drawGrid(grid, nextPoly):

    efface_tout()

    drawNextPoly(nextPoly)

    yGrid = 0
    xGrid = 0

    thickness = 8

    # ligne basse de la grille
    ligne(largeurFenetre/2 - sizeSquareGrid*numXSquare/2 - thickness//2, hauteurFenetre - yMargin, largeurFenetre/2 + sizeSquareGrid*numXSquare/2 + thickness//2, hauteurFenetre - yMargin, "black", thickness)

    #ligne de gauche
    ligne(largeurFenetre/2 - sizeSquareGrid*numXSquare/2, hauteurFenetre - yMargin, largeurFenetre/2 - sizeSquareGrid*numXSquare/2, hauteurFenetre - yMargin - sizeSquareGrid*numYSquare, "black", thickness)

    #ligne de droite
    ligne(largeurFenetre/2 + sizeSquareGrid*numXSquare/2, hauteurFenetre - yMargin, largeurFenetre/2 + sizeSquareGrid*numXSquare/2, hauteurFenetre - yMargin - sizeSquareGrid*numYSquare, "black", thickness)

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
                elif n == -1:
                    rectangle(xGrid, yGrid, xGrid + sizeSquareGrid, yGrid + sizeSquareGrid, "gray", squareColors[n])
                else:
                    rectangle(xGrid, yGrid, xGrid + sizeSquareGrid, yGrid + sizeSquareGrid, squareColors[n], squareColors[n])


def genPolyominoLst(n):
    """génère une liste de tous les polyomino unique et unilatérale de taille n """

    lstPolyomino = []

    # selon la page wikipedia des polyomino il existe 7 polyomino de forme unilatérale de taille 4
    
    lenLstMaxPolyomino = [1, 1, 2, 7, 17, 57, 184, 500, 500]

    polyIn = False

    # tant qu'on a pas dans cette liste tout les polyomino de forme unilatératle de taille n 
    while len(lstPolyomino) < lenLstMaxPolyomino[n-1]:
        
        polyRotationLst = genPolyRoationLst(n)

        print(len(lstPolyomino))
        # on met la liste des rotation du polyomino si ce polyomino n'y est pas deja
        k = 0
        while k < len(lstPolyomino):
            if polyRotationLst[0] in lstPolyomino[k]:
                # ce polyomino est deja dans la liste
                polyIn = True
                break
            polyIn = False
            k += 1

        if polyIn == False:
            lstPolyomino.append(polyRotationLst)

    # on identifie chaque pièce par son index
    # pour chaque liste contenant toute les rotation d'un meme polyomino
    for k in range(len(lstPolyomino)):
        
        # on remplace le n par i

        polyominoRotaLst = lstPolyomino[k]

        for polyomino in polyominoRotaLst:
            for i in range(len(polyomino)):
                for j in range(len(polyomino[0])):
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

    polyRoationLst = []

    # on tourne la piece 4 fois
    for i in range(4):

        # on tourne la pièce
        poly = rotatePoly(poly)

        cleanPoly = polyCleanUp(poly)

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


def isPolyMaxY(grid, poly, x, y, ori):
    """revoie True si le poly ne peut pas aller plus bas"""


    # bloqué par le limite de la grille 
    if y + len(poly[ori]) >= len(grid):
        print("bloqué par la limite de la grille")
        return True
    
    # si la ligne la plus basse du poly peut aller une case plus bas

    
    # pour chaque case pleinne du poly
    # si la case du dessou est un 0 sur le poly 
    # si la case en dessou est pleinne alors True 
    for i in range(len(poly[ori])):
        for j in range(len(poly[ori][0])):
            if poly[ori][i][j] != 0:
                # pour ne pas détécter la piece elle meme
                if i + 1 < len(poly[ori]) and poly[ori][i + 1][j] == 0:
                    if grid[y + i + 1][x + j] != 0:
                        #print("poly posé")
                        return True
                    
                # les case en dessous du poly
                elif i + 1 == len(poly[ori]):
                    if grid[y + i + 1][x + j] != 0:
                        #print("poly posé")
                        return True
    return False



        


def drawPiece(grid, poly, prevX, prevY, x, y, ori, change, maxY, rotated = 0):
    """dessine sur la grille la pièce active et gestion des colision"""
    
    # si le poly sort de la griille de jeu

    # depasse a droite 
    
    while x + len(poly[ori][0]) > len(grid[0]): 
        change = 0

        print("depasse grille")

        # on remet les ancienne bonne coordonnées
        x -= 1 
        y = y


    if  x < 0:
        x += 1
        y = prevY


    while y + len(poly[ori]) > len(grid):
        print("depasse en bas")
        y -= 1


    # si il existe une piece précédente pour que la pièce n'ait pas de colisions avec elle meme 
    # et que la pièce ne vien pas d'etre tourné car la piece précédanta déja été effacé
    if prevX != None and prevY != None and maxY != None and rotated == 0:
        erasePiece(grid, poly, prevX, prevY, ori)

        #print("max Y =", maxY)
        # on efface aussi l'ombre
        erasePiece(grid, poly, prevX, maxY, ori)

        #print("piece supp")

    # gestion des colisions sur la partie basse entre les pièces

    # gesion des colision entre les pièces
    if y != 0 and isColision(grid, poly, x, y, ori) == True:
        print("colision")
        grid, poly, x, y, ori = colisionResolve(grid, poly, prevX, prevY, x, y, ori, rotated)

    
    # on dessine l'ombre de la pièce active, la piece a sa position la plus basse
    

    # on prend les coordonnées du poly
    # on augmente y tant que c'set possible
    maxY = y
    while isPolyMaxY(grid, poly, x, maxY, ori) == False:
        maxY += 1

    
    # on dessine le poly avec ces coords
    for i in range(len(poly[ori])):
        for j in range(len(poly[ori][0])):

            # pour ne pas mettre de 0 sur des cases deja remplis
            if poly[ori][i][j] != 0:

                # -1 est l'index de la couleur gris 
                grid[maxY + i][x + j] = -1


    # si on peut bien poser la pièce 
    # on efface l'ancienne piece
    # et on dessine la nouvelle
    
    for i in range(len(poly[ori])):
        for j in range(len(poly[ori][0])):

            # pour ne pas mettre de 0 sur des cases deja remplis
            if poly[ori][i][j] != 0:
                grid[y + i][x + j] = poly[ori][i][j]

    change = 1

    # on update le coordonnés de la pièce précédante
    prevX = x
    prevY = y

    return grid, poly, prevX, prevY, x, y, ori, change, maxY





def isColision(grid, poly, x, y, ori):
    """renvoie True si la piece actice se supperpose a une case deja remplis"""

    # pour chaque case du poly
    for i in range(len(poly[ori])):
        for j in range(len(poly[ori][0])):

            # pour chaque case non vide
            if poly[ori][i][j] != 0:

                # si la case sur la grille de jeu n'est pas vide 
                if grid[y + i][x + j] != 0:
                    return True  
    return False



def colisionResolve(grid, poly, prevX, prevY, x, y, ori, rotated):
    """change x et y pour que la pièce ne se supperpose plus a une autre pièce"""
    

    # si la pièce viens d'etre tounée
    if rotated == 1: 

        while isColision(grid, poly, x, y, ori) == True:

            # si des case a gauche se supperpose et si on peu bien déplacer la pièce vers la droite
            if colisionLeft(grid, poly, x, y, ori) == True and x + 1 + len(poly[ori][0]) <= len(grid[0]) and colisionRight(grid, poly, x + 1, y, ori) == False: 
                x += 1 
                # on refait le test du while

                print("col left")
                continue
            
            # meme chose pour la droite
            if colisionRight(grid, poly, x, y, ori) == True and x - 1 >= 0 and colisionLeft(grid, poly, x - 1, y, ori) == False:

                x -= 1
                print("col right")
                continue

            # meme chose pour le bas
            if colisionBottom(grid, poly, x, y, ori) == True and y - 1 + len(poly[ori]) > len(grid):
                y -= 1

                print("col bot")
                continue
            

            # si la piece ne peut pas etre posé avec cette orientation 
            # on refait les test de colisions avec l'ancienne orientation
            
            
            # on cherche l'ancienne ori
            if ori == 0:
                ori = 3
            else:
                ori -= 1


            print("x =", prevX)
            print("y =", y)
            


            # et on renvoie directement les anciennes coordonées avec l'ancienne ori
            return grid, poly, prevX, y, ori

            

            

            
        
        return grid, poly, x, y, ori



    else:

        # colision classique 
        if isColision(grid, poly, x, y, ori) == True:

            print("colisions classique")
            return grid, poly, prevX, prevY, ori
        
        print("pas de colision")
        return grid, poly, x, y, ori
            
def colisionLeft(grid, poly, x, y, ori):
    """gère les colision sur la gauche de la piece"""
    # pour chaque case a gauche de la pièce 
    for i in range(len(poly[ori])):
           
        # si case est remplit
        if poly[ori][i][0] != 0:
            
            # si la case est deja pris sur la grille
            if grid[y + i][x] != 0:
                return True
    return False
    
def colisionRight(grid, poly, x, y, ori):
    """gère les colision sur la droite de la piece"""
    # pour chaque case a gauche de la pièce 
    for i in range(len(poly[ori])):
           
        # si case est remplit
        if poly[ori][i][len(poly[ori][0]) - 1] != 0:
            
            # si la case est deja pris sur la grille
            if grid[y + i][x + len(poly[ori][0]) - 1] != 0:
                return True
    return False
                

def colisionBottom(grid, poly, x, y, ori):
    for j in range(len(poly[ori][0])):
           
        # si la case est remplit
        if poly[ori][len(poly[ori]) - 1][j] != 0:
            
            # si la case est deja pris sur la grille
            if grid[y + len(poly[ori]) - 1][x + j] != 0:
                return True
    return False
    

def erasePiece(grid, poly, x, y, ori):
    """efface la prièce active""" 

    for i in range(len(poly[ori])):
        for j in range(len(poly[ori][0])):
            if poly[ori][i][j] != 0:
                grid[y + i][x + j] = 0


    

def spawnPiece(grid, poly, ori, change):
    """on dessine une piece n aux coordonnées par défaut (x = 4 et y = 0)"""
    return drawPiece(grid, poly, None, None, 4, 0, ori, change, None)
        
                
def rotatePiece(grid, poly, prevX, prevY, x, y, ori, change, maxY):
    """tourne la pièce active de 90° puis la dessine"""

    # on efface l'ancienne piece et son ombre 
    erasePiece(grid, poly, x, y, ori)
    erasePiece(grid, poly, x, maxY, ori)

 
    if ori == 3:
        ori = 0
    else:
        ori += 1

    # on redessine la pièce avec sa nouvelle orientation 
    return drawPiece(grid, poly, prevX, prevY, x, y, ori, change, maxY, 1)



def keyPressed(key, grid, poly, prevX, prevY, x, y, ori, change, maxY, pieceActivated):
    """prends en argument la touche pressée et appelle differentes fonction selon la touche pressée"""
    
    #debug 
    print(key)

    # pour touner la pièce d'1/4 vers la droite
    if key == 'Up':
        grid, poly, prevX, prevY, x, y, ori, change, maxY = rotatePiece(grid, poly, prevX, prevY, x, y, ori, change, maxY)
        return grid, poly, prevX, prevY, x, y, ori, change, maxY, pieceActivated

    # pour déplacer la pièce de une case vers la gauche
    if key == 'Left':
        x -= 1

        grid, poly, prevX, prevY, x, y, ori, change, maxY = drawPiece(grid, poly, prevX, prevY, x, y, ori, change, maxY)
        return grid, poly, prevX, prevY, x, y, ori, change, maxY, pieceActivated


    # pour déplacer la pièce de une case vers la gauche
    elif key == 'Right':
        x += 1

        grid, poly, prevX, prevY, x, y, ori, change, maxY = drawPiece(grid, poly, prevX, prevY, x, y, ori, change, maxY)
        return grid, poly, prevX, prevY, x, y, ori, change, maxY, pieceActivated

    
    # pour placer intantanément la pièce 
    elif key == 'space':
        
        
        grid, poly, prevX, prevY, x, y, ori, change, maxY = drawPiece(grid, poly, prevX, prevY, x, maxY, ori, change, maxY)

        # on pose la pièce définitivement
        pieceActivated = 0

        return grid, poly, prevX, prevY, x, y, ori, change, maxY, pieceActivated


    # 'down' pour baisser la pièce plus rapidement 
    else:
        y += 1

        grid, poly, prevX, prevY, x, y, ori, change, maxY = drawPiece(grid, poly, prevX, prevY, x, y, ori, change, maxY)
        return grid, poly, prevX, prevY, x, y, ori, change, maxY, pieceActivated


def drawNextPoly(nextPoly):
    """dsesine a droite de la grille le poly suivant"""
    
    # ligne du dessus a droite de la grille a la 4eme case et 
    # de logueur la longueur de next poly + une 1 case pour le padding 
    ligne(largeurFenetre/2 + sizeSquareGrid*numXSquare/2, hauteurFenetre - yMargin - numYSquare*sizeSquareGrid + 4*sizeSquareGrid, largeurFenetre/2 + sizeSquareGrid*numXSquare/2 + sizeSquareGrid*len(nextPoly[0][0]) + 1*sizeSquareGrid, hauteurFenetre - yMargin - numYSquare*sizeSquareGrid + 4*sizeSquareGrid, "black", 4)

    # on dessine le poly avec sont orientation de base a une case en dessous de la ligne
    # et 1/2 case horizontalement

    y = hauteurFenetre - yMargin - numYSquare*sizeSquareGrid + 4*sizeSquareGrid + 0.5*sizeSquareGrid
    x = largeurFenetre/2 + sizeSquareGrid*numXSquare/2 + 0.5*sizeSquareGrid

    for i in range(len(nextPoly[0])):
        for j in range(len(nextPoly[0][0])):
            
            # on affiche que les case remplit pour ne pas avoir de cases blanches
            if nextPoly[0][i][j] == 0:
                pass
            else:
                rectangle(x+j*sizeSquareGrid, y+i*sizeSquareGrid, x+j*sizeSquareGrid + sizeSquareGrid, y+i*sizeSquareGrid + sizeSquareGrid, squareColors[nextPoly[0][i][j]], squareColors[nextPoly[0][i][j]])



if __name__ == "__main__":
    #### constantes et variables globales ####

    largeurFenetre = 1200
    hauteurFenetre = largeurFenetre
    yMargin = int(0.15*hauteurFenetre)

    # constante
    numYSquare = 20
    numXSquare = 10
    sizeSquareGrid = int(0.65*hauteurFenetre/numYSquare)

    # au début du jeu on génére dans une liste toutes les polyomino de taille n 
    # dans une autre liste, a l'index de la piece on insert une autre liste contenant toute les rotation de cette piece
    # n =  4 pour le mode de jeu classique 
    polyLst = genPolyominoLst(n=4)

    squareColors = genColorRGBLst(len(polyLst))


    main()