#include <stdio.h>
#include <stdlib.h>  /* For exit() function */

int main(int argc, char* argv[])
{
   if (argc < 2)
      return 1;

   char* c = argv[1];
   FILE *fptr;
   fptr=fopen("program.txt","w");
   if(fptr==NULL){
      printf("Error!");
      exit(1);
   }
   fprintf(fptr,"%s",c);
   fclose(fptr);
   return 0;
}

