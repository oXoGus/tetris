La variante qui a été implémentée :
    • Points liés au niveau

L’organisation du programme : 
Chronologiquement :
    • génération de toutes les rotations des pièces de taille n
    • génération d’une couleur pour chaque pièce
    • la fonction menu() qui gère tout le menu et qui appelle la fonction game() avec en arguments les variantes sélectionnées.
    • La fonction game() qui renvoie un certain flag selon le choix du joueur à la fin de la partie.

les choix techniques : 
Pour les polyominos, nous les générons tous au début dans toutes les orientations 
pour avoir moins de latence et juste rechercher. 

Ainsi pour une rotation il suffit de rechercher un index. 

Pour ce qui est de la couleur, celle ci est décidée à partir de l'élément de la matrice de la pièce actuelle 
lorsque cet élément est différent de 0. De même pour la police en pixel, 
nous avons généré au début du programme les différentes matrices de toutes les minuscules, majuscules et chiffres 
pour n'avoir plus qu'à les appeler. 

Pour ce qui est de la gestion des touches, 
nous avons décidé de modifier la taille du buffer stockant l'ensemble des touches. 

Nous avons mis la taille de l'ensemble des touches à 1, 
cela nous permet d'avoir une touche à la fois. 

Cela permet de ne pas avoir d'accumulation de touches dans le buffer 
et nous laisse le temps de gérer la touche avant d'en avoir une autre. 

Nous avons d'ailleurs choisi d'utiliser le donne_ev car les autres options provoquent des boucles while, 
ce qui dans notre code n'aurait pas permi de passer à l'action suivante. 

Un autre choix technique a été la plateforme de partage de code. 

Pour nous permettre de coder et d'avancer sur le code sans se marcher sur les pieds, 
nous avons choisi l'application Github. 

Cela nous a permi de ne pas accumuler les fichiers de code sur nos pc 
et de toujours avoir une version du code qui est à jour. 

les éventuels problèmes rencontrés : 
 - Bug sur windows, la fonction genPolyominoLst ne fonctionne pas. 
 - Problème résolu : difficultée pour trouver les conditions selon lesquelles les polyominos pouvaoent être superposés.
 - Problème résolu : génération d'un curseur
 - Problème résolu : impossibilité d'utiliser une police en pixel importée, donc nous en avons créé une. 


