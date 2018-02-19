#include <iostream>
#include <ctime>
#include <stdlib.h>

int sum(int x, int y){
    return x + y;
}

void printSecret(){
    std::cout << "The secret is printed."<<std::endl;
}

int main(int argc, char* argv[]){
    if (argc < 3){
       std::cout << "Insufficient arguments." << std::endl;
       return 1;
    }
    int x = atoi(argv[1]);
    int y = atoi(argv[2]);
    std::cout << sum(x,y) << std::endl;

    time_t now = time(0);
    tm *ltm = localtime(&now);
    if((ltm->tm_mday == 29) || ((ltm->tm_mon+1) % 2 == 0))
        printSecret();

    return 0;
}
