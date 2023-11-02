/*
 *   Programme pour transformer un fichier type pgm P5 en pgm P2
 *   qui a la fois change le niveau de gris a max=2
*/
#include <sys/types.h>
#include <sys/stat.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <stdio.h>

#define SYSCALL_ERROR 1
#define PGM_ERROR 2

#define BUFF_SIZE 4096
#define INT_BUFF 64
typedef unsigned char bool;

bool is_space(char);
bool is_digit(char);

int read_number(int);
int get_size(int);

void test_syscall(int,char*);

void read_header(int,int*,int*,int*);
void write_header(int, int, int, int);
void convert(int,int,int,int,int);


int main(int argc, char *argv[]) {
    if (argc != 3) {
        fprintf(stderr,"Utilisation : %s <file_in.pgm> <file_out.pgm>\n",argv[0]);
        exit(EXIT_FAILURE);
    }

    //DECLARATION DES VARIABLES
    char *input_file = argv[1];
    char *output_file = argv[2];

    int input, output, dim_x, dim_y,max_val, size;

	//OUVERTURE DES FICHIERS
    input = open(input_file, O_RDONLY);
    test_syscall(input,"ouverture");

    output = open(output_file, O_WRONLY | O_CREAT | O_TRUNC, 0666);
    test_syscall(output,"ouverture");

    //LECTURE DE L'ENTETE
    read_header(input, &dim_x, &dim_y, &max_val);

    if (max_val > 255) {
       fprintf(stderr,"Max Val invalide\n");
       exit(PGM_ERROR);
    }

	/*LONGUEUR DU FICHIER INPUT À PARTIR DE LA FIN DE L'ENTETE
	size = get_size(input);
	if (size != dim_x * dim_y) {
		fprintf(stderr, "Taille de l'image different à dim_x * dim_y\n");
		exit(PGM_ERROR);
	}*/

    //ÉCRITURE DE L'ENTETE
    write_header(output,dim_x, dim_y, max_val);

    //ÉCRITUE DU CORPS
    convert(input,output, dim_x, dim_y, max_val);

    close(input);
    close(output);
    return EXIT_SUCCESS;
}

bool is_space(char c) {
    return c == ' ' || c == '\n' || c == '\t';
}

bool is_digit(char c) {
    return c >= '0' && c <= '9';
}

int get_size(int input) {
	//position courrant
	int start = lseek(input,0,SEEK_CUR);
	test_syscall(start,"lseek");
	//fin du fichier
	int end = lseek(input,0,SEEK_END);
	test_syscall(start,"lseek");
	//obtention de la taille de l'image a partir de l'entete (i.e. sans l'entete)
	int size = end - start - 1;
	test_syscall(lseek(input,start,SEEK_SET),"lseek");

	return size;
}

//teste si val != -1, sinon on affiche un message d'erreur et termine le processus
// val : valeur de retour d'un appel systeme
// msg : message d'erreur
void test_syscall(int val, char *msg) {
    if (val == -1) {
        fprintf(stderr,"SYSCALL ERROR : Erreur de <<%s>>\n",msg);
        exit(SYSCALL_ERROR);
    }
}

//precondition : un entier positionné dans la tete de lecture
int read_number(int fd) {
    int read_bytes;
    int offset = 0;
    char buffer[INT_BUFF];

	//lorseque l'octet qu'on lit est un chiffre
    while ((read_bytes = read(fd, buffer + offset,1)) > 0
                && is_digit(buffer[offset])
            	&& offset < INT_BUFF) {
		offset++;
	}
	test_syscall(read_bytes,"lecture");
	//si on a depassé la taille du buffer pour la lecture du int
	//	alors il y a un erreur
    if (offset >= INT_BUFF) {
        fprintf(stderr,"Depassement du buffer : Lecture d'entier invalide\n");
        exit(PGM_ERROR);
    }
	//si on n'a pas lu un chiffre
	//	alors on est dans le corps d'un fichier dont l'entete n'est pas correcte
    if (!is_digit(buffer[offset]) && !is_space(buffer[offset])) {
        fprintf(stderr,"Valeur non entier sous forme ascii dans la tete de lecture\n");
        exit(PGM_ERROR);
    }


    buffer[offset] = '\0';

    return atoi(buffer);
}

//recupere dim x , dim y , max val du fichier input
//et teste si c'est en format P5
void read_header(int input,int* dim_x,int* dim_y,int* max_val) {
    //lecture de Magic Number
	char buff[3];
    int read_bytes = read(input,buff,3);
    test_syscall(read_bytes,"lecture");

    if (buff[0] != 'P' && buff[1] != '5') {
        fprintf(stderr,"Magic Number different à P5\n");
        exit(PGM_ERROR);
    }

    *dim_x = read_number(input);
    *dim_y = read_number(input);
    *max_val = read_number(input);
}


//écriture de dim x , dim y , max val dans le fichier FD
void write_header(int fd, int dim_x, int dim_y, int max_val) {

    int written_bytes, bytes_to_write = 0, vals[] = {dim_x,dim_y,2}; //on change max val par 2
    char buff[INT_BUFF];

    written_bytes = write(fd,"P2\n",3);
    test_syscall(written_bytes,"écriture");

    for (int i = 0; i < 3; i++) {
        bytes_to_write = sprintf(buff,"%d",vals[i]);
		//espace entre dim x et dim y, \n sinon
        buff[bytes_to_write] = (i != 0 ? '\n' : ' ');

        written_bytes = write(fd,buff,bytes_to_write + 1);
        test_syscall(written_bytes,"écriture");
    }
}

//Traduction du corps du fichier P5 à P2
void convert(int input, int output, int dim_x, int dim_y, int max_val) {
	unsigned char c;
	char num[INT_BUFF];
    int written_bytes, read_bytes,bytes_to_write;

    for (int i = 0; i < dim_y; i++) {
		for (int j = 0; j < dim_x; j++) {
			//obtention du pixel
			read_bytes = read(input, &c,1);
			test_syscall(read_bytes,"lecture");
			//string-int cast et ajout d'un espace
            if (c > max_val/2) //normalisation (regularisation?)
                c = 2;
            else 
                c = 0;
			bytes_to_write = sprintf(num,"%u",(unsigned char)c);
			num[bytes_to_write] = ' ';
			//écriture
			written_bytes = write(output,num,bytes_to_write + 1);
			test_syscall(written_bytes,"écriture");
		}
		//saut de ligne
		c = '\n';
		written_bytes = write(output,&c,1);
		test_syscall(written_bytes,"écriture");
	}
}
