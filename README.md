# Tomographie Discrète 

## 1 Methode Incomplete de Resolution
### 1.1 Premiere etape
On montre comment d´eterminer si, pour une sequence donnee, il est possible de colorier une ligne en respectant cette sequence.
### 1.2 Generalisation
On generalise au cas d’une ligne dont la couleur de certaines cases est imposee.
### 1.3 Propagation
On montre comment tirer parti de cet algorithme afin d’identifier des cases necessairement blanches ou noires dans une ligne/colonne, et on procede par propagation pour colorier partiellement une grille.


### Q1 Si on a calcule tous les T[j,l]...
Alors en particulier on a calcule T(M-1,k) qui nous dit s'il est possible de colorier les M cases de la ligne L_i avec la sequence (s1...sk) qui revient a la sequence de tous les k blocs qui doivent etre places a la ligne L_i. Autrement dit, avec T(M-1,k) on peut determiner si l'on peut colorier la ligne L_i.

