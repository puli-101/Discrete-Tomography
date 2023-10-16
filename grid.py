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
                if (self.grid[i][j] == 0):
                    print("   |",end="")
                else:
                    print(" █ |",end="")
            print()
            self.print_line()
        print("Line constraints:",self.contrainte_l)
        print("Column constraints:",self.contrainte_c)