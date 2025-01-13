# hypotèses 
# pour chaque nouvelle pièce
# on test toutes les places ou on peut poser le poly
# a chaque place 
# on regarde combien il pourait rapporter de points 
# si aucun ne raporte de points
# on regarde la place qui donne le "moins de trou"
# nombre de case vide dans le plus grand rectangle 
# le bas de la grid jusqu'au plus haut poly sur la grille

# pseudo path finding 
# une fois qu'on a trouver l'emplacement qui rapport le plus de points ou crére le moin de trou
# on décale le x du poly pour etre aligné au poly visé
# on le tourne pour avoir la bonne ori 
# et si la pos est correspond bien
# on le 'appui sur espace' pour le décrendre instant


def trainingBot(varPtsDiffSelect, varPolyArbitraires, varModePourrisement, coefNbLigneSupp, coefCasePerdu, coefCaseManquantes, coefHauteurRect, polyLst, squareColors, polyOrder):
    """simule une partie simplifier pour voir combien le bot fait de points"""

    
    # si on ne charge pas une partie 

    # grille du haut contenant les id des carrées pour pouvoir les supprimer 

    # structure de donnée pour représenter la grille de jeu
    # la grille de jeu fait du 10 par 20 
    # mais comme les pièces apparaissent au dessus des 20 de hauteur 
    # on doit rajouter 4 cases sur les y
    grid = []

    for i in range(24):
        grid.append([])
        for j in range(10):
            grid[i].append(0)



    # les variables locales, on ne peut pas utiliser de variables globales en les définissant hors de la fonction son accessible qu'en lecture exeption faite au liste 
    pieceActivated = 0

    # on initialise la variable qui va contenir le poly que le joueur va jouer, celui qui apparaitera a la droite de la grille
    nextPoly = None

    # Initialisation du score à 0
    score = 0


    # intialisation du nombre totale de ligne supprimer pour calculer le niveau de difficulté 
    nbLignesSuppTotale = 0

    # on initialise le flag pour détecter si il y a eu une modification sur la grille pour la redessiner qu'une fois
    change = 1

    # on intitialise le score pour svoir si le temps de dessendre la pièce est passé 
    timer = 0

    globalTimer = time.perf_counter()

    nPoly = 0

    while True:

        # si la dernière piece a été déposé 
        if pieceActivated == 0:

            score, nbLignesSuppTotale = suppLignes(grid, score, nbLignesSuppTotale, varPtsDiffSelect)


            # si c'est la première pièce de la partie 
            if nextPoly == None:
                
                # on génère les deux poly

                # on choisit aléatoirement la nouvelle pièce 
                poly = polyLst[polyOrder[nPoly]]

                # on choisit aléatoirement le prochaine pièce
                nextPoly = polyLst[polyOrder[nPoly+1]]
            else : 
                
                # la pièce suivante devient la pièce active et on génère la pièce suivante 
                poly = nextPoly

                if nPoly+1 >= len(polyOrder):
                    return 100000000 

                # on choisit aléatoirement la nouvelle pièce 
                nextPoly = polyLst[polyOrder[nPoly+1]]

            # on initialise l'oriantation de la pièce a 0
            ori = 0
            
            # condition de défaite
            # si on a le polyomino va se supperposer a une pièce de la grille 
            # avant qu'on l'affiche a l'écrant 

            x = 4
            y = 1
            while x + len(poly[ori][0]) > len(grid[0]): 
                x -= 1 
                y = y

            if isColision(grid, poly, x, y, ori) == True:
                break

            
            nGrid = list()
            nGrid = [l[:] for l in grid]

            # on trouve les meileur coord pour les 2 poly suivant
            objX, objOri = findBestPolyPlace(nGrid, poly, nextPoly, x, y, ori, coefNbLigneSupp, coefCasePerdu, coefCaseManquantes, coefHauteurRect)
        

            # on fait apparaitre un pièce aléatoirement 
            # avec la fonction spawnPiece() qui prend en argument le numéro de la piece que l'on génère aléatoirement 
            grid, poly, prevX, prevY, x, y, ori, change, maxY = spawnPiece(grid, poly, ori, change)

            mooveLst = genMooveList(x, ori, objX, objOri)

            pieceActivated = 1

            desactivateCounter = 0

            nPoly += 1


        # timer pour descendre la pièce de une case toute les une secondes
        if timer == 0:
            timer = time.perf_counter()
        
        # variable de difficulté avec la fonction temps()
        if time.perf_counter() - timer > temps(nbLignesSuppTotale):
            #print(nbLignesSuppTotale, temps(nbLignesSuppTotale))
            

            # gestion du délais pour desactiver la piece

            if isPolyMaxY(grid, poly, x, y, ori) == True:
                desactivateCounter += 1
            
            # on reinitialise la score dès qu'il y a de l'espace sous la pièce active
            else:
                desactivateCounter = 0

            if desactivateCounter > 3:

                # on desactive la pièce pour en faire spawn une autre
                pieceActivated = 0
                
            # print(desactivateCounter)

            y += 1
            
            grid, poly, prevX, prevY, x, y, ori, change, maxY = drawPiece(grid, poly, prevX, prevY, x, y, ori, change, maxY)
            
            # on reset le timer pour déclancher le if dans la prochaine itération
            timer = 0
    
        # on retire la touche a 'actionner'
        moove = mooveLst.pop(0)
        #print(moove)
        grid, poly, prevX, prevY, x, y, ori, change, maxY, pieceActivated = keyPressedBot(moove['key'], grid, poly, prevX, prevY, x, y, ori, change, maxY, pieceActivated, nextPoly, score, squareColors)
        
    # on renvoie les données 
    return score

def findBestPolyPlace(nGrid, poly, nextPoly, x, y, ori, coefNbLigneSupp, coefCasePerdu, coefCaseManquantes, coefHauteurRect):
    """renvoie le x et l'ori du poly qui rapporte le plus de points 
    ou si il ne peut pas recup le plus de points on prend ceux qui créer moins de trous
    on prend en param une copie de la grille pour pouvoir faire tout les test
    """

    # iste de toutes les position qui créer le moins de case inaccessible 
    # ou qui supprime une ou plusieurs lignes
    polyPosLst = getGoodPolyAndNextPolyPlace(nGrid, poly, nextPoly, x, y, ori)

    # on attribue un score a chaque grille 
    for polyPos in polyPosLst:
        addScoreGrid(polyPos, coefNbLigneSupp, coefCasePerdu, coefCaseManquantes, coefHauteurRect)
    
    bestPosLst = sorted(polyPosLst, key=lambda polyPos: polyPos['score'], reverse=True)
    bestPos = bestPosLst[0]

    return bestPos['x'], bestPos['ori']

def addScoreGrid(polyPos, coefNbLigneSupp = 13, coefCasePerdu=1, coefCaseManquantes=28, coefHauteurRect=20):
    """attribue un score a partir 
    du nombre de ligne suprimé
    nombre case perdu crées
    nombre de case avant de finir la ligne 
    """
    # plus un score est élévé plus le coup est bon
    # score max 40 
    score = 0

    # pour les lignes supp 

    # 1 ligne vaut 10 points
    score += polyPos['nbLigneSupp']*coefNbLigneSupp 

    # 1 case perdu retire 2 points
    score -= polyPos['casePerdu']*coefCasePerdu

    # 1 case en moins rapporte 1 point 
    score -= polyPos['caseManquantes']*coefCaseManquantes

    # pour ne pas faire de colonne 
    # on prend en compte le plus la hauteur 
    # du rectangle pouvant contenir 
    # toutes les pièces
    score -= polyPos['HauteurRect']*coefHauteurRect


    polyPos['score'] = score

def getGoodPolyAndNextPolyPlace(nGrid, poly, nextPoly, x, y, ori):
    """géneres tout les pos deux coup a l'avance"""
    

    # les bonnes pos pour le poly
    polyPosLst = getGoodPolyPlace(nGrid, poly, x, y, ori)


    # nextPoly
    poly2PosLst = list()

    # pour chaque bonne position 
    # on genere les bonnes positions du coup suivant 
    for polyPos in polyPosLst:
        
        polyNextPosLst = getGoodPolyPlace(polyPos['nGrid'], nextPoly, x, y, ori)

        for poly2pos in polyNextPosLst:

            # on ajoute le x et l'ori du poly 1
            poly2pos['x'] = polyPos['x']
            poly2pos['ori'] = polyPos['ori']


        # on a juste a changer la grille 
        poly2PosLst.extend(polyNextPosLst)

    return poly2PosLst

def getGoodPolyPlace(nGrid, poly, x, y, ori):
    """génere la liste de toutes les position qui créer le moins de case inaccessible 
    ou qui supprime une ou plusieurs lignes"""
    
    # on stock tout les grilles qui créer le moins de case inaccessible ou qui supprime une ou plusieurs lignes
    nGridLst = list()

    minNbCasePerdu = 100    
    
    # le nombre de cas possible = nb de x possible * ori 
    # 10*4 = 40 possiblité au max
    for ori in range(4):
        
        # pour ne pas dépasser a droite pck on ne fait pas les colision sur le déplacement horisontale 
        for x in range(len(nGrid[0]) - len(poly[ori][0]) + 1):

            # on dessine la piece posé sur nGrid
            maxY = drawShadow(nGrid, poly, ori, x, y)


            # on fait la somme de tout les i des case en partant du bas
            # V2 du Hauteur rect
            HeightRectV2 = 0
            
            # nb de pts par case 
            pts = 1

            for i in range(len(nGrid) - 1, -1, -1):
                if nGrid[i] == [0]*len(nGrid[0]):
                    break
                for j in range(len(nGrid[0])):
                    if nGrid[i][j] != 0:
                        HeightRectV2 += pts
                    
                # on incr le nb de pts 
                pts += 1


            # on fait la somme de tout les i des case en partant du bas
            # V2 du Hauteur rect
            HeightRect = 0
            for i in range(len(nGrid) - 1, -1, -1):
                if nGrid[i] == [0]*len(nGrid[0]):
                    break
                for j in range(len(nGrid[0])):
                    if nGrid[i][j] != 0:
                        HeightRect += 1
                        break

            # on test cette pos
            # en prio les lignes supp
            n = nbLignesSuppBot(nGrid)

            casePerdu = nbCasePerdu(nGrid, HeightRect)

            # si des lignes ont été supp ou que la pos creer le moins de case inaccessible
            if n or len(casePerdu) <= minNbCasePerdu:

                # on ajoute les info de la bonne position 
                nGridLst.append(
                    {
                        'nGrid': [l[:] for l in nGrid],
                        'nbLigneSupp': n,
                        'casePerdu': len(casePerdu),
                        'x' : x,
                        'ori': ori,
                        'caseManquantes': caseUtileLineFull(nGrid, casePerdu),
                        'HauteurRect': HeightRectV2
                    }
                )

                # nouveau min
                minNbCasePerdu = len(casePerdu)


            # on efface la shadow
            eraseShadow(nGrid, poly, ori, x, maxY)
            

    
    return nGridLst

def drawPos(nGrid, poly, x, y, ori):
    """version simplifier de drawPiece"""

    for i in range(len(poly[ori])):
        for j in range(len(poly[ori][0])):

            # pour ne pas mettre de 0 sur des cases deja remplis
            if poly[ori][i][j] != 0:
                nGrid[y + i][x + j] = poly[ori][i][j]

def reversePathFinding(nGrid, poly, x, y, ori, objX, objY, objOri):
    """pathfinding inversé"""

    path = list()
    xInit = x
    yInit = y

    # si le poly peux monter 
    # alors il est accessible
    nGrid, poly, prevX, prevY, x, y, ori, change, maxY = drawPiece(nGrid, poly, x, y, x, y-1, ori, 0, y)
    
    # si on a bien pu remonter 
    if y == yInit - 1:

        # on peut y accéder sans path finding
        path.append('Down')
        return path
    
    for _ in range(100):
        pass
               
def tryLeft(nGrid, poly, prevX, prevY, x, y, ori, change, maxY, path):
    # on essaye a droite 
    nGrid, poly, prevX, prevY, x, y, ori, change, maxY = drawPiece(nGrid, poly, prevX, prevY, x + 1, y, ori, change, maxY)
    if x == prevX + 1:

        # on ajoute le path si ça a marché 
        path.append('Left')

    return nGrid, poly, prevX, prevY, x, y, ori, change, maxY
        
def tryRight(nGrid, poly, prevX, prevY, x, y, ori, change, maxY, path):
    # a gauche
    nGrid, poly, prevX, prevY, x, y, ori, change, maxY = drawPiece(nGrid, poly, prevX, prevY, x - 1, y, ori, change, maxY)
    if x == prevX - 1:

        # on ajoute le path si ça a marché 
        path.append('Right')

    return nGrid, poly, prevX, prevY, x, y, ori, change, maxY

def tryUp(nGrid, poly, prevX, prevY, x, y, ori, change, maxY, path):
    # en haut
    nGrid, poly, prevX, prevY, x, y, ori, change, maxY = drawPiece(nGrid, poly, prevX, prevY, x, y - 1, ori, change, maxY)
    if y == prevY - 1:

        # on ajoute le path si ça a marché 
        path.append('Down')

    return nGrid, poly, prevX, prevY, x, y, ori, change, maxY

def tryRota(nGrid, poly, prevX, prevY, x, y, ori, change, maxY, path):
    # et enfin l'ori
    erasePiece(nGrid, poly, x, y, ori)

    if ori == 3:
        ori = 0
    else:
        ori += 1    

    nGrid, poly, prevX, prevY, x, y, ori, change, maxY = drawPiece(nGrid, poly, prevX, prevY, x, y, ori, change, maxY, 1)
    if y == prevY - 1:

        # on ajoute le path si ça a marché 
        path.append('Up')

    return nGrid, poly, prevX, prevY, x, y, ori, change, maxY

def getGoodPolyPlaceV2(nGrid, poly, x, y, ori):
    """Brutforce."""
    
    # on stock tout les grilles qui créer le moins de case inaccessible ou qui supprime une ou plusieurs lignes
    nGridLst = list()

    minNbCasePerdu = 100    
    
    xInit = x
    yInit = y
    oriInit = ori 
    
    # oe génére TOUTES les pos possible
    for ori in range(4):
        for y in range(len(nGrid) - len(poly[ori]) + 1):
            for x in range(len(nGrid[0]) - len(poly[ori][0]) + 1):

                # si la piece n'est pas en colision et que est a son maxY
                if not isColision(nGrid, poly, x, y, ori) and isPolyMaxY(nGrid, poly, x, y, ori):
                    
                    drawPos(nGrid, poly, x, y, ori)

                    # on fait la somme de tout les i des case en partant du bas
                    # V2 du Hauteur rect
                    HeightRectV2 = 0
                    
                    # nb de pts par case 
                    pts = 1

                    for i in range(len(nGrid) - 1, -1, -1):
                        if nGrid[i] == [0]*len(nGrid[0]):
                            break
                        for j in range(len(nGrid[0])):
                            if nGrid[i][j] != 0:
                                HeightRectV2 += pts
                            
                        # on incr le nb de pts 
                        pts += 1


                    # on fait la somme de tout les i des case en partant du bas
                    # V2 du Hauteur rect
                    HeightRect = 0
                    for i in range(len(nGrid) - 1, -1, -1):
                        if nGrid[i] == [0]*len(nGrid[0]):
                            break
                        for j in range(len(nGrid[0])):
                            if nGrid[i][j] != 0:
                                HeightRect += 1
                                break

                    
                    # on test cette pos
                    # en prio les lignes supp
                    n = nbLignesSuppBot(nGrid)

                    casePerdu = nbCasePerdu(nGrid, HeightRect)
                    
                    if n or len(casePerdu) <= minNbCasePerdu:
                        # on stock les infos 
                        nGridLst.append({
                            'nGrid' : [str(l[:]) for l in nGrid],
                            'x': x,
                            'y': y,
                            'ori': ori,
                            'nbLigneSupp': n,
                            'casePerdu': len(casePerdu),
                            'caseManquantes': caseUtileLineFull(nGrid, casePerdu),
                            'HauteurRect': HeightRectV2
                        })

                    # nouveau min
                    minNbCasePerdu = len(casePerdu)

                    eraseShadow(nGrid, poly, ori, x, y)

    with open('posV2.json', 'w') as f:
        json.dump(nGridLst, f, indent=4)
                
    return nGridLst
    
def drawShadow(nGrid, poly, ori, x, y):

    # calc la pos du shadow
    maxY = y
    while isPolyMaxY(nGrid, poly, x, maxY, ori) == False:
        maxY += 1

    # on dessine que la shadow pour gagner du temps

    # on dessine le poly avec ces coords
    for i in range(len(poly[ori])):
        for j in range(len(poly[ori][0])):

            # pour ne pas mettre de 0 sur des cases deja remplis
            if poly[ori][i][j] != 0:
                nGrid[maxY + i][x + j] = poly[ori][i][j]

    return maxY

def nbLignesSuppBot(nGrid):
    n = 0
    for i in range(len(nGrid)):

        if nGrid[i].count(0) == 0:
            n += 1

    return n

def nbCasePerdu(nGrid, HeightRect):
    """renvoit le nombre de case perdu dans le plus petit rectangle (pas sur les cotés :/) 
    pouvant contenir tout les case pleines"""


    # une case perdu est une case inaccessible sans path finding 

    casePerdu = set()
    for i in range(len(nGrid) - HeightRect, len(nGrid)):
        for j in range(len(nGrid[0])):
            
            # tout les case qui sont vide et qu'il y'a une case pleine au dessu
            if nGrid[i][j] == 0:
                
                # nb de case perdu test pck 
                # on ne sait pas si les case vide 
                # sont perdu avant d'avoir trouvé 
                # un block plein au dessus
                # on remonte la grile 
                for k in range(1, HeightRect - (len(nGrid) - i) + 2):
                    
                    if nGrid[i-k][j] != 0:
                        
                        # on enregistre les corrds de la case perdu
                        casePerdu.add((i, j))
                        # on s'arrête au premier
                        break
    
    return casePerdu

def eraseShadow(nGrid, poly, ori, x, maxY):

    # on supprime le poly avec ces coords
    for i in range(len(poly[ori])):
        for j in range(len(poly[ori][0])):

            # pour ne pas mettre de 0 sur des cases deja remplis
            if poly[ori][i][j] != 0:
                nGrid[maxY + i][x + j] = 0

def caseUtileLineFull(nGrid, casePerdu):
    """renvoie le nombre de case restant pour compléter 
    la ligne la plus basse qui peut encore etre complété
    """
    for i in range(len(nGrid) - 1, -1, -1):
        
        # si la ligne peut etre complété
        # on prend touts les i des case perdu
        # on garde ceux de la meme ligne que i 
        # en gros 
        # si le nombre de case perdu est sur la ligne i est 0
        # alors on peut supprimer la ligne 
        nbCasePerduLigne = len(list(filter(lambda x: x==i, map(lambda coords: coords[0], casePerdu))))
        nbCaseVideLigne = nGrid[i].count(0)
        if nbCasePerduLigne == 0:
            
            # le nombre de case restantes est jsute le nb de case vide 
            # moins le nb de case perdu sur la ligne 
            return nbCaseVideLigne
    
    # par précaution
    return len(nGrid[0])

def genMooveList(x, ori, objX, objOri):
    """génere la liste de touche a appuyer pour 
    déplacer le poly jusqu'au x et l'ori donné"""

    # liste contenant chaque touch par cycle
    # ainsi que les résulats (x, y, ori) attendus 
    mooveLst = []
    # on commence par la rotation 
    
    # calcule le nombre nb de touche Up pour avoir la bonne ori 
    for i in range(objOri):
        mooveLst.append({
            'key': 'Up',
            'objOri': objOri,
            'oriAttendu': ori + i + 1,
            'objX': objX,
            'xAttendu': x
        })

    # le déplacement horizontale
    # on doit se déplace a droite
    if objX > x:
        for i in range(objX - x):
            mooveLst.append({
                'key': 'Right',
                'objOri': objOri,
                'oriAttendu': ori,
                'objX': objX,
                'xAttendu': x + i + 1 
            })

    # a gauche
    elif objX < x:
        for i in range(x - objX):
            mooveLst.append({
                'key': 'Left',
                'objOri': objOri,
                'oriAttendu': ori,
                'objX': objX,
                'xAttendu': x - i - 1 
            })

    # on déscent la pièce 
    mooveLst.append({
        'key': 'space',
        'objOri': objOri,
        'oriAttendu': ori,
        'objX': objX,
        'xAttendu': x 
    })

    return mooveLst

def keyPressedBot(key, grid, poly, prevX, prevY, x, y, ori, change, maxY, pieceActivated, nextPoly, score, squareColors):
    """prends en argument la touche pressée et appelle differentes fonction selon la touche pressée"""
    
    #debug 
    #print(key)

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

def isPolyMaxY(grid, poly, x, y, ori):
    """revoie True si le poly ne peut pas aller plus bas"""


    # bloqué par le limite de la grille 
    if y + len(poly[ori]) >= len(grid):
        #print("bloqué par la limite de la grille")
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
                    if grid[y + i + 1][x + j] > 0 or grid[y + i + 1][x + j] == -2:
                        return True
                    
                # les case en dessous du poly
                elif i + 1 == len(poly[ori]):

                    # l'index -2 correspond au case rajouté par l'adversaire dans le mode 2 joueurs 
                    if grid[y + i + 1][x + j] > 0 or grid[y + i + 1][x + j] == -2:
                        return True
    return False

def selectNatCoef(nGen, nTest, nGames, coefNbLigneSuppInit, coefCasePerduInit, coefCaseManquantesInit, coefHauteurRectInit, genPolyF, genColF):
    """on essaye de reproduire la séléction naturel 
    
    on fait ça pour un nombre de génération : nGen
    on fait nTest ou 'individu' par génération
    et on se base sur la moyenne des nGames simulé pour savoir le meilleur  
    """

    # coef de départ
    coefNbLigneSuppParent, coefCasePerduParent, coefCaseManquantesParent, coefHauteurRectParent = coefNbLigneSuppInit, coefCasePerduInit, coefCaseManquantesInit, coefHauteurRectInit

    # pour chaque gen 
    for gen in range(nGen):

        # liste contenant toutes les info pour les coef
        L = list()
        

        # on supprime l'aléatoire 
        # toutes les parties ont jouront avec les memes pièces dans le meme ordre
        polyLst = genPolyF(n=4)

        # génération des couleurs pour chaque poly 
        squareColors = genColF(len(polyLst))

        polyOrder = [randrange(1, len(polyLst)) for _ in range(7000)]


        # on refait un cas ou il n'y a pas de mutation 
        # sur les meilleurs gènes
        # pour ne pas perdre 'regresser' 
        # si on a a chaque fois des 'mauvaise' mutations 

        coefNbLigneSupp = coefNbLigneSuppParent
        coefCasePerdu = coefCasePerduParent
        coefCaseManquantes = coefCaseManquantesParent
        coefHauteurRect = coefHauteurRectParent

        gameScore = trainingBot(False, False, False, coefNbLigneSupp, coefCasePerdu, coefCaseManquantes, coefHauteurRect, polyLst, squareColors, polyOrder)

        coefResult = {   
            'score': gameScore,
            'coefNbLigneSupp':coefNbLigneSupp, 
            'coefCasePerdu': coefCasePerdu, 
            'coefCaseManquantes': coefCaseManquantes, 
            'coefHauteurRect': coefHauteurRect
        }
        print(coefResult)
        L.append(coefResult)

        # pour chaque combinaison de coef
        for test in range(nTest - 1):

            minCoefDiff = -100//(2*(gen + 1))
            maxCoefDiff = 100//(2*(gen + 1))

            # on effectue des mutations 
            coefNbLigneSupp = coefNbLigneSuppParent + random.randrange(minCoefDiff, maxCoefDiff)
            coefCasePerdu = coefCasePerduParent + random.randrange(minCoefDiff, maxCoefDiff)
            coefCaseManquantes = coefCaseManquantesParent + random.randrange(minCoefDiff, maxCoefDiff)
            coefHauteurRect = coefHauteurRectParent + random.randrange(minCoefDiff, maxCoefDiff)


            gameScore = trainingBot(False, False, False, coefNbLigneSupp, coefCasePerdu, coefCaseManquantes, coefHauteurRect, polyLst, squareColors, polyOrder)

            coefResult = {   
                'score': gameScore,
                'coefNbLigneSupp':coefNbLigneSupp, 
                'coefCasePerdu': coefCasePerdu, 
                'coefCaseManquantes': coefCaseManquantes, 
                'coefHauteurRect': coefHauteurRect
            }
            print(coefResult)
            L.append(coefResult)

        L = sorted(L, key=lambda test: test['score'], reverse=True)

        with open ('gen'+str(gen+9)+'.json', 'w') as f:
            json.dump(L, f, indent=4)

        bestCoef = L[0]

        # transmission des meilleurs coef pour la gen suivant
        coefNbLigneSuppParent = bestCoef['coefNbLigneSupp']
        coefCasePerduParent = bestCoef['coefCasePerdu']
        coefCaseManquantesParent = bestCoef['coefCaseManquantes']
        coefHauteurRectParent = bestCoef['coefHauteurRect']


if __name__ == '__main__':

    from tetriV3 import *

    # on récumpère la resolution de l'écran en executat la commande `xrandr | grep \\* | cut -d' ' -f4`
    # avec la module subprocess
    resolution = subprocess.Popen("xrandr | grep \\* | cut -d' ' -f4", shell=True, stdout=subprocess.PIPE).communicate()[0]


    # cela renvoie : b'2560x1600\n'

    # le b au début signifit que cette chaine est encodé en UTF-8
    # pour le retirer un faut décoder la chaine de caractère  

    # la methode decode a pour argument par défaut encodage UTF-8
    resolution = resolution[:-1].decode()

    # on obtient bien 2560x1600
    print(resolution)

    largeurScreen = int(resolution.split('x')[0])

    hauteurScreen = int(resolution.split('x')[1])

    largeurFenetre = largeurScreen//2

    hauteurFenetre = largeurScreen//2

    yMargin = int(0.10*largeurFenetre)

    # constante
    numYSquare = 20
    numXSquare = 10
    sizeSquareGrid = int(0.73*hauteurFenetre/numYSquare)

    #selectNatCoef(nGen=50, nTest=25, nGames=10, coefNbLigneSuppInit=88, coefCasePerduInit=82, coefCaseManquantesInit=153, coefHauteurRectInit=3, genPolyF=genPolyominoLst, genColF=genColorRGBLst)