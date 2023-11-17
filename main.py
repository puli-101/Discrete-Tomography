from src.grid import *
from src.algorithms import *
from src.image import *
import src.debugging as db
import sys
import os
import time

if __name__ == "__main__":
    #option defaults
    inpt = 'instances/0.txt'
    cst_inpt = 'input/omori.pgm'
    custom = False 
    compress = True 
    chunk_size = 13
    chrono = False
    start_time = 0
    partial=False
    exec_time = 0

    if len(sys.argv) > 1:
        #options d'execution
        for option in sys.argv[1:]:
            option = option.lower()

            option_val = option.endswith("true") 
            #permet de creer une video (n'execute pas l'algorithme)
            if option == "mkvid": 
                name = Grid.save_video()
                os.system('make mp4 INPUT='+name)
                os.system('make gif INPUT='+name)
                exit()
            #affiche sur le terminal les etapes d'exec de l'algo
            elif option.startswith("debug="): 
                db.DEBUG = option_val
            #cree des images a chaque etape de l'algorithme de coloration
            elif option.startswith("img_debug="):
                os.system("rm -rf output/*")
                db.GRAPHICS_DEBUG = option_val
            #permet de choisir la grille input
            elif option.startswith("input="):
                inpt = option.removeprefix("input=")
            #permet de choisir une image comme input (et puis on la recolorie)
            elif option.startswith("custom_input="):
                cst_inpt = option.removeprefix("custom_input=")
                custom = True
            #permet de definir la taille des blocks si on decide de compresser l'image input
            elif option.startswith("chunk_size="):
                chunk_size = int(option.removeprefix("chunk_size="))
            #option pour compresser l'image input
            elif option.startswith("compress="):
                compress = option_val
            #option pour chronometrer le temps d'execution du programme
            elif option.startswith("time="):
                chrono = option_val
            #option pour executer uniquement la coloration partielle
            elif option.startswith("partial="):
                partial = option_val
            #option aide
            elif option == "help" or option == "--help" or option == "-help":
                print("Discrete Tomography Image Reconstructor")
                print("Execution:\t\tpython3 main.py [options]")
                print("Options and arguments (and corresponding environment variables):")
                print("debug=true\t\t: Prints on screen logs related to the image reconstruction process")
                print("img_debug=true\t\t: Saves on folder 'output' reconstruction "+
                    "trace and on 'videos' a video version of the image reconstruction process")
                print("input=<PATH>\t\t: Loads the instance of a grid saved at PATH (format .txt)")
                print("custom_input=<PATH>\t: Loads the instance of a grid corresponding to a certain image at PATH")
                print("chunk_size=<NUMBER>\t: States the size of each block in terms of pixels in the image compression process")
                print("compress=true\t\t: Compresses the loaded image to optimize the algorithm")
                print("mkvid\t\t\t: Transforms the reconstruction trace on 'output' to an mp4, avi, and gif video")
                print("time=true\t\t: Returns the execution time on the standard error output")
                print("partial=true\t\t: Executes a partial coloration instead of a full recursive coloration")
                exit()
            else:
                print("Error: unknown option "+option)
                exit(-1)

    #initialisation de l'environement
    os.system("mkdir -p output/")
    
    G = None
    solver = None
    ok = None

    if not(custom):
        #Chargement_d'une grille (.txt)
        G = Grid.read_file(inpt)
    else:
        #chargement d'une image (.png, .jpg, .pgm ...)
        G = Image.to_grid(cst_inpt,compress=compress,chunk_size=chunk_size)
        G.save_grid(name='output/target.pgm')

        G.reset()

    
    G.print_grid()

    start_time = time.time()
    #Execution de l'algorithme de coloration complete
    if not(partial):
        ok,G = Solver.enumeration(G)
    #Execution de l'algorithme de coloration partiel
    else:
        ok,G = Solver.coloration(G)

    #on enregistre le temps d'execution avant de faire les traitement d'images finals
    if chrono:
        exec_time = time.time() - start_time

    if ok != False:
        G.print_grid()
        G.print_txt()
        G.save_grid(name='sample_results/latest_result.pgm', png=True)
    else:
        print("No solution")

    
    #generation de la video
    if db.GRAPHICS_DEBUG:
        name = Grid.save_video()
        if name != None:
            os.system('make mp4 INPUT='+name)
            os.system('make gif INPUT='+name)
    #affichage du temps d'exec
    if chrono:
        print(exec_time, file=sys.stderr)