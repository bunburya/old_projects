#include "calc.h"

int main() {
    /* Reverse Polish Notation calculator */
    int type;
    double op2;
    char s[MAXOP];
    while ((type = getop(s)) != EOF) {
        switch (type) {
            case NUMBER:
                push(atof(s));
                break;
            case MCO:
                handlemco(s);
                break;
            case '+':
                push(pop() + pop());
                break;
            case '*':
                push(pop() * pop());
                break;
            case '-':
                op2 = pop();
                push(pop() - op2);
                break;
            case '/':
                op2 = pop();
                if (op2 == 0.0) {
                    printf("Error: Division by zero.\n");
                } else {
                    push(pop() / op2);
                }
                break;
            case '%':
                op2 = pop();
                if (op2 == 0.0) {
                    printf("Error: Division by zero.\n");
                } else {
                    push(fmod(pop(), op2));
                }
                break;
            case '\n':
                printf("%f\n", pop());
                break;
            default:
                printf("Error: Unknown command: %d\n", type);
        }
    }
    return 0;
}

