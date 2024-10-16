## découper le projet en plusieurs parties : 

Nous avons découpé le projet selon les parties suivantes :

1.  Création des éléments graphiques du jeu (grille, formes ...)
2.  Création de l'interaction en les éléments et l'utilisateur
3.  Ajout de la variable difficulté, vitesse ...
4.  Création du menu
5.  Création des variantes de la version de base
6.  Création et ajout des bonus et amélioration
7.  Finalisations globales

## choisir les structures de données que vous allez utiliser : 

Une matrice qui représente la grille

La grille de jeu fait du 10 par 20, mais comme les pièces apparaissent
au dessus des 20 de hauteur, on doit rajouter 4 cases sur les y.


On représentera les différentes pièces sur cette matrice.

Chaque case de la grille est représentée par un 0.

Pour représenter chaque carré d'une certaine pièce on remplacera le zéro
par une variable associée au nom de la pièce (a, b, c, etc... ).

squareColors = \[\"white\", \"red\", \"blue\", \"yellow\", \"green\",
\"orange\", \"pink\", \]

\[

\[0, 0, 0, 0, 0, 0, 0, 0, 0, 0\], \[0, 0, 0, 0, 0, 0, 0, 0, 0, 0\], \[0,
0, 0, 0, 0, 0, 0, 0, 0, 0\], \[0, 0, 0, 0, 0, 0, 0, 0, 0, 0\], \[0, 0,
0, 0, 0, 0, 0, 0, 0, 0\], \[0, 0, 0, 0, 0, 0, 0, 0, 0, 0\], \[0, 0, 0,
0, 0, 0, 0, 0, 0, 0\], \[0, 0, 0, 0, 0, 0, 0, 0, 0, 0\], \[0, 0, 0, 0,
0, 0, 0, 0, 0, 0\], \[0, 0, 0, 0, 0, 0, 0, 0, 0, 0\], \[0, 0, 0, 0, 0,
0, 0, 0, 0, 0\], \[0, 0, 0, 0, 0, 0, 0, 0, 0, 0\], \[0, 0, 0, 0, 0, 0,
0, 0, 0, 0\], \[0, 0, 0, 0, 0, 0, 0, 0, 0, 0\], \[0, 0, 0, 0, 0, 0, 0,
0, 0, 0\], \[0, 0, 0, 0, 0, 0, 0, 0, 0, 0\], \[0, 0, 0, 0, 0, 0, 0, 0,
0, 0\], \[0, 0, 0, 0, 0, 0, 0, 0, 0, 0\], \[0, 0, 0, 0, 0, 0, 0, 0, 0,
0\], \[0, 0, 0, 0, 0, 0, 0, 0, 0, 0\], \[0, 0, 0, 0, 0, 0, 0, 0, 0, 0\],
\[0, 0, 0, 0, 0, 0, 0, 0, 0, 0\], \[0, 0, 0, 0, 0, 0, 0, 0, 0, 0\], \[0,
0, 0, 0, 0, 0, 0, 0, 0, 0\],

\]

## Faire pour chaque partie une esquisse des principales fonctions dont vous aurez besoin : 

## Création des éléments graphiques du jeu (grille, formes ...) 

la fonction drawGrid() qui dessine sur la fenêtre ce qu'il y a dans le
tableau

la fonction drawPiece() qui dessine sur le tableau une pièce si
possible. Si ce n'est pas possible, si on essaye de placer un pixel de
la pièce en dehors de la grille ou sur un pixel occuper on décale cette
pièce (exemple : le cas d'une rotation collée a un coté), mais si la
pièce est bloquée des deux cotés on ne la bouge pas

la fonction piecePreview() qui dessine la piece active lorsqu'elle sera
bloqué par d'autre pièce

# Création de l'interaction en les éléments et l'utilisateur

la fonction main() où l'on met à jour la fenêtre, on gère et enregistre
les touches pressées

une fonction keyPressed() s'occupe d'appeler d'autres fonctions selon
les touches

la fonction rotatePiece() qui tourne la pièce active, on efface la
pièce, change son orientation et redessine la piece

la fonction isOneRowFull() qui renvoie l'index de la premiere ligne
complète en partant du bas.

la fonction deleteRow() qui efface une ligne

la fonction fallRows() qui fait descendre toute les pièces des lignes
qui sont au dessus d'une certaine ligne

la fonction movePieceLeft() qui déplace une pièce vers la gauche
movePieceRight() et movePieceDown() pour la droite et le bas

on peut aussi avoir une fonction isOneSecondPassed() qui renvoie vrai
toute les x secondes qui dépendra de la variable vitesse

la fonction moveDownPieceActivated() qui descend la piece active d'une
case

La fonction dropPiece() qui dessine la pièce active au coordonnées de la
pièce de preview

## Ajout de la variable difficulté, vitesse ... 

La fonction vitesse() permet de contrôler et d'adapter le vitesse de
descente des pièces

une fonction addDifficulty() qui incrémente et renvoie la variable qui
représente la vitesse de chute des pièces

## Création du menu initiale

une fonction menu() qui gèrera toute la logique de sélection du mode de
jeu

## Création des variantes de la version de base

**principales fonctions pour le mode 2 joueurs :**

La fonction updatePlayer() permet de mettre à jour le joueur qui doit
jouer et l'affichage.

**principales fonctions pour la variante points par rapport à la
difficulté**

La fonction drawCompteur() permet de dessiner le compteur des points.

La fonction updateCompteur() permet de mettre à jour le compteur si
besoin.

La fonction showPoints() permet de dessiner le nombre de points.

La fonction getPoints() permet d'aller chercher et d'update le nombre de
points à afficher.

**principales fonctions pour avoir un menu de pause et de pouvoir
sauvgearder**

une fonction save() qui enregistrera la structure de données
représentant la grille de jeu, le nombre de points qu'a le joueur dans
la partie en cours, et l'identifiant de la pièce active

une fonction chargeGame() qui charge les données d'une partie
sauvegardée

une fonction pause() qui affichera le menu de pause en appelant la
fonction showStopMenu() et fera entrer le programme dans une boucle tant
que le joueur n'a quitté le menu de pause en appuyant sur une touche. De
ce menu le joueur pourra aussi revenir au menu principale en appellant
la fonction menu(), en apuyant sur une touche. Le joueur pourra
sauvegarder les données de sa partie en cours depuis ce même menu.

showPauseMenu() qui affiche un menu de pause sur la fenêtre

## Création et ajout des bonus/amélioration

**Bonnus rotation du plateau**

La fonction rotationGrid() permet de dessiner la grille qui fait un
quart de tour vers la droite ou la gauche toutes les x secondes.

La fonction fallPiece() permet de faire tomber les pièces suspendues
lors de la rotation de la grille.

La fonction drawGrid45() permet de dessiner la grille avec la rotation
de 45°.

**Sauvegarde des paramètres**

La fonction dataParameters() permet de créer un fichier qui contient les
paramètres du jeux.

La fonction saveData() permet de modifier dans le fichier des paramètres
les paramètres modifiés par le joueur.

La fonction chargeData() permet de lire les paramètres dans le fichier
et de les réinstaurer dans le jeu.

**Bonus Elimination par couleurs adjacentes**

pour l'élimination des pièces adjacente de meme couleur on a la fonction
deleteCloseColor() qui remplace les case de meme courleur que la piece
active par des 0 dans la grille de jeu

**bonnus IA**

utilisation du module PyAutoGUI pour que l'IA interagisse avec le jeu en
appuyant virtuellement sur les touches, si toute fois ce module est

le restant des fonctions pour implémenter l'IA ne conseptualisé

## Finalisations globales

## l'organisation du travail en équipe, ainsi que la répartition prévisionnelle des tâches. 
Plateformes utilisées pour permettre le travail d'équipe : Notion,
notamment pour les parties textuelles de ce projet, Github, pour le
code. Nous avons décidé pour ce projet de nous répartir les tâches par
fonctions.

Organisation et répartition des tâches :

Prévision détaillée du jeu de base :

| fonction                 | Giglioni Maëllys | Dintrat Mathis | Non individuel |
|--------------------------|-----|-----|-----|
| main()                   |     |     | X   |
| keypressed()             |     | x   |     |
| drawGrid()               |     | x   |     |
| drawPiece()              |     | x   |     |
| rotatePiece()            |     | x   |     |
| isOneRowFull()           | X   |     |     |
| deleteRow()              | X   |     |     |
| fallRows()               | X   |     |     |
| movePieceLeft()          | X   |     |     |
| movePieceRight()         | X   |     |     |
| movePieceDown()          | X   |     |     |
| movePieceDownActivated() | X   |     |     |
| isOneSecondPassed()      | X   |     |     |
| PiecePreview()           | X   |     |     |
| dropPiece()              | X   |     |     |
| SpawnPiece()             |     | x   |     |
| drawPieceA()             |     | x   |     |
| drawPieceB()             |     | x   |     |
| deletepiece()            |     | x   |     |
| drawPieceC()             |     | X   |     |
| drawPieceD()             |     | X   |     |
| drawPieceE()             | X   |     |     |
| drawPieceF()             | X   |     |     |
| drawPieceG()             | X   |     |     |

Prévision globale des ajouts aux jeux : (cette liste n'est ni exhaustive
ni définitive)

|            fonction                                                                        |  Giglioni Maëllys   |  Dintrat Mathis   |  Non individuel   |
|------------------------------------------------------------------------------------|-----|-----|-----|
| Variable difficulté                                                                |     | X   |     |
| Variable vitesse                                                                   | X   |     |     |
| vitesse()                                                                          |     |     |     |
| Création menu                                                                      |     | X   |     |
| Variante Mode 2 joueurs                                                            | X   |     |     |
| création d'une liste contenant les pseudos et les points de chaque joueurs         |     |     |     |
| boucle pour alterner les joueurs                                                   |     |     |     |
| updatePlayers()                                                                    |     |     |     |
| Variante Pause et sauvegarde                                                       |     | X   |     |
| Variante points liés au niveau                                                     | X   |     |     |
| drawCompteur()                                                                     |     |     |     |
| updateCompteur()                                                                   |     |     |     |
| showPoints()                                                                       |     |     |     |
| getPoinst()                                                                        |     |     |     |
| Création Bonus Elimination par couleurs adjacentes                                 |     | X   |     |
| Création Bonus Rotation du plateau                                                 | X   |     |     |
| rotationGrid()                                                                     |     |     |     |
| fallPiece()                                                                        |     |     |     |
| IA                                                                                 |     | X   |     |
| Création Bonus Rotation 45 degrés                                                  | X   |     |     |
| drawGrid45()                                                                       |     |     |     |
| Sauvegarde des paramètres                                                          | X   |     |     |
| saveData()                                                                         |     |     |     |
| chargeData()                                                                       |     |     |     |
| dataParameters()                                                                   |     |     |     |
| Implémentation menu                                                                | X   |     |     |
| Si possibilité de le faire dans les dates limites : Bonus polyominos de taille ≤ n |     |     | X   |
| Si possibilité de le faire dans les dates limites : bloc bonus                     |     |     | X   |
| Finalisation globale                                                               |     |     | X   |
