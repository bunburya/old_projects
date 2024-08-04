#include "calc.h"

int getop(char s[]) {
    /* Get next character or numeric operand */
    
    static int c = ' '; /* initialise c to ' ' so that getch will definitely
                        be called on the first call of the function */
    int result;
    int i = 0;
    int ch;
    int mco = FALSE;    /* whether we have a multi-char operator */
    while (c == ' ' || c == '\t') {
        s[0] = c = getch();
    } 
    if (c == '\n' || c == EOF || c == '\0') {
        /* preliminary check to see if we are at a newline or EOS */
        result = c;
        c = ' ';    /* reset c to ' ' to ensure that getch is called next time */
        return result;
    }
    if (!isdigit(c) && c != '.') {
        /* c is a sign or operator */
        s[i] = c;
        if ((c == '+' || c == '-') && (isdigit(ch = peekch()) || ch == '.')) {
            /* c is a sign, not an operator */
        } else {
            /* c is an operator, or the first character of an MCO */
            while (!isspace(s[++i] = c = getch()) && !isdigit(c) && c != '.') {
                /* more operator-type chars ahead; therefore, we have an MCO */
                mco = TRUE;
            }
            s[i--] = '\0';
            if (mco == TRUE) {
                return MCO;
            } else {
                return s[i];
            }
        }
    }
    if (isdigit(c) || c == '-' || c == '+') {   /* collect integer part */
        while (isdigit(s[++i] = c = getch()));
    }
    if (c == '.') { /* collect fraction part */
        while (isdigit(s[++i] = c = getch()));
    }
    s[i] = '\0';
    return NUMBER;
}

void handlemco(char s[]) {
    double op2;
    if (strcmp(s, "tan") == 0) {
        push(tan(pop()));
    } else if (strcmp(s, "sin") == 0) {
        push(sin(pop()));
    } else if (strcmp(s, "cos") == 0) {
        push(cos(pop()));
    } else if (strcmp(s, "**") == 0) {
        op2 = pop();
        push(pow(pop(), op2));
    }
}
