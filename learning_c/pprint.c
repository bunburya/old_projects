#include <stdio.h>

#define MAXLINE 1000

int mygetline(char s[], int lim);
int strindex(char str[], char sub[]);

char pattern[] = "ould";

int main()
{
    char line[MAXLINE];
	while (mygetline(line, MAXLINE) > 0) {
        if (strindex(line, pattern) != -1) {
            printf("%s", line);
        }
    }
    return 0;
}
