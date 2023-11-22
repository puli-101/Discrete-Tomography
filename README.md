# Tomographie Discrète 

## 0 Description
Description du projet...

## 1 Pre-requis
    python version 3.9+
    pip install opencv-python
    pip install moviepy
    pip install ez_setup (avec --break-system-packages si necessaire)

    sudo apt install ffmpeg 
    sudo apt install imagemagick

## 2 Distribution des Fichiers

### root
main.py :
makefile :
README.md :

### src
algorithms.py :
grid.py :
image.py :
debugging.py :
#### src/img_handler
convert_pgm.c : code qui transforme une image pgm format P5 dans une image pgm format P2 et change le niveau de gris a max=2

### input
Contient des images format pgm P2 que l'algorithme peut lire et transformer dans une matrice et une liste de contraintes

### instances
Instances donnees 

### output
Contient des images liees a la resolution partielle, ce dossier est cree une fois qu'on execute en mode img_debug=true

### videos
Contient une visualisation 

### bin
cree une fois qu'on compile (avec make) le fichier src/img_handler/convert_pgm.c

### sample_results
Contient les resultats d'execution des grilles du dossier instances/

## 3 Execution

python3.x main.py [options]

avec les options suivantes:

debug=true : pour une affichage detaillee de l'algorithme de resolution partiel
img_debug=true : pour une generation d'une suite d'images et une video de la coloration sequentielle
color_printing=true : pour une affichage en terminal de la grille avec des couleurs
