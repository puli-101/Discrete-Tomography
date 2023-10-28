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
            T[j,l] = (l == 1)
        elif j > s[l - 1] - 1:
            #IL FAUT TESTER J > 0

            blanche, noire = False
            #CAS 1 On considere la case comme etant blanche
            if (j-1,l) in T.keys(): 
                blanche = T[j-1,l]
            else: 
                T[j-1,l] = blanche = (j - 1 >= 0) and self.line_is_colorable(T,j-1,l,s)
            #CAS 2 On considere la case comme etant noire
            if (j - s[l-1] - 1, l-1) in T.keys():
                noire = T[(j - s[l-1] - 1, l-1)]
            else:
                T[(j - s[l-1] - 1, l-1)] = (j - s[l-1] - 1 >= 0) and self.line_is_colorable(T,j - s[l-1] - 1,l-1,s)
                noire = T[(j - s[l-1] - 1, l-1)]
            #...
            T[j,l] = blanche or noire 
        return T[j,l]
    
    def line_is_colorable_generalized(self,line, T, j, l, s):
        """
            On considere la i-eme ligne 'line'
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
            T[j,l] = (l == 1)
            #and the rest of the segment hasn't been colored differently
            for k in range(0,j):
                T[j,l] = T[j,l] and (line[k] == Color.UNCOLORED)
        elif j > s[l - 1] - 1:
            white_or_uncolored, noire = False
            #CAS 1 Soit la case est deja colorie soit on considere la case comme etant blanche
            if (j-1,l) in T.keys(): 
                white_or_uncolored = T[j-1,l]
            else: 
                T[j-1,l] = white_or_uncolored = (j - 1 >= 0) and self.line_is_colorable(ligne,T,j-1,l,s)
            #CAS 2 On considere la case comme etant noire
            if (j - s[l-1] - 1, l-1) in T.keys():
                noire = T[(j - s[l-1] - 1, l-1)]
            else:
                #on teste si on peut placer le dernier block
                enough_space = (j - s[l-1] - 1 >= 0)
                for k in range(j - s[l-1], j):
                    enough_space = enough_space and (line[k] == Color.UNCOLORED)
                enough_space = enough_space and (line[j - s[l-1] - 1] != Color.BLACK) #on ne peut pas avoir 2 blocks contigus
                #si on a assez de place alors on teste si on peut placer les autres blocks aussi
                if enough_space:
                    T[(j - s[l-1] - 1, l-1)] = (j - s[l-1] - 1 >= 0) and self.line_is_colorable(ligne,T,j - s[l-1] - 1,l-1,s)

                noire = enough_space and T[(j - s[l-1] - 1, l-1)]
                
            T[j,l] = white_or_uncolored or noire 
        return T[j,l]