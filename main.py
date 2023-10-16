from grid import *

def line_is_colorable(ligne, j, l, s):
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

def propagation(G):
    """
        Methode de resolution partiel
        G est une grille
        1 == white
        2 == black
    """
    for i in range(0, G.n_lignes):
        for j in range(0, G.m_colonnes):
            #on ignore les cases deja colories
            if (G.grid[i][j] != 0):
                continue
            l = len(G.contrainte_l[i])
            #on teste si on peut colorier en blanc
            G.grid[i][j] = 1
            white = line_is_colorable(G.grid[i], m_colonnes - 1, l, G.contrainte_l[i])
            
            #on teste si on peut colorier en noir
            G.grid[i][j] = 2
            black = line_is_colorable(G.grid[i], m_colonnes - 1, l, G.contrainte_l[i])

            #si on ne peut pas colorier ni en blanc ni en noir...
            if not(black) and not(white):
                print("PUZZLE N'A PAS DE SOLUTION")
            elif not(black) and white:
                G.grid[i][j] = 1
            elif black and not(white):
                G.grid[i][j] = 2
            #else (black and white) -> on gagne aucune information
            

if __name__ == "__main__":
    #grille dans l'enonce
    G = Grid.read_file("instances/1.txt")
    G.print_grid()

