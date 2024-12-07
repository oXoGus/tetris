from fltk import *

import random, string, math



# liste contenant la matrice de chaque lettre 
# exemple pour obtenire la matrice représentant la lettre :
# tetriFontLst[ord(lettre) - ord(' ')] 
# ord est la code ascii d'un caractère
# le premier code ascii est pour le caractère ' ' 
# donc le - ord(' ') permet d'avoir l'index 0  pour le caractère ' '
# 
#
# table ascii
#  !"#$%&'()*+,-./
# 0123456789:;<=>?
# @ABCDEFGHIJKLMNO
# PQRSTUVWXYZ[\]^_
# `abcdefghijklmno
# pqrstuvwxyz{|}~
    
# les caractères non utilisé seront
# représenté par des matrices vides

# caractère ' '
spMat = [
        [0, 0],
        [0, 0],
        [0, 0],
        [0, 0],
        [0, 0]
    ]


deuxPtsMat = [
        [0, 0, 0],
        [0, 1, 0],
        [0, 0, 0],
        [0, 1, 0],
        [0, 0, 0]
]

# les chiffres de 0 à 9
tetriFontLstNumber = [
    # '0'
    [
        [0, 1, 1, 0],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [0, 1, 1, 0]
    ],
    # '1'
    [
        [0, 0, 1],
        [0, 1, 1],
        [1, 0, 1],
        [0, 0, 1],
        [0, 0, 1]
    ],
    # '2'
    [
        [0, 1, 1, 0],
        [1, 0, 0, 1],
        [0, 0, 1, 0],
        [0, 1, 0, 0],
        [1, 1, 1, 1]
    ],
    # '3'
    [
        [1, 1, 1, 0],
        [0, 0, 0, 1],
        [0, 1, 1, 0],
        [0, 0, 0, 1],
        [1, 1, 1, 0]
    ],
    # '4'
    [
        [1, 0, 1],
        [1, 0, 1],
        [1, 1, 1],
        [0, 0, 1],
        [0, 0, 1]
    ],
    # '5'
    [
        [1, 1, 1, 1],
        [1, 0, 0, 0],
        [1, 1, 1, 1],
        [0, 0, 0, 1],
        [1, 1, 1, 1]
    ],
    # '6'
    [
        [0, 1, 1, 0],
        [1, 0, 0, 0],
        [1, 1, 1, 0],
        [1, 0, 0, 1],
        [0, 1, 1, 0]
    ],
    # '7'
    [
        [1, 1, 1],
        [0, 0, 1],
        [0, 1, 0],
        [0, 1, 0],
        [0, 1, 0]
    ],
    # '8'
    [
        [0, 1, 1, 0],
        [1, 0, 0, 1],
        [0, 1, 1, 0],
        [1, 0, 0, 1],
        [0, 1, 1, 0]
    ],
    # '9'
    [
        [0, 1, 1, 0],
        [1, 0, 0, 1],
        [0, 1, 1, 1],
        [0, 0, 0, 1],
        [0, 1, 1, 0]
    ],
]

# Lettres majuscules de A à Z
tetriFontLstUpper = [
    # 'A'
    [
        [0, 1, 1, 0],
        [1, 0, 0, 1],
        [1, 1, 1, 1],
        [1, 0, 0, 1],
        [1, 0, 0, 1]
    ],
    # 'B'
    [
        [1, 1, 1, 0],
        [1, 0, 0, 1],
        [1, 1, 1, 0],
        [1, 0, 0, 1],
        [1, 1, 1, 0]
    ],
    # 'C'
    [
        [0, 1, 1, 1],
        [1, 0, 0, 0],
        [1, 0, 0, 0],
        [1, 0, 0, 0],
        [0, 1, 1, 1]
    ],
    # 'D'
    [
        [1, 1, 1, 0],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [1, 1, 1, 0]
    ],
    # 'E'
    [
        [1, 1, 1, 1],
        [1, 0, 0, 0],
        [1, 1, 1, 1],
        [1, 0, 0, 0],
        [1, 1, 1, 1]
    ],
    # 'F'
    [
        [1, 1, 1, 1],
        [1, 0, 0, 0],
        [1, 1, 1, 0],
        [1, 0, 0, 0], 
        [1, 0, 0, 0]
    ],
    # 'G'
    [
        [1, 1, 1, 0],
        [1, 0, 0, 0],
        [1, 0, 1, 1],
        [1, 0, 0, 1], 
        [1, 1, 1, 1]
    ],
    # 'H'
    [
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [1, 1, 1, 1],
        [1, 0, 0, 1], 
        [1, 0, 0, 1]
    ],
    # 'I'
    [
        [1, 1, 1],
        [0, 1, 0],
        [0, 1, 0],
        [0, 1, 0], 
        [1, 1, 1]
    ],
    # 'J'
    [
        [0, 1],
        [0, 1],
        [0, 1],
        [0, 1], 
        [1, 0]
    ],
    # 'K'
    [
        [1, 0, 0, 1],
        [1, 0, 1, 0],
        [1, 1, 0, 0],
        [1, 0, 1, 0], 
        [1, 0, 0, 1]
    ],
    # 'L'
    [
        [1, 0, 0],
        [1, 0, 0],
        [1, 0, 0],
        [1, 0, 0], 
        [1, 1, 1]
    ],
    # 'M'
    [
        [1, 0, 0, 0, 1],
        [1, 1, 0, 1, 1],
        [1, 0, 1, 0, 1],
        [1, 0, 0, 0, 1], 
        [1, 0, 0, 0, 1]
    ],
    # 'N'
    [
        [1, 0, 0, 1],
        [1, 1, 0, 1],
        [1, 1, 0, 1],
        [1, 0, 1, 1], 
        [1, 0, 0, 1]
    ],
    # 'O'
    [
        [0, 1, 1, 0],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [1, 0, 0, 1], 
        [0, 1, 1, 0]
    ],
    # 'P'
    [
        [1, 1, 1, 1],
        [1, 0, 0, 1],
        [1, 1, 1, 1],
        [1, 0, 0, 0], 
        [1, 0, 0, 0]
    ],
    # 'Q'
    [
        [0, 1, 1, 0],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [0, 1, 1, 0], 
        [0, 0, 0, 1]
    ],
    # 'R'
    [
        [1, 1, 1, 0],
        [1, 0, 0, 1],
        [1, 1, 1, 0],
        [1, 0, 0, 1], 
        [1, 0, 0, 1]
    ],
    # 'S'
    [
        [0, 1, 1, 1],
        [1, 0, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 0, 1], 
        [1, 1, 1, 0]
    ],
    # 'T'
    [
        [1, 1, 1, 1, 1],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0], 
        [0, 0, 1, 0, 0]
    ],
    # 'U'
    [
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [1, 0, 0, 1], 
        [0, 1, 1, 0]
    ],
    # 'V'
    [
        [1, 0, 1],
        [1, 0, 1],
        [1, 0, 1],
        [1, 0, 1], 
        [0, 1, 0]
    ],
    # 'W'
    [
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 1, 0, 1],
        [1, 1, 0, 1, 1], 
        [1, 0, 0, 0, 1]
    ],
    # 'X'
    [
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [0, 1, 1, 0],
        [1, 0, 0, 1], 
        [1, 0, 0, 1]
    ],
    # 'Y'
    [
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [1, 1, 1, 1],
        [0, 1, 1, 0], 
        [0, 1, 1, 0]
    ],
    # 'Z'
    [
        [1, 1, 1, 1],
        [0, 0, 0, 1],
        [0, 0, 1, 0],
        [0, 1, 0, 0], 
        [1, 1, 1, 1]
    ]
]

# les lettres minuscule
tetriFontLstLower = [
    # a
    [
        [0, 0, 0],
        [0, 1, 1],
        [1, 0, 1],
        [1, 0, 1], 
        [0, 1, 1]
    ],
    # b
    [
        [1, 0, 0],
        [1, 1, 0],
        [1, 1, 1],
        [1, 0, 1], 
        [1, 1, 0]
    ],
    # c
    [
        [0, 0, 0],
        [0, 1, 1],
        [1, 0, 0],
        [1, 0, 0], 
        [0, 1, 1]
    ],
    # d
    [
        [0, 0, 1],
        [0, 1, 1],
        [1, 0, 1],
        [1, 0, 1], 
        [0, 1, 1]
    ],
    # e
    [   
        [0, 0, 0],
        [0, 1, 0],
        [1, 0, 1],
        [1, 1, 1],
        [1, 0, 0], 
        [0, 1, 0]
    ],
    # f
    [
        [0, 1],
        [1, 0],
        [1, 1],
        [1, 0], 
        [1, 0]
    ],
    # g
    [   
        [0, 0, 0],
        [0, 1, 1],
        [1, 0, 1],
        [1, 0, 1],
        [0, 1, 1], 
        [1, 1, 0]
    ],
    # h
    [
        [1, 0, 0],
        [1, 0, 0],
        [1, 1, 1],
        [1, 0, 1], 
        [1, 0, 1]
    ],
    # i
    [
        [1],
        [0],
        [1],
        [1], 
        [1]
    ],
    # j
    [   
        [0, 1],
        [0, 0],
        [0, 1],
        [0, 1],
        [0, 1], 
        [1, 1]
    ],
    # k
    [
        [1, 0, 0],
        [1, 0, 1],
        [1, 1, 0],
        [1, 1, 0], 
        [1, 0, 1]
    ],
    # l
    [
        [1],
        [1],
        [1],
        [1], 
        [1]
    ],
    # m
    [
        [0, 0, 0, 0, 0],
        [1, 1, 1, 1, 0],
        [1, 0, 1, 0, 1], 
        [1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1]
    ],
    # n 
    [
        [0, 0, 0],
        [1, 1, 0],
        [1, 0, 1], 
        [1, 0, 1],
        [1, 0, 1]
    ],
    # o
    [
        [0, 0, 0],
        [0, 1, 0],
        [1, 0, 1],
        [1, 0, 1], 
        [0, 1, 0]
    ],
    # p
    [   
        [0, 0, 0],
        [1, 1, 0],
        [1, 0, 1],
        [1, 0, 1],
        [1, 1, 0],
        [1, 0, 0]
    ],
    # q
    [
        [0, 0, 0],
        [0, 1, 1],
        [1, 0, 1],
        [1, 0, 1],
        [0, 1, 1],
        [0, 0, 1]
    ],
    # r
    [
        [0, 0],
        [1, 1],
        [1, 0],
        [1, 0], 
        [1, 0]
    ],
    # s
    [   
        [0, 0, 0],
        [1, 1, 1],
        [1, 0, 0],
        [0, 0, 1], 
        [1, 1, 1]
    ], 
    # t
    [
        [1, 0],
        [1, 1],
        [1, 0],
        [1, 0], 
        [1, 1]
    ],
    # u
    [
        [0, 0, 0],
        [1, 0, 1],
        [1, 0, 1],
        [1, 0, 1], 
        [0, 1, 1]
    ],
    # v
    [
        [0, 0, 0],
        [1, 0, 1],
        [1, 0, 1],
        [1, 0, 1], 
        [0, 1, 0]
    ],
    # w
    [
        [0, 0, 0, 0, 0],
        [1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1], 
        [0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0]
    ],
    # x
    [
        [0, 0, 0],
        [1, 0, 1],
        [0, 1, 0], 
        [0, 1, 0], 
        [1, 0, 1]
    ],
    # y
    [   
        [0, 0, 0],
        [1, 0, 1],
        [1, 0, 1],
        [1, 0, 1],
        [0, 1, 0], 
        [1, 0, 0]
    ],
    # z
    [
        [0, 0, 0, 0],
        [1, 1, 0, 1],
        [0, 0, 1, 0],
        [0, 1, 0, 0], 
        [1, 0, 1, 1]
    ]
    
]


def tetriTexte(x: float,
        y: float,
        chaine: str,
        couleur: str = "black",
        taille: int = 24,
        tag = 'default'):
    
    """affiche une chaine de caractère donnée en paramètre avec un style pixélisé"""

    # sauvegarde du x initiale
    xInit = x


    # on calcule la taille de la police en fonction de la taille de la fenêtre
    
    # la taille de la fenêtre ou toutes polices on été bien calibré
    sizeSquareGridInit = 1200

    taille = taille*(largeur_fenetre()/sizeSquareGridInit)
    
    # taille de chaque pixel de la lettre
    sizePix = taille//2

    # initailisation de la variable contenant la taille verticale max de la chaine 
    yMax = 0

    # pour chaque lettre de la chaine
    for lettre in chaine:
        
        # si le caractère est un espace
        if lettre == ' ':
            lettreMat = spMat

        # un chiffre
        if lettre in '0123456789':
            lettreMat = tetriFontLstNumber[ord(lettre) - ord('0')]

        # une lettre minuscule
        elif lettre in 'abcdefghijklmnopqrstuvwxyz':
            lettreMat = tetriFontLstLower[ord(lettre) - ord('a')]
        
        # une lettre majuscule
        elif lettre in 'abcdefghijklmnopqrstuvwxyz'.upper():
            lettreMat = tetriFontLstUpper[ord(lettre) - ord('A')]

        elif lettre == ':':
            lettreMat = deuxPtsMat
        
        # si la lettre n'est pas reconnue on la remplace par un espace
        else:
            lettreMat = spMat


        # on dessine la lettre ou posision x y
        drawTetriLettre(x, y, lettreMat, couleur, taille, tag)

        # après avoir dessiné la lettre 
        # on décale la posision de la prochaine lettre 
        # pour avoir un espacement entre les lettres

        # pour l'espacement des lettres on utilise le nombre d'or comme proprtion entre la taille et l'espacement 
        x += len(lettreMat[0])*sizePix + taille*(1/1.6180339887)

        # on trouve la taille y max (les p, q, etc son plus grand pour qu'ils dépassent en bas)
        if len(lettre) > yMax:
            yMax = len(lettre)*sizePix

    # on renvoie les dimention du rectangle pour supprimer le texte
    return (xInit, y, x, y + yMax)
    
def tailleTetriTexte(
        chaine: str,
        taille: int = 24):
    """renvoie la taille x et y d'un texte"""
    x, y = 0, 0


    # on calcule la taille de la police en fonction de la taille de la fenêtre
    
    # la taille de la fenêtre ou toutes polices on été bien calibré
    sizeSquareGridInit = int(0.65*1200/20)

    # taille actuel
    sizeSquareGridActual = int(0.65*largeur_fenetre()/20)

    taille = taille*(sizeSquareGridActual/sizeSquareGridInit)

    # taille de chaque pixel de la lettre
    sizePix = taille//2

    # initailisation de la variable contenant la taille verticale max de la chaine 
    yMax = 0

    # pour chaque lettre de la chaine
    for lettre in chaine:
        


        # un chiffre
        if lettre in '0123456789':
            lettreMat = tetriFontLstNumber[ord(lettre) - ord('0')]

        # une lettre minuscule
        elif lettre in 'abcdefghijklmnopqrstuvwxyz':
            lettreMat = tetriFontLstLower[ord(lettre) - ord('a')]
        
        # une lettre majuscule
        elif lettre in 'abcdefghijklmnopqrstuvwxyz'.upper():
            lettreMat = tetriFontLstUpper[ord(lettre) - ord('A')]

        elif lettre == ':':
            lettreMat = deuxPtsMat
        
        # si la lettre n'est pas reconnue on la remplace par un espace
        else:
            lettreMat = spMat

        # après avoir dessiné la lettre 
        # on décale la posision de la prochaine lettre 
        # pour avoir un espacement entre les lettres

        # pour l'espacement des lettres on utilise le nombre d'or comme proprtion entre la taille et l'espacement 
        x += len(lettreMat[0]) * sizePix + taille*(1/1.6180339887)

        # on trouve la taille y max (les p, q, etc son plus grand pour qu'ils dépassent en bas)
        if len(lettre)*sizePix > yMax:
            yMax = len(lettre)*sizePix

    # on retire l'espacement de la dernière lettre
    return (x - taille*(1/1.6180339887), yMax)

    


def drawTetriLettre(x: float,
        y: float,
        lettreMat: str,
        couleur: str = "black",
        taille: int = 24, 
        tag = 'default'):
    
    sizePix = taille//2

    # on lit la matrice de la lettre
    for i in range(len(lettreMat)):
        for j in range(len(lettreMat[0])):
            
            # pixel plein
            if lettreMat[i][j] == 1:
                rectangle(x + j * sizePix, y + i * sizePix, x + j * sizePix + sizePix, y + i * sizePix + sizePix, couleur, couleur, tag=tag)


if __name__ == "__main__":
    cree_fenetre(900, 800)
    print(largeur_fenetre())

    tetriTexte(100, 50, "0123456789")
    tetriTexte(100, 200, "abcdefghijklmnopqrs", "black", 18)
    tetriTexte(100, 250, "tuvwxyz", "black", 18)

    tetriTexte(100, 300, "ABCDEFGHIJKLMOP", "black", 18)

    xOffset, yOffset = tailleTetriTexte("TETRIS", 30)

    print(xOffset, yOffset)
    tetriTexte(400 - xOffset/2, 400 - yOffset/2, ":", "black", 30)
    

    while True:
        mise_a_jour()
    

    ferme_fenetre()