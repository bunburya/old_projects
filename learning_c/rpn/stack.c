#include "calc.h"
#define MAXVAL  100 /* max depth of value stack */


static double vstack[MAXVAL];
static int sp = 0; /* current position on the stack */

void push(double d) {
    if (sp < MAXVAL) {
        vstack[sp++] = d;
    } else {
        printf("Error: Stack size exceeds limit.\n");
        exit(1);
    }
}

double pop() {
    if (sp > 0) {
        return vstack[--sp];
    } else {
        printf("Error: Pop from empty stack.\n");
        exit(1);
        return -1.0;
    }
}
