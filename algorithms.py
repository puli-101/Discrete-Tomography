from grid import *

class Solver:
    def __init__(self, grid=None):
        if grid == None:
            grid = Grid.read_file("instances/1.txt")
        self.G = grid
        self.n = grid.n_lignes #access plus directe
        self.m = grid.m_colonnes

    def line_is_colorable(self,ligne, j, l, s):
        """
            On considere la i-eme ligne 
            les j+1 premiers cases de la i-eme ligne
            et les l premiers blocks de s
            T[a,b] = line_is_colorable()
            retour : Vrai si on peut colorier les j+1 premiers cases d'une certaine ligne
                avec les l premiers blocks de s
        """
        v = True
        if l == 0:
            #we dont have to place any block -> OK
            v = True 
        elif j < s[l - 1] - 1: 
            #we're trying to place a block bigger than the space we have available
            v = False
        elif j == s[l - 1] - 1:
            #if the current available size (j+1) matches the size of the last block of the sequence
            #then we can color the line only if that's the only block in the sequence (i.e. l == 0)
            #and there isn't any other block already
            v = l == 0 
            for x in ligne[:j+1]:
                v = v and (x == 0)
        elif j > s[l - 1] - 1:
            #si la case est blanche...
            if ligne[j] == 0:
                #!!!!!!!!!!!!!!!!!!
                v = line_is_colorable(ligne, j - s[l - 1], l - 1, T, s)
            else:
                v = line_is_colorable(ligne, j, )
        return v 
    
