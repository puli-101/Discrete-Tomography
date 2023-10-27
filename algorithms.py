from grid import *

class Solver:
    def __init__(self, grid=None):
        if grid == None:
            grid = Grid.read_file("instances/1.txt")
        self.G = grid
        self.n = grid.n_lignes #access plus directe
        self.m = grid.m_colonnes

    def line_is_colorable(self,ligne, T, j, l, s):
        """
            On considere la i-eme ligne 
            les j+1 premiers cases de la i-eme ligne
            et les l premiers blocks de s
            T[a,b] = line_is_colorable()
            retour : Vrai si on peut colorier les j+1 premiers cases d'une certaine ligne
                avec les l premiers blocks de s
        """
        if l == 0:
            #we dont have to place any block -> OK
            T[j,l] = True 
        elif j < s[l - 1] - 1: 
            #we're trying to place a block bigger than the space we have available
            T[j,l] = False
        elif j == s[l - 1] - 1:
            #if the current available size (j+1) matches the size of the last block of the sequence
            #then we can color the line only if that's the only block in the sequence (i.e. l == 0)
            #and there isn't any other block already
            T[j,l] = (l == 1)
        elif j > s[l - 1] - 1:
            #IL FAUT TESTER J > 0

            blanche, noire = False
            #CAS 1 On considere la case comme etant blanche
            if (j-1,l) in T.keys(): 
                blanche = T[j-1,l]
            else: 
                T[j-1,l] = blanche = (j - 1 >= 0) and self.line_is_colorable(ligne,T,j-1,l,s)
            #CAS 2 On considere la case comme etant noire
            if (j - s[l-1] - 1, l-1) in T.keys():
                noire = T[(j - s[l-1] - 1, l-1)]
            else:
                T[(j - s[l-1] - 1, l-1)] = (j - s[l-1] - 1 >= 0) and self.line_is_colorable(ligne,T,j - s[l-1] - 1,l-1,s)
                blanche = T[(j - s[l-1] - 1, l-1)]
            #...
            T[j,l] = blanche or noire 
        return T[j,l]
    
