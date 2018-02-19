#include <stdio.h>

char* secret = "happynewyear";
int sum(int x, int y){
    return x+y;
}

void printSecret(){
    printf("Ach!! You found me!!\n");
}

int main(int argc, char* argv[]){

    if (argc < 3){
        printf("Insufficient number of arguments\n");
        return 1;
     }
     int x = atoi(argv[1]);
     int y = atoi(argv[2]);
     printf("The sum of %d+%d is %d\n", x, y, sum(x, y));

     if (argc == 4){
         char *input = argv[3];
         if (strcmp(input, secret) == 0)
             printSecret();
     }
     return 0;
}
