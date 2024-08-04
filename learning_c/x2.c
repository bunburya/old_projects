#include <stdio.h>

#define MAXLINE 1000

int atoi(char s[]) {
    /* Convert a string of chars to an int. */
    int i, c, total;
    total = 0;
    for (i=0;(c = s[i]) != '\0'; i++) {
        if (c < '0' || c > '9') {
            printf("Input must be a string of digits.\n");
            return NULL;
        } else {
            total *= 10;
            total += (c - '0'); 
        }
    }
    return total;
}

main() {
    /* Test atoi function. */
    char s[MAXLINE];
    int i = 0;
    char c;
    while ((c = getchar()) != EOF && c != '\n') {
        s[i] = c;
        i++;
    }
    s[i] = '\0';
    int n = atoi(s);
    if (n != NULL) {
        printf("%d\n", n);
        n *= 2;
        printf("%d\n", n);
    }
}
