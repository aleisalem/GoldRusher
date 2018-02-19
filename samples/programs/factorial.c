#include <stdio.h>
#include <stdlib.h>

int main(int argc, char* argv[])
{
    if (argc < 2)
        return 1;
    int n, count;
    unsigned long long int factorial=1;         
    n = atoi(argv[1]);
    if (n<0)
        printf("Error!!! Factorial of negative number doesn't exist.");
    else
    {
       for(count=1;count<=n;++count)    /* for loop terminates if count>n */
       {
          factorial*=count;              /* factorial=factorial*count */
       }
    printf("Factorial = %lu",factorial);
    }
    return 0;
}
