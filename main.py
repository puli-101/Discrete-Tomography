from grid import *
from algorithms import *
import os

if __name__ == "__main__":
    #initialisation de l'environement
    os.system("mkdir -p output/")
    #grille dans l'enonce
    G = Grid.read_file("instances/1.txt")
    solver = Solver(G)

    #Test fonctions avec la grille dans l'enonce
    for i in range(0,G.n_lignes):
        T = {}
        constraints = G.contrainte_l[i]
        res = solver.line_is_colorable(T, G.m_colonnes - 1, len(constraints), constraints)
        print("Line",i,"is colorable")
    
    #Test fonctions avec la grille dans l'enonce
    for i in range(0,G.n_lignes):
        ligne = G.grid[i]
        T = {}
        constraints = G.contrainte_l[i]
        res = solver.line_is_colorable_generalized(ligne,T, G.m_colonnes - 1, len(constraints), constraints)
        print("Line",i,"is colorable (Generalized)")
    

    G.print_grid()



    #G.save_grid()
    #Grid.save_video()

