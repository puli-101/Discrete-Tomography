import datetime
import os

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
    
    def save_grid(self, name="", comment=""):
        """
            Methode pour transformer la grille actuelle en image
            de taille n * m
        """
        if name == "":
            #generation d'un nom aleatoire
            basename = "output/temp_grid"
            suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
            name = "_".join([basename, suffix])+".bmp"
        f = open(name, "w")
        dialation = 512 // min(self.m_colonnes, self.n_lignes)

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
        os.system("open "+name)