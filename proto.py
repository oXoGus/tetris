from fltk import *
from tetriFont import *
import time
from random import randrange



def main():


    # initialisation des varible pour le menu
    fermer = 0
    jouer=["Jouer", "Quitter"]
    flag = None

    # initialisation des flag de selection des variante 
    
    # variante points lié au niveau
    varPtsDiffSelect = False

    # variante polyominos arbitraires
    varPolyArbitraires = False

    # variante mode pourrisement
    varModePourrisement = False

    # variante Mode 2 joueurs 
    varMode2joueurs = False

    # variante pause et sauvegarde
    varPauseEtSave = False
    


    # création de la fenêtre
    cree_fenetre(largeurFenetre, hauteurFenetre)


    # choix par défaut est jouer c'es pour cela qu'il est plus gros, pour indiquer qu'il est selectionner
    choix = 0

    # le titre
    xOffset, yOffset = tailleTetriTexte("TETRIS", 50)
    tetriTexte(largeurFenetre*1/2 - xOffset/2, hauteurFenetre*1/4 - yOffset/2 , "TETRIS", 'black', 50) 



    # pour centrer le tetriTexte
    xOffset, yOffset = tailleTetriTexte(jouer[0], 18)
    tetriTexte(largeurFenetre*1/2 - xOffset/2, hauteurFenetre*1/2 - yOffset/2 - 50, jouer[0], 'black', 18)
            



    # Quitter
    xOffset, yOffset = tailleTetriTexte(jouer[1], 18)
    tetriTexte(largeurFenetre*1/2 - xOffset/2, hauteurFenetre*1/2 - yOffset/2 + 50, jouer[1], 'black', 18)

    # curseur 
    drawCurseur(largeurFenetre*1/2 - xOffset/2 - 60, hauteurFenetre*1/2 - yOffset/2 - 50, polyLst[randrange(0, len(polyLst))][randrange(4)])

    # boucle de jeu
    while True: 

        # si le joueur a appuié sur réessayer 
        if flag == 'retry':

            # on relance une partie avec les memes variantes activés
            flag = game(varPtsDiffSelect)
            
            # on ne refait pas une boucle sinon le menu sera affiché 
            continue

        # pour le menu
        elif flag == 'menu':

            efface_tout()

            # on redessine tout une fois 
            # le titre
            xOffset, yOffset = tailleTetriTexte("TETRIS", 50)
            tetriTexte(largeurFenetre*1/2 - xOffset/2, hauteurFenetre*1/4 - yOffset/2 , "TETRIS", 'black', 50) 



            # pour centrer le tetriTexte
            xOffset, yOffset = tailleTetriTexte(jouer[0], 18)
            tetriTexte(largeurFenetre*1/2 - xOffset/2, hauteurFenetre*1/2 - yOffset/2 - 50, jouer[0], 'black', 18)
                    



            # Quitter
            xOffset, yOffset = tailleTetriTexte(jouer[1], 18)
            tetriTexte(largeurFenetre*1/2 - xOffset/2, hauteurFenetre*1/2 - yOffset/2 + 50, jouer[1], 'black', 18)

            # curseur 
            drawCurseur(largeurFenetre*1/2 - xOffset/2 - 60, hauteurFenetre*1/2 - yOffset/2 - 50, polyLst[randrange(0, len(polyLst))][randrange(4)])

            flag = None



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
                break
            
            # si la touche est une touche de clavier
            elif key == 'Touche':
                
                # on enregistre la touche
                key = touche(ev)

                # flèche du bas
                if key=='Down':

                    # on inverse l'état de choix
                    if choix == 1: 
                        choix = 0
                        efface("Curseur")   
                        drawCurseur(largeurFenetre*1/2 - xOffset/2 - 60, hauteurFenetre*1/2 - yOffset/2 - 50, polyLst[randrange(0, len(polyLst))][randrange(4)])
                        
                    
                    else : 
                        choix += 1
                        efface("Curseur")
                        drawCurseur(largeurFenetre*1/2 - xOffset/2 - 60, hauteurFenetre*1/2 - yOffset/2 + 50, polyLst[randrange(0, len(polyLst))][randrange(4)])

                # flêche du haut
                elif key=='Up':
                    # on inverse l'état de choix
                    if choix == 0: 
                        choix = 1
                        efface("Curseur")
                        drawCurseur(largeurFenetre*1/2 - xOffset/2 - 60, hauteurFenetre*1/2 - yOffset/2 + 50, polyLst[randrange(0, len(polyLst))][randrange(4)])
                    else : 
                        choix -= 1
                        efface("Curseur")
                        drawCurseur(largeurFenetre*1/2 - xOffset/2 - 60, hauteurFenetre*1/2 - yOffset/2 - 50, polyLst[randrange(0, len(polyLst))][randrange(4)])

                
                
                # si l'utilisateur appuis sur la touche entrer
                if key == 'Return' : 
                    
                    # si le joueur a selectionné 'jouer'
                    if choix==0 :

                        # liste contentant les tetriTextes pour les variantes
                        variantes = ["Score en fonction \nde la difficulte", "Polynomios \nArbitraires", "Mode 2 joueurs", "Mode pourrissement"]
                        descriptionVar = ["Score en fonction de la difficulte", "comming soon", "comming soon", "comming soon"]
                        
                        saisie = 0 
                        
                        # on efface tout l'ancien menu
                        efface_tout()
                        
                        
                        
                        suivant=0 
                        saisie = 0 
                        
                        # on stoque toues les couleurs selon les saisi possible
                        colSaissieLst = [["black", "light gray", "light gray", "light gray"], 
                                         ["light gray", "black", "light gray", "light gray"],
                                         ["light gray", "light gray", "black", "light gray"],
                                         ["light gray", "light gray", "light gray", "black"]
                                         ]

                        while suivant != 1 : 


                            # affichage de la selection des variantes
                            efface_tout()


                            
                            
                            # rectangle encatrant tout les choix
                            rectangleOmbre(largeurFenetre*1/5, hauteurFenetre*1/5 , largeurFenetre*4/5,  hauteurFenetre*4/5, 1*sizeSquareGrid, "white", "black", "gray", 5)


                            # tetriTexte explicatif
                            tetriTexteCentre(largeurFenetre/2, hauteurFenetre*0.25, "choisisez vos variantes", 'black', 14)
                            tetriTexteCentre(largeurFenetre/2, hauteurFenetre*0.3, "avec les fleches", 'black', 14)

                            
                            # case 1
                            xCase1 = largeurFenetre*1/5 + 1*sizeSquareGrid
                            yCase1 = hauteurFenetre/2 - 2*sizeSquareGrid
                            rectangleOmbre(xCase1, yCase1, xCase1 + sizeSquareGrid, yCase1 + sizeSquareGrid, 1/6*sizeSquareGrid, "white", "black", "gray", 5)
                            
                            #case 2
                            xCase2 = largeurFenetre*1/5 + 1*sizeSquareGrid
                            yCase2 = hauteurFenetre/2 + 2*sizeSquareGrid
                            rectangleOmbre(xCase2, yCase2, xCase2 + sizeSquareGrid, yCase2 + sizeSquareGrid, 1/6*sizeSquareGrid, "white", "black", "gray", 5)

                            # case 3
                            xCase3 = largeurFenetre/2 
                            yCase3 = hauteurFenetre/2 - 2*sizeSquareGrid
                            rectangleOmbre(xCase3, yCase3, xCase3 + sizeSquareGrid, yCase3 + sizeSquareGrid, 1/6*sizeSquareGrid, "white", "black", "gray", 5)                            
                            
                            
                            # case 3
                            xCase4 = largeurFenetre/2 
                            yCase4 = hauteurFenetre/2 + 2*sizeSquareGrid
                            rectangleOmbre(xCase4, yCase4, xCase4 + sizeSquareGrid, yCase4 + sizeSquareGrid, 1/6*sizeSquareGrid, "white", "black", "gray", 5)                                                 
                            
                            
                                
                            # tetriTextes des variantes a droite de chaque cases
                            
                            textMarginLeft = sizeSquareGrid + 0.2*sizeSquareGrid

                            # case 1
                            tetriTexte(xCase1 + textMarginLeft, yCase1, "Score en fonction", colSaissieLst[saisie][0], 8)
                            tetriTexte(xCase1 + textMarginLeft, yCase1 + 0.70*sizeSquareGrid, "de la difficulte", colSaissieLst[saisie][0], 8)
                            
                            # case 2
                            tetriTexte(xCase2 + textMarginLeft, yCase2, "Polynomios", colSaissieLst[saisie][1], 8)
                            tetriTexte(xCase2 + textMarginLeft, yCase2 + 0.70*sizeSquareGrid, "arbitraire", colSaissieLst[saisie][1], 8)
                            
                            # case 3
                            tetriTexte(xCase3 + textMarginLeft, yCase3 + 0.2*sizeSquareGrid, "Mode 2 joueurs", colSaissieLst[saisie][2], 8)
                            
                            # case 4
                            tetriTexte(xCase4 + textMarginLeft, yCase4, variantes[3], colSaissieLst[saisie][3], 8)
                            

                            # tetriTexte de description de la variante
                            tetriTexteCentre(largeurFenetre*1/2, hauteurFenetre*0.7, descriptionVar[saisie], "black", 10)
                            
                            # cases cochés 
                            if varPtsDiffSelect == True : 

                                # on coche la première case
                                ligne(xCase1, yCase1, xCase1 + sizeSquareGrid, yCase1 + sizeSquareGrid, "black", 5)
                                ligne(xCase1 + sizeSquareGrid, yCase1, xCase1, yCase1 + sizeSquareGrid, "black", 5)
                            
                            if varPolyArbitraires==True : 
                                ligne(xCase2, yCase2, xCase2 + sizeSquareGrid, yCase2 + sizeSquareGrid, "black", 5)
                                ligne(xCase2 + sizeSquareGrid, yCase2, xCase2, yCase2 + sizeSquareGrid, "black", 5)
                            
                            if varModePourrisement==True : 
                                ligne(xCase3, yCase3, xCase3 + sizeSquareGrid, yCase3 + sizeSquareGrid, "black", 5)
                                ligne(xCase3 + sizeSquareGrid, yCase3, xCase3, yCase3 + sizeSquareGrid, "black", 5)
                                        
                            if varMode2joueurs==True :
                                ligne(xCase4, yCase4, xCase4 + sizeSquareGrid, yCase4 + sizeSquareGrid, "black", 5)
                                ligne(xCase4 + sizeSquareGrid, yCase4, xCase4, yCase4 + sizeSquareGrid, "black", 5)
                                    
                            tetriTexteCentre(largeurFenetre*1/2, hauteurFenetre*0.9, "appuyez sur espace pour lancer la partie", "black", 10)

                            # gestion des touches
                            
                            # on récupère la dernière touche  
                            mise_a_jour()
                            ev=donne_ev()

                            # si une touche a bien été pressé
                            if ev is not None : 
                                
                                # on store son type
                                key = type_ev(ev)
                                
                                # si l'utilisateur veut fermer la fenêtre
                                if key == 'Quitte':
                                    ferme_fenetre()
                                    fermer = True
                                    break

                                elif key=='Touche' : 
                                    
                                    # on enregistre la touche
                                    key=touche(ev)
                                    print(key)
                                    

                                    if key=='Up' : 

                                        # on change saisie
                                        if saisie==3 : 
                                            saisie=0
                                        else : 
                                            saisie+=1

                                        
                                        
        
                                    elif key=='Down':

                                        # on change la saisie
                                        if saisie==0 : 
                                            saisie=3 
                                        else : 
                                            saisie-=1
                                        
                                           
                                    elif key=='Return' : 

                                        # gestions des cases cochées, on inverse leurs états si la variante est implémanté  
                                        if saisie == 0 :    
                                            if varPtsDiffSelect == True:
                                                varPtsDiffSelect = False
                                            else:
                                                varPtsDiffSelect = True 
                                    
                                    elif key=='space' :
                                        
                                        #  on démare la partie avec les variantes
                                        flag = game(varPtsDiffSelect)

                                        # la fenêtre est deja fermer on ferme le programme
                                        if flag == 'Quitte':
                                            return None
                                        
                                        # pour ne pas refaire la boucle et afficher la selection des variantes
                                        if flag == 'retry' or flag == 'menu':
                                            break
                                        
                                        
                    
                        if fermer ==  True:
                            break
                    
                    elif choix==1 : 

                        # on ferme la fenêtre puis arrête le programme
                        ferme_fenetre() 
                        break
 
                        

# Dans la boucle ci dessus, il faut rajouter le tetriTexte description de ce que l'utilisateur doit faire, ainsi que lde la description des modes 
#Activer en fonction les modes 




def game(varPtsDiffSelect):
    """une partie de tertis
    
    prend en argument les variantes activées
    renvoie un flag pour qui sera traité par le menu
    """
    
    # on efface le menu
    efface_tout()
    
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

    flag = None


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

    # on initialise la variable pour la condition de défaite
    maxY = len(grid)


    # TODO : menu
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
            # si le maxY de la dernière pièce qui vient d'être posé va se supperposer avec le nouveau poly généré
            if len(poly[ori]) - 1 >= maxY:
                break

            

            # on fait apparaitre un pièce aléatoirement 
            # avec la fonction spawnPiece() qui prend en argument le numéro de la piece que l'on génère aléatoirement 
            grid, poly, prevX, prevY, x, y, ori, change, maxY = spawnPiece(grid, poly, ori, change)

            #printGrid(grid)

            pieceActivated = 1

            desactivateCounter = 0


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

            #printGrid(grid)


        

        # il faut redessiner la grille uniquemnt si elle a changé avec le flag 'change' pour des soucis de performance
        if change == 1:
            drawGrid(grid, nextPoly, score)

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
                    grid, poly, prevX, prevY, x, y, ori, change, maxY, pieceActivated = keyPressed(key, grid, poly, prevX, prevY, x, y, ori, change, maxY, pieceActivated)
            else:
                pass
                #print(key)

    # ecran de fin revoie un flag
    return endScreen(score)


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

def drawGrid(grid, nextPoly, score):
    """
    dessine sur la fennêtre la représentation de la `grid`

    `grid` : matrice qui représente la partie elle même
    `nextPoly` : matice contenant la pochaine pièce à jouer pour la passer en param à la fonction `drawNextPoly()`
    `score` : variable contenant le score pour la passer en param à la fonction `drawScore()`
    """

    efface_tout()

    # affichage du poly suivant
    drawNextPoly(nextPoly)

    # affichage du score
    drawScore(score)

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
                rectangle(x+j*sizeSquareGrid, y+i*sizeSquareGrid, x+j*sizeSquareGrid + sizeSquareGrid, y+i*sizeSquareGrid + sizeSquareGrid, "black", squareColors[nextPoly[0][i][j]], 3)

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
    
    # TODO : taille de police en fonction de la taille de la fenêtre
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




def endScreen(score):
    """dessine l'écran de fin de partie 
    affiche le score avec en dessous 2 boutton rejouer et revenir au menu  
    revoie une chaine de caractère 'menu' ou 'retry'"""

    # la sélection est déja sur l'option retry
    select = 0


    # les deux options qu'a l'utilisateur
    option = ['retry', 'menu']

    offset = 0.5*sizeSquareGrid




    # on affiche le score dans un rectangle puis deux boutons pour réessayer 
    # et pour revenir au menu
    
    # dans un rectangle 

    
    # affichage des éléments fixe une seul fois ici


    # décalage du rectange pour que cela créer du relief avec le deuxieme rectengle qui le superpose


    rectangleOmbre(ax = largeurFenetre/2 - 4*sizeSquareGrid, 
                    ay = hauteurFenetre/2 - 4*sizeSquareGrid, 
                   bx = largeurFenetre/2 + 4*sizeSquareGrid, 
                   by = hauteurFenetre/2 + 4*sizeSquareGrid, 
                   offsetOmbre = offset, 
                   colBordure = "black", 
                   colRemplissage = "white",
                    colOmbre = "gray",
                   epaisseur = 4)
       
    # tetriTexte du game over
    xOffset, yOffset = tailleTetriTexte('GAME OVER', 12)
    tetriTexte(x = largeurFenetre/2 - xOffset/2, 
          y = hauteurFenetre/2 - 3*sizeSquareGrid - yOffset/2, 
          chaine =  "GAME OVER", 
          taille =  12)

    # score
    tetriTexteCentre(x = largeurFenetre/2, 
                y = hauteurFenetre/2 - 1*sizeSquareGrid,
                chaine="Score:" + str(score),
                taille=11
                )
    
    # on recupere la hauteure et la largeurs du tetriTexte pour les caluls de position du cuseur 

    # retry
    tetriTexteCentre(x = largeurFenetre/2, 
                        y = hauteurFenetre/2 + 1*sizeSquareGrid, 
                        chaine =  option[0], 
                        taille =  10)
    
    xRetryLen, yRetryHight = tailleTetriTexte(option[0], 10)

    # menu
    tetriTexteCentre(x = largeurFenetre/2, 
                        y = hauteurFenetre/2 + 2.5*sizeSquareGrid, 
                        chaine =  option[1], 
                        taille =  10)
    
    xMenuLen, yMenuHight = tailleTetriTexte(option[1], 10)

    # on enregistre toutes les posistions possible du curseur
    # ici 2 (retry et menu) dans une liste
    
    cursorPoseLst = [
        # tuple contenant ax, ay, bx, by pour le retry
        (
            largeurFenetre/2 - xRetryLen/2 - 1.2*sizeSquareGrid, 
            hauteurFenetre/2 + 1*sizeSquareGrid + yRetryHight/2
         ), 
         # meme chose pour le menu
         (
            largeurFenetre/2 - xMenuLen/2 - 1.2*sizeSquareGrid, 
            hauteurFenetre/2 + 2.5*sizeSquareGrid + yMenuHight/2
        )
        ]

    # on dessine le curseur a la posision par défaut
    drawCurseur(cursorPoseLst[select][0], cursorPoseLst[select][1], polyLst[randrange(0, len(polyLst))][randrange(4)])

    
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

                    
                
                # touche du haut 
                elif key == 'Up':

                    if select == 0:
                        select = 1
                    else:
                        select -= 1


                    efface("Curseur")
                    drawCurseur(cursorPoseLst[select][0], cursorPoseLst[select][1], polyLst[randrange(0, len(polyLst))][randrange(4)])                
                

                # touche entrer
                elif key == 'Return':
                    return option[select]
                


def rectangleOmbre(ax, ay, bx, by, offsetOmbre, colRemplissage, colBordure = "", colOmbre = "gray",epaisseur = 1):
    """dessine 2 rectangle de façon a voire l'ombre du rectangle"""
    
    # ombre
    rectangle(ax - offsetOmbre, ay + offsetOmbre, bx - offsetOmbre, by + offsetOmbre, colOmbre , colOmbre)
    
    # le rectangle par dessus
    rectangle(ax, ay, bx, by, colBordure, colRemplissage, epaisseur)



def tetriTexteCentre(x, y, chaine, couleur = "black", taille = 24):
    """dessine un tetriTexte centré sur x et y"""

    # on centre le tetriTexte sur x et y
    xOffset, yOffset = tailleTetriTexte(chaine=chaine, taille=taille)
    return tetriTexte(x = x - xOffset/2, y = y - yOffset/2, chaine = chaine, couleur = couleur, taille = taille)


def drawCurseur (x, y, poly ) : 
    #largeur d'un carré du curseur 
    largeurCarreCurseur=10
    
    #on va dessiner le polyomino grâce à une boucle for pour les colonnes et les lignes 
    for i in range(len(poly)):
        for j in range(len(poly[0])) : 
            
            #Si le coefficient ij de la matrice vaut 0, alors on dessine un carre transparent 
            if poly[i][j]==0 : 
                pass
            #Si le coefficient ij de la matrice vaut 1, alors on dessine un carre de la couleur choisie 
            elif poly[i][j]!=0 :
                rectangle((i*largeurCarreCurseur)+x, (j*largeurCarreCurseur)+y, x+((i+1)*largeurCarreCurseur), y+((j+1)*largeurCarreCurseur), "black", squareColors[poly[i][j]], 3, "Curseur") 

if __name__ == "__main__":
    ## on charge la police d'écriture style rétro

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

    # génération des couleurs pour chaque poly 
    squareColors = genColorRGBLst(len(polyLst))


    main()