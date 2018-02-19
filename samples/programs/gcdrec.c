#include<stdio.h>

int main(int argc, char* argv[]){
  if (argc < 3)
      return 1;
  int n1,n2,gcd;
  n1 = atoi(argv[1]);
  n2 = atoi(argv[2]);
  gcd=findgcd(n1,n2);
  printf("\nGCD of %d and %d is: %d",n1,n2,gcd);
  return 0;
}

int findgcd(int x,int y){
     while(x!=y){
          if(x>y)
              return findgcd(x-y,y);
          else
             return findgcd(x,y-x);
     }
     return x;
}
