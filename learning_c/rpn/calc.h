#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <ctype.h>

#define MAXOP   100 /* max size of operand/operator */
#define MAXLINE 1000
#define NUMBER  '0' /* signal that getop encountered a number */
#define MCO     -10 /* signal that getop encountered a multi-char operator */
#define TRUE    1
#define FALSE   0

void push(double);
double pop();

int getop(char []);
void handlemco(char []);

char getch();
void ungetch(char);
char peekch();
