#include <stdio.h>
#include <stdlib.h>
#include <time.h>
 
int main(int argc, char* argv[])
{
  if (argc < 2)
      return 1;
  int n, i,  c, a = 1;
  n = atoi(argv[1]);
  for (i = 1; i <= n; i++)
  {
    for (c = 1; c <= i; c++)
    {
      printf("%d ",a);
      a++;
    }
    printf("\n");
  }
 
  return 0;
}
