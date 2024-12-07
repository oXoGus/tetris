from random import randrange
from tetriV2 import erasePiece

def pourrissement (grid, polyLst) : 


    
    # pour tout les poly
    for poly in polyLst:

        # on trouve la longueur max du poly
        # pour chaque rota du poly
        maxLen = 0
        for rota in poly:
            for l in rota:
                if len(l) > maxLen:
                    maxLen = len(l)

        # on compte le nb de case pleines dans le poly
        n = 0
        for i in range(len(poly[0])):
            for j in range(len(poly[0][0])):
                if poly[0][i][j] != 0:
                    n += 1    

        # 50 essaie pour trouvé une correspondance par poly
        for _ in range(50):

            y=randrange(len(grid)-maxLen)
            x=randrange(len(grid[0])-maxLen)

            #Parcours les différentes orientations du polyomino 
            match, ori = verification(grid, poly, y, x, n)

            # toute les case correspondent
            if match == n:   
                erasePiece(grid, poly, x, y, ori)
                return 1
    return 0 



def verification (grid, poly, y, x, n) : 
    
    # nombre de cases qui correspondent
    match=0

    

    #Parcours les différentes orientations du polyomino  
    for ori in range(len(poly)) : 

        # on réinitialise le nb de case qui corespondent
        match = 0

        for i in range(len(poly[ori])):
            for j in range(len(poly[ori][0])):
                
                # pour ne pas prendre les cases vides
                if poly[ori][i][j] != 0:

                    # dès qu'une case correspond
                    if poly[ori][i][j]==grid[y+i][x+j] : 
                        
                        # on incrémente le match
                        match += 1
        

        # on foit qu'on a testé toute les cases
        # si toutes les cases correspondent
        if match == n : 
            return match, ori
    
    # aucun match...
    return 0, None