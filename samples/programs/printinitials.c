#include<stdio.h>

int main(int argc, char* argv[]){
   if (argc < 2)
       return 1;
  
   char* str = argv[1];
   int i=0;
   printf("%c",*str);
   while(str[i]!='\0'){
       if(str[i]==' '){
            i++;
            printf("%c",*(str+i));
       }
       i++;
   }
   return 0;
}
