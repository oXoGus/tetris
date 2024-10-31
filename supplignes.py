def supplignes (grid) : 
  nb_lignes_supp=0
  while i<= len(grid[][]) :
    for i in range(len(grid)) : 
      if 0 not in grid[i] : 
        for j in range(len(grid[i]) : 
          grid[i][j]=0
        nb_lignes_supp+=1
  return nb_lignes_supp ; 

def points (nb_lignes_supp) : 
  compteur = 0 
  if nb_lignes_supp==1 : 
    compteur += 40
  elif nb_lignes_supp ==2 : 
    compteur += 100 
  elif nb_lignes_supp == 3 : 
    compteur += 300
  elif nb_lignes_supp == 4 : 
    compteur += 500 
return compteur ; 
