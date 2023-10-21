import datetime
import os
import moviepy.video.io.ImageSequenceClip
import cv2

class Grid:
    def __init__(self, n_lignes, m_colonnes, contrainte_l = None, contrainte_c = None):
        if (contrainte_c == None):
            contrainte_c = [[]]*m_colonnes
        if (contrainte_l == None):
            contrainte_l = [[]]*n_lignes
        
        self.n_lignes =  n_lignes
        self.m_colonnes = m_colonnes
        self.contrainte_c = contrainte_c #liste de listes
        self.contrainte_l = contrainte_l #liste de listes
        self.grid = []
        for i in range(n_lignes):
            self.grid.append([0] * m_colonnes)
    
    def print_line(self):
        for j in range(0, self.m_colonnes*4+1):
            print("-",end="")
        print()

    def print_grid(self):
        self.print_line()
        for i in range(0,self.n_lignes):
            print("|",end="")
            for j in range(0,self.m_colonnes):
                if (self.grid[i][j] == 1):
                    print(" W |",end="")
                elif (self.grid[i][j] == 2):
                    print(" B |",end="")
                else:
                    print("   |",end="")
            print()
            self.print_line()
        print("Line constraints:",self.contrainte_l)
        print("Column constraints:",self.contrainte_c)
    
    @staticmethod
    def read_file(name):
        """
            Lecture d'un fichier .txt contenant une grille
            Format:
            n1
            n2 
            .. 
            nk
            #
            m1
            m2
            ..
            ml
            representant les contraintes par ligne puis par colonne
            separees par un #
        """
        f = open(name, "r")
        Lines = f.readlines()
        f.close()
        
        line_constraints = []
        column_constraints = []
        #pointeur a la liste que l'on l'ajoute
        constraints = line_constraints

        for line in Lines:
            #on enleve le dernier caractere si c'est un \n
            if (line[-1] == '\n'):
                line = line[:-1]
            if line == "#" and constraints == line_constraints:
                constraints = column_constraints
            elif line == "":
                constraints.append([])
            else:
                constraints.append([int(x) for x in line.split(' ')])

        n = len(line_constraints)
        m = len(column_constraints)
        return Grid(n,m,line_constraints,column_constraints)
    
    def save_grid(self, name="", comment="", openFile=False):
        """
            Methode pour transformer la grille actuelle en image
            de taille n * m
        """
        if name == "":
            #generation d'un nom 
            name = "output/grid_"+str(len(os.listdir("output")))+".bmp"
        f = open(name, "w")
        dialation = max(512 // min(self.m_colonnes, self.n_lignes), 1)

        #header :
        # P2
        # #comment
        # width * height
        # max gray value
        f.write("P2\n#"+comment+"\n")
        f.write(str(self.m_colonnes * dialation)+" ")
        f.write(str(self.n_lignes * dialation)+"\n2\n")

        for i in range(0,self.n_lignes):
            for k1 in range(dialation):
                for j in range(0,self.m_colonnes):
                    for k2 in range(dialation):
                        f.write(str(abs(2 - self.grid[i][j]))+" ")
                f.write("\n")
        f.close()

        if openFile:
            os.system("open "+name)
    
    @staticmethod
    def save_video():
        """
            Generation d'une video a partir d'une suite d'images
            stockes dans output/

            Output format: .avi
        """
        fps = 10

        image_folder = "output"
        files = os.listdir(image_folder)
        n_files = len(files)
        os.system("mkdir -p videos")
        video_name = "videos/video"+str(len(os.listdir("videos")))+".avi"

        #FPS adjustment
        if n_files < 3:
            print("Error: not enough files to generate video") 
            return
        elif n_files < 10: 
            fps = 2
        elif n_files < 50: #ensure video time of 5 seconds
            fps = n_files//5

        images = [img for img in files if img.endswith(".bmp")]
        frame = cv2.imread(os.path.join(image_folder, images[0]))
        height, width, layers = frame.shape
        video = cv2.VideoWriter(video_name, 0, fps, (width,height))

        for image in images:
            video.write(cv2.imread(os.path.join(image_folder, image)))

        cv2.destroyAllWindows()
        video.release()