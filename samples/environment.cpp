#include <iostream>
#include <stdio.h>
#include <string>
#include <stdlib.h>

int sum(int x, int y){
    return x + y;
}

void printSecret(){
    std::cout << "The secret is printed."<<std::endl;
}

std::string exec(char* cmd) {
    FILE* pipe = popen(cmd, "r");
    if (!pipe) return "ERROR";
    char buffer[128];
    std::string result = "";
    while(!feof(pipe)) {
    	if(fgets(buffer, 128, pipe) != NULL)
    		result += buffer;
    }
    pclose(pipe);
    return result;
}

int main(int argc, char* argv[]){
    if (argc < 3){
       std::cout << "Insufficient arguments." << std::endl;
       return 1;
    }
    int x = atoi(argv[1]);
    int y = atoi(argv[2]);
    std::cout << sum(x,y) << std::endl;

    std::string result = exec("uname -a");
    if(result.find("Fedora") == std::string::npos)
        std::cout << "I am in my happy place :)" << std::endl;
    else
        printSecret();

    return 0;
}
