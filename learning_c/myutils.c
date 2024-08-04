#include <stdio.h>
#include <ctype.h>
#include <math.h>

#define MAXLINE 1000

int mygetline(char s[], int lim) {
    /* Read a line from input into an array; return length */
    int c, i;
    for (i=0; i < lim-1 && (c = getchar()) != EOF && c != '\n'; ++i) {
        s[i] = c;
    }
    s[i++] = c;
    s[i] = '\0';
    return i;
}

void copy(char from[], char to[]) {
    /* Copy the contents of one array to another */
    int i = 0;
    while ((to[i] = from[i]) != '\0')
        ++i;
}

int strindex(char str[], char sub[]) {
    /* Find a substring within a string. Return index at which substring
    begins if substring is present, -1 otherwise. */
    int i, j, k;
    for (i = 0; str[i] != '\0'; i++) {
        for (j = 0, k = i; str[k] != '\0' && sub[j] == str[k]; j++, k++) {
            ;
        }
        if (j > 0 && sub[j] == '\0') {
            return j;
        }
    }
    return -1;
}

double myatof(char s[]) {
    /* Convert a string array to a double. */
    double val, power, pow(double, double);
    int i, sign;
    for (i = 0; isspace(s[i]); i++) {
        ;
    }
    sign = (s[i] == '-') ? -1 : 1;
    if (s[i] == '-' || s[i] == '+') {
        i++;
    }
    for (val = 0.0; isdigit(s[i]); i++) {
        val = 10.0 * val + (s[i] - '0');
    }
    if (s[i] == '.') {
        i++;
        for (power = 1.0; isdigit(s[i]); i++) {
            val = 10.0 * val + (s[i] - '0');
            power *= 10;
        }
        val = sign * val / power;
    }
    if (s[i] == 'e' || s[i] == 'E') {
        i++;
        double exp;
        sign = (s[i] == '-') ? -1 : 1;
        if (s[i] == '-' || s[i] == '+') {
            i++;
        }
        for (exp = 0.0; isdigit(s[i]); i++) {
            exp = 10.0 * exp + (s[i] - '0');
        }
        val *= pow(10.0, (sign * exp));
    }
    return val;
    
}

