#include <stdio.h>
#include <stdlib.h>

int main(int argc, char* argv[])
{
  if (argc < 2)
      return 1;

  int n, reverse=0, rem,temp;
  n = atoi(argv[1]);

  temp=n;
  while(temp!=0)
  {
     rem=temp%10;
     reverse=reverse*10+rem;
     temp/=10;
  }  
/* Checking if number entered by user and it's reverse number is equal. */  
  if(reverse==n)  
      printf("%d is a palindrome.",n);
  else
      printf("%d is not a palindrome.",n);
  return 0;
}
