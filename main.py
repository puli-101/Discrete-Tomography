from grid import *
from algorithms import *
import os

if __name__ == "__main__":
    #initialisation de l'environement
    os.system("mkdir -p output/")
    #grille dans l'enonce
    G = Grid.read_file("instances/0.txt")
    solver = Solver(G)

    #Test fonctions avec la grille dans l'enonce
    for i in range(0,G.n_lignes):
        T = {}
        constraints = G.contrainte_l[i]
        res = solver.line_is_colorable(T, G.m_colonnes - 1, len(constraints), constraints)
        if res:
            print("Line",i,"is colorable")
        else:
            print("Line",i,"is not colorable")
    
    #Test fonctions avec la grille dans l'enonce
    for i in range(0,G.n_lignes):
        G.grid[i][3] = Color.WHITE
        #G.grid[i][2] = Color.WHITE
        ligne = G.grid[i]
        T = {}
        constraints = G.contrainte_l[i]
        print(constraints)
        res = solver.line_is_colorable_generalized(ligne,T, G.m_colonnes - 1, len(constraints), constraints)
        if res:
            print("Line",i,"is colorable (Generalized)")
        else:
            print("Line",i,"is not colorable (Generalized)")
    
    

    
    G.print_grid()



    #G.save_grid()
    #Grid.save_video()