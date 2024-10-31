def supplignes (grid) : 
  #fonction qui va supprimer les lignes remplies dans la grille et qui va renvoyer le nombre de lignes supprimées 
  nb_lignes_supp=0
  #boucle while qui va parcourir les sous listes, soit les lignes de la grille
  while i<= len(grid[][]) :
    #boucle for qui va parcourir les diverses éléments de la lignes et les passer à vide si il n'y a pas de zéro, c'est à dire qu'elle est remplie 
    for i in range(len(grid)) : 
      if 0 not in grid[i] : 
        for j in range(len(grid[i]) : 
          grid[i][j]=0
        nb_lignes_supp+=1
  return nb_lignes_supp ; 
  
compteur = 0 

def points (compteur, nb_lignes_supp) : 
  #fonction qui va ajouter les points selon le nombre de lignes supprimées 
  if nb_lignes_supp==1 : 
    compteur += 40
  elif nb_lignes_supp ==2 : 
    compteur += 100 
  elif nb_lignes_supp == 3 : 
    compteur += 300
  elif nb_lignes_supp == 4 : 
    compteur += 500 
  return compteur ; 

def draw_compteur (compteur) : 
  pass 
