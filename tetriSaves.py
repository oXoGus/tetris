def getSavesData():
    """récupère toutes les données de toutes les saves 
    et les renvoient dans une liste de str contenant 
    toutes les info pour charger la partie"""

    with open('tetriSave.txt') as f:

        # on lit la première ligne qui est vide pour ne pas a avoir a la gerer avec 
        f.readline()


        # liste qui des différentes saves
        savesLst = list()

        # liste des information d'une save
        saveInfoLst = list()

        for ligne in f:
            
            # nouvelle sauvegarde 
            if ligne == '\n':
                
                # on ajoute les donnée de la sauvegarde précédante
                savesLst.append(saveInfoLst)

                # on réinistialise saveInfoLst
                saveInfoLst = []

            else:
                saveInfoLst.append(ligne[:-1])

        # on ajoute la dernière save puisqu'il n'y a pas de saut de ligne a la fin
        if saveInfoLst != []:
            savesLst.append(saveInfoLst)

    return savesLst

def savesDataToDict():  
    """créer une liste de dict avec toutes les donncées bien convertie"""

    savesLst = getSavesData()

    # création des dict pour une meilleur compréhension des données
    savesDictLst = list()
    
    # pour chaque données brutes
    for save in savesLst:

        dicoSave = dict()
        
        # chaque ligne est une donnée du type nomDonné:donné

        # id 
        ligneId = save[0].split(':')
        dicoSave[ligneId[0]] = ligneId[1]

        # date
        ligneDate = save[1].split(':')
        dicoSave[ligneDate[0]] = ligneDate[1] + ':' + ligneDate[2] 

        # score
        ligneScore = save[2].split(':') 

        # tout est en str il faut donc convertir
        dicoSave[ligneScore[0]] = int(ligneScore[1])

        # poly
        lignePoly = save[3].split(':')
        polyStr = lignePoly[1].split(' ')[:-1]
        dicoSave[lignePoly[0]] = polyStrToLst(polyStr)

        # x
        ligneX = save[4].split(':')
        dicoSave[ligneX[0]] = int(ligneX[1])

        # y
        ligneY = save[5].split(':')
        dicoSave[ligneY[0]] = int(ligneY[1])
        
        # ori
        ligneOri = save[6].split(':')
        dicoSave[ligneOri[0]] = int(ligneOri[1])

        # nextPoly
        ligneNextPoly = save[7].split(':')
        nextPolyStr = ligneNextPoly[1].split(' ')[:-1]
        dicoSave[ligneNextPoly[0]] = polyStrToLst(nextPolyStr)

        # polyLst 
        lignePolyLst = save[8].split(':')

        polyLst = list()

        # les rotation des differents poly totale
        polyStr = lignePolyLst[1][:-1].split(' ')

        # on met un pas de 4 puisque la fonction polyStrToLst convertie les matrice 4 par 4

        for k in range(0, len(polyStr), 4):
            
            # les 4 rotations
            polyRotaLst = list()

            for l in range(k, k+4):

                # matrice du poly
                polyMat = list()
               
                # chaque ligne de polyRota est séparé d'un ','
                for i, ligne in enumerate(polyStr[l].split(',')):
                    polyMat.append([])
                    for case in ligne:
                        polyMat[i].append(int(case))
                
                # mat du poly dans la liste des rota du poly
                polyRotaLst.append(polyMat)
                
            # liste des rota du poly dans la liste globale
            polyLst.append(polyRotaLst)

        dicoSave[lignePolyLst[0]] = polyLst

        # colors liste
        ligneSquareCol = save[9].split(':')
        dicoSave[ligneSquareCol[0]] = ligneSquareCol[1][:-1].split(' ')

        # grid 
        ligneGrid = save[10].split(':')

        # on peut utiliser la fonction polyStrToLst pour ocnvertir n'importe quelle matrice
        # a condition que la chaine de la matrice soit dans une liste
        gridStr = ligneGrid[1].split()
        
        dicoSave[ligneGrid[0]] = polyStrToLst(gridStr)[0]

        # les variantes active
        ligneVar = save[11].split(':')
        dicoSave[ligneVar[0]] = ligneVar[1][:-1].split(' ')

        # savegarde des donnée dans la liste des saves
        savesDictLst.append(dicoSave)

    #print(savesDictLst[0])

    return savesDictLst


def polyStrToLst(polyStr):
    """retransforme une chaine de caractère en liste"""

    poly = list()
    
    # chaque rotation du poly est séparé par un ' ' 
    for polyRota in polyStr:
        
        polyRotaLst = list()
        # chaque ligne de polyRota est séparé d'un ','
        for i, ligne in enumerate(polyRota.split(',')):
            polyRotaLst.append([])
            for case in ligne:
                polyRotaLst[i].append(int(case))
        
        poly.append(polyRotaLst)

    return poly

def deleteSave(saveId):
    """supprime une save d'index saveId"""
    
    # on réecrit le fichier a l'indentique sans la save
    saves = getSavesData()

    with open('tetriSave.txt', 'w') as f:
        
        # réecriture
        for save in saves:
            
            # sans la save contenant la saveId
            if save[0] != 'id:'+saveId:

                # saut de ligne
                f.write('\n')

                for ligne in save:
                    f.write(ligne + '\n')


def lstToStr(lst):
    """créer un chaine de carctère contenant tout les lm 
    d'une liste espacé par des espaces"""
    
    s = ''
    for lm in lst:
        s += str(lm)+' '
        
    return s
        

def polyLstToStr(polyLst):
    # on sauvegarde les pièces utilisés
    # format :
    # polyLst:matrice des polyomino ligne par lignes, 
    # chaque lignes est séparé par des ',' et chaque matrice est séparé par un ' '

    
    polyLstTxt = ''
    for poly in polyLst:
        for polyRota in poly:
            for i in range(len(polyRota)):
        
                
                # on colle les chiffre pour pouvoir bien les reconvertir en liste
                for j in range(len(polyRota[0])):
                    polyLstTxt += str(polyRota[i][j])
                
                # nouvelle ligne marqué par une virgule
                # on ne met pas de virgule pour la dernière ligne
                if i != len(polyRota) - 1:
                    polyLstTxt += ','
                                
            # on saute une ligne pour differencier les matrices
            polyLstTxt += ' '
    
    return polyLstTxt + '\n'
