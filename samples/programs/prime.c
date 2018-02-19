#include <stdio.h>
#include <stdlib.h>

int main(int argc, char* argv[])
{
  if (argc < 2)
      return 1;
  int n, i, flag=0;
  n = atoi(argv[1]);

  for(i=2;i<=n/2;++i)
  {
      if(n%i==0)
      {
          flag=1;
          break;
      }
  }
  if (flag==0)
      printf("%d is a prime number.",n);
  else
      printf("%d is not a prime number.",n);
  return 0;
}
