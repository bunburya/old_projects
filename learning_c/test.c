#include <stdio.h>
#include <string.h>
#include <math.h>

const int MAXPERMS = 159; /* eventually have to raise this and use malloc */
const int PERMLEN = 26;
const char OPERS[4] = "+- ";

void getopperms(int n, char s[MAXPERMS][PERMLEN], int slen) {
    int p, i = 0;
    int m;
    for (p = 0; p < MAXPERMS; p++) {
        n = p;
        printf("p: %d\n", p);
        printf("n: %d\n", n);
        do {
            m = n % 3;
            if (m == 0) {
                s[p][i++] = ' ';
            } else if (m == 1) {
                s[p][i++] = '+';
            } else {
                s[p][i++] = '-';
            }
            n /= 3;
        } while (i < slen);
        s[p][i++] = '\0';
        i = 0;
        printf("got string %s\n", s[p]);
    }
}


int main() {
    int i, n = 1234;
    char perms[MAXPERMS][PERMLEN];
    printf("just before b3\n");
    base3(n, perms, 4);
    printf("just after b3\n");
    for (i = 0; i < MAXPERMS; i++) {
        printf(perms[i]);
        putchar('\n');
    }
    return 0;
}
