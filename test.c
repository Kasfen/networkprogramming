#include <stdio.h>      /* printf, scanf, NULL */
#include <stdlib.h>     /* malloc, free, rand */

char* read_line(char str[], int n)
{
	  int ch, i = 0;
	    char *ptr;
	      while ((ch = getchar()) != '\n')
		          if (i < n)
				          str[i++] = ch;
	          else{else//array is full, use malloc and strncpy for more memory
			          n+=10;
				          ptr= (char*) malloc(n);//宣告大小為n的陣列
					          strncpy(ptr,str,n);
						          ptr[i++] = ch;
							          free(str);
								          str=ptr;
									      }

  str[i] = '\0';
    return str;
    }

int main ()
{
	  int i,n;
	    char *buffer = (char*) malloc (10);
	      if (buffer==NULL) exit (1);
	        buffer=read_line(buffer, 10);
		  puts(buffer);
		    free(buffer);
		      return 0;
}

