from grid import *

def line_is_colorable(ligne, j, l, T, s):
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
        v = l == 0
    elif j > s[l - 1] - 1:
        #si la case est blanche...
        if ligne[j] == 0:
            #!!!!!!!!!!!!!!!!!!
            V = line_is_colorable(ligne, j - s[l - 1], l - 1, T, s)
        else:
            #d'apres l'enonce si la case est noire alors
            #le dernier block de longueur s[l] est a la fin de la partie de la ligne
            #il se termine a la ligne T[i,j]
            v = True
    return v 



if __name__ == "__main__":
    #grille dans l'enonce
    G = Grid(4,5,[[3],[],[1,1,1],[3]], [[1,1],[1],[1,2],[1],[2]])
    G.print_grid()
    for i in range(0,G.n_lignes):
        l = len(G.contrainte_l[i])
        T = []
        for j in range(G.m_colonnes + 1):
            T.append([0] * (l+1))
        print(str(i)+"-eme ligne coloreable ?",line_is_colorable(G.grid[i],G.m_colonnes-1,l,T,G.contrainte_l[i]))

