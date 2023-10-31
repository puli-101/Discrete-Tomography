from src.grid import *

class Image:
    def __init__(self,src):
        self.src = src
    
    @staticmethod
    def calc_constraints_lst(lst):
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
    def to_grid(img_src, compress=False, chunk_size=1):
        """
            Transforme une image format pgm en une grille
            et si les dimensions sont trop grandes alors on force une compression
        """
        if not(img_src.endswith(".pgm")):
            print("Incompatible file type")
            return 
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
                        print("Error: Incompatible header")
                        return
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
                        return
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
        
        if compress or (n > 70 and m > 70):
            print(n,m)
            matrix, n, m = Image.compress_matrix(matrix, n, m, chunk_size=chunk_size)
        cl,cc = Image.calc_constraints(matrix)


        G = Grid(n,m,cl,cc)
        G.grid = matrix 
        
        return G
    
    @staticmethod
    def compress_matrix(matrix,n,m, chunk_size=1):
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