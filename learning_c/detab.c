#include <stdio.h>

#define TABLEN  8

main() {
    int posn = 0;   /* Our position on the current line */
    int i = 0;
    int spaces;
    char c;
    while ((c = getchar()) != EOF) {
        if (c == '\t') {
            spaces = TABLEN - (posn % TABLEN);
            for (i=0;i<spaces;i++)
                putchar(' ');
        } else {
            putchar(c);
        }
        if (c == '\n')
            posn = 0;
        else
            posn++;
    }
}
