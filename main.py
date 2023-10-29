from grid import *
from algorithms import *
import os

if __name__ == "__main__":
    #initialisation de l'environement
    os.system("mkdir -p output/")
    #grille dans l'enonce
    G = Grid.read_file("instances/0.txt")
    solver = Solver(G)
    G.print_grid()

    ok,G2 = solver.coloration(G, G.n_lignes, G.m_colonnes)
    
    #T = {}
    #G.grid[2][0] = Color.BLACK
    #print(solver.line_is_colorable_generalized(G.grid[2],T,4,3,G.contrainte_l[2]))

    if ok != False:
        G2.print_grid()
    else:
        print("No solution")


    #G.save_grid()
    #Grid.save_video()