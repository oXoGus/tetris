from fltk import *
import time

def main():

    largeurFenetre = 1000
    hauteurFenetre = largeurFenetre
    yMargin = int(0.15*hauteurFenetre)

    # constante
    numYSquare = 20
    numXSquare = 10
    sizeSquareGrid = int(0.65*hauteurFenetre/numYSquare)

    cree_fenetre(largeurFenetre, hauteurFenetre)

    # on definit les variables pour les differentes pièce 
    a = 1
    b = 2
    c = 3
    d = 4
    e = 5
    f = 6
    g = 7
    
    #cadrillage

    yGrid = 0
    xGrid = 0
    for i in range(numYSquare):

        yGrid = hauteurFenetre - yMargin - i* sizeSquareGrid
        for j in range(numXSquare):
                
            xGrid = largeurFenetre/2 - sizeSquareGrid*numXSquare/2 + j*sizeSquareGrid
            rectangle(xGrid, yGrid, xGrid + sizeSquareGrid, yGrid - sizeSquareGrid, "gray",)
                

    # grille dynamique en fonction de la taille de la fenêtre 

    # ligne basse de la grille
    ligne(largeurFenetre/2 - sizeSquareGrid*numXSquare/2, hauteurFenetre - yMargin, largeurFenetre/2 + sizeSquareGrid*numXSquare/2, hauteurFenetre - yMargin, "black", 4)

    #ligne gauche
    ligne(largeurFenetre/2 - sizeSquareGrid*numXSquare/2, hauteurFenetre - yMargin, largeurFenetre/2 - sizeSquareGrid*numXSquare/2, hauteurFenetre - yMargin - sizeSquareGrid*numYSquare, "black", 4)

    #ligne droit
    ligne(largeurFenetre/2 + sizeSquareGrid*numXSquare/2, hauteurFenetre - yMargin, largeurFenetre/2 + sizeSquareGrid*numXSquare/2, hauteurFenetre - yMargin - sizeSquareGrid*numYSquare, "black", 4)
    
    # structure de donnée pour représenter la grille de jeu
    # la grille de jeu fait du 10 par 20 
    # mais comme les pièces apparaissent au dessus des 20 de hauteur 
    # on doit rajouter 4 cases sur les y
    grid = []

    for y in range(numYSquare + 4):
        grid.append([])
        for x in range(numXSquare):
            grid[y].append(0)
        #print(grid[y])
   
    #grid[1][1] = 1

    printGrid(grid)

    while True:
        
        # il faut mettre à jour pour pouvoir afficher le cadrillage et mettre les touches en attente 
        mise_a_jour()


        #### on gère les touches ####
        
        # on enregiste l'évenement en attente le plus ancien
        ev = donne_ev()

        # si aucune touche à été pressé 
        if ev is not None:
            startTime = time.perf_counter()

            key = type_ev(ev)
            

            # si l'utilisateur appuis pour sur la croix ou alt + f4 pour fermer la fenêtre
            if key == 'Quitte':
                ferme_fenetre()
                break
            elif key == 'Touche':
                key = touche(ev)

                # si la touche est utile pour le jeu
                if key == 'space' or key == 'Up' or key == 'Down' or key == 'Right' or key == 'Left':
                    endTime = keyPressed(key=key)
                    print(f"en : {endTime - startTime:0.4f}s")

           
                


            else:
                print(key)
            

def printGrid(grid):
    for y in range(len(grid)):
        print(grid[y])
    return


def keyPressed(key):
    print(key)

    # pour touner la pièce d'1/4 vers la droite
    if key == 'Up':
        return time.perf_counter()

    # pour déplacer la pièce de une case vers la gauche
    if key == 'Left':
        return time.perf_counter()


    # pour déplacer la pièce de une case vers la gauche
    elif key == 'Right':
        return time.perf_counter()

    
    # pour placer intantanément la pièce 
    elif key == 'space':
        return time.perf_counter()


    # 'down' pour baisser la pièce plus rapidement 
    else:
        return time.perf_counter()



                




if __name__ == "__main__":
    main()