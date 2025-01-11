from fltk import *
from tetriV2 import numYSquare, numXSquare, largeurScreen, hauteurScreen, polyLst, genColorRGBLst, isColision, isPolyMaxY, spawnPiece, drawPiece, temps, points, rotatePiece, downLignes, pointsEnFonctionDifficulte, rectangleOmbre, drawCurseur, tetriTexteCentre
from tetriGenPolyArbi import *
from tetriFont import *
from tetriGenPoly import *
from tetriGenPolyArbi import *
import time
from tetriPourrissement import *

yMargin = int(0.075*largeurScreen)

sizeSquareGrid = int(0.73*hauteurScreen/numYSquare)

largeurFenetre = largeurScreen
hauteurFenetre = hauteurScreen

def gameModeDeuxJoueurs(varPtsDiffSelect, varPolyArbitraires, varModePourrissement, save = None):
    """une partie de tertis
    
    prend en argument les variantes activées
    renvoie un flag pour qui sera traité par le menu
    """
    
    
    ## on ferme la fennetre du menu 
    ferme_fenetre()

    # on répuvre une fenêtre plus grande pour accueillir les deux grilles
    cree_fenetre(largeurScreen, hauteurScreen)
    
    # grille du haut contenant les id des carrées pour pouvoir les supprimer 

    # structure de donnée pour représenter la grille de jeu
    # la grille de jeu fait du 10 par 20 
    # mais comme les pièces apparaissent au dessus des 20 de hauteur 
    # on doit rajouter 4 cases sur les y
    grid1 = []

    for i in range(numYSquare + 4):
        grid1.append([])
        for j in range(numXSquare):
            grid1[i].append(0)

    grid2 = []

    for i in range(numYSquare + 4):
        grid2.append([])
        for j in range(numXSquare):
            grid2[i].append(0)



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

    flag = None


    # les variables locales, on ne peut pas utiliser de variables globales en les définissant hors de la fonction son accessible qu'en lecture exeption faite au liste 
    pieceActivated = 0

    # on initialise la variable qui va contenir le poly que le joueur va jouer, celui qui apparaitera a la droite de la grille
    nextPoly1 = None
    nextPoly2 = None

    # Initialisation du score du joueur 1 à 0
    score1 = 0
    score2 = 0
    

    # intialisation du nombre totale de ligne supprimer pour calculer le niveau de difficulté 
    nbLignesSuppTotale = 0

    # on initialise le flag pour détecter si il y a eu une modification sur la grille pour la redessiner qu'une fois
    change = 1

    # on intitialise le score pour svoir si le temps de dessendre la pièce est passé 
    timer = 0

    # on initialise la variable pour la condition de défaite
    maxY = len(grid1)

    # on initialise la variable pour détecter si le score a changé 
    scoreChange=0
    
    #Variable permettant de vérifier à quel joueur est ce le tour, si c'est impair c'est le joueur 1 sinon c'est le joueur 2 
    joueurOn = "joueur1"
    joueurOff="joueur2"


    # on dessine une fois les bordures des grilles


    # joueur 1 a guauche
    thickness = 8

    # ligne basse de la grille
    ligne(largeurFenetre*1/4 - sizeSquareGrid*numXSquare/2 - thickness//2, hauteurFenetre - yMargin, largeurFenetre*1/4 + sizeSquareGrid*numXSquare/2 + thickness//2, hauteurFenetre - yMargin, "black", thickness)

    #ligne de gauche
    ligne(largeurFenetre*1/4 - sizeSquareGrid*numXSquare/2, hauteurFenetre - yMargin, largeurFenetre*1/4 - sizeSquareGrid*numXSquare/2, hauteurFenetre - yMargin - sizeSquareGrid*numYSquare, "black", thickness)

    #ligne de droite
    ligne(largeurFenetre*1/4 + sizeSquareGrid*numXSquare/2, hauteurFenetre - yMargin, largeurFenetre*1/4 + sizeSquareGrid*numXSquare/2, hauteurFenetre - yMargin - sizeSquareGrid*numYSquare, "black", thickness)

    # joueur 2 a droite

    # ligne basse de la grille
    ligne(largeurFenetre*3/4 - sizeSquareGrid*numXSquare/2 - thickness//2, hauteurFenetre - yMargin, largeurFenetre*3/4 + sizeSquareGrid*numXSquare/2 + thickness//2, hauteurFenetre - yMargin, "black", thickness)

    #ligne de gauche
    ligne(largeurFenetre*3/4 - sizeSquareGrid*numXSquare/2, hauteurFenetre - yMargin, largeurFenetre*3/4 - sizeSquareGrid*numXSquare/2, hauteurFenetre - yMargin - sizeSquareGrid*numYSquare, "black", thickness)

    #ligne de droite
    ligne(largeurFenetre*3/4 + sizeSquareGrid*numXSquare/2, hauteurFenetre - yMargin, largeurFenetre*3/4 + sizeSquareGrid*numXSquare/2, hauteurFenetre - yMargin - sizeSquareGrid*numYSquare, "black", thickness)


    # affchage du score
    drawScoreJoueur1(score1)
    drawScoreJoueur2(score2)

    # dessine la grille du joueur 2
    yGrid = 0
    xGrid = 0

    # on dessine les case vide pour que les épaisseurs des case des case pleines ne soit 'écrasé' par l'épaisseur de la case vide
    for i in range(len(grid2)):

        yGrid = hauteurFenetre - yMargin - sizeSquareGrid*(numYSquare + 4) + i* sizeSquareGrid
        for j in range(len(grid2[0])):

            # on enregistre la couleur de la case
            n = grid2[i][j]

            xGrid = largeurFenetre*3/4 - sizeSquareGrid*numXSquare/2 + j*sizeSquareGrid

            # si on est dans les 4 première ligne
            if i < 4:
                # on affiche que les pièce, pas la grille
                if n == 0:
                    rectangle(xGrid, yGrid, xGrid + sizeSquareGrid, yGrid + sizeSquareGrid, "#D9D9D9", "#D9D9D9")

            
            else:

                # on affiche bien que les case vide
                if n == 0:
                    rectangle(xGrid, yGrid, xGrid + sizeSquareGrid, yGrid + sizeSquareGrid, "light gray", "white")
    
    # variable qui va contenir quel joueur a perdu
    joueurLose = None

    # pour le mode pourrissemnt
    globalTimer1 = 0
    globalTimer2 = 0

    while joueurOn != None:
        
        #A chaque début, on cherche à savoir si c'est au tout du joueur 1 ou 2, 
        while joueurOn == "joueur1" : 
            
            # il faut mettre à jour pour pouvoir afficher le cadrillage et mettre les touches en attente 
            mise_a_jour()


            # si la dernière piece a été déposé 
            if pieceActivated == 0:


                # si c'est la première pièce de la partie 
                if nextPoly1 == None:
                    
                    # on génère les deux poly

                    # on choisit aléatoirement la nouvelle pièce 
                    poly1 = polyLst[randrange(0, len(polyLst))]

                    # on choisit aléatoirement le prochaine pièce
                    nextPoly1 = polyLst[randrange(0, len(polyLst))]
                else : 
                    
                    # la pièce suivante devient la pièce active et on génère la pièce suivante 
                    poly1 = nextPoly1

                    # on choisit aléatoirement la nouvelle pièce 
                    nextPoly1 = polyLst[randrange(0, len(polyLst))]

                # on initialise l'oriantation de la pièce a 0
                ori = 0
                
                # condition de défaite
                # si on a le polyomino va se supperposer a une pièce de la grille 
                # avant qu'on l'affiche a l'écrant 

                x = 4
                y = 1
                while x + len(poly1[ori][0]) > len(grid1[0]): 
                    x -= 1 
                    y = y

                if isColision(grid1, poly1, x, y, ori) == True:
                    joueurLose = joueurOn
                    break


                # on fait apparaitre un pièce aléatoirement 
                # avec la fonction spawnPiece() qui prend en argument le numéro de la piece que l'on génère aléatoirement 
                grid1, poly1, prevX, prevY, x, y, ori, change, maxY = spawnPiece(grid1, poly1, ori, change)

                pieceActivated = 1

                desactivateCounter = 0

                


            # timer pour descendre la pièce de une case toute les une secondes
            if timer == 0:
                timer = time.perf_counter()
            
            # variable de difficulté avec la fonction temps()
            if time.perf_counter() - timer > temps(nbLignesSuppTotale):
                #print(nbLignesSuppTotale, temps(nbLignesSuppTotale))
                
                # gestion du délais pour desactiver la piece

                if isPolyMaxY(grid1, poly1, x, y, ori) == True:
                    desactivateCounter += 1
                
                # on reinitialise la score dès qu'il y a de l'espace sous la pièce active
                else:
                    desactivateCounter = 0

                if desactivateCounter > 3:

                    # on desactive la pièce pour en faire spawn une autre
                    pieceActivated = 0
                    
                # print(desactivateCounter)
                
                y += 1
                
                grid1, poly1, prevX, prevY, x, y, ori, change, maxY = drawPiece(grid1, poly1, prevX, prevY, x, y, ori, change, maxY)

                #print(y)
                
                # on reset le timer pour déclancher le if dans la prochaine itération
                timer = 0

                #printGrid(grid)

            # il faut redessiner la grille uniquemnt si elle a changé avec le flag 'change' pour des soucis de performance
            if change == 1:
                
                updateGridModeDeuxJoueurs(grid1, nextPoly1, score1, squareColors, joueurOn)
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

                    # on met le flag a 'Quitte' pour ne pas refaire le menu
                    flag = 'Quitte'
                    return flag
                    
                elif key == 'Touche':
                    key = touche(ev)

                    # si la touche est utile pour le jeu
                    if key == 'space' or key == 'Up' or key == 'Down' or key == 'Right' or key == 'Left':
                        grid1, poly1, prevX, prevY, x, y, ori, change, maxY, pieceActivated = keyPressedModeDeuxJoueurs(key, grid1, grid2, poly1, prevX, prevY, x, y, ori, change, maxY, pieceActivated, nextPoly1, score1, score2, squareColors, joueurOn, joueurOff)
                else:
                    pass
                    #print(key)
        
            if pieceActivated==0 : 

                score1, nbLignesSuppTotale, nbLignesSupp = suppLignesModeDeuxJoueurs(grid1, score1, nbLignesSuppTotale, varPtsDiffSelect)
                
                # si des lignes ont été supp
                if nbLignesSupp != 0 : 

                    # on affiche la grille avec la ligne pleinne en moins maintenant 
                    # puisque on sort directement de cette boucle while pour aller 
                    # dans la boucle de l'autre joueur
                    updateGridModeDeuxJoueurs(grid1, nextPoly1, score1, squareColors, joueurOn)

                    grid2=ajoutLignesModeDeuxJoueurs(grid2, nbLignesSupp)
                
                 # pour le mode pourrissement 
                if varModePourrissement:
                    if time.perf_counter() - globalTimer1 > temps(nbLignesSuppTotale) * 15:
                        pourrissement(grid1, polyLst)
                        globalTimer1 = time.perf_counter()
                        
                        # on affiche le poly supprimé 
                        updateGridModeDeuxJoueurs(grid1, nextPoly1, score1, squareColors, joueurOn)


                mise_a_jour()
                joueurOn="joueur2"
                joueurOff="joueur1"

               
                # on dessine la grille du joueur en grise pour indiquer que son tour est terminé
                drawJoueurOffGrid(grid1, nextPoly1, score2, score1, joueurOn, joueurOff)

        # teste de défaite
        if joueurLose != None:
            break 

        while joueurOn=="joueur2" : 
                
            # il faut mettre à jour pour pouvoir afficher le cadrillage et mettre les touches en attente 
            mise_a_jour()

            # si la dernière piece a été déposé 
            if pieceActivated == 0:

                # si c'est la première pièce de la partie 
                if nextPoly2 == None:
                    
                    # on génère les deux poly

                    # on choisit aléatoirement la nouvelle pièce 
                    poly2 = polyLst[randrange(0, len(polyLst))]

                    # on choisit aléatoirement le prochaine pièce
                    nextPoly2 = polyLst[randrange(0, len(polyLst))]
                else : 
                    
                    # la pièce suivante devient la pièce active et on génère la pièce suivante 
                    poly2 = nextPoly2

                    # on choisit aléatoirement la nouvelle pièce 
                    nextPoly2 = polyLst[randrange(0, len(polyLst))]

                # on initialise l'oriantation de la pièce a 0
                ori = 0
                
                # condition de défaite
                # si on a le polyomino va se supperposer a une pièce de la grille 
                # avant qu'on l'affiche a l'écrant 

                x = 4
                y = 1
                while x + len(poly2[ori][0]) > len(grid2[0]): 
                    x -= 1 
                    y = y

                if isColision(grid2, poly2, x, y, ori) == True:
                    joueurLose = joueurOn
                    break


                # on fait apparaitre un pièce aléatoirement 
                # avec la fonction spawnPiece() qui prend en argument le numéro de la piece que l'on génère aléatoirement 
                grid2, poly2, prevX, prevY, x, y, ori, change, maxY = spawnPiece(grid2, poly2, ori, change)

                

                pieceActivated = 1

                desactivateCounter = 0

                


            # timer pour descendre la pièce de une case toute les une secondes
            if timer == 0:
                timer = time.perf_counter()
            
            # variable de difficulté avec la fonction temps()
            if time.perf_counter() - timer > temps(nbLignesSuppTotale):
                #print(nbLignesSuppTotale, temps(nbLignesSuppTotale))
                
                # gestion du délais pour desactiver la piece

                if isPolyMaxY(grid2, poly2, x, y, ori) == True:
                    desactivateCounter += 1
                
                # on reinitialise la score dès qu'il y a de l'espace sous la pièce active
                else:
                    desactivateCounter = 0

                if desactivateCounter > 3:

                    # on desactive la pièce pour en faire spawn une autre
                    pieceActivated = 0
                    
                # print(desactivateCounter)
                
                y += 1
                
                grid2, poly2, prevX, prevY, x, y, ori, change, maxY = drawPiece(grid2, poly2, prevX, prevY, x, y, ori, change, maxY)

                #print(y)
                
                # on reset le timer pour déclancher le if dans la prochaine itération
                timer = 0

                #printGrid(grid)


            

            # il faut redessiner la grille uniquemnt si elle a changé avec le flag 'change' pour des soucis de performance
            if change == 1:

                updateGridModeDeuxJoueurs(grid2, nextPoly2, score2, squareColors, joueurOn)
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

                    # on met le flag a 'Quitte' pour ne pas refaire le menu
                    flag = 'Quitte'
                    return flag
                    
                elif key == 'Touche':
                    key = touche(ev)

                    # si la touche est utile pour le jeu
                    if key == 'space' or key == 'Up' or key == 'Down' or key == 'Right' or key == 'Left':
                        grid2, poly2, prevX, prevY, x, y, ori, change, maxY, pieceActivated = keyPressedModeDeuxJoueurs(key, grid2, grid1, poly2, prevX, prevY, x, y, ori, change, maxY, pieceActivated, nextPoly2, score2, score1, squareColors, joueurOn, joueurOff)
                else:
                    pass
                    #print(key)
            
            if pieceActivated==0 : 

                score2, nbLignesSuppTotale, nbLignesSupp = suppLignesModeDeuxJoueurs(grid2, score2, nbLignesSuppTotale, varPtsDiffSelect)

                if nbLignesSupp!=0 : 

                    # on affiche la grille avec la ligne pleinne en moins maintenant 
                    # puisque on sort directement de cette boucle while pour aller 
                    # dans la boucle de l'autre joueur
                    updateGridModeDeuxJoueurs(grid2, nextPoly2, score2, squareColors, joueurOn)

                    grid1 = ajoutLignesModeDeuxJoueurs(grid1, nbLignesSupp)
                
                # pour le mode pourrissement 
                if varModePourrissement:
                    if time.perf_counter() - globalTimer2 > temps(nbLignesSuppTotale) * 15:
                        pourrissement(grid2, polyLst)
                        globalTimer2 = time.perf_counter()
                        
                        # on affiche le poly supprimé 
                        updateGridModeDeuxJoueurs(grid2, nextPoly2, score2, squareColors, joueurOn)
                
                mise_a_jour()
                
                # on change de joueur 
                joueurOn="joueur1"
                joueurOff="joueur2"


                

                # on dessine la grille du joueur en grise pour indiquer que son tour est terminé
                drawJoueurOffGrid(grid2, nextPoly2, score1, score2, joueurOn, joueurOff)


    # on ré affiche la grille du gagnant en couleurs
    if joueurLose == 'joueur1':
        drawJoueurOffGrid(grid1, nextPoly1, score2, score1, 'joueur2', 'joueur1')
        updateGridModeDeuxJoueurs(grid2, nextPoly2, score2, squareColors, 'joueur2')

    else:
        drawJoueurOffGrid(grid2, nextPoly2, score1, score2, 'joueur1', 'joueur2')
        updateGridModeDeuxJoueurs(grid1, nextPoly1, score1, squareColors, 'joueur1')


    # ecran de fin revoie un flag
    return endScreenDeuxJoueurs(joueurLose, score1, score2)


def endScreenDeuxJoueurs(joueurLose, score1, score2):


    

    # la sélection est déja sur l'option retry
    select = 0

    # les deux options qu'a l'utilisateur
    option = ['retry', 'menu']

    offset = 0.5*sizeSquareGrid


    ##### menu j1 #####

    # on affiche le score dans un rectangle puis deux boutons pour réessayer 
    # et pour revenir au menu
    
    # dans un rectangle 

    
    # affichage des éléments fixe une seul fois ici


    # décalage du rectange pour que cela créer du relief avec le deuxieme rectengle qui le superpose


    rectangleOmbre(ax = largeurFenetre*1/4 - 4*sizeSquareGrid, 
                ay = hauteurFenetre/2 - 4*sizeSquareGrid, 
                bx = largeurFenetre*1/4 + 4*sizeSquareGrid, 
                by = hauteurFenetre/2 + 4*sizeSquareGrid, 
                offsetOmbre = offset, 
                colBordure = "black", 
                colRemplissage = "white",
                colOmbre = "gray",
                epaisseur = 4)
       

    if joueurLose == 'joueur1':

        # tetriTexte du game over
        xOffset, yOffset = tailleTetriTexte('GAME OVER', 10)
        tetriTexte(x = largeurFenetre*1/4 - xOffset/2, 
            y = hauteurFenetre/2 - 3*sizeSquareGrid - yOffset/2, 
            chaine =  "GAME OVER", 
            taille = 10)
    else:

        # tetriTexte du game over
        xOffset, yOffset = tailleTetriTexte('WIN', 12)
        tetriTexte(x = largeurFenetre*1/4 - xOffset/2, 
            y = hauteurFenetre/2 - 3*sizeSquareGrid - yOffset/2, 
            chaine =  "WIN", 
            taille =  12)


    # score
    tetriTexteCentre(x = largeurFenetre*1/4, 
                y = hauteurFenetre/2 - 1*sizeSquareGrid,
                chaine="Score:" + str(score1),
                taille=7
                )
    
    # on recupere la hauteure et la largeurs du tetriTexte pour les caluls de position du cuseur 

    # retry
    tetriTexteCentre(x = largeurFenetre*1/4, 
                        y = hauteurFenetre/2 + 1*sizeSquareGrid, 
                        chaine =  option[0], 
                        taille =  6)
    
    xRetryLen, yRetryHight = tailleTetriTexte(option[0], 10)

    # menu
    tetriTexteCentre(x = largeurFenetre*1/4, 
                        y = hauteurFenetre/2 + 2.5*sizeSquareGrid, 
                        chaine =  option[1], 
                        taille =  6)
    
    xMenuLen, yMenuHight = tailleTetriTexte(option[1], 10)

    # on enregistre toutes les posistions possible du curseur
    # ici 2 (retry et menu) dans une liste
    
    cursorPoseLst = [
        # tuple contenant ax, ay, bx, by pour le retry
        (
            largeurFenetre*1/4 - xRetryLen/2 - 0.5*sizeSquareGrid, 
            hauteurFenetre/2 + 1*sizeSquareGrid + yRetryHight/2
         ), 
         # meme chose pour le menu
         (
            largeurFenetre*1/4 - xMenuLen/2 - 0.5*sizeSquareGrid, 
            hauteurFenetre/2 + 2.5*sizeSquareGrid + yMenuHight/2
        )
        ]

    # on dessine le curseur a la posision par défaut
    drawCurseur(cursorPoseLst[select][0], cursorPoseLst[select][1], polyLst[randrange(0, len(polyLst))][randrange(4)])


    ### menu j2 ####

    rectangleOmbre(ax = largeurFenetre*3/4 - 4*sizeSquareGrid, 
                ay = hauteurFenetre/2 - 4*sizeSquareGrid, 
                bx = largeurFenetre*3/4 + 4*sizeSquareGrid, 
                by = hauteurFenetre/2 + 4*sizeSquareGrid, 
                offsetOmbre = offset, 
                colBordure = "black", 
                colRemplissage = "white",
                colOmbre = "gray",
                epaisseur = 4)
       

    if joueurLose == 'joueur2':

        # tetriTexte du game over
        xOffset, yOffset = tailleTetriTexte('GAME OVER', 10)
        tetriTexte(x = largeurFenetre*3/4 - xOffset/2, 
            y = hauteurFenetre/2 - 3*sizeSquareGrid - yOffset/2, 
            chaine =  "GAME OVER", 
            taille = 10)
    else:

        # tetriTexte du game over
        xOffset, yOffset = tailleTetriTexte('WIN', 12)
        tetriTexte(x = largeurFenetre*3/4 - xOffset/2, 
            y = hauteurFenetre/2 - 3*sizeSquareGrid - yOffset/2, 
            chaine =  "WIN", 
            taille =  10)


    # score
    tetriTexteCentre(x = largeurFenetre*3/4, 
                y = hauteurFenetre/2 - 1*sizeSquareGrid,
                chaine="Score:" + str(score2),
                taille=7
                )
    
    # on recupere la hauteure et la largeurs du tetriTexte pour les caluls de position du cuseur 

    # retry
    tetriTexteCentre(x = largeurFenetre*3/4, 
                        y = hauteurFenetre/2 + 1*sizeSquareGrid, 
                        chaine =  option[0], 
                        taille =  6)
    
    xRetryLen, yRetryHight = tailleTetriTexte(option[0], 10)

    # menu
    tetriTexteCentre(x = largeurFenetre*3/4, 
                        y = hauteurFenetre/2 + 2.5*sizeSquareGrid, 
                        chaine =  option[1], 
                        taille =  6)
    
    xMenuLen, yMenuHight = tailleTetriTexte(option[1], 10)

    # on enregistre toutes les posistions possible du curseur
    # ici 2 (retry et menu) dans une liste
    
    cursorPoseLstJ2 = [
        # tuple contenant ax, ay, bx, by pour le retry
        (
            largeurFenetre*3/4 - xRetryLen/2 - 0.5*sizeSquareGrid, 
            hauteurFenetre/2 + 1*sizeSquareGrid + yRetryHight/2
         ), 
         # meme chose pour le menu
         (
            largeurFenetre*3/4 - xMenuLen/2 - 0.5*sizeSquareGrid, 
            hauteurFenetre/2 + 2.5*sizeSquareGrid + yMenuHight/2
        )
        ]

    # on dessine le curseur a la posision par défaut
    drawCurseur(cursorPoseLstJ2[select][0], cursorPoseLstJ2[select][1], polyLst[randrange(0, len(polyLst))][randrange(4)])

    
    while True:

        # partie gestions des input 
       
        # on met a jour le fenêtre pour récuperer les touches pressées
        mise_a_jour()
        
        # recuperation de la touche 
        ev=donne_ev() 

        # si une touche a été pressé 
        if ev is not None : 

            # on enregistre son type
            key = type_ev(ev)

            # si l'utilisateur veut fermer la fenêtre
            if key == 'Quitte':

                # on ferme la fenre et on sort de la boucle de jeu ce qui revien a arrêter le programme
                ferme_fenetre()                
                return 'Quitte'
            
            # si la touche est une touche de clavier
            elif key == 'Touche':
                
                # on enregistre la touche
                key = touche(ev)

                # touche du bas 
                if key == 'Down':

                    if select == 1:
                        select = 0
                    else:
                        select += 1

                    efface("Curseur")
                    drawCurseur(cursorPoseLst[select][0], cursorPoseLst[select][1], polyLst[randrange(0, len(polyLst))][randrange(4)])
                    drawCurseur(cursorPoseLstJ2[select][0], cursorPoseLstJ2[select][1], polyLst[randrange(0, len(polyLst))][randrange(4)])

                    
                
                # touche du haut 
                elif key == 'Up':

                    if select == 0:
                        select = 1
                    else:
                        select -= 1


                    efface("Curseur")
                    drawCurseur(cursorPoseLst[select][0], cursorPoseLst[select][1], polyLst[randrange(0, len(polyLst))][randrange(4)])                
                    drawCurseur(cursorPoseLstJ2[select][0], cursorPoseLstJ2[select][1], polyLst[randrange(0, len(polyLst))][randrange(4)])



                # touche entrer
                elif key == 'Return':
                    return option[select]


def drawJoueurOffGrid(gridOff, nextPoly, scoreOn, scoreOff, joueurOn, joueurOff):
    """
    dessine sur la fennêtre la représentation de la `grid` du joueyr off en grise

    `grid1` : matrice qui représente la partie elle même du joueur 1 
    `grid2` : matrice qui représente la partie elle même du joueur 2
    `nextPoly` : matrice contenant la pochaine pièce à jouer pour la passer en param à la fonction `drawNextPoly()`
    `score1` : variable contenant le score pour la passer en param à la fonction `drawScore()` du joueur 1
    `score2` : variable contenant le score pour la passer en param à la fonction `drawScore()` du joueur 2
    `joueurOn` : variable contenant le nom du joueur dont c'est le tour
    `joueurOff` : variable contenant le nom du joueur en attente 
    """

    if joueurOn=="joueur1" : 

        coeffJoueurOn=1/4
        coeffJoueurOff=3/4

        efface("scoreJ2")
        # affichage du score
        drawScoreJoueur2(scoreOff)

    
    elif joueurOn=="joueur2" : 
        coeffJoueurOn=3/4
        coeffJoueurOff=1/4

        efface("scoreJ1")
        
        # affichage du score
        drawScoreJoueur1(scoreOff)

    
    ####################################Affichage joueur off ###############################################################
    # affichage du poly suivant

    yGrid = 0
    xGrid = 0

    thickness = 8

    # ligne basse de la grille
    ligne(largeurFenetre*coeffJoueurOff - sizeSquareGrid*numXSquare/2 - thickness//2, hauteurFenetre - yMargin, largeurFenetre*coeffJoueurOff + sizeSquareGrid*numXSquare/2 + thickness//2, hauteurFenetre - yMargin, "black", thickness)

    #ligne de gauche
    ligne(largeurFenetre*coeffJoueurOff - sizeSquareGrid*numXSquare/2, hauteurFenetre - yMargin, largeurFenetre*coeffJoueurOff - sizeSquareGrid*numXSquare/2, hauteurFenetre - yMargin - sizeSquareGrid*numYSquare, "black", thickness)

    #ligne de droite
    ligne(largeurFenetre*coeffJoueurOff + sizeSquareGrid*numXSquare/2, hauteurFenetre - yMargin, largeurFenetre*coeffJoueurOff + sizeSquareGrid*numXSquare/2, hauteurFenetre - yMargin - sizeSquareGrid*numYSquare, "black", thickness)



    # on dessine les case vide pour que les épaisseurs des case des case pleines ne soit 'écrasé' par l'épaisseur de la case vide
    for i in range(len(gridOff)):

        yGrid = hauteurFenetre - yMargin - sizeSquareGrid*(numYSquare + 4) + i* sizeSquareGrid
        for j in range(len(gridOff[0])):

            # on enregistre la couleur de la case
            n = gridOff[i][j]

            xGrid = largeurFenetre*coeffJoueurOff - sizeSquareGrid*numXSquare/2 + j*sizeSquareGrid

            # si on est dans les 4 première ligne
            if i < 4:
                # on affiche que les pièce, pas la grille
                if n == 0:
                    rectangle(xGrid, yGrid, xGrid + sizeSquareGrid, yGrid + sizeSquareGrid, "#D9D9D9", "#D9D9D9")

            
            else:

                # on affiche bien que les case vide
                if n == 0:
                    rectangle(xGrid, yGrid, xGrid + sizeSquareGrid, yGrid + sizeSquareGrid, "light gray", "white")
    
    
    # on dessine que les cases pleines
    for i in range(len(gridOff)):

        yGrid = hauteurFenetre - yMargin - sizeSquareGrid*(numYSquare + 4) + i* sizeSquareGrid
        for j in range(len(gridOff[0])):

            # on enregistre la couleur de la case
            n = gridOff[i][j]

            xGrid = largeurFenetre*coeffJoueurOff - sizeSquareGrid*numXSquare/2 + j*sizeSquareGrid

            # si on est dans les 4 première ligne
            if i < 4:
                # on affiche que les pièce, pas la grille
                if n == 0:
                    pass
                else:
                    rectangle(xGrid, yGrid, xGrid + sizeSquareGrid, yGrid + sizeSquareGrid, "black", "grey", 3)
                    
                
            else:
                if n != 0:
                    rectangle(xGrid, yGrid, xGrid + sizeSquareGrid, yGrid + sizeSquareGrid, "black", "grey", 3)
                
def drawGrid1(grid1, squareColors):

    # coef pour l'emplacement de la grid
    coeffJoueurOn=1/4

    yGrid = 0
    xGrid = 0
    for i in range(len(grid1)):

        yGrid = hauteurFenetre - yMargin - sizeSquareGrid*(numYSquare + 4) + i* sizeSquareGrid
        for j in range(len(grid1[0])):

            # on enregistre la couleur de la case
            n = grid1[i][j]

            xGrid = largeurFenetre*coeffJoueurOn - sizeSquareGrid*numXSquare/2 + j*sizeSquareGrid

            # si on est dans les 4 première ligne
            if i < 4:
                # on affiche que les pièce, pas la grille
                if n == 0:
                    rectangle(xGrid, yGrid, xGrid + sizeSquareGrid, yGrid + sizeSquareGrid, "#D9D9D9", "#D9D9D9", tag='grid1')
            
            else:

                # on affiche bien que les case vide
                if n == 0:
                    rectangle(xGrid, yGrid, xGrid + sizeSquareGrid, yGrid + sizeSquareGrid, "light gray", "white", tag='grid1')
                    
    # on dessine que les cases pleines
    for i in range(len(grid1)):

        yGrid = hauteurFenetre - yMargin - sizeSquareGrid*(numYSquare + 4) + i* sizeSquareGrid
        for j in range(len(grid1[0])):

            # on enregistre la couleur de la case
            n = grid1[i][j]

            xGrid = largeurFenetre*coeffJoueurOn - sizeSquareGrid*numXSquare/2 + j*sizeSquareGrid

            # si on est dans les 4 première ligne
            if i < 4:
                # on affiche que les pièce, pas la grille
                if n == 0:
                    pass
                else:
                    rectangle(xGrid, yGrid, xGrid + sizeSquareGrid, yGrid + sizeSquareGrid, "black", squareColors[n], 3, tag='grid1')
            
            else:
                if n != 0:
                    rectangle(xGrid, yGrid, xGrid + sizeSquareGrid, yGrid + sizeSquareGrid, "black", squareColors[n], 3, tag='grid1')


def drawGrid2(grid2, squareColors):

    # coef pour l'emplacement de la grid
    coeffJoueurOn=3/4

    yGrid = 0
    xGrid = 0
    for i in range(len(grid2)):

        yGrid = hauteurFenetre - yMargin - sizeSquareGrid*(numYSquare + 4) + i* sizeSquareGrid
        for j in range(len(grid2[0])):

            # on enregistre la couleur de la case
            n = grid2[i][j]

            xGrid = largeurFenetre*coeffJoueurOn - sizeSquareGrid*numXSquare/2 + j*sizeSquareGrid

            # si on est dans les 4 première ligne
            if i < 4:
                # on affiche que les pièce, pas la grille
                if n == 0:
                    rectangle(xGrid, yGrid, xGrid + sizeSquareGrid, yGrid + sizeSquareGrid, "#D9D9D9", "#D9D9D9", tag='grid2')
            
            else:

                # on affiche bien que les case vide
                if n == 0:
                    rectangle(xGrid, yGrid, xGrid + sizeSquareGrid, yGrid + sizeSquareGrid, "light gray", "white", tag='grid2')
                    
    # on dessine que les cases pleines
    for i in range(len(grid2)):

        yGrid = hauteurFenetre - yMargin - sizeSquareGrid*(numYSquare + 4) + i* sizeSquareGrid
        for j in range(len(grid2[0])):

            # on enregistre la couleur de la case
            n = grid2[i][j]

            xGrid = largeurFenetre*coeffJoueurOn - sizeSquareGrid*numXSquare/2 + j*sizeSquareGrid

            # si on est dans les 4 première ligne
            if i < 4:
                # on affiche que les pièce, pas la grille
                if n == 0:
                    pass
                else:
                    rectangle(xGrid, yGrid, xGrid + sizeSquareGrid, yGrid + sizeSquareGrid, "black", squareColors[n], 3, tag='grid2')
            
            else:
                if n != 0:
                    rectangle(xGrid, yGrid, xGrid + sizeSquareGrid, yGrid + sizeSquareGrid, "black", squareColors[n], 3, tag='grid2')



def updateGridModeDeuxJoueurs(gridOn, nextPoly, scoreOn, squareColors, joueurOn):
    """
    dessine sur la fennêtre la représentation de la `grid`

    `grid1` : matrice qui représente la partie elle même du joueur 1 
    `grid2` : matrice qui représente la partie elle même du joueur 2
    `nextPoly` : matrice contenant la pochaine pièce à jouer pour la passer en param à la fonction `drawNextPoly()`
    `score1` : variable contenant le score pour la passer en param à la fonction `drawScore()` du joueur 1
    `score2` : variable contenant le score pour la passer en param à la fonction `drawScore()` du joueur 2
    `joueurOn` : variable contenant le nom du joueur dont c'est le tour
    `joueurOff` : variable contenant le nom du joueur en attente 
    """

    if joueurOn=="joueur1" : 
        
        # on efface la grille précedente 
        efface('grid1')

        # on la redessine
        drawGrid1(gridOn, squareColors)

        # efface le next poly du joueur
        efface('nextPolyJoueur1')
        
        drawNextPolyJoueur1(nextPoly, squareColors) 

        # efface le score du joueurs 
        efface("scoreJ1")

        drawScoreJoueur1(scoreOn)

    else : 

        # on efface la grille précedente 
        efface('grid2')

        # on la redessine
        drawGrid2(gridOn, squareColors)

        # efface le next poly du joueur
        efface('nextPolyJoueur2')
        
        drawNextPolyJoueur2(nextPoly, squareColors) 

        # efface le score du joueurs 
        efface("scoreJ2")

        drawScoreJoueur2(scoreOn)
    
    
    
def drawScoreJoueur1(score) : 
    """dessine a droite de la grille le score"""
    
    ############Affichage Score joueur 1#############################################
    # le décalage de chaque coté pour que la ligne du dessous soit un peut plus grande que la taille du tetriTexte
    xOffset = sizeSquareGrid/4
    yOffset = sizeSquareGrid/8

    # ligne du dessous a droite de la grille a la 2eme case
    ligne(largeurFenetre/4 + sizeSquareGrid*numXSquare/2, hauteurFenetre - yMargin - sizeSquareGrid*numYSquare  + 2*sizeSquareGrid , largeurFenetre/4 + sizeSquareGrid*numXSquare/2 + tailleTetriTexte(str(score), 10)[0] + xOffset + yOffset, hauteurFenetre - yMargin - sizeSquareGrid*numYSquare + 2*sizeSquareGrid, "black", 7, "scoreJ1") 
    
    # possition du tetriTexte 
    xPose = largeurFenetre/4 + sizeSquareGrid*numXSquare/2 + xOffset
    yPose = hauteurFenetre - yMargin - sizeSquareGrid*numYSquare + sizeSquareGrid  - yOffset
    
    tetriTexte(xPose, yPose ,str(score), "black", 10, 'scoreJ1')
    

def drawScoreJoueur2(score):

    # le décalage de chaque coté pour que la ligne du dessous soit un peut plus grande que la taille du tetriTexte
    xOffset = sizeSquareGrid/4
    yOffset = sizeSquareGrid/8

    # ligne du dessous a droite de la grille a la 2eme case
    ligne(3*largeurFenetre/4 + sizeSquareGrid*numXSquare/2, hauteurFenetre - yMargin - sizeSquareGrid*numYSquare  + 2*sizeSquareGrid , 3*largeurFenetre/4 + sizeSquareGrid*numXSquare/2 + tailleTetriTexte(str(score), 10)[0] + xOffset + yOffset, hauteurFenetre - yMargin - sizeSquareGrid*numYSquare + 2*sizeSquareGrid, "black", 7, tag = "scoreJ2") 
    
    # possition du tetriTexte 
    xPose = 3*largeurFenetre/4 + sizeSquareGrid*numXSquare/2 + xOffset
    yPose = hauteurFenetre - yMargin - sizeSquareGrid*numYSquare + sizeSquareGrid  - yOffset
    
    # TODO : taille de police en fonction de la taille de la fenêtre
    tetriTexte(xPose, yPose ,str(score), "black", 10, 'scoreJ2')



def drawNextPolyJoueur1(nextPoly, squareColors):
    """dsesine a droite de la grille le poly suivant"""
 
    coeff=1/4

    # ligne du dessus a droite de la grille a la 4eme case et 
    # de logueur la longueur de next poly + une 1 case pour le padding 
    ligne(largeurFenetre*coeff + sizeSquareGrid*numXSquare/2, hauteurFenetre - yMargin - numYSquare*sizeSquareGrid + 4*sizeSquareGrid, largeurFenetre*coeff + sizeSquareGrid*numXSquare/2 + sizeSquareGrid*len(nextPoly[0][0]) + 1*sizeSquareGrid, hauteurFenetre - yMargin - numYSquare*sizeSquareGrid + 4*sizeSquareGrid, "black", 8, tag='nextPolyJoueur1')

    # on dessine le poly avec sont orientation de base a une case en dessous de la ligne
    # et 1/2 case horizontalement

    y = hauteurFenetre - yMargin - numYSquare*sizeSquareGrid + 4*sizeSquareGrid + 0.5*sizeSquareGrid
    x = largeurFenetre*coeff + sizeSquareGrid*numXSquare/2 + 0.5*sizeSquareGrid

    for i in range(len(nextPoly[0])):
        for j in range(len(nextPoly[0][0])):
            
            # on affiche que les case remplit pour ne pas avoir de cases blanches
            if nextPoly[0][i][j] == 0:
                pass
            else:
                rectangle(x+j*sizeSquareGrid, y+i*sizeSquareGrid, x+j*sizeSquareGrid + sizeSquareGrid, y+i*sizeSquareGrid + sizeSquareGrid, "black", squareColors[nextPoly[0][i][j]], 3, tag='nextPolyJoueur1')


def drawNextPolyJoueur2(nextPoly, squareColors):
    """dsesine a droite de la grille le poly suivant"""
    
    # coef pour la position du nextPoly 
    coeff=3/4

    
    # ligne du dessus a droite de la grille a la 4eme case et 
    # de logueur la longueur de next poly + une 1 case pour le padding 
    ligne(largeurFenetre*coeff + sizeSquareGrid*numXSquare/2, hauteurFenetre - yMargin - numYSquare*sizeSquareGrid + 4*sizeSquareGrid, largeurFenetre*coeff + sizeSquareGrid*numXSquare/2 + sizeSquareGrid*len(nextPoly[0][0]) + 1*sizeSquareGrid, hauteurFenetre - yMargin - numYSquare*sizeSquareGrid + 4*sizeSquareGrid, "black", 8, tag='nextPolyJoueur2')

    # on dessine le poly avec sont orientation de base a une case en dessous de la ligne
    # et 1/2 case horizontalement

    y = hauteurFenetre - yMargin - numYSquare*sizeSquareGrid + 4*sizeSquareGrid + 0.5*sizeSquareGrid
    x = largeurFenetre*coeff + sizeSquareGrid*numXSquare/2 + 0.5*sizeSquareGrid

    for i in range(len(nextPoly[0])):
        for j in range(len(nextPoly[0][0])):
            
            # on affiche que les case remplit pour ne pas avoir de cases blanches
            if nextPoly[0][i][j] == 0:
                pass
            else:
                rectangle(x+j*sizeSquareGrid, y+i*sizeSquareGrid, x+j*sizeSquareGrid + sizeSquareGrid, y+i*sizeSquareGrid + sizeSquareGrid, "black", squareColors[nextPoly[0][i][j]], 3, tag='nextPolyJoueur2')


def keyPressedModeDeuxJoueurs(key, gridOn, gridOff, poly, prevX, prevY, x, y, ori, change, maxY, pieceActivated, nextPoly, scoreOn, scoreOff, squareColors, joueurOn, joueurOff):
    """prends en argument la touche pressée et appelle differentes fonction selon la touche pressée"""
    
    #debug 
    #print(key) 
    # pour touner la pièce d'1/4 vers la droite
    if key == 'Up':
        gridOn, poly, prevX, prevY, x, y, ori, change, maxY = rotatePiece(gridOn, poly, prevX, prevY, x, y, ori, change, maxY)
        return gridOn, poly, prevX, prevY, x, y, ori, change, maxY, pieceActivated

    # pour déplacer la pièce de une case vers la gauche
    if key == 'Left':
        x -= 1

        gridOn, poly, prevX, prevY, x, y, ori, change, maxY = drawPiece(gridOn, poly, prevX, prevY, x, y, ori, change, maxY)
        return gridOn, poly, prevX, prevY, x, y, ori, change, maxY, pieceActivated


    # pour déplacer la pièce de une case vers la gauche
    elif key == 'Right':
        x += 1

        gridOn, poly, prevX, prevY, x, y, ori, change, maxY = drawPiece(gridOn, poly, prevX, prevY, x, y, ori, change, maxY)
        return gridOn, poly, prevX, prevY, x, y, ori, change, maxY, pieceActivated

    
    # pour placer intantanément la pièce 
    elif key == 'space':
        
        
        gridOn, poly, prevX, prevY, x, y, ori, change, maxY = drawPiece(gridOn, poly, prevX, prevY, x, maxY, ori, change, maxY)

        # on pose la pièce définitivement
        pieceActivated = 0


        # on dessine la pièce qui viens de se possé directement sinon elle restait en l'air si la condition de défaite 
        updateGridModeDeuxJoueurs(gridOn, nextPoly, scoreOn, squareColors, joueurOn)

        return gridOn, poly, prevX, prevY, x, y, ori, change, maxY, pieceActivated


    # 'down' pour baisser la pièce plus rapidement 
    else:
        y += 1

        gridOn, poly, prevX, prevY, x, y, ori, change, maxY = drawPiece(gridOn, poly, prevX, prevY, x, y, ori, change, maxY)
        return gridOn, poly, prevX, prevY, x, y, ori, change, maxY, pieceActivated


def ajoutLignesModeDeuxJoueurs(grid, nbLignesSupp):
    """ajoute une ligne tout en bas de grid avec une case vide """

    newGrid=[]

    for a in range(nbLignesSupp, len(grid)) : 
        newGrid.append(grid[a])
    
    # case vide aléatoire
    nb=randrange(len(grid[-1]))
    for _ in range(nbLignesSupp) : 
        newGrid.append([])
        
        for b in range(len(grid[-1])) :
            if b==nb : 
                newGrid[-1].append(0)
            else : 

                # -2 est l'index des cases rajouté
                newGrid[-1].append(-2)
    return newGrid 
            
             
def suppLignesModeDeuxJoueurs(grid : list[list], score, nbLignesSuppTotale, varPtsDiffSelect) : 
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

            # on n'augmente pas le nb de ligne supp 
            # si le joueur vien de suupprimer une ligne rajouté par son adversaire

            # l'index -2 représente les case rajouté
            # comme on en rajoute 9 si la ligne en contient c'est une ligne rajouté
            if grid[i].count(-2) != 9:
                nbLignesSupp += 1

            downLignes(grid, i)
            
        i+=1

    # on augmente le nb de lignes supprimé toltale par le nb de lignes suppp
    nbLignesSuppTotale += nbLignesSupp

    # choix de la fonction a utiliser si la variante est selectionner
    if varPtsDiffSelect == True:
        return pointsEnFonctionDifficulte(score, nbLignesSupp, nbLignesSuppTotale), nbLignesSuppTotale, nbLignesSupp
    else:
        return points(score, nbLignesSupp), nbLignesSuppTotale, nbLignesSupp
