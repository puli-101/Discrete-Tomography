from grid import *
import os

if __name__ == "__main__":
    #initialisation de l'environement
    os.system("mkdir -p output/")
    #grille dans l'enonce
    G = Grid.read_file("instances/1.txt")
    G.print_grid()
    G.grid[1][1] = 1
    G.grid[2][2] = 2
    G.save_grid()

    Grid.save_video()

