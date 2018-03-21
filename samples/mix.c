#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

char* secret = "happynewyear";
int sum(int x, int y){
    return x+y;
}

void printSecret(){
    printf("Ach!! You found me!!\n");
}

int main(int argc, char* argv[]){

    if (argc < 4){
        printf("[USAGE]: ./mix (number) (number) (greeting)\n");
        return 1;
     }
     int x = atoi(argv[1]);
     int y = atoi(argv[2]);
     char *input = argv[3];
     printf("%s: %d+%d=%d\n", input, x, y, sum(x, y));

     if (strcmp(input, secret) == 0){
        time_t t = time(NULL);
        struct tm ltm = *localtime(&t);
        if((ltm.tm_mday == 29) || ((ltm.tm_mon+1) % 2 == 0))
            printSecret();
        else if(sum(x, y) % 50 == 0)
            printf("Oooh!! You're a lucky one!\n");
     }
     return 0;
}
