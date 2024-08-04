#include <stdio.h>

void strcopy(char *, char *);
void mystrcat(char *, char *);
int mystrlen(char *);
int strend(char *, char *);

int main() {
    char s[] = "hello there";
    char t[] = "ello there";
    printf("%d\n", strend(s, t));
}

int mystrlen(char *s) {
    char *start = s;
    while (*s++);
    return s - start;
}

void strcopy(char *from, char *to) {
    while (*to++ = *from++);
}

void mystrcat(char *from, char *to) {
    for (;*to; *to++);
    strcopy(from, to);
}

int strend(char *s, char *t) {
    int diff = mystrlen(s) - mystrlen(t);
    if (diff < 0) {
        return 0;
    }
    s += diff;
    while (*s++ == *t++) {
        if (*s == '\0') {
            return 1;
        }
    }
    return 0;
}
