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





def tetriBot(varPtsDiffSelect, varPolyArbitraires, varModePourrisement):
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

    for i in range(numYSquare + 4):
        grid.append([])
        for j in range(numXSquare):
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
            # on trouve les meileur coord pour le poly
            objX, objOri = findBestPolyPlace(nGrid, poly, x, y, ori)

            # on fait apparaitre un pièce aléatoirement 
            # avec la fonction spawnPiece() qui prend en argument le numéro de la piece que l'on génère aléatoirement 
            grid, poly, prevX, prevY, x, y, ori, change, maxY = spawnPiece(grid, poly, ori, change)

            mooveLst = genMooveList(x, ori, objX, objOri)

            pieceActivated = 1

            desactivateCounter = 0


            # pour le mode pourrissement 
            if varModePourrisement:
                if time.perf_counter() - globalTimer > temps(nbLignesSuppTotale) * 15:
                    pourrissement(grid, polyLst)
                    globalTimer = time.perf_counter()
                    
                    # on affiche le poly supprimé 
                    drawGrid(grid, nextPoly, score, squareColors)


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
            drawGrid(grid, nextPoly, score, squareColors)

            change = 0

        

        # on déplace le


    
        # on retire la touche a 'actionner'
        moove = mooveLst.pop(0)
        print(moove)
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
    return score



def trainingBot(varPtsDiffSelect, varPolyArbitraires, varModePourrisement, coefNbLigneSupp, coefCasePerdu, coefCaseManquantes, coefHauteurRect):
    """simule une partie simplifier pour voir combien le bot fait de points"""

    
    # si on ne charge pas une partie 

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
            # on trouve les meileur coord pour le poly
            objX, objOri = findBestPolyPlace(nGrid, poly, x, y, ori, coefNbLigneSupp, coefCasePerdu, coefCaseManquantes, coefHauteurRect)

            # on fait apparaitre un pièce aléatoirement 
            # avec la fonction spawnPiece() qui prend en argument le numéro de la piece que l'on génère aléatoirement 
            grid, poly, prevX, prevY, x, y, ori, change, maxY = spawnPiece(grid, poly, ori, change)

            mooveLst = genMooveList(x, ori, objX, objOri)

            pieceActivated = 1

            desactivateCounter = 0


            # pour le mode pourrissement 
            if varModePourrisement:
                if time.perf_counter() - globalTimer > temps(nbLignesSuppTotale) * 15:
                    pourrissement(grid, polyLst)
                    globalTimer = time.perf_counter()
                    
                    # on affiche le poly supprimé 
                    drawGrid(grid, nextPoly, score, squareColors)


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


def findBestPolyPlace(nGrid, poly, x, y, ori, coefNbLigneSupp, coefCasePerdu, coefCaseManquantes, coefHauteurRect):
    """renvoie le x et l'ori du poly qui rapporte le plus de points 
    ou si il ne peut pas recup le plus de points on prend ceux qui créer moins de trous
    on prend en param une copie de la grille pour pouvoir faire tout les test
    """

    # iste de toutes les position qui créer le moins de case inaccessible 
    # ou qui supprime une ou plusieurs lignes
    polyPosLst = getGoodPolyPlace(nGrid, poly, x, y, ori)

    # on attribue un score a chaque grille 
    for polyPos in polyPosLst:
        addScoreGrid(polyPos, coefNbLigneSupp, coefCasePerdu, coefCaseManquantes, coefHauteurRect)
    
    bestPosLst = sorted(polyPosLst, key=lambda polyPos: polyPos['score'], reverse=True)
    bestPos = bestPosLst[0]

    return bestPos['x'], bestPos['ori']

def addScoreGrid(polyPos, coefNbLigneSupp = 10, coefCasePerdu=1, coefCaseManquantes=1, coefHauteurRect=1):
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
        for x in range(numXSquare - len(poly[ori][0]) + 1):

            # on dessine la piece posé sur nGrid
            maxY = drawShadow(nGrid, poly, ori, x, y)

            HeightRect = 0
            for i in range(numYSquare - 1 + 4, -1, -1):
                if nGrid[i] == [0]*numXSquare:
                    break
                for j in range(numXSquare):
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
                        'nGrid': [str(l[:]) for l in nGrid if l.count(0) != numXSquare],
                        'nbLigneSupp': n,
                        'casePerdu': len(casePerdu),
                        'x' : x,
                        'ori': ori,
                        'caseManquantes': caseUtileLineFull(nGrid, casePerdu),
                        'HauteurRect': HeightRect
                    }
                )

                # nouveau min
                minNbCasePerdu = len(casePerdu)


            # on efface la shadow
            eraseShadow(nGrid, poly, ori, x, maxY)
            

    
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
    for i in range(numYSquare + 4 - HeightRect, numYSquare + 4):
        for j in range(numXSquare):
            
            # tout les case qui sont vide et qu'il y'a une case pleine au dessu
            if nGrid[i][j] == 0:
                
                # nb de case perdu test pck 
                # on ne sait pas si les case vide 
                # sont perdu avant d'avoir trouvé 
                # un block plein au dessus
                # on remonte la grile 
                for k in range(1, HeightRect - (numYSquare + 4 - i) + 2):
                    
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
    return numXSquare


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

    
def selectNatCoef(nGen, nTest, nGames, coefNbLigneSuppInit, coefCasePerduInit, coefCaseManquantesInit, coefHauteurRectInit):
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

        # pour chaque combinaison de coef
        for test in range(nTest):
            lstScore = []

            # on effectue des mutations 
            coefNbLigneSupp = coefNbLigneSuppParent + random.randrange(-3, 4)
            coefCasePerdu = coefCasePerduParent + random.randrange(-3, 4)
            coefCaseManquantes = coefCaseManquantesParent + random.randrange(-3, 4)
            coefHauteurRect = coefHauteurRectParent + random.randrange(-3, 4)

            # pour des même coef 
            # on simule n parties a cause de l'aléatoire des pièces
            # on prend la moyenne du score
            for _ in range(nGames):

                gameScore = trainingBot(False, False, False, coefNbLigneSupp, coefCasePerdu, coefCaseManquantes, coefHauteurRect)

                lstScore.append(gameScore)

            coefResult = {   
                'avgScore': sum(lstScore) / float(len(lstScore)),
                'coefNbLigneSupp':coefNbLigneSupp, 
                'coefCasePerdu': coefCasePerdu, 
                'coefCaseManquantes': coefCaseManquantes, 
                'coefHauteurRect': coefHauteurRect
            }

            L.append(coefResult)

        L = sorted(L, key=lambda test: test['avgScore'], reverse=True)

        with open ('gen'+str(gen)+'.json', 'w') as f:
            json.dump(L, f, indent=4)

        bestCoef = L[0]
        print(bestCoef)
        # transmission des meilleurs coef pour la gen suivant
        coefNbLigneSuppParent = bestCoef['coefNbLigneSupp']
        coefCasePerduParent = bestCoef['coefCasePerdu']
        coefCaseManquantesParent = bestCoef['coefCaseManquantes']
        coefHauteurRectParent = bestCoef['coefHauteurRect']




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



if __name__ == '__main__':
    from fltk import *
    from tetriFont import *
    import time
    from random import randrange
    from tetriGenPolyArbi import *
    from tetriSaves import *
    from tetri2players import *
    from tetriGenPoly import *
    import subprocess
    import json
    from tetriV2 import drawGrid, printGrid, isPolyMaxY, drawPiece, isColision, colisionResolve, colisionLeft, colisionRight, colisionBottom, erasePiece, spawnPiece, rotatePiece, drawNextPoly, suppLignes, downLignes, points, pointsEnFonctionDifficulte, drawScore, temps, endScreen, rectangleOmbre, tetriTexteCentre, menuPause, createSave, saveMenu, drawSaveData, loadSave, drawSaveGrid

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

    # moyenne du score 
    # création de la fenêtre carré 
    #cree_fenetre(largeurFenetre, largeurFenetre)

    #tetriBot(False, False, False)


    selectNatCoef(nGen=20, nTest=25, nGames=25, coefNbLigneSuppInit=16, coefCasePerduInit=1, coefCaseManquantesInit=23, coefHauteurRectInit=20)