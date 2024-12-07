from random import randrange

def genPolyominoLst(n):
    """génère une liste de tous les polyomino unique et unilatérale de taille n """

    lstPolyomino = []

    # selon la page wikipedia des polyomino il existe 7 polyomino de forme unilatérale de taille 4
    
    lenLstMaxPolyomino = [1, 1, 2, 7, 17, 57, 184, 500, 500]

    polyIn = False

    # tant qu'on a pas dans cette liste tout les polyomino de forme unilatératle de taille n 
    while len(lstPolyomino) < lenLstMaxPolyomino[n-1]:
        
        polyRotationLst = genPolyRoationLst(n)

        
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

        #print(len(lstPolyomino))

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


def genPolyominoBonnusLst(n):
    """génère une liste de tous les polyomino unique et unilatérale de taille inférieur ou égale a n """

    lstPolyomino = []

    # selon la page wikipedia des polyomino il existe 7 polyomino de forme unilatérale de taille 4
    
    lenLstMaxPolyomino = [1, 1, 2, 7, 17, 57, 184, 500, 500]



    # on enregistre la longueur de la liste pour la condition du while
    lenLstPolyPrevN = len(lstPolyomino)

    # pour n allant de 1 a n
    for nPoly in range(1, n+1):

        # pour inserer le premier poly
        polyIn = False

        # tant qu'on a pas dans cette liste tout les polyomino de forme unilatératle de taille n 
        while len(lstPolyomino) - lenLstPolyPrevN  < lenLstMaxPolyomino[nPoly-1]:
            
            polyRotationLst = genPolyRoationLst(nPoly)

            
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
        
        # on enregistre la longueur de la liste pour la condition du while
        lenLstPolyPrevN = len(lstPolyomino)

        #print(len(lstPolyomino))

    # on identifie chaque pièce par son index
    # pour chaque liste contenant toute les rotation d'un meme polyomino
    for k in range(len(lstPolyomino)):
        
        # on remplace le n par k

        polyominoRotaLst = lstPolyomino[k]

        for polyomino in polyominoRotaLst:
            for i in range(len(polyomino)):
                for j in range(len(polyomino[0])):
                    if polyomino[i][j] != 0:
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


def genColorRGBLst(nbPoly):
    """génére une liste de couleurs RGB contenant une couleur par pièces avec 0 a l'index 0 une case vide
    
    :param nbPoly: nombre de polyomino qu'il faut affecter une couleur
    :return lst: une liste contenant une couleur pour chaque polymino
    """

    lst = [0]

    for i in range(nbPoly):
        lst.append(genColorRGB())
    
    # couleur grise pour l'ombre de la pièce active
    lst.append("#b2b7bf")
    lst.append("#b2b7bf")
    return lst

def genColorRGB():
    """
    génère une couleur aléatoire formaté pour fltk

    :return hexColor:
    """


    # composante rouge verte et bleu aléatoire
    return '#' + toHex(randrange(0, 256)) + toHex(randrange(0, 256)) + toHex(randrange(0, 256))

def toHex(n):
    """
    convertie un nombre en base 10 en base 16 sur deux octets 
    """


    if n < 16:
        return "0" + hex(n)[2:]
    return hex(n)[2:]    