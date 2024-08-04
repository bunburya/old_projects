#include "calc.h"
#define BUFSIZE 100

static char buf[BUFSIZE];
static int bp = 0; /* current position on buffer */

char getch() {
    return (bp > 0) ? buf[--bp] : getchar();
}

void ungetch(char c) {
    if (bp >= BUFSIZE) {
        printf("Error: Character buffer full\n");
    } else {
        buf[bp++] = c;
    }
}

char peekch() {
    /* see what the next character is, without altering the stream. */
    char nextch = getch();
    ungetch(nextch);
    return nextch;
}
