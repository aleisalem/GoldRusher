#include <stdio.h>
#include <stdlib.h>

int main(int argc, char* argv[])
{
  if (argc < 3)
      return 1;

  int num1, num2, max;
  num1 = atoi(argv[1]);
  num2 = atoi(argv[2]);

  max=(num1>num2) ? num1 : num2; /* maximum value is stored in variable max */
  while(1)                       /* Always true. */
  {
      if(max%num1==0 && max%num2==0)
      {
          printf("LCM of %d and %d is %d", num1, num2,max);
          break;          /* while loop terminates. */
      }
      ++max;
  }
  return 0;
}
