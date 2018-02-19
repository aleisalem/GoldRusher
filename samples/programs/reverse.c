#include<stdio.h>

int main(int argc, char* argv[]){
   
    if (argc < 2)
        return 1;

    int num,r,reverse=0;
    num = atoi(argv[1]);

    while(num){
         r=num%10;
         reverse=reverse*10+r;
         num=num/10;
    }

    printf("Reversed of number: %d",reverse);
    return 0;
}
