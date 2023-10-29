from grid import *
import logging, sys

DEBUG = False
GRAPHICS_DEBUG = False

def log(msg='', end='\n',override=False):
    msg = str(msg)
    if DEBUG or override:
        log(msg,end=end)

def graph_debug(G):
    if GRAPHICS_DEBUG:
        G.save_grid()

class Solver:
    def __init__(self, grid=None):
        if grid == None:
            grid = Grid.read_file("instances/1.txt")
        self.G = grid
        self.n = grid.n_lignes #access plus directe
        self.m = grid.m_colonnes

    def line_is_colorable(self, T, j, l, s):
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

            blanche = noire = False
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
        log((j,l))
        if l == 0:
            log("Case 0 ! No more blocks to place")
            #we dont have to place any block -> OK
            T[j,l] = True 
        elif j < s[l - 1] - 1: 
            log("Case 1 ! Bigger block than space available")
            #we're trying to place a block bigger than the space we have available
            T[j,l] = False
        elif j == s[l - 1] - 1:
            log("Case 3 ! Current available size matches block")
            #if the current available size (j+1) matches the size of the last block of the sequence
            #then we can color the line only if that's the only block in the sequence (i.e. l == 0)
            T[j,l] = (l == 1)
            #and the rest of the segment hasn't been colored differently
            for k in range(0,j+1):
                T[j,l] = T[j,l] and (line[k] != Color.WHITE)
            log("-> "+str(T[j,l]))
        elif j > s[l - 1] - 1:
            log("Case 4 ! Block may fit with extra space")
            white = noire = False
            #CAS 1 Soit la case est blanche ou elle est incolore et on teste si on peut colorier en blanc
            if line[j] != Color.BLACK:
                log("Is not black")
                if (j-1,l) in T.keys(): 
                    white = T[j-1,l]
                else: 
                    T[j-1,l] = white = (j - 1 >= 0) and self.line_is_colorable_generalized(line,T,j-1,l,s)
                    log("return"+str((j,l)))
            #CAS 2 Soit elle est noire ou elle est incolore et on teste si on peut colorier en noir
            if line[j] != Color.WHITE:
                log("Is not white")
                if (j - s[l-1] - 1, l-1) in T.keys():
                    noire = T[(j - s[l-1] - 1, l-1)]
                else:
                    #on teste si on peut placer le dernier block
                    enough_space = True 
                    for k in range(j - s[l-1] + 1, j+1):
                        log(str(k),end=" ")
                        enough_space = enough_space and (line[k] != Color.WHITE)
                    log()
                    log("Enough space? "+str(enough_space))
                    enough_space = enough_space and (line[j - s[l-1]] != Color.BLACK) #on ne peut pas avoir 2 blocks contigus
                    #si on a assez de place alors on teste si on peut placer les autres blocks aussi
                    if enough_space:
                        log("Enough space!")
                        T[(j - s[l-1] - 1, l-1)] = (j - s[l-1] - 1 >= 0) and self.line_is_colorable_generalized(line,T,j - s[l-1] - 1,l-1,s)
                    else:
                        log("Not Enough space !")
                    noire = enough_space and T[(j - s[l-1] - 1, l-1)]
            T[j,l] = white or noire 
        return T[j,l]
    
    @staticmethod
    def check(G):
        """
            Determine si on a colorie completement une grille
        """
        for line in G.grid:
            for cell in line:
                if cell == Color.UNCOLORED:
                    return False
        return True

    def colorier(self,lst,constraints):
        ok = True
        modif = []
        log(constraints)
        log(lst)
        for i in range(0, len(lst)):
            if lst[i] != Color.UNCOLORED:
                continue
            #check if we can color black
            lst[i] = Color.BLACK
            T = {} 
            black = self.line_is_colorable_generalized(lst,T, len(lst) - 1, len(constraints), constraints)
            #check if we can color white
            lst[i] = Color.WHITE
            T = {} 
            white = self.line_is_colorable_generalized(lst,T, len(lst) - 1, len(constraints), constraints)
            if white and black:
                log("No info")
                lst[i] = Color.UNCOLORED
                continue
            elif white and not(black):
                log("White")
                lst[i] = Color.WHITE
                modif.append(i)
            elif black and not(white):
                log("Black")
                lst[i] = Color.BLACK 
                modif.append(i)
            else:
                log("Nono")
                log("!!!! - ",lst)
                return False,[]
        log(lst)
        return True,modif


    def colorierLig(self, G, i):
        line = G.grid[i]
        constraints = G.contrainte_l[i]
        return self.colorier(line,constraints)
    
    def colorierCol(self, G, j):
        colonne = [line[j] for line in G.grid]
        constraints = G.contrainte_c[j]
        return self.colorier(line,constraints)

    def coloration(self, G, n, m):
        """
            Retourne 
            - True, G' 
                si on peut colorier le graphe G entierement et on retourne le resultat G'
            - None, G'
                si on peut colorier partiellement G (on obtient donc G')
            - False, None
                si on ne peut pas colorier partiellement G
        """
        G2 = G.deepcopy()
        lignesAVoir = range(0,n)
        colonnesAVoir = [] #range(0,m)

        while len(lignesAVoir) > 0: #or len(colonnesAVoir) > 0:
            for i in lignesAVoir:
                (ok,nouveaux) = self.colorierLig(G2,i) #Colorie par r´ecurrence un max de cases de la ligne i de G2
                #ok=Faux si d´etection d’impossibilit´e, ok=Vrai sinon 
                if not(ok):
                    return (False,None)
                colonnesAVoir += nouveaux
            lignesAVoir = []
            #for j in colonnesAVoir:
            #    (ok,nouveaux) = self.colorierCol(G2,j)
            #    if not(ok):
            #        return (False,None)
            #    lignesAVoir += nouveaux
            #colonnesAVoir = []

        ok = self.check(G2)
        #si on a colorie tous les cases (check) alors OK = TRUE
        if (ok):
            return (True,G2)
        else:
            #sinon alors on a une coloration partielle
            return (None,G2)
