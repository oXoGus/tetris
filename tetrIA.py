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





def tetriBot(varPtsDiffSelect, varPolyArbitraires, varModePourrisement, coefNbLigneSupp=14, coefCasePerdu=2, coefCaseManquantes=26, coefHauteurRect=19):
    """partie de tetris ou le programme joue"""
    
    # on efface le menu
    efface_tout()
    
    # si on ne charge pas une partie 

    # grille du haut contenant les id des carrées pour pouvoir les supprimer 

    # structure de donnée pour représenter la grille de jeu
    # la grille de jeu fait du 10 par 20 
    # mais comme les pièces apparaissent au dessus des 20 de hauteur 
    # on doit rajouter 4 cases sur les y
    grid = []

    for i in range(20 + 4):
        grid.append([])
        for j in range(10):
            grid[i].append(0)



    # génération des pièce ainsi que leurs couleurs
    
    # si la variante est activé 
    if varPolyArbitraires:
        # dans une autre liste, a l'index de la piece on insert une autre liste contenant toute les rotation de cette piece
        # n =  4 pour le mode de jeu classique 
        polyLst = genVarPolyArbitraire()

        # génération des couleurs pour chaque poly 
        squareColors = genColorRGBLst(len(polyLst))
    else:
        # dans une autre liste, a l'index de la piece on insert une autre liste contenant toute les rotation de cette piece
        # n =  4 pour le mode de jeu classique 
        polyLst = genPolyominoLst(n=4)

        # génération des couleurs pour chaque poly 
        squareColors = genColorRGBLst(len(polyLst))


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



    while True:


        # il faut mettre à jour pour pouvoir afficher le cadrillage et mettre les touches en attente 
        mise_a_jour()


        # si la dernière piece a été déposé 
        if pieceActivated == 0:

            score, nbLignesSuppTotale = suppLignes(grid, score, nbLignesSuppTotale, varPtsDiffSelect)


            # si c'est la première pièce de la partie 
            if nextPoly == None:
                
                # on génère les deux poly

                # on choisit aléatoirement la nouvelle pièce 
                poly = polyLst[randrange(0, len(polyLst))]

                # on choisit aléatoirement le prochaine pièce
                nextPoly = polyLst[randrange(0, len(polyLst))]
            else : 
                
                # la pièce suivante devient la pièce active et on génère la pièce suivante 
                poly = nextPoly

                # on choisit aléatoirement la nouvelle pièce 
                nextPoly = polyLst[randrange(0, len(polyLst))]

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
                

            # copie profonde de la grille 
            nGrid = list()
            nGrid = [l[:] for l in grid]

            # on trouve les meileur coord pour les 2 poly suivant
            objX, objOri = findBestPolyPlace(nGrid, poly, nextPoly, x, y, ori, coefNbLigneSupp, coefCasePerdu, coefCaseManquantes, coefHauteurRect)
        
            # on fait apparaitre un pièce aléatoirement 
            # avec la fonction spawnPiece() qui prend en argument le numéro de la piece que l'on génère aléatoirement 
            grid, poly, prevX, prevY, x, y, ori, change, maxY = spawnPiece(grid, poly, ori, change)

            getGoodPolyPlaceV2(nGrid, poly, x, y, ori)
            mooveLst = genMooveList(x, ori, objX, objOri)

            pieceActivated = 1

            desactivateCounter = 0

            #nPoly += 1

            # pour le mode pourrissement 
            if varModePourrisement:
                if time.perf_counter() - globalTimer > temps(nbLignesSuppTotale) * 15:
                    pourrissement(grid, polyLst)
                    globalTimer = time.perf_counter()
                    
                    # on affiche le poly supprimé 
                    drawGrid(grid, nextPoly, score, squareColors, nbLignesSuppTotale//10)


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

            #print(y)
            
            # on reset le timer pour déclancher le if dans la prochaine itération
            timer = 0


        # il faut redessiner la grille uniquemnt si elle a changé avec le flag 'change' pour des soucis de performance
        if change == 1:
            drawGrid(grid, nextPoly, score, squareColors, nbLignesSuppTotale//10)

            change = 0


    
        # on retire la touche a 'actionner'
        moove = mooveLst.pop(0)
        time.sleep(0.5)
        grid, poly, prevX, prevY, x, y, ori, change, maxY, pieceActivated = keyPressed(moove['key'], grid, poly, prevX, prevY, x, y, ori, change, maxY, pieceActivated, nextPoly, score, squareColors)
        

        #### on gère les touches ####
        
        # on enregiste l'évenement en attente le plus ancien
        ev = donne_ev()
        
        # si une touche  bien été pressé 
        if ev is not None:
            
            key = type_ev(ev)
            
            # si l'utilisateur appuis pour sur la croix ou alt + f4 pour fermer la fenêtre
            if key == 'Quitte':

                # test de sauvegarde automatique
                createSave(polyLst, score, poly, x, y, maxY, ori, grid, squareColors, nextPoly, varPtsDiffSelect, varPolyArbitraires, varModePourrisement, varMode2joueurs = False)
                ferme_fenetre()

                # on met le flag a 'Quitte' pour ne pas refaire le menu
                flag = 'Quitte'
                return flag
                
            elif key == 'Touche':
                key = touche(ev)
                
                if key == 'Escape':
                    flag = menuPause()

                    if flag == 'reprendre':

                        # on met le change a un pour réafficher la grille 
                        change = 1

                    # save&quit
                    else:
                        createSave(polyLst, score, poly, x, y, maxY, ori, grid, squareColors, nextPoly, varPtsDiffSelect, varPolyArbitraires, varModePourrisement, varMode2joueurs = False)
                        ferme_fenetre()
                        
                        return 'Quitte'
                        

            else:
                pass
                #print(key)

    # ecran de fin revoie un flag
    if endScreen(score) == 'retry':
        tetriBot(False, False, False)



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

    
def drawNextPoly(nextPoly, squareColors):
    """dsesine a droite de la grille le poly suivant"""
    
    # ligne du dessus a droite de la grille a la 4eme case et 
    # de logueur la longueur de next poly + une 1 case pour le padding 
    ligne(largeurFenetre/2 + sizeSquareGrid*numXSquare/2, hauteurFenetre - yMargin - numYSquare*sizeSquareGrid + 5.5*sizeSquareGrid, largeurFenetre/2 + sizeSquareGrid*numXSquare/2 + sizeSquareGrid*len(nextPoly[0][0]) + 1*sizeSquareGrid, hauteurFenetre - yMargin - numYSquare*sizeSquareGrid + 5.5*sizeSquareGrid, "black", 7)

    # on dessine le poly avec sont orientation de base a une case en dessous de la ligne
    # et 1/2 case horizontalement

    y = hauteurFenetre - yMargin - numYSquare*sizeSquareGrid + 5.5*sizeSquareGrid + 0.5*sizeSquareGrid
    x = largeurFenetre/2 + sizeSquareGrid*numXSquare/2 + 0.5*sizeSquareGrid

    for i in range(len(nextPoly[0])):
        for j in range(len(nextPoly[0][0])):
            
            # on affiche que les case remplit pour ne pas avoir de cases blanches
            if nextPoly[0][i][j] == 0:
                pass
            else:
                rectangle(x+j*sizeSquareGrid, y+i*sizeSquareGrid, x+j*sizeSquareGrid + sizeSquareGrid, y+i*sizeSquareGrid + sizeSquareGrid, "black", squareColors[nextPoly[0][i][j]], 3)




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


from random import randrange
import time


def suppLignes (grid, score, nbLignesSuppTotale, varPtsDiffSelect) : 
    """Supprimer les lignes lorsque toutes les valeurs sont diférentes de 0 et appelle la fonction qui descend les lignes au dessus de celle supprimée"""
    
    #fonction qui va supprimer les lignes remplies dans la grille 
    # et qui va renvoyer le nombre de lignes supprimées 
    nbLignesSupp = 0
    
    # boucle while qui va parcourir les sous listes, 
    # soit les lignes de la grille
    i = 0
    while i < len(grid) :
        
        # boucle for qui va parcourir les diverses éléments de la lignes 
        # et les passer à vide si il n'y a pas de zéro, c'est à dire qu'elle est remplie 
        if 0 not in grid[i] : 
            for j in range(len(grid[i])) : 
                grid[i][j] = 0

            nbLignesSupp += 1

            
            downLignes(grid, i)
            
        i+=1

    # on augmente le nb de lignes supprimé toltale par le nb de lignes suppp
    nbLignesSuppTotale += nbLignesSupp

    # choix de la fonction a utiliser si la variante est selectionner
    if varPtsDiffSelect == True:
        return pointsEnFonctionDifficulte(score, nbLignesSupp, nbLignesSuppTotale), nbLignesSuppTotale
    else:
        return points(score, nbLignesSupp), nbLignesSuppTotale

def downLignes(grid, i) :
    """ Parcourt les lignes supérieures à la ligne supprimée pour les descendre """
    
    # pour toutes les lignes au dessus de celle qui vient d'être supprimé
    while i>0: 

        # on abaisse la ligne du dessus
        for j in range(len(grid[i])) : 
            grid[i][j]=grid[i-1][j]
        i-=1 
    return grid  


def points (score, nbLignesSupp) : 
    """Lorsque le nombre de lignes supprimées est égal à une valeur, un certain nombre de points est ajouté"""
    
    #fonction qui va ajouter les points selon le nombre de lignes supprimées 
    if nbLignesSupp==1 : 
        score += 40
    
    elif nbLignesSupp ==2 : 
        score += 100 
    
    elif nbLignesSupp == 3 : 
        score += 300
    
    elif nbLignesSupp == 4 : 
        score += 500 
    
    return score 

def pointsEnFonctionDifficulte(score, nbLignesSupp, nbLignesSuppTotale) : 
    """fonction a utiliser quand la variante des points en fonction du niveau est sélectionner"""
    
    # fonction qui va ajouter les points selon le nombre de lignes supprimées 
    # nbLignesSuppTotale//10 représente la difficulté

    # on commence avec une difficulté de 1 pour ne pas avoir de score = 0
    difficulty = 1 + int(nbLignesSuppTotale//10/2)
    if nbLignesSupp==1 : 
        score += 40*difficulty
    
    elif nbLignesSupp ==2 : 
        score += 100*difficulty
    
    elif nbLignesSupp == 3 : 
        score += 300*difficulty
    
    elif nbLignesSupp == 4 : 
        score += 500 *difficulty
    
    return score 

def drawScore(score) : 
    """dessine a droite de la grille le score"""
    
    # le décalage de chaque coté pour que la ligne du dessous soit un peut plus grande que la taille du tetriTexte
    xOffset = sizeSquareGrid/4
    yOffset = sizeSquareGrid/8

    # ligne du dessous a droite de la grille a la 2eme case
    ligne(largeurFenetre/2 + sizeSquareGrid*numXSquare/2, hauteurFenetre - yMargin - sizeSquareGrid*numYSquare  + 2*sizeSquareGrid , largeurFenetre/2 + sizeSquareGrid*numXSquare/2 + tailleTetriTexte(str(score), 14)[0] + xOffset + yOffset, hauteurFenetre - yMargin - sizeSquareGrid*numYSquare + 2*sizeSquareGrid, "black", 7) 
    
    # possition du tetriTexte 
    xPose = largeurFenetre/2 + sizeSquareGrid*numXSquare/2 + xOffset
    yPose = hauteurFenetre - yMargin - sizeSquareGrid*numYSquare + sizeSquareGrid  - yOffset
    
    tetriTexte(xPose, yPose ,str(score), "black", 14)


def temps(nbLignesSuppTotale):
    """renvoie le temps d'attente avant que la pièce tombe toute seule"""
    
    # courbe de difficulté linéaire

    # on augmente la difficulté toute les 10 lignes supprimé
    nbLignesSuppTotale = nbLignesSuppTotale // 10

    # la difficulté de base est a une seconde
    # on abaisse la difficulté de 0.1 seconde toutes les 10 lignes supprimés

    # on empêche que on renvoie un temps négatif
    if 1 - 0.1*nbLignesSuppTotale > 0:
        return 1 - 0.1*nbLignesSuppTotale 
    else:

        # on renvoie le temps minimum
        return 0.1


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

                #print("col left")
                continue
            
            # meme chose pour la droite
            if colisionRight(grid, poly, x, y, ori) == True and x - 1 >= 0 and colisionLeft(grid, poly, x - 1, y, ori) == False:

                x -= 1
                #print("col right")
                continue

            # meme chose pour le bas
            if colisionBottom(grid, poly, x, y, ori) == True and y - 1 + len(poly[ori]) > len(grid):
                y -= 1

                #print("col bot")
                continue
            

            # si la piece ne peut pas etre posé avec cette orientation 
            # on refait les test de colisions avec l'ancienne orientation
            
            
            # on cherche l'ancienne ori
            if ori == 0:
                ori = 3
            else:
                ori -= 1


            #print("x =", prevX)
            #print("y =", y)
            


            # et on renvoie directement les anciennes coordonées avec l'ancienne ori
            return grid, poly, prevX, y, ori

            

            

            
        
        return grid, poly, x, y, ori



    else:

        # colision classique 
        if isColision(grid, poly, x, y, ori) == True:

            #print("colisions classique")
            return grid, poly, prevX, prevY, ori
        
        #print("pas de colision")
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
    return drawPiece(grid, poly, None, None, 4, 1, ori, change, None)
        
                
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

def drawPiece(grid, poly, prevX, prevY, x, y, ori, change, maxY, rotated = 0):
    """dessine sur la grille la pièce active et gestion des colision"""
    
    # si le poly sort de la griille de jeu

    # depasse a droite 
    
    while x + len(poly[ori][0]) > len(grid[0]): 
        change = 0

        #print("depasse grille")

        # on remet les ancienne bonne coordonnées
        x -= 1 
        y = y


    if  x < 0:
        x += 1
        y = prevY


    while y + len(poly[ori]) > len(grid):
        #print("depasse en bas")
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
        #print("colision")
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


def drawGrid(grid, nextPoly, score, squareColors, niveau):
    """
    dessine sur la fennêtre la représentation de la `grid`

    `grid` : matrice qui représente la partie elle même
    `nextPoly` : matice contenant la pochaine pièce à jouer pour la passer en param à la fonction `drawNextPoly()`
    `score` : variable contenant le score pour la passer en param à la fonction `drawScore()`
    """

    efface_tout()

    # affichage du poly suivant
    drawNextPoly(nextPoly, squareColors)

    # affichage du score
    drawScore(score)

    # affichage du niveau
    drawLevel(niveau)

    yGrid = 0
    xGrid = 0

    thickness = 8

    # ligne basse de la grille
    ligne(largeurFenetre/2 - sizeSquareGrid*numXSquare/2 - thickness//2, hauteurFenetre - yMargin, largeurFenetre/2 + sizeSquareGrid*numXSquare/2 + thickness//2, hauteurFenetre - yMargin, "black", thickness)

    #ligne de gauche
    ligne(largeurFenetre/2 - sizeSquareGrid*numXSquare/2, hauteurFenetre - yMargin, largeurFenetre/2 - sizeSquareGrid*numXSquare/2, hauteurFenetre - yMargin - sizeSquareGrid*numYSquare, "black", thickness)

    #ligne de droite
    ligne(largeurFenetre/2 + sizeSquareGrid*numXSquare/2, hauteurFenetre - yMargin, largeurFenetre/2 + sizeSquareGrid*numXSquare/2, hauteurFenetre - yMargin - sizeSquareGrid*numYSquare, "black", thickness)



    # on dessine les case vide pour que les épaisseurs des case des case pleines ne soit 'écrasé' par l'épaisseur de la case vide
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

                # on affiche bien que les case vide
                if n == 0:
                    rectangle(xGrid, yGrid, xGrid + sizeSquareGrid, yGrid + sizeSquareGrid, "light gray", "white")
    
    
    # on dessine que les cases pleines
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
                    rectangle(xGrid, yGrid, xGrid + sizeSquareGrid, yGrid + sizeSquareGrid, "black", squareColors[n], 3)
            
            else:
                if n == 0:
                    pass
                elif n == -1:
                    rectangle(xGrid, yGrid, xGrid + sizeSquareGrid, yGrid + sizeSquareGrid, "black", squareColors[n], 3)
                else:
                    rectangle(xGrid, yGrid, xGrid + sizeSquareGrid, yGrid + sizeSquareGrid, "black", squareColors[n], 3)


def drawLevel(niveau):

    # le décalage de chaque coté pour que la ligne du dessous soit un peut plus grande que la taille du tetriTexte
    xOffset = sizeSquareGrid/4
    yOffset = sizeSquareGrid/8

    # ligne du dessous a droite de la grille a la 2eme case
    ligne(largeurFenetre/2 + sizeSquareGrid*numXSquare/2, hauteurFenetre - yMargin - sizeSquareGrid*numYSquare + 4*sizeSquareGrid , largeurFenetre/2 + sizeSquareGrid*numXSquare/2 + tailleTetriTexte('lvl : ' + str(niveau), 14)[0] + xOffset + yOffset, hauteurFenetre - yMargin - sizeSquareGrid*numYSquare + 4*sizeSquareGrid, "black", 7) 
    
    # possition du tetriTexte 
    xPose = largeurFenetre/2 + sizeSquareGrid*numXSquare/2 + xOffset
    yPose = hauteurFenetre - yMargin - sizeSquareGrid*numYSquare + 3*sizeSquareGrid - yOffset
    
    tetriTexte(xPose, yPose , 'lvl : ' + str(niveau), "black", 14)



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

import random
import json
from fltk import *
from tetriGenPoly import *
import subprocess

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

largeurFenetre = largeurScreen//10

hauteurFenetre = largeurScreen//10

yMargin = int(0.10*largeurFenetre)

# constante
numYSquare = 20
numXSquare = 10
sizeSquareGrid = int(0.73*hauteurFenetre/numYSquare)



from tetriFont import *

def keyPressed(key, grid, poly, prevX, prevY, x, y, ori, change, maxY, pieceActivated, nextPoly, score, squareColors, nbLignesSuppTotale=0):
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

        # on dessine la pièce qui viens de se possé directement sinon elle restait en l'air si la condition de défaite 
        drawGrid(grid, nextPoly, score, squareColors, niveau=nbLignesSuppTotale//10)

        return grid, poly, prevX, prevY, x, y, ori, change, maxY, pieceActivated

    
            

    # 'down' pour baisser la pièce plus rapidement 
    else:
        y += 1

        grid, poly, prevX, prevY, x, y, ori, change, maxY = drawPiece(grid, poly, prevX, prevY, x, y, ori, change, maxY)
        return grid, poly, prevX, prevY, x, y, ori, change, maxY, pieceActivated


if __name__ == '__main__':
    
    
    from tetriGenPolyArbi import *
    from tetriSaves import *
    from tetri2players import *
    from tetriGenPoly import *
    
    
    from tetriV2 import drawGrid, printGrid, isPolyMaxY, drawPiece, isColision, colisionResolve, colisionLeft, colisionRight, colisionBottom, erasePiece, spawnPiece, rotatePiece, drawNextPoly, suppLignes, downLignes, points, pointsEnFonctionDifficulte, drawScore, temps, endScreen, rectangleOmbre, tetriTexteCentre, menuPause, createSave, saveMenu, drawSaveData, loadSave, drawSaveGrid, keyPressed, genPolyominoLst

    import subprocess

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

    cree_fenetre(largeurFenetre, hauteurFenetre)  
    print(largeurFenetre, largeur_fenetre())
      
    tetriBot(False, False, False, 118, 21, 101, 34)

    
    #selectNatCoef(nGen=50, nTest=25, nGames=10, coefNbLigneSuppInit=88, coefCasePerduInit=82, coefCaseManquantesInit=153, coefHauteurRectInit=3, genPolyF=genPolyominoLst, genColF=genColorRGBLst)