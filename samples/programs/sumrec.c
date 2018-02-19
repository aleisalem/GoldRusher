#include<stdio.h>

int main(int argc, char* argv[]){

  if (argc < 2)
      return 1;

  int num,x;
  num = atoi(argv[1]);
  x=findsum(num);
  printf("Sum of the digits of %d is: %d",num,x);
  return 0;
}

int r,s;
int findsum(int n){
if(n){
         r=n%10;
         s=s+r;
         findsum(n/10);
     }
     else
       return s;
}
