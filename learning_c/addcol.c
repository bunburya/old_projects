#include <stdio.h>
#define MAXLINE 1000

double myatof(char s[]); /* without this the total printed is 0.00000 */

int main() {
    char line[MAXLINE];
    double total = 0.0;
    while (mygetline(line, MAXLINE) > 0) {
        total += myatof(line);
    }
    printf("%f\n", total);
}
