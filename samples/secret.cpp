#include <iostream>
#include <ctime>
#include <stdlib.h>

std::string secret = "happynewyear";

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
    std::string input = "";
    if (argc == 4){
        input = argv[3];
    }
    
    int x = atoi(argv[1]);
    int y = atoi(argv[2]);
    std::cout << sum(x,y) << std::endl;

    if (secret.compare(input) == 0)         
        printSecret();

    return 0;
}
