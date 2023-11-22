# Tomographie Discrète 

## 1 Distribution des Fichiers

- main.py: (En dehors de src) permet d'exécuter tous les algorithmes de coloration et fonctionnalités supplémentaires. Voici la liste d'options (disponible en exécutant python3.x main.py --help) :

    - Execution             : python3 main.py [options]
    - Options and arguments (and corresponding environment variables):
    - debug=true            : Prints on screen logs related to the image reconstruction process
    - img_debug=true        : Saves on folder 'output' reconstruction trace and on 'videos' a video version of the image reconstruction process
    - input=PATH            : Loads the instance of a grid saved at PATH (format .txt)
    - custom_input=PATH     : Loads the instance of a grid corresponding to a certain image at PATH
    - chunk_size=NUMBER     : States the size of each block in terms of pixels in the image compression process
    - compress=true         : Compresses the loaded image to optimize the algorithm (default = true)
    - mkvid                 : Transforms the reconstruction trace on 'output' to an mp4, avi, and gif video
    - time=true             : Returns the execution time on the standard error output
    - partial=true          : Executes a partial coloration instead of a full recursive coloration
    - show=true             : Opens the resulting image at the end of the execution

- src: Ce répertoire contient les codes source avec les fonctions implémentant les algorithmes du projet et la définition d'autres fonctions et outils nécessaires pour leur exécution. Ce répertoire contient notamment le fichier grid.py dans lequel nous avons définit l'objet "grille" qui représente nos le tableau à colorier.  src contient aussi le fichier algorithms.py qui contient les fonctions implémentant les algorithmes du projet. src contient aussi des fichiers nous permettant de lire et générer les images des grilles. Pour pouvoir générer des images et vidéos il est nécessaire d'avoir installé les bibliothèques: opencv-python, moviepy,ez_setup (pip), ffmpeg et finalement imagemagick (apt ou brew). 
Le répertoire src contient aussi des fichiers que nous avons utilisé pour éliminer des bugs et le sous-répertoire misc. Ce dernier contient un programme en bash nommé "tester.sh" qui prend en argument un entier n et un booléen b. Si b est faux (respectivement true), il exécute la fonction d'énumération (resp: colorationPartielle) sur chaque instance du sujet n fois et il écrit la somme du temps d'exécution pour chaque instance sur le fichier res_full.csv (resp: res_partiel.csv) dans le répertoire exec_times.

- instances: Dans ce répertoire nous avons installé les instances de test fournies pour le projet. Nous avons aussi installé d'autres instances additionnelles sous le format d'une liste de contraintes. 
        
- custom_input: Dans ce répertoire nous avons enregistré des images pixelées en noir et blanc sous le format pgn ou pmg. Dans la fonction main il est possible de mettre en paramètres l'argument "custom_input=custom_input/nom_doc" afin de qu'une image soit transformé dans un grille qui sera après coloriée avec nos algorithmes de tomographie discrète.
        
- output: Contient les images générées par les coloriages intermédiaires d'une grille. 
        
- videos: Contient les vidéos et gifs engendrées lors d'un coloriage.
        
- sample_results: Contient les images finales engendrées par coloriage d'une grille. Ce répertoire contient aussi un zip avec toutes les images que nous avons obtenu en appliquant la fonction d'énumération aux instances fournies par le projet.