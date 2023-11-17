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

    if len(sys.argv) > 1:
        #options d'execution
        for option in sys.argv[1:]:
            option = option.lower()

            option_val = option.endswith("true") 

            if option == "mkvid":
                name = Grid.save_video()
                os.system('make mp4 INPUT='+name)
                os.system('make gif INPUT='+name)
                exit()
            elif option.startswith("debug="):
                db.DEBUG = option_val
            elif option.startswith("img_debug="):
                os.system("rm -rf output/*")
                db.GRAPHICS_DEBUG = option_val
            elif option.startswith("color_printing="):
                db.COLOR_PRINTING = option_val
            elif option.startswith("input="):
                inpt = option.removeprefix("input=")
            elif option.startswith("custom_input="):
                cst_inpt = option.removeprefix("custom_input=")
                custom = True
            elif option.startswith("chunk_size="):
                chunk_size = int(option.removeprefix("chunk_size="))
            elif option.startswith("compress="):
                compress = option_val
            elif option.startswith("time="):
                chrono = option_val
                start_time = time.time()
            elif option.startswith("partial="):
                partial = option_val
            elif option == "help" or option == "--help" or option == "-help":
                print("Discrete Tomography Image Reconstructor")
                print("Execution:\t\tpython3 main.py [options]")
                print("Options and arguments (and corresponding environment variables):")
                print("debug=true\t\t: Prints on screen logs related to the image reconstruction process")
                print("img_debug=true\t\t: Saves on folder 'output' reconstruction "+
                    "trace and on 'videos' a video version of the image reconstruction process")
                print("input=<PATH>\t\t: Loads the instance of a grid saved at PATH (format .txt)")
                print("custom_input=<PATH>\t: Loads the instance of a grid corresponding to a certain image at PATH (format .pgm)")
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
    ok,G2 = None,None 

    if not(custom):
        #Chargement_d'une grille
        G = Grid.read_file(inpt)
    else:
        #chargement d'une image
        G = Image.to_grid(cst_inpt,compress=compress,chunk_size=chunk_size)
        G.save_grid(name='output/target.pgm')

        G.reset()

    
    G.print_grid()

    #Execution de l'algorithme de coloration complete
    if not(partial):
        ok,G2 = Solver.enumeration(G)
    #Execution de l'algorithme de coloration partiel
    else:
        ok,G2 = Solver.coloration(G,G.n_lignes, G.m_colonnes)

    if ok != False:
        G2.print_grid()
        G2.print_txt()
        G2.save_grid(name='sample_results/latest_result.pgm')
    else:
        print("No solution")

    #affichage du temps d'execution
    if chrono:
        print(time.time() - start_time, file=sys.stderr)
    #generation de la video
    if db.GRAPHICS_DEBUG:
        name = Grid.save_video()
        if name != None:
            os.system('make mp4 INPUT='+name)
            os.system('make gif INPUT='+name)