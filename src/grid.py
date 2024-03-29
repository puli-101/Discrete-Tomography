import datetime
import os
import moviepy.video.io.ImageSequenceClip
import cv2
from enum import Enum
import src.debugging as db

class Color(Enum):
    WHITE = 1
    BLACK = 2
    UNCOLORED = 3 

    def __str__(self):
        """
            toString()
        """
        if self.value == 1:
            return "Color(white)"
        elif self.value == 2:
            return "Color(black)"
        else:
            return "Color(uncolored)"

class Grid:
    def __init__(self, n_lignes, m_colonnes, contrainte_l = None, contrainte_c = None, name="Grid 1"):
        """
            Initialisation de l'objet Grid
        """
        if (contrainte_c == None):
            contrainte_c = [[]]*m_colonnes
        if (contrainte_l == None):
            contrainte_l = [[]]*n_lignes
        self.name = name
        self.n_lignes =  n_lignes
        self.m_colonnes = m_colonnes
        self.contrainte_c = contrainte_c.copy() #liste de listes
        self.contrainte_l = contrainte_l.copy() #liste de listes
        #initialisation d'une grille vide (avec des 0)
        self.grid = []
        for i in range(n_lignes):
            self.grid.append([Color.UNCOLORED] * m_colonnes)
    
    def print_dash(self):
        """
            Affichage d'une ligne de '-'
        """
        for j in range(0, self.m_colonnes*4+1):
            print("-",end="")
        print()

    def print_line(self, i):
        """
            affichage d'une ligne
        """
        #print("|",end="")
        for j in range(0,self.m_colonnes):
            if (self.grid[i][j] == Color.WHITE):
                print("██",end="")
            elif (self.grid[i][j] == Color.BLACK):
                print("░░",end="")
            else:
                print("??",end="")
        print()

    def print_grid(self, show_constraints=False):
        """
            Affichage ligne par ligne de la grille
        """
        print(self.name+":")
        #self.print_dash()
        for i in range(0,self.n_lignes):
            self.print_line(i)
            #self.print_dash()
        if show_constraints:
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
                int_line = []
                for x in line.split(' '):
                    if x != '':
                        int_line.append(int(x))
                constraints.append(int_line)

        n = len(line_constraints)
        m = len(column_constraints)
        return Grid(n,m,line_constraints,column_constraints)
    
    def save_grid(self, name="", comment="", openFile=False,dialate=True,png=False):
        """
            Methode pour transformer la grille actuelle en image
            de taille n * m

            openFile=True : ouvre le fichier name apres l'avoir cree
            png=True : on reemplace le fichier pgm cree par un fichier png
        """
        if name == "":
            #generation d'un nom 
            name = "output/grid_"+str(len(os.listdir("output")))+".pgm"
        f = open(name, "w")
        dialation = 1
        
        if dialate:
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
                        #black
                        color = "0"
                        #gray (uncolored)
                        if (self.grid[i][j] == Color.UNCOLORED):
                            color = "1"
                        #white
                        elif (self.grid[i][j] == Color.WHITE):
                            color = "2"
                        f.write(color+" ")
                f.write("\n")
        f.close()

        if png:
            new_name = name.removesuffix(".pgm")+".png"
            os.system("convert "+name+" "+new_name)
            name = new_name
        if openFile:
            os.system("open "+name+" 2> /dev/null")
    
    @staticmethod
    def save_video():
        """
            Generation d'une video a partir d'une suite d'images
            stockes dans output/

            Output format: .avi
        """
        fps = 10

        image_folder = "output"
        files = [file for file in os.listdir(image_folder) if ("target" not in file)]
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
        elif n_files > 1000:
            fps = 24 * (n_files//1000)

        images = [img for img in files if img.endswith(".pgm")]
        frame = cv2.imread(os.path.join(image_folder, images[0]))
        height, width, layers = frame.shape
        video = cv2.VideoWriter(video_name, 0, fps, (width,height))

        images.sort(key=lambda nm: int(nm.removeprefix("grid_").removesuffix(".pgm")) )
        print("Loading images...")
        for image in images:
            #print(image)
            video.write(cv2.imread(os.path.join(image_folder, image)))

        cv2.destroyAllWindows()
        video.release()

        return video_name
    
    def deepcopy(self):
        G = Grid(self.n_lignes, self.m_colonnes,self.contrainte_l,self.contrainte_c)
        for i in range(0,self.n_lignes):
            for j in range(0,self.m_colonnes):
                G.grid[i][j] = self.grid[i][j]
        return G 
    
    def print_txt(self):
        f = open("output/output.txt", "w")
        for line in self.grid:
            for c in line:
                if c == Color.WHITE:
                    f.write("██")
                elif c == Color.BLACK:
                    f.write("░░")
                else:
                    f.write("??")
            f.write("\n")
        f.write(str(self.m_colonnes)+" "+str(self.n_lignes)+"\n")
        f.write(str(self.contrainte_l)+"\n")
        f.write(str(self.contrainte_c)+"\n")
        f.close()
    
    def reset(self):
        for i in range(0,self.n_lignes):
            for j in range(0,self.m_colonnes):
                self.grid[i][j] = Color.UNCOLORED