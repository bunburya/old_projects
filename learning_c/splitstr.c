#include <stdio.h>
#include <string.h>
#define MAXLINE 1000

int splitstr(char str[], char (*secs)[MAXLINE], char delim[]) {
    int i;      /* current index in string we are splitting */
    int s = 0;  /* current index in array of subsections */
    int j, k;   /* if we find the beginning of delim in str,
                   j = current position in delim;
                   k = current position in str. */

    char buf[MAXLINE];    /* current buffer of characters, to be stored
                             in secs when a delimiter is found */
    int b = 0;            /* current position in buffer */

    for (i=0; str[i] != '\0'; i++) {
        for (j=0, k=i; str[k] != '\0' && str[k] == delim[j]; j++, k++);
        if (j > 0 && delim[j] == '\0') {
            buf[b] = '\0';
            strcpy(secs[s++], buf);
            b = 0;
            i += (j-1);
        } else {
            buf[b++] = str[i];
        }
    }
    /* add the last section to secs */
    strcpy(secs[s++], buf);
    return s;
}

int main() {
    char secs[MAXLINE][MAXLINE];
    int i, n;
    n = splitstr("hello there", secs, "ll");
    for (i = 0; i < n; i++) {
        printf(secs[i]);
        putchar('\n');
    }
}
