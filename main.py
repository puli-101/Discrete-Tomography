from grid import *
from algorithms import *
import os

if __name__ == "__main__":
    #initialisation de l'environement
    os.system("mkdir -p output/")
    #grille dans l'enonce
    G = Grid.read_file("instances/0.txt")
    solver = Solver(G)

    solver.coloration(G, G.n_lignes, G.m_colonnes)
    
    

    
    G.print_grid()



    #G.save_grid()
    #Grid.save_video()