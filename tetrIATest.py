from tetriV3 import *


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

if __name__ == '__main__':

    cree_fenetre(largeurFenetre, hauteurFenetre)  
      
    tetriBot(False, False, False, 118, 21, 101, 34)
