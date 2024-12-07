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



###### fonction pour la variante : polyominos arbitraires #######
def genVarPolyArbitraire():
    """génère les matrice de chaque pièce dans le fichier polyArbi.txt

    Dans le ficher polyArbi.txt 
    chaque pièce est précisée par des lignes où un bloc est représenté 
    par un +, et les pièces sont séparées par une ou plusieurs lignes vides
    """

    # on ouvre le fichier 
    with open("polyArbi.txt") as f:

        # on déplace le curseur pour ne pas suvegarder 
        # les explicaiton qui se trouvent au deux première ligne
        f.readline()
        f.readline()


        # on prend toutes les lignes restantes du fichier dans une liste
        polyArbiLignes = list(f)


    # on creer une liste contenant une liste des lignes formant un poliomino 
    polyArbiLst = []
    nouveauPoly = True 
    polyLst = []
    for ligne in polyArbiLignes:

        # si on saute une ligne marque la fin d'un poly
        if ligne == '\n':
            nouveauPoly = True
            
            # si la liste du poly est non vide
            # cas du \n au tout début du fichier 
            if polyLst != []:
                
                # on ajoute ce poly 
                polyArbiLst.append(polyLst)

        else:

            # nouveau poly
            if nouveauPoly == True:
                
                # on crée une liste qui contiendra les lignes du poly
                polyLst = []

                # on ajoute le ligne sans le \n avec le [:-1] qui retire le dernier caract de la chaine
                
                # si le dernier caract est un '\n'
                if ligne[len(ligne) - 1] == '\n':
                    polyLst.append(ligne[:-1])
                else:
                    polyLst.append(ligne)

                nouveauPoly = False

            # les lignes suivantes du poly            
            else:
                
                # on ajoute le ligne sans le \n avec le [:-1] qui retire le dernier caract de la chaine
                
                # si le dernier caract est un '\n'
                if ligne[len(ligne) - 1] == '\n':
                    polyLst.append(ligne[:-1])
                else:
                    polyLst.append(ligne)
    
    # si le fichier ne se termine pas par un saut de ligne on n'engregistre pas le dernier poly
    if polyLst != []:
        polyArbiLst.append(polyLst)

    # liste contenant tout les matrice de chaque poly arbitraire
    polyArbiMatLst = []

    # maintenant qu'on a un poly a un index on le tranforme en matrice
    for poly in polyArbiLst:
        
        # on prend la ligne la plus longue
        maxLen = 0
        for l in poly:
            if len(l) > maxLen:
                maxLen = len(l)

        # on prend aussi le nombre de ligne pour maxLen

        if len(poly) > maxLen:
            maxLen = len(poly)

        # si le polyomino peut sortir de la grille
        if maxLen >= 10:
            
            # on passe au polyomino suivant
            continue

        # matrice du poly
        polyMat = []

        # pour chaque lignes du poly
        for n, l in enumerate(poly):

            # ligne de la matrice 
            polyMat.append([])

            # on prend comme largeur de la matreice la largeur max du poly
            for i in range(maxLen):
                
                # si on est dehors de la liste ou que la caractère est un espace, 
                # on ajoute une case vide
                if i >= len(l) or l[i] == ' ':
                    polyMat[n].append(0)
                
                # case pleine représenter par un + dans le fichier texte
                elif l[i] == '+':
                    polyMat[n].append(1)
        
        # pour avoir une matrice carré de taille maxLen
        # ajout des lignes vides si besoin
        for i in range(maxLen - len(poly)):
            polyMat.append([0 for _ in range(maxLen)])

        # on ajoute la matrice du poly
        polyArbiMatLst.append(polyMat)


    # on génere toutes les rotations de chaque poly


    # liste qui va contenire les liste des 4 rotations pour chaque poly
    polyArbiLst = list()

    # pour chaque poly
    for poly in polyArbiMatLst:
        
        polyRoationLst = []

        # on tourne la piece 4 fois
        for _ in range(4):

            # on tourne la pièce
            poly = rotatePoly(poly)
            
            cleanPoly = polyCleanUp(poly)

            polyRoationLst.append(cleanPoly)

        

        # on ajoute toute les rotation du poly
        polyArbiLst.append(polyRoationLst)


    # on assigne à chaque poly son identifiant qui sera 
    # l'index de sa couleur dans la liste des couleurs

    for k in range(len(polyArbiLst)):
    
        # on remplace le n par k

        polyominoRotaLst = polyArbiLst[k]

        for polyomino in polyominoRotaLst:
            for i in range(len(polyomino)):
                for j in range(len(polyomino[0])):
                    if polyomino[i][j] != 0:
                        polyomino[i][j] = k + 1

    # on renvoie tout les poly arbitraire avec leurs rotations
    return polyArbiLst