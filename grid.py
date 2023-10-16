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