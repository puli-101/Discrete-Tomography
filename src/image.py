from src.grid import *

class Image:
    def __init__(self,src):
        """
            src == path de l'image
        """
        self.src = src
    
    @staticmethod
    def calc_constraints_lst(lst):
        """
            Fonction qui a partir d'une liste calcule
            les contraintes associees a cette liste
        """
        block_size = 0
        res = []
        for c in lst:
            if c == Color.BLACK:
                block_size+=1
            elif block_size > 0:
                res += [block_size]
                block_size = 0
        if block_size > 0:
            res += [block_size]
            block_size = 0
        return res

    @staticmethod
    def calc_constraints(matrix):
        """
            Fonction qui a partir d'une matrice deja colorie
            on determine l'ensemble de contraintes par ligne/colonne
        """
        cl = []
        cc = []
        for line in matrix:
            cl.append(Image.calc_constraints_lst(line))
        for j in range(0,len(matrix[0])):
            lst = []
            for i in range(0, len(matrix)):
                lst += [matrix[i][j]]
            cc.append(Image.calc_constraints_lst(lst))
        return cl,cc

    @staticmethod
    def to_grid(img_src, compress=False, chunk_size=1, force_conversion=False):
        """
            Transforme une image format pgm en une grille
            et si les dimensions sont trop grandes alors on force une compression
        """
        conversion = False
        if not(img_src.endswith(".pgm")) or force_conversion:
            #si l'image n'est pas format pgm alors on essaie de convertir en pgm 
            conversion = True
            print("Warning: Non pgm source input detected")
            print("Executing automatic image conversion...")
            os.system("make > /dev/null && mkdir -p custom_input/")
            os.system("convert "+img_src+" custom_input/to_p5.pgm")
            os.system("./bin/convert_pgm custom_input/to_p5.pgm custom_input/to_p2.pgm")
            img_src = "custom_input/to_p2.pgm"
        matrix = []
        n = 0
        m = 0
        with open(img_src) as file:
            readHeader=False
            readDim=False
            readGrayScale=False
            for line in file:
                line = line.rstrip()
                if line.startswith("#"):
                    continue
                if not(readHeader):
                    readHeader = True
                    if line!="P2":
                        print("Error: Incompatible header pgm format")
                        print("Re execute with force=true ?")
                        exit(-1)
                    continue
                if not(readDim):
                    nums = line.split(' ')
                    m = int(nums[0])
                    n = int(nums[1])
                    readDim = True 
                    continue
                if not(readGrayScale):
                    readGrayScale = True
                    scale = int(line)
                    if scale != 2:
                        print("Error: Incompatible scale")
                        exiit(-1)
                    continue
                matrix_line = []
                for c in line.split(' '):
                    if c == "0":
                        matrix_line.append(Color.BLACK)
                    elif c == "1":
                        matrix_line.append(Color.UNCOLORED)
                    else:
                        matrix_line.append(Color.WHITE)
                matrix.append(matrix_line)
        
        #compression de la matrice (on force la compression si trop grande)
        if compress or (n > 151 and m > 151):
            print(n,m)
            matrix, n, m = Image.compress_matrix(matrix, n, m, chunk_size=chunk_size)

        #calcul des contraintes
        cl,cc = Image.calc_constraints(matrix)
        name = img_src
        Image.save_constraints(cl,cc,name.removesuffix(".pgm")+".txt")

        G = Grid(n,m,cl,cc)
        G.grid = matrix 
        
        #on elimine les fichiers temporaires
        if (conversion):
            os.system("rm custom_input/to_p5.pgm")
            os.system("rm custom_input/to_p2.pgm")

        return G
    
    @staticmethod
    def compress_matrix(matrix,n,m, chunk_size=1):
        """
            Reduit la taille d'une matrice de taille n x m
            en prennant la moyenne des valeurs de carres de taille chunk_size
        """
        if chunk_size == 1:
            chunk_size = min(n,m)//70
        new_mat=[]
        for i in range(0,n,chunk_size):
            line = []
            for j in range(0,m,chunk_size):
                c = 0
                n_c = 0
                for k1 in range(i, min(n, i + chunk_size)):
                    for k2 in range(j, min(m, j + chunk_size)):
                        c += matrix[k1][k2].value
                        n_c += 1
                line += [Color(round(c/n_c))]
            new_mat += [line]
        new_n = len(new_mat)
        new_m = len(new_mat[0])
        return new_mat, new_n, new_m
    
    @staticmethod
    def save_constraints(cl,cc,name):
        """
            Transforme une image dans une liste de contraintes ligne colonne
            dans le meme format que les instances de base
        """
        f = open(name, "w")
        for line in cl:
            for elt in line:
                f.write(str(elt)+" ")
            f.write("\n")
        f.write("#\n")
        for line in cc:
            for elt in line:
                f.write(str(elt)+" ")
            f.write("\n")
        f.close()