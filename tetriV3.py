from fltk import *
from tetriFont import *
import time
from random import randrange
from tetriGenPolyArbi import *
from datetime import datetime
from tetriSaves import *
from tetri2players import *
from tetriGenPoly import *
import subprocess
import platform 
from tetrIA import *


#### constantes et variables globales ####

# si la commande marche bien 

if platform.system() == 'Linux':
    # on récumpère la resolution de l'écran en executat la commande `xrandr | grep \\* | cut -d' ' -f4`
    # avec la module subprocess

    resolution = subprocess.Popen("xrandr | grep \\* | cut -d' ' -f4", shell=True, stdout=subprocess.PIPE).communicate()[0]

    #print(resolution)

    # cela renvoie : b'2560x1600\n'

    # le b au début signifit que cette chaine est encodé en UTF-8
    # pour le retirer un faut décoder la chaine de caractère  

    # la methode decode a pour argument par défaut encodage UTF-8
    resolution = resolution[:-1].decode()

    # on obtient bien 2560x1600
    #print(resolution)

    largeurScreen = int(resolution.split('x')[0])

    hauteurScreen = int(resolution.split('x')[1])

# val par défaut 
else:
    largeurScreen = 1920

    hauteurScreen = 1024

largeurFenetre = largeurScreen//2

hauteurFenetre = largeurScreen//2

yMargin = int(0.10*largeurFenetre)

# constante
numYSquare = 20
numXSquare = 10
sizeSquareGrid = int(0.73*hauteurFenetre/numYSquare)

# pièces par défaut

# au début du jeu on génére dans une liste toutes les polyomino de taille n 
# dans une autre liste, a l'index de la piece on insert une autre liste contenant toute les rotation de cette piece
# n =  4 pour le mode de jeu classique 
polyLst = genPolyominoLst(n=4)

# génération des couleurs pour chaque poly 
squareColors = genColorRGBLst(len(polyLst))

def main(settings):
    # initialisation des varible pour le menu
    fermer = 0
    jouer=["Jouer", "Charger une partie", "Quitter"]
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

    # bonus IA
    bonusIA = False

    # bonus élimination par couleurs
    bonusElimCoul = False

    # création de la fenêtre carré 
    cree_fenetre(largeurFenetre, largeurFenetre)


    # choix par défaut est jouer c'es pour cela qu'il est plus gros, pour indiquer qu'il est selectionner
    choix = 0

    # le titre
    xOffset, yOffset = tailleTetriTexte("TETRIS", 50)
    tetriTexte(largeurFenetre*1/2 - xOffset/2, hauteurFenetre*1/4 - yOffset/2 , "TETRIS", 'black', 50) 


    # pour centrer le tetriTexte
    xOffsetJouer, yOffsetJouer = tailleTetriTexte(jouer[0], 18)
    tetriTexte(largeurFenetre*1/2 - xOffsetJouer/2, hauteurFenetre*1/2 - yOffsetJouer/2 - 50, jouer[0], 'black', 18)
    
    # charger une partie
    xOffsetCharger, yOffsetCharger = tailleTetriTexte(jouer[1], 18)
    tetriTexteCentre(largeurFenetre/2, hauteurFenetre/2 - yOffsetJouer/2 + 50, jouer[1], "black", 18)

    # Quitter
    xOffsetQuit, yOffsetQuit = tailleTetriTexte(jouer[2], 18)
    tetriTexte(largeurFenetre*1/2 - xOffsetQuit/2, hauteurFenetre*1/2 - yOffsetQuit/2 + 150, jouer[2], 'black', 18)


    # liste de toutes le coordonnées du curseur a l'index de l'option
    cursorPoseLst = [
        # tuple contenant ax, ay, bx, by pour le 'jouer'
        (
            largeurFenetre/2 - xOffsetJouer/2 - 1*sizeSquareGrid, 
            hauteurFenetre*1/2 - yOffsetJouer/2 - 50 + yOffsetJouer/2
         ), 
         # pour le 'charger une partie'
         (
            largeurFenetre/2 - xOffsetCharger/2 - 1*sizeSquareGrid, 
            hauteurFenetre*1/2 - yOffsetCharger/2 + 50 + yOffsetCharger/2
         ), 
         # pour le 'quitter'
         (
            largeurFenetre/2 - xOffsetQuit/2 - 1*sizeSquareGrid, 
            hauteurFenetre*1/2 - yOffsetQuit/2 + 150 + yOffsetQuit/2
         ), 
        ]

    # curseur 
    drawCurseur(cursorPoseLst[choix][0],cursorPoseLst[choix][1], polyLst[randrange(0, len(polyLst))][randrange(4)])

    # boucle de jeu
    while True: 

        # si le joueur a appuié sur réessayer 
        while flag == 'retry':

            # on relance une partie avec les memes variantes activés
            flag = game(varPtsDiffSelect, varPolyArbitraires, varModePourrisement, bonusIA, bonusElimCoul, settings)

            if flag == 'Quitte':
                return
            else:
                continue
            

        # pour le menu
        if flag == 'menu':

            efface_tout()

            # on redessine tout une fois 
            # le titre
            xOffset, yOffset = tailleTetriTexte("TETRIS", 50)
            tetriTexte(largeurFenetre*1/2 - xOffset/2, hauteurFenetre*1/4 - yOffset/2 , "TETRIS", 'black', 50) 



            # pour centrer le tetriTexte
            xOffsetJouer, yOffsetJouer = tailleTetriTexte(jouer[0], 18)
            tetriTexte(largeurFenetre*1/2 - xOffsetJouer/2, hauteurFenetre*1/2 - yOffsetJouer/2 - 50, jouer[0], 'black', 18)
            
            # charger une partie
            xOffsetCharger, yOffsetCharger = tailleTetriTexte(jouer[1], 18)
            tetriTexteCentre(largeurFenetre/2, hauteurFenetre/2 - yOffsetJouer/2 + 50, jouer[1], "black", 18)

            # Quitter
            xOffsetQuit, yOffsetQuit = tailleTetriTexte(jouer[2], 18)
            tetriTexte(largeurFenetre*1/2 - xOffsetQuit/2, hauteurFenetre*1/2 - yOffsetQuit/2 + 150, jouer[2], 'black', 18)

            # curseur 
            drawCurseur(cursorPoseLst[choix][0],cursorPoseLst[choix][1], polyLst[randrange(0, len(polyLst))][randrange(4)])

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
                return
            
            # si la touche est une touche de clavier
            elif key == 'Touche':
                
                # on enregistre la touche
                key = touche(ev)

                # flèche du bas
                if key=='Down':

                    # on inverse l'état de choix
                    if choix == 2: 
                        choix = 0
                    
                    else : 
                        choix += 1
                        
                # flêche du haut
                elif key=='Up':
                    # on inverse l'état de choix
                    if choix == 0: 
                        choix = 2

                    else : 
                        choix -= 1
                    
                    
                efface("Curseur")
                drawCurseur(cursorPoseLst[choix][0],cursorPoseLst[choix][1], polyLst[randrange(0, len(polyLst))][randrange(4)])

                
                
                # si l'utilisateur appuis sur la touche entrer
                if key == 'Return' : 
                    
                    # le joueur a sélectionné 'charger une partie'
                    if choix == 1:
                        flag = saveMenu()

                        if flag == 'Escape':

                            # on réaffiche le menu
                            flag = 'menu'
                            continue
                        
                        elif flag == 'Quitte':
                            return 
                        
                        # on charge une partie 
                        else:
                            save = flag

                            # on supprime la save
                            deleteSave(save['id'])
                            
                            # détéction des variantes 
                            if 'varModePourrisement' in save['varActiv']:
                                varModePourrisement = True 
                            else:
                                varModePourrisement = False
                            
                            if 'varPtsDiffSelect' in save['varActiv']:
                                varPtsDiffSelect = True
                            else:
                                varPtsDiffSelect = False

                            if 'varPolyArbitraires' in save['varActiv']:
                                varPolyArbitraires = True
                            else:
                                varPolyArbitraires = False 

                            if 'elimCoul' in save['varActiv']:
                                varPolyArbitraires = True
                            else:
                                varPolyArbitraires = False 

                            if 'IA' in save['varActiv']:
                                bonusIA = True
                            else:
                                bonusIA = False
                            

                            # on appel les deux fonction avec la save en param pour récuperer la grille, les couleurs, les poly...
                            if 'varMode2joueurs' in save['varActiv']:
                                flag = gameModeDeuxJoueurs(varPtsDiffSelect, varPolyArbitraires, varModePourrisement, bonusIA, bonusElimCoul, settings, save)

                            else:
                                flag = game(varPtsDiffSelect, varPolyArbitraires, varModePourrisement, bonusIA, bonusElimCoul, settings, save)

                            # la fenêtre est deja fermer on ferme le programme
                            if flag == 'Quitte':
                                return None
                            
                            # pour ne pas refaire la boucle et afficher la selection des variantes
                            if flag == 'retry' or flag == 'menu':
                                continue
                    
                    # si le joueur a selectionné 'jouer'
                    elif choix==0 :

                        # liste contentant les tetriTextes pour les variantes
                        variantes = ["Score en fonction \nde la difficulte", "Polyominos \nArbitraires", "Mode 2 joueurs", "Mode pourrissement"]
                        descriptionVar = ["Score en fonction de la difficulte", "Polyominos arbitraires", "elimination par couleurs adjacentes", "jouer un partie a 2", "des blocks disparaisse", "laissez une IA jouer a votre place"]
                        
                        saisie = 0 
                        
                        # on efface tout l'ancien menu
                        efface_tout()
                        
                        
                        
                        suivant = 0 
                        saisie = 0 
                        
                        # on stoque toues les couleurs selon les saisi possible
                        colSaissieLst = [["black", "light gray", "light gray", "light gray", "light gray", "light gray"], 
                                         ["light gray", "black", "light gray", "light gray", "light gray", "light gray"],
                                         ["light gray", "light gray", "black", "light gray", "light gray", "light gray"],
                                         ["light gray", "light gray", "light gray", "black", "light gray", "light gray"],
                                         ["light gray", "light gray", "light gray", "light gray", "black", "light gray"],
                                         ["light gray", "light gray", "light gray", "light gray", "light gray", "black"],
                                         ]

                        while suivant != 1: 


                            # affichage de la selection des variantes
                            efface_tout()

                            # rectangle encatrant tout les choix
                            rectangleOmbre(largeurFenetre*1/5, hauteurFenetre*1/6 , largeurFenetre*4/5,  hauteurFenetre*4/5, 1*sizeSquareGrid, "white", "black", "gray", 5)


                            # tetriTexte explicatif
                            tetriTexteCentre(largeurFenetre/2, hauteurFenetre*0.22, "choisisez vos variantes", 'black', 14)
                            tetriTexteCentre(largeurFenetre/2, hauteurFenetre*0.27, "avec les fleches", 'black', 14)

                            
                            # case 1
                            xCase1 = largeurFenetre*1/5 + 1*sizeSquareGrid
                            yCase1 = hauteurFenetre/2 - 3*sizeSquareGrid
                            rectangleOmbre(xCase1, yCase1, xCase1 + sizeSquareGrid, yCase1 + sizeSquareGrid, 1/6*sizeSquareGrid, "white", "black", "gray", 5)
                            
                            #case 2
                            xCase2 = largeurFenetre*1/5 + 1*sizeSquareGrid
                            yCase2 = hauteurFenetre/2 
                            rectangleOmbre(xCase2, yCase2, xCase2 + sizeSquareGrid, yCase2 + sizeSquareGrid, 1/6*sizeSquareGrid, "white", "black", "gray", 5)

                            # case 3
                            xCase3 = largeurFenetre*1/5 + 1*sizeSquareGrid
                            yCase3 = hauteurFenetre/2 + 3*sizeSquareGrid
                            rectangleOmbre(xCase3, yCase3, xCase3 + sizeSquareGrid, yCase3 + sizeSquareGrid, 1/6*sizeSquareGrid, "white", "black", "gray", 5)


                            # case 4
                            xCase4 = largeurFenetre/2 
                            yCase4 = hauteurFenetre/2 - 3*sizeSquareGrid
                            rectangleOmbre(xCase4, yCase4, xCase4 + sizeSquareGrid, yCase4 + sizeSquareGrid, 1/6*sizeSquareGrid, "white", "black", "gray", 5)                            
                            
                            
                            # case 5
                            xCase5 = largeurFenetre/2 
                            yCase5 = hauteurFenetre/2 
                            rectangleOmbre(xCase5, yCase5, xCase5 + sizeSquareGrid, yCase5 + sizeSquareGrid, 1/6*sizeSquareGrid, "white", "black", "gray", 5)                                                 
                            
                            # case 6
                            xCase6 = largeurFenetre/2 
                            yCase6 = hauteurFenetre/2 + 3*sizeSquareGrid
                            rectangleOmbre(xCase6, yCase6, xCase6 + sizeSquareGrid, yCase6 + sizeSquareGrid, 1/6*sizeSquareGrid, "white", "black", "gray", 5)                                                 
                            
                                
                            # tetriTextes des variantes a droite de chaque cases
                            
                            textMarginLeft = sizeSquareGrid + 0.2*sizeSquareGrid

                            # case 1
                            tetriTexte(xCase1 + textMarginLeft, yCase1, "Score en fonction", colSaissieLst[saisie][0], 8)
                            tetriTexte(xCase1 + textMarginLeft, yCase1 + 0.70*sizeSquareGrid, "de la difficulte", colSaissieLst[saisie][0], 8)
                            
                            # case 2
                            tetriTexte(xCase2 + textMarginLeft, yCase2, "Polynomios", colSaissieLst[saisie][1], 8)
                            tetriTexte(xCase2 + textMarginLeft, yCase2 + 0.70*sizeSquareGrid, "arbitraire", colSaissieLst[saisie][1], 8)
                            
                            # case 3
                            tetriTexte(xCase3 + textMarginLeft, yCase3, "elimination par", colSaissieLst[saisie][2], 8)
                            tetriTexte(xCase3 + textMarginLeft, yCase3 + 0.70*sizeSquareGrid, "couleurs", colSaissieLst[saisie][2], 8)
                            
                            # case 4
                            tetriTexte(xCase4 + textMarginLeft, yCase4 + 0.2*sizeSquareGrid, "Mode 2 joueurs", colSaissieLst[saisie][3], 8)
                            
                            # case 5
                            tetriTexte(xCase5 + textMarginLeft, yCase5, variantes[3], colSaissieLst[saisie][4], 8)

                            # case 6
                            tetriTexte(xCase6 + textMarginLeft, yCase6 + 0.2*sizeSquareGrid, "IA", colSaissieLst[saisie][5], 8)

                            # tetriTexte de description de la variante
                            tetriTexteCentre(largeurFenetre*1/2, hauteurFenetre*0.73, descriptionVar[saisie], "black", 10)
                            
                            # cases cochés 
                            if varPtsDiffSelect == True : 
                                # on coche la première case
                                ligne(xCase1, yCase1, xCase1 + sizeSquareGrid, yCase1 + sizeSquareGrid, "black", 5)
                                ligne(xCase1 + sizeSquareGrid, yCase1, xCase1, yCase1 + sizeSquareGrid, "black", 5)
                            
                            if varPolyArbitraires==True : 
                                ligne(xCase2, yCase2, xCase2 + sizeSquareGrid, yCase2 + sizeSquareGrid, "black", 5)
                                ligne(xCase2 + sizeSquareGrid, yCase2, xCase2, yCase2 + sizeSquareGrid, "black", 5)

                            if bonusElimCoul == True:
                                ligne(xCase3, yCase3, xCase3 + sizeSquareGrid, yCase3 + sizeSquareGrid, "black", 5)
                                ligne(xCase3 + sizeSquareGrid, yCase3, xCase3, yCase3 + sizeSquareGrid, "black", 5)
                            
                            if varMode2joueurs==True :
                                ligne(xCase4, yCase4, xCase4 + sizeSquareGrid, yCase4 + sizeSquareGrid, "black", 5)
                                ligne(xCase4 + sizeSquareGrid, yCase4, xCase4, yCase4 + sizeSquareGrid, "black", 5)
                            
                            if varModePourrisement==True : 
                                ligne(xCase5, yCase5, xCase5 + sizeSquareGrid, yCase5 + sizeSquareGrid, "black", 5)
                                ligne(xCase5 + sizeSquareGrid, yCase5, xCase5, yCase5 + sizeSquareGrid, "black", 5)
                                 
                            if bonusIA==True : 
                                ligne(xCase6, yCase6, xCase6 + sizeSquareGrid, yCase6 + sizeSquareGrid, "black", 5)
                                ligne(xCase6 + sizeSquareGrid, yCase6, xCase6, yCase6 + sizeSquareGrid, "black", 5)
                                 
                            
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
                                    #print(key)
                                    

                                    if key=='Up' : 

                                        # on change saisie
                                        if saisie == 0: 
                                            saisie = 5
                                        else : 
                                            saisie -= 1

        
                                    elif key=='Down':

                                        # on change la saisie
                                        if saisie == 5: 
                                            saisie = 0 
                                        else : 
                                            saisie += 1
                                        
                                           
                                    elif key=='Return' : 

                                        # gestions des cases cochées, on inverse leurs états si la variante est implémanté  
                                        
                                        if saisie == 0 :    
                                            varPtsDiffSelect = not varPtsDiffSelect 

                                        elif saisie == 1:

                                            # on inverse l'état 
                                            varPolyArbitraires = not varPolyArbitraires
                                        
                                        elif saisie == 2:
                                            bonusElimCoul = not bonusElimCoul
                                    
                                        elif saisie == 3:
                                            varMode2joueurs = not varMode2joueurs

                                        elif saisie == 4:
                                            varModePourrisement = not varModePourrisement

                                        elif saisie == 5:
                                            bonusIA = not bonusIA


                                    elif key=='space' :
                                        
                                        if varMode2joueurs==True : 
                                        
                                            flag = gameModeDeuxJoueurs(varPtsDiffSelect, varPolyArbitraires, varModePourrisement, bonusIA, bonusElimCoul, settings)
                                            
                                            while flag == 'retry':
                                                flag = gameModeDeuxJoueurs(varPtsDiffSelect, varPolyArbitraires, varModePourrisement, bonusIA, bonusElimCoul, settings)
                                        

                                            if flag == 'menu':

                                                ferme_fenetre()

                                                # on recréer une fenêtre de la bonne taille
                                                cree_fenetre(largeurFenetre, largeurFenetre)

                                                continue

                                            
                                        else : 
                                            #  on démare la partie avec les variantes
                                            flag = game(varPtsDiffSelect, varPolyArbitraires, varModePourrisement, bonusIA, bonusElimCoul, settings)

                                            if flag == 'Quitte':
                                                return

                                        # la fenêtre est deja fermer on ferme le programme
                                        if flag == 'Quitte':
                                            return None
                                        
                                        # pour ne pas refaire la boucle et afficher la selection des variantes
                                        if flag == 'retry' or flag == 'menu':
                                            break

                                    # la touche echape
                                    elif key == 'Escape':
                                        
                                        flag = 'menu'
                                        break
                                        
                                        
                    
                        if fermer ==  True:
                            break
                    
                    # Quitter
                    elif choix == 2 : 

                        # on ferme la fenêtre puis arrête le programme
                        ferme_fenetre() 
                        return
 
                        

# Dans la boucle ci dessus, il faut rajouter le tetriTexte description de ce que l'utilisateur doit faire, ainsi que lde la description des modes 
#Activer en fonction les modes 




def game(varPtsDiffSelect, varPolyArbitraires, varModePourrisement, bonusIA, bonusElimCoul, settings, save=None):
    """une partie de tetris
    
    prend en argument les variantes activées
    renvoie un flag pour qui sera traité par le menu
    """

    # on efface le menu
    efface_tout()
    
    # si on ne charge pas une partie 
    if save is None:
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
            polyLst = genPolyominoLst(n=settings['taillePoly'])

            # génération des couleurs pour chaque poly 
            squareColors = genColorRGBLst(len(polyLst))


        # les variables locales, on ne peut pas utiliser de variables globales en les définissant hors de la fonction son accessible qu'en lecture exeption faite au liste 
        pieceActivated = 0

        # on initialise la variable qui va contenir le poly que le joueur va jouer, celui qui apparaitera a la droite de la grille
        nextPoly = None

        # Initialisation du score à 0
        score = 0


    # on récupère tout les éléments de la save
    else:
        grid = save['grid']
        polyLst = save['polyLst']
        squareColors = save['squareColors']
        score = save['score']
        poly = save['poly']
        nextPoly = save['nextPoly']
        x = save['x']
        y = save['y']
        ori = save['ori']

        prevX = x
        prevY = y

        # on efface la pièce active pour la redessiner avec son ombre 
        erasePiece(grid, poly, x, y, ori)

        change = 1

        # calcule du maxY pour placer l'ombre
        maxY = y
        while isPolyMaxY(grid, poly, x, maxY, ori) == False:
            maxY += 1

        if bonusIA:

            # copie profonde de la grille 
            nGrid = list()
            nGrid = [l[:] for l in grid]

            # on trouve les meileur coord pour les 2 poly suivant
            objX, objOri = findBestPolyPlace(nGrid, poly, nextPoly, 4, 1, ori, coefNbLigneSupp=83, coefCasePerdu=19, coefCaseManquantes=165, coefHauteurRect=67)
            mooveLst = genMooveList(x, ori, objX, objOri)


        grid, poly, prevX, prevY, x, y, ori, change, maxY = spawnPiece(grid, poly, ori, change)

        # la pièce est déja activé
        pieceActivated = 1

        desactivateCounter = 0



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

                # on change la couleur du poly...
                col = randrange(1, len(polyLst))
                for polyRota in poly:

                    for i in range(len(polyRota)):
                        for j in range(len(polyRota[0])):
                            
                            if polyRota[i][j] != 0:
                                polyRota[i][j] = col

                # on choisit aléatoirement le prochaine pièce
                nextPoly = polyLst[randrange(0, len(polyLst))]

                # on change la couleur du nextPoly...
                col = randrange(1, len(polyLst))
                for polyRota in nextPoly:

                    for i in range(len(polyRota)):
                        for j in range(len(polyRota[0])):
                            
                            if polyRota[i][j] != 0:
                                polyRota[i][j] = col


            else : 

                if bonusElimCoul:
                    score=suppcolor(grid, score, poly, ori, x, y, varPtsDiffSelect, nbLignesSuppTotale)

                # la pièce suivante devient la pièce active et on génère la pièce suivante 
                poly = nextPoly

                # on choisit aléatoirement la nouvelle pièce 
                nextPoly = polyLst[randrange(0, len(polyLst))]

                # on change la couleur du nextPoly...
                col = randrange(1, len(polyLst))
                for polyRota in nextPoly:

                    for i in range(len(polyRota)):
                        for j in range(len(polyRota[0])):
                            
                            if polyRota[i][j] != 0:
                                polyRota[i][j] = col

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

            
            
                

            if bonusIA:

                 # copie profonde de la grille 
                nGrid = list()
                nGrid = [l[:] for l in grid]

                # on trouve les meileur coord pour les 2 poly suivant
                objX, objOri = findBestPolyPlace(nGrid, poly, nextPoly, x, y, ori, coefNbLigneSupp=83, coefCasePerdu=19, coefCaseManquantes=165, coefHauteurRect=67)
            
                # on fait apparaitre un pièce aléatoirement 
                # avec la fonction spawnPiece() qui prend en argument le numéro de la piece que l'on génère aléatoirement 
                grid, poly, prevX, prevY, x, y, ori, change, maxY = spawnPiece(grid, poly, ori, change)

                mooveLst = genMooveList(x, ori, objX, objOri)

            else:
                # on fait apparaitre un pièce aléatoirement 
                # avec la fonction spawnPiece() qui prend en argument le numéro de la piece que l'on génère aléatoirement 
                grid, poly, prevX, prevY, x, y, ori, change, maxY = spawnPiece(grid, poly, ori, change)


            pieceActivated = 1

            desactivateCounter = 0


            # pour le mode pourrissement 
            if varModePourrisement:
                if time.perf_counter() - globalTimer > temps(nbLignesSuppTotale, settings['vInit']) * 15:
                    pourrissement(grid, polyLst)
                    globalTimer = time.perf_counter()
                    
                    # on affiche le poly supprimé 
                    drawGrid(grid, nextPoly, score, squareColors, niveau=nbLignesSuppTotale//10)


        # timer pour descendre la pièce de une case toute les une secondes
        if timer == 0:
            timer = time.perf_counter()
        
        # variable de difficulté avec la fonction temps()
        if time.perf_counter() - timer > temps(nbLignesSuppTotale, settings['vInit']):
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
            drawGrid(grid, nextPoly, score, squareColors, niveau=nbLignesSuppTotale//10)

            change = 0

        if bonusIA: 
            # on retire la touche a 'actionner'
            moove = mooveLst.pop(0)

            if settings['vIA'] is not None:
                time.sleep(settings['vIA'])

            grid, poly, prevX, prevY, x, y, ori, change, maxY, pieceActivated = keyPressed(moove['key'], grid, poly, prevX, prevY, x, y, ori, change, maxY, pieceActivated, nextPoly, score, squareColors, nbLignesSuppTotale)
            

        #### on gère les touches ####
        
        # on enregiste l'évenement en attente le plus ancien
        ev = donne_ev()
        
        # si une touche  bien été pressé 
        if ev is not None:
            
            key = type_ev(ev)
            
            # si l'utilisateur appuis pour sur la croix ou alt + f4 pour fermer la fenêtre
            if key == 'Quitte':

                # test de sauvegarde automatique
                createSave(polyLst, score, poly, x, y, maxY, ori, grid, squareColors, nextPoly, varPtsDiffSelect, varPolyArbitraires, varModePourrisement, varMode2joueurs = False, bonusIA=bonusIA, bonusElimCoul=bonusElimCoul)
                ferme_fenetre()

                # on met le flag a 'Quitte' pour ne pas refaire le menu
                flag = 'Quitte'
                return flag
                
            elif key == 'Touche':
                key = touche(ev)

                # si la touche est utile pour le jeu
                if (key == 'space' or key == 'Up' or key == 'Down' or key == 'Right' or key == 'Left') and not bonusIA:
                    grid, poly, prevX, prevY, x, y, ori, change, maxY, pieceActivated = keyPressed(key, grid, poly, prevX, prevY, x, y, ori, change, maxY, pieceActivated, nextPoly, score, squareColors, nbLignesSuppTotale)
            
                elif key == 'Escape':
                    flag = menuPause()

                    #print(flag)

                    if flag == 'reprendre':

                        # on met le change a un pour réafficher la grille 
                        change = 1

                    # save&quit
                    else:
                        createSave(polyLst, score, poly, x, y, maxY, ori, grid, squareColors, nextPoly, varPtsDiffSelect, varPolyArbitraires, varModePourrisement, varMode2joueurs = False, bonusIA=bonusIA, bonusElimCoul=bonusElimCoul)
                        ferme_fenetre()
                        
                        return 'Quitte'
         
            else:
                pass
                #print(key)

    # ecran de fin revoie un flag
    return endScreen(score)


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
                    if grid[y + i + 1][x + j] > 0 or grid[y + i + 1][x + j] == -2:
                        return True
                    
                # les case en dessous du poly
                elif i + 1 == len(poly[ori]):

                    # l'index -2 correspond au case rajouté par l'adversaire dans le mode 2 joueurs 
                    if grid[y + i + 1][x + j] > 0 or grid[y + i + 1][x + j] == -2:
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


def temps(nbLignesSuppTotale, vInit):
    """renvoie le temps d'attente avant que la pièce tombe toute seule"""
    
    # courbe de difficulté linéaire

    # on augmente la difficulté toute les 10 lignes supprimé
    nbLignesSuppTotale = nbLignesSuppTotale // 10

    # la difficulté de base est a une seconde
    # on abaisse la difficulté de 0.1 seconde toutes les 10 lignes supprimés

    # on empêche que on renvoie un temps négatif
    if vInit - 0.1*nbLignesSuppTotale > 0:
        return vInit - 0.1*nbLignesSuppTotale 
    else:

        # on renvoie le temps minimum
        return 0.05




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


def drawCurseur (x, y, poly) : 
    #largeur d'un carré du curseur 
    largeurCarreCurseur=10

    ### centrage de curseur sur x et y
    maxX = 0
    for i in range(len(poly)):
        if len(poly[i]) > maxX:
            maxX = len(poly[i])

    x = x - (maxX*largeurCarreCurseur)/2
    y = y + len(poly)*largeurCarreCurseur/2

    #on va dessiner le polyomino grâce à une boucle for pour les colonnes et les lignes 
    for i in range(len(poly)):
        for j in range(len(poly[0])) : 
            
            #Si le coefficient ij de la matrice vaut 0, alors on dessine un carre transparent 
            if poly[i][j]==0 : 
                pass
            #Si le coefficient ij de la matrice vaut 1, alors on dessine un carre de la couleur choisie 
            elif poly[i][j]!=0 :
                rectangle((i*largeurCarreCurseur)+x, (j*largeurCarreCurseur)+y, x+((i+1)*largeurCarreCurseur), y+((j+1)*largeurCarreCurseur), "black", squareColors[poly[i][j]], 3, "Curseur") 




######## fonctions pour le menu pause et sauvegarde ########

def menuPause():
    """menu de pase dans une partie"""
    # la sélection est déja sur l'option retry
    select = 0


    # les deux options qu'a l'utilisateur
    option = ['reprendre', 'sauvegarder', 'et quitter']

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
    xOffset, yOffset = tailleTetriTexte('PAUSE', 14)
    tetriTexte(x = largeurFenetre/2 - xOffset/2, 
          y = hauteurFenetre/2 - 3*sizeSquareGrid - yOffset/2, 
          chaine =  "PAUSE", 
          taille =  14)

    
    # on recupere la hauteure et la largeurs du tetriTexte pour les caluls de position du cuseur 

    # reprendre
    tetriTexteCentre(x = largeurFenetre/2, 
                        y = hauteurFenetre/2 - 0.7*sizeSquareGrid, 
                        chaine =  option[0], 
                        taille =  10)
    
    xReprendreLen, yReprendreHight = tailleTetriTexte(option[0], 10)

    # save
    tetriTexteCentre(x = largeurFenetre/2, 
                        y = hauteurFenetre/2 + 1*sizeSquareGrid, 
                        chaine =  'sauvegarder', 
                        taille =  10)
    
    xSaveLen, ySaveHight = tailleTetriTexte('sauvegarder', 10)
    
    # et quitter
    tetriTexteCentre(x = largeurFenetre/2, 
                        y = hauteurFenetre/2 + 2*sizeSquareGrid, 
                        chaine =  'et quitter', 
                        taille =  10)

 

    # on enregistre toutes les posistions possible du curseur
    # ici 2 (retry et menu) dans une liste
    
    cursorPoseLst = [
        # tuple contenant ax, ay, bx, by pour le retry
        (
            largeurFenetre/2 - xReprendreLen/2 - 1.2*sizeSquareGrid, 
            hauteurFenetre/2 - 0.7*sizeSquareGrid + yReprendreHight/2
         ), 
         # meme chose pour le menu
         (
            largeurFenetre/2 - xReprendreLen/2 - 1.2*sizeSquareGrid, 
            hauteurFenetre/2 + 1.5*sizeSquareGrid
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
                    if option[select] == 'reprendre':
                        return option[select]
                    
                    # save & quit
                    else:
                        return 'save&quit'

                
                elif key == 'Escape' :
                    return option[select]

    


def createSave(polyLst, score, poly, x, y, maxY, ori, grid, squareColors, nextPoly, varPtsDiffSelect, varPolyArbitraires, varModePourrisement, varMode2joueurs, bonusIA, bonusElimCoul):
    """sauvegarde une partie avec la grille, les pièces, les couleurs, le score, le poly (x, y, ori) et le nextpoly"""

    # on supprime l'ombre de la la pièce active pour ne pas a gérer les -1 sur la grid
    erasePiece(grid, poly, x, maxY, ori)

    # on regarde l'identifiant de la dernière partie 
    with open('tetriSave.txt') as f:
        f_save = list(f)
    

    # on ouvre le fichier texte contentant toutes les saves espacé par des \n
    with open('tetriSave.txt', 'a') as f:
        
        # saut de ligne pour diferencier les différentes sauvegarde
        f.write('\n')
        
        saveIdLst = list()
        # identifiant de la sauvegarde unique
        for ligne in f_save:

            # on trouve tout les identifiants des saves
            if ligne.split(":")[0] == 'id':
                saveIdLst.append(int(ligne.split(':')[1]))

        # si il n'y a pas de sauvegarde
        if saveIdLst == []:
            saveId = 0
        
        else:
            saveId = None
            # on trouve l'id qui n'est pas dans saveIdLst le plus petit possible 
            for i in range(max(saveIdLst)+1):

                # si l'id est unique
                if i not in saveIdLst:
                    saveId = i
                    break
            
            # si il n'y a pas d'id disponible entre 0 et le plus grand id
            if saveId == None:
                saveId = max(saveIdLst)+1
        
        # on savegarde l'id au forma id:saveId
        f.write("id:" + str(saveId)+'\n')

        # sauvegarde de la date 
        # on extrait la date
        Date  =str(datetime.now()).split(' ')
        date = Date[0].split('-')
        
        # on remplace les - par des /
        date = date[2]+'/'+date[1]+'/'+date[0]

        # on extrait l'heure
        # on retire les micosecondes
        hours = Date[1].split('.')[0]

        # on retire les secondes
        hours = hours[:-3]

        # on peut recomposer la date de la save
        f.write('date:'+date + ' a ' + hours + '\n')
        
        # sauvegarde du score
        f.write('score:'+str(score)+'\n')

        # sauvegarde du poly actif
        f.write('poly:'+polyLstToStr([poly]))
        
        # sauvegarde des info pour reprendre la partie au même moment de la sauvegarde
        # cords de x et y et l'ori
        f.write('x:'+str(x)+'\n')
        f.write('y:'+str(y)+'\n')
        f.write('ori:'+str(ori)+'\n')

        # nextPoly
        f.write('nextPoly:'+polyLstToStr([nextPoly]))

        # sauvegarde de polyLst
        f.write('polyLst:'+ polyLstToStr(polyLst))

        # sauvegarde des couleurs
        f.write('squareColors:'+lstToStr(squareColors)+'\n')
        
        # sauvegarde de la grille
        f.write('grid:'+polyLstToStr([[grid]]))


        f.write('varActiv:')

        # sauvegardes variantes active
        if varPtsDiffSelect == True:
            f.write('varPtsDiffSelect ')
        
        if varPolyArbitraires == True:
            f.write('varPolyArbitraires ')
        
        if varMode2joueurs == True:
            f.write('varMode2joueurs ')

        if varModePourrisement == True:
            f.write('varModePourrisement ')
        
        if bonusElimCoul:
            f.write('elimCoul ')
        
        if bonusIA:
            f.write('IA ')

        f.write('\n')


def saveMenu():
    """met en forme les donnés de toutes les saves
    et gère la sélection de la sauvegarde a charger 
    """

    
    
    # on récup les données formaté 
    saves = savesDataToDict()
    
    # partie affichage
    efface_tout()

    tetriTexteCentre(largeurFenetre//2, hauteurFenetre*0.1, "sauvegardes", "black", 30)

    saveSelected = 0
    
    # aucune save a montrer
    if saves == []:
        tetriTexteCentre(largeurFenetre//2, hauteurFenetre//2, "aucune sauvegardes a charger", taille=18)

        # on attend que le joueur quitte 

        # gestion des touches 

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

                    # la touche echape
                    if key == 'Escape':
                        
                        return key


    else:
        
        # on montre les info de la première save
        drawSaveData(saves[saveSelected])

        # si si il y a plus d'une save
        if len(saves) > 1:

            # on dessine une fleche de droite
            drawTetriFleche(largeurFenetre*0.9, hauteurFenetre//2 - 2.5*sizeSquareGrid*2/3, sizeSquareGrid*0.3, 'right')


        # gestion des touches 

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

                    # flèche de gauche  
                    if key == 'Left':

                        if saveSelected == 0:
                            saveSelected = 0
                        else:
                            saveSelected -= 1

                            # on affiche la nouvelle save
                            efface_tout()

                            tetriTexteCentre(largeurFenetre//2, hauteurFenetre*0.1, "sauvegardes", "black", 30)

                            drawSaveData(saves[saveSelected])

                            # si on est pas a la derniere save 
                            if saveSelected != 0:

                                # on dessine une fleche de gauche
                                drawTetriFleche(largeurFenetre*0.1 - 6*sizeSquareGrid*0.3, hauteurFenetre//2 - 2.5*sizeSquareGrid*2/3, sizeSquareGrid*0.3, 'left')

                            # on dessine la fleche de droite
                            drawTetriFleche(largeurFenetre*0.9, hauteurFenetre//2 - 2.5*sizeSquareGrid*2/3, sizeSquareGrid*0.3, 'right')
                            
                        
                        
                    
                    # flèche de droite  
                    elif key == 'Right':

                        if saveSelected == len(saves) - 1:
                            saveSelected == len(saves) - 1
                        else:
                            saveSelected += 1 

                            # on affiche la nouvelle save
                            efface_tout()

                            tetriTexteCentre(largeurFenetre//2, hauteurFenetre*0.1, "sauvegardes", "black", 30)
        
                            drawSaveData(saves[saveSelected])

                            # si on est pas a la derniere save 
                            if saveSelected < len(saves) - 1:

                                # on dessine une fleche de droite
                                drawTetriFleche(largeurFenetre*0.9, hauteurFenetre//2 - 2.5*sizeSquareGrid*2/3, sizeSquareGrid*0.3, 'right')

                            # on dessine la fleche de gauche
                            drawTetriFleche(largeurFenetre*0.1 - 6*sizeSquareGrid*0.3, hauteurFenetre//2 - 2.5*sizeSquareGrid*2/3, sizeSquareGrid*0.3, 'left')




                    # touche entrer 
                    elif key == 'space':
                        
                        efface_tout()

                        # on renvoie la save sélectioné
                        return saves[saveSelected]
                    

                    # la touche echape
                    elif key == 'Escape':
                        
                        return key


    

    
        
        

def drawSaveData(save):
    
    # on utilise les memes couleus que pour la partie

    # on dessine la grille a gauche
    drawSaveGrid(save['grid'], sizeSquareGrid*2/3, save['squareColors'])

    # date de la save
    xOffset, yOffset = tailleTetriTexte("Date : " + save['date'].split(' ')[0])
    tetriTexte(largeurFenetre*1/4 + numXSquare/2*sizeSquareGrid*2/3 + sizeSquareGrid*2/3, hauteurFenetre/2 + numYSquare*0.70*sizeSquareGrid*2/3 - sizeSquareGrid*2/3*numYSquare + yOffset//2, "Date : " + save['date'].split(' ')[0], taille=12)

    xOffsetDate, yOffsetDate = tailleTetriTexte("Date : ", 12)
    xOffset, yOffset = tailleTetriTexte('a ' + save['date'].split(' ')[2])
    tetriTexte(largeurFenetre*1/4 + numXSquare/2*sizeSquareGrid*2/3 + sizeSquareGrid*2/3 + xOffsetDate + 0.2*sizeSquareGrid, hauteurFenetre/2 + numYSquare*0.70*sizeSquareGrid*2/3 - sizeSquareGrid*2/3*numYSquare + 3.3*yOffset + yOffsetDate, 'a ' + save['date'].split(' ')[2], taille=12)


    # score
    tetriTexte(largeurFenetre*1/4 + numXSquare/2*sizeSquareGrid*2/3 + sizeSquareGrid*2/3, hauteurFenetre/2 + numYSquare*0.70*sizeSquareGrid*2/3 - sizeSquareGrid*2/3*numYSquare + 3*yOffset + yOffsetDate + 1.3*sizeSquareGrid, "Score : " + str(save['score']), taille=12)


    # varActiv
    tetriTexte(largeurFenetre*1/4 + numXSquare/2*sizeSquareGrid*2/3 + sizeSquareGrid*2/3, hauteurFenetre/2 + numYSquare*0.70*sizeSquareGrid*2/3 - sizeSquareGrid*2/3*numYSquare + 3*yOffset + yOffsetDate + 1.3*sizeSquareGrid + 1.3*sizeSquareGrid, "variantes actives : ", taille=12)

    for i, varActiv in enumerate(save['varActiv']):
        tetriTexte(largeurFenetre*1/4 + numXSquare/2*sizeSquareGrid*2/3 + sizeSquareGrid*2/3, hauteurFenetre/2 + numYSquare*0.70*sizeSquareGrid*2/3 - sizeSquareGrid*2/3*numYSquare + 3*yOffset + yOffsetDate + 3*1.3*sizeSquareGrid + i*1*sizeSquareGrid, varActiv, taille=10)

    # poly utilisés


    # pour charger cette save
    tetriTexteCentre(largeurFenetre//2, hauteurFenetre*0.9, "Appuyer sur espace pour charger cette save", taille=12)





def drawSaveGrid(grid, sizeSquareGrid, squareColors):
    """dssine une version miniature de la grille de jeu 
    spécialement prévu pour l'affichage des données de la save"""

    

    # on reprend la fonction drawGrid mais avec les bonne dimentions et les bonnes 

    yGrid = 0
    xGrid = 0

    thickness = 8

    # ligne basse de la grille
    ligne(largeurFenetre*1/4 - sizeSquareGrid*numXSquare/2 - thickness//2, hauteurFenetre/2 + numYSquare*0.70*sizeSquareGrid, largeurFenetre*1/4 + sizeSquareGrid*numXSquare/2 + thickness//2, hauteurFenetre/2 + numYSquare*0.70*sizeSquareGrid, "black", thickness)

    #ligne de gauche
    ligne(largeurFenetre*1/4 - sizeSquareGrid*numXSquare/2, hauteurFenetre/2 + numYSquare*0.70*sizeSquareGrid - numYSquare*sizeSquareGrid, largeurFenetre*1/4 - sizeSquareGrid*numXSquare/2, hauteurFenetre/2 + numYSquare*0.70*sizeSquareGrid, "black", thickness)

    #ligne de droite
    ligne(largeurFenetre*1/4 + sizeSquareGrid*numXSquare/2, hauteurFenetre/2 + numYSquare*0.70*sizeSquareGrid - numYSquare*sizeSquareGrid, largeurFenetre*1/4 + sizeSquareGrid*numXSquare/2, hauteurFenetre/2 + numYSquare*0.70*sizeSquareGrid, "black", thickness)

    

    # on dessine les case vide pour que les épaisseurs des case des case pleines ne soit 'écrasé' par l'épaisseur de la case vide
    for i in range(len(grid)):

        yGrid = hauteurFenetre/2 + numYSquare*0.70*sizeSquareGrid - sizeSquareGrid*(numYSquare + 4) + i* sizeSquareGrid
        for j in range(len(grid[0])):

             # on enregistre la couleur de la case
            n = grid[i][j]

            xGrid = largeurFenetre*1/4 - sizeSquareGrid*numXSquare/2 + j*sizeSquareGrid

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

        yGrid = hauteurFenetre/2 + numYSquare*0.70*sizeSquareGrid - sizeSquareGrid*(numYSquare + 4) + i* sizeSquareGrid
        for j in range(len(grid[0])):

             # on enregistre la couleur de la case
            n = grid[i][j]

            xGrid = largeurFenetre*1/4 - sizeSquareGrid*numXSquare/2 + j*sizeSquareGrid

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


def suppcolor (grid, score, poly, ori, x, y, varPtsDiffSelect, nbLignesSuppTotale) :
    """Supprimer les pieces lorsqu'elles sont de la même couleur et qu'elles ont au mininum deux points de contact"""
    #on cherche le point de contact à y+len(poly[ori]) soit la fin de 
    
    cmpc=0
    contacts=set()
    piece=set()
    sameColor=set()
    color=0
    for i in range(len(poly[ori])) : 
        for j in range(len(poly[ori][i])): 

            # on ne met pas les case vide 
            if poly[ori][i][j]!=0 : 
                piece.add((y+i,x+j))
                color=grid[y+i][x+j]

            # case de meme couleur a proximité
                for coords in searchGrid(grid, y+i, x+j) : 
                    contacts.add(coords)
    
    nContacte = len(contacts) - len(piece)
    #print(nContacte, "color", grid[y][x])

    if nContacte >1 and color!=0: 

        sameColor=cases_accessibles(grid, y, x, color, sameColor)
        
        for s in sameColor : 

            i=s[0]
            j=s[1]
            grid[i][j]=0
            cmpc+=1


    if varPtsDiffSelect == True:
        return pointsDiffColor(score, cmpc, nbLignesSuppTotale)
    else:
        return pointsColor(score, cmpc)


def pointsColor (score, cmpc) : 
    """Lorsque le nombre de lignes supprimées est égal à une valeur, un certain nombre de points est ajouté"""
    
    #fonction qui va ajouter les points selon le nombre de lignes supprimées 
    score+=cmpc*5
    return score 

def pointsDiffColor(score, cmpc, nbLignesSuppTotale) : 
    """fonction a utiliser quand la variante des points en fonction du niveau est sélectionner"""
    
    # fonction qui va ajouter les points selon le nombre de lignes supprimées 
    # nbLignesSuppTotale//10 représente la difficulté

    # on commence avec une difficulté de 1 pour ne pas avoir de score = 0
    difficulty = 1 + int(nbLignesSuppTotale//10/2)
    score+=cmpc*difficulty
    return score 
        
def searchGrid (grid, i, j) : 
    lst=set()

    lst.add((i, j))

    # en bas 
    if i+1<len(grid) and grid[i+1][j]==grid[i][j] :
        lst.add((i+1, j))

    # en haut
    if i-1>=0 and grid[i-1][j]==grid[i][j] :
        lst.add((i-1, j))

    # a droite
    if j+1<len(grid[i]) and grid[i][j+1]==grid[i][j] :
        lst.add((i, j+1))
        
    # a gauche
    if j-1>=0 and grid[i][j-1]==grid[i][j] :
        lst.add((i, j-1))
        
    return lst
    
def cases_accessibles(M, i, j, color, cases_visitees):

    cases_visitees.add((i, j))

    if j+1<len(M[i]) and M[i][j+1]==color and (i,j+1) not in cases_visitees:
        cases_accessibles(M, i, j+1, color, cases_visitees)
        
    if i+1<len(M) and M[i+1][j]==color and (i+1,j) not in cases_visitees:
        cases_accessibles(M, i+1, j, color, cases_visitees)
        
    if j-1>=0 and j-1<len(M[i]) and M[i][j-1]==color and (i,j-1) not in cases_visitees:
        cases_accessibles(M, i, j-1, color, cases_visitees)
        
    if i-1>=0 and j<len(M[i]) and M[i-1][j]==color and (i-1,j) not in cases_visitees:
        cases_accessibles(M, i-1, j, color, cases_visitees)
    return cases_visitees  


if __name__ == "__main__":
    import argparse

    # gestion des param 
    argparser = argparse.ArgumentParser()

    settings = {
        'vInit': 1,
        'taillePoly': 4,
        'vIA': None
    }

    # on créer les arguments 
    argparser.add_argument('-vInit')
    argparser.add_argument('-taillePoly')
    argparser.add_argument('-vIA')

    arg = argparser.parse_args()

    if arg.vInit is not None:
        settings['vInit'] = float(arg.vInit)

    if arg.taillePoly is not None:
        settings['taillePoly'] = int(arg.taillePoly)

    if arg.vIA is not None:
        settings['vIA'] = float(arg.vIA)

    main(settings)

    



    
    
    