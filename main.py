from grid import *
from algorithms import *
import debugging as db
import sys
import os

if __name__ == "__main__":
    inpt = 'instances/0.txt'

    if len(sys.argv) > 1:
        for option in sys.argv[1:]:
            option = option.lower()
            if option == "mkvid":
                Grid.save_video()
                exit()
            elif option == "debug=true":
                db.DEBUG = True 
            elif option == "img_debug=true":
                db.GRAPHICS_DEBUG = True 
            elif option == "color_printing=true":
                db.COLOR_PRINTING = True
            elif option.startswith("input="):
                inpt = option.removeprefix("input=")

    #initialisation de l'environement
    os.system("mkdir -p output/")

    #Chargement_d'une grille
    G = Grid.read_file(inpt)
    solver = Solver(G)
    G.print_grid()

    ok,G2 = solver.coloration(G, G.n_lignes, G.m_colonnes)

    if ok != False:
        G2.print_grid()
    else:
        print("No solution")

    if db.GRAPHICS_DEBUG:
        Grid.save_video()