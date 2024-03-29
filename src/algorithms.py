from src.grid import *
from src.debugging import *
import numpy as np

class Solver:
    @staticmethod
    def create_T(j,l):
        """
            Allocation de la matrice T de taille j x l
        """
        T = []
        for i in range(j+1):
            T.append([None] * (l+1))
        return T
    
    @staticmethod
    def line_is_colorable(T, j, l, s):
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
    
    @staticmethod
    def line_is_colorable_generalized(line, T, j, l, s):
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
            #we just have to check that there arent any 'extra' black blocks in the j first cases
            #(in that case we would need at least one extra block)
            ok = True
            for i in range(0,j + 1):
                ok = ok and (line[i] != Color.BLACK)
            T[j][l] = ok 
        elif j < s[l - 1] - 1: 
            #we're trying to place a block bigger than the space we have available
            T[j][l] = False
        elif j == s[l - 1] - 1:
            if T[j][l] != None:
                return T[j][l]
            #if the current available size (j+1) matches the size of the last block of the sequence
            #then we can color the line only if that's the only block in the sequence (i.e. l == 0)
            else:
                T[j][l] = (l == 1)
                #and the rest of the segment hasn't been colored differently
                for k in range(0,j+1):
                    T[j][l] = T[j][l] and (line[k] != Color.WHITE)
        elif j > s[l - 1] - 1:
            white = noire = False
            #CAS 1 Soit la case est blanche ou elle est incolore et on teste si on peut colorier en blanc
            if line[j] != Color.BLACK:
                if T[j-1][l] != None: 
                    white = T[j-1][l]
                else: 
                    T[j-1][l] = white = (j - 1 >= 0) and Solver.line_is_colorable_generalized(line,T,j-1,l,s)
            #CAS 2 Soit elle est noire ou elle est incolore et on teste si on peut colorier en noir
            if not(white) and line[j] != Color.WHITE:
                left_extremum = max(0,j - s[l-1] - 1)
                if T[left_extremum][l-1] != None:
                    noire = T[left_extremum][l-1]
                else:
                    #on teste si on peut placer le dernier block
                    enough_space = True 
                    for k in range(j - s[l-1] + 1, j+1):
                        enough_space = enough_space and (line[k] != Color.WHITE)
                    enough_space = enough_space and (line[j - s[l-1]] != Color.BLACK) #on ne peut pas avoir 2 blocks contigus
                    #si on a assez de place alors on teste si on peut placer les autres blocks aussi
                    if enough_space:
                        T[left_extremum][l-1] = Solver.line_is_colorable_generalized(line,T,left_extremum,l-1,s)
                    noire = enough_space and T[left_extremum][l-1]
            T[j][l] = white or noire 
        return T[j][l]
    
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

    @staticmethod
    def colorier(lst,constraints):
        """
            Coloration d'une liste (ligne ou colonne)
            a partir d'une liste de contraintes
        """
        ok = True
        modif = []
        #on verifie d'abord que la ligne est coloriable 
        #(peut etre on a une coloration partielle initiale incompatible)
        j,l = len(lst) - 1, len(constraints)
        T = Solver.create_T(j,l) 
        if not(Solver.line_is_colorable_generalized(lst, T, j, l, constraints)):
            return False,[]
        for i in range(0, len(lst)):
            if lst[i] != Color.UNCOLORED:
                continue
            #si on n'a pas de contraintes alors immediatement toute la ligne est blanche
            elif len(constraints) == 0:
                lst[i] = Color.WHITE
                modif.append(i)
                continue
            #check if we can color black
            lst[i] = Color.BLACK
            T = Solver.create_T(j,l) 
            black = Solver.line_is_colorable_generalized(lst,T, j, l, constraints)
            #check if we can color white
            lst[i] = Color.WHITE
            T = Solver.create_T(j,l)  
            white = Solver.line_is_colorable_generalized(lst,T, j, l, constraints)
            if white and black:
                lst[i] = Color.UNCOLORED
                continue
            elif white and not(black):
                lst[i] = Color.WHITE
                modif.append(i)
            elif black and not(white):
                lst[i] = Color.BLACK 
                modif.append(i)
            else:
                return False,[]
        return True,modif

    @staticmethod
    def colorierLig(G, i):
        """
            Coloration d'une ligne
        """
        line = G.grid[i].copy()
        constraints = G.contrainte_l[i]

        ok,modif = Solver.colorier(line,constraints)

        #mis a jour de la ligne
        for j in modif:
            G.grid[i][j] = line[j]
            log_img(G)

        return ok,modif
    
    @staticmethod
    def colorierCol(G, j):
        """ 
            Coloration d'une colonne
        """
        colonne = [line[j] for line in G.grid]
        constraints = G.contrainte_c[j]
        ok,modif = Solver.colorier(colonne,constraints)

        #mis a jour de la colonne
        for i in modif:
            G.grid[i][j] = colonne[i]
            log_img(G)
        return ok,modif

    @staticmethod
    def coloration(G,lignesAVoir=[],colonnesAVoir=[]):
        """
            Retourne 
            - True, G' 
                si on peut colorier le graphe G entierement et on retourne le resultat G'
            - None, G'
                si on peut colorier partiellement G (on obtient donc G')
            - False, None
                si on ne peut pas colorier partiellement G
        """
        n = G.n_lignes
        m = G.m_colonnes

        lignesAVoir = list(range(0,n))
        colonnesAVoir = list(range(0,m))
        
        while len(lignesAVoir) > 0 or len(colonnesAVoir) > 0:
            for i in lignesAVoir:
                (ok,nouveaux) = Solver.colorierLig(G,i) #Colorie par r´ecurrence un max de cases de la ligne i de G2
                #ok=Faux si d´etection d’impossibilit´e, ok=Vrai sinon 
                if not(ok):
                    return (False,None)
                colonnesAVoir += nouveaux
            lignesAVoir = []
            for j in colonnesAVoir:
                (ok,nouveaux) = Solver.colorierCol(G,j)
                if not(ok):
                    return (False,None)
                lignesAVoir += nouveaux
            colonnesAVoir = []

        ok = Solver.check(G)
        #si on a colorie tous les cases (check) alors OK = TRUE
        if (ok):
            return (True,G)
        else:
            #sinon alors on a une coloration partielle
            return (None,G)
    
    @staticmethod
    def enumeration(G):
        """
            Debut d'algo de resolution complete
        """
        ok,G = Solver.coloration(G, G.n_lignes, G.m_colonnes)
        if ok == False:
            return (False,None)
        elif ok == True:
            return (True,G)
        else:
            G.print_grid()
            #print("ok=None")
            i,j = Solver.next_coord(G,0,0)
            #print("next_cord")
            ok,res = Solver.enum_rec(G,i,j,Color.WHITE)
            if ok:
                return ok,res 
            return Solver.enum_rec(G,i,j,Color.BLACK)


    @staticmethod
    def next_coord(G,i,j):
        """
            On determine la prochaine case sans colorier de G
            a partir des coordonnees i,j
        """
        x = i
        y = j + 1
        while x < G.n_lignes:
            while y < G.m_colonnes:
                if G.grid[x][y] == Color.UNCOLORED:
                    return x,y
                y += 1
            y = 0
            x += 1
        return x,y

    @staticmethod
    def colorierEtPropager(G,x,y,color):
        """
            Meme fonction que coloration sauf l'initialisation de lignes a voir et colonnes a voir
        """
        G2 = G.deepcopy()
        G2.grid[x][y] = color
        lignesAVoir = [x]
        colonnesAVoir = [y]
        
        while len(lignesAVoir) > 0 or len(colonnesAVoir) > 0:
            for i in lignesAVoir:
                (ok,nouveaux) = Solver.colorierLig(G2,i) 
                if not(ok):
                    return (False,None)
                colonnesAVoir += nouveaux
            lignesAVoir = []
            for j in colonnesAVoir:
                (ok,nouveaux) = Solver.colorierCol(G2,j)
                #print("second ok",ok,nouveaux)
                if not(ok):
                    return (False,None)
                lignesAVoir += nouveaux
                #print(colonnesAVoir,lignesAVoir)
            colonnesAVoir = []

        ok = Solver.check(G2)
        #si on a colorie tous les cases (check) alors OK = TRUE
        if (ok):
            return (True,G2)
        else:
            #print("yeah")
            #sinon alors on a une coloration partielle
            return (None,G2)

    @staticmethod
    def enum_rec(G,i,j,color):
        """
            Algorithme de resolution complet
        """
        n = G.n_lignes
        m = G.m_colonnes

        if j >= m: #saut de ligne si necessaire
            j = 0
            i += 1
        if i >= n: #si on a deja colorie tous les lignes -> OK
            return (True,G) 
        ok,G_partial_col = Solver.colorierEtPropager(G,i,j,color)
        #si apres avoir fait une coloration partielle on une coloration complete -> OK
        if ok == True: 
            return (True,G_partial_col)
        #s'il est impossible de continuer a colorier -> Erreur
        elif ok == False: 
            return (False, None)
        #sinon
        #on trouve la prochaine case sans colorier
        (next_i,next_j) = Solver.next_coord(G_partial_col,i,j) 

        #on essaie de colorier cette case en blanc
        ok,G_res = Solver.enum_rec(G_partial_col, next_i, next_j, Color.WHITE) 
        if ok:
            return (ok, G_res)
        #si on n'a pas reussi on essaie de colorier en noir
        return Solver.enum_rec(G_partial_col, next_i, next_j, Color.BLACK) 
