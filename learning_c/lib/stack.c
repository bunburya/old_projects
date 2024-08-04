#include <stdlib.h>
#include <stdio.h>
#include "brainfuck.h"

STACK *new_stack(int size) {
    STACK *stack = (STACK *) malloc(sizeof(STACK));
    stack->size = size;
    stack->array = (int *) malloc(size * sizeof(int));
    stack->i = 0;
    return stack;
}

void push(STACK *stack, int val) {
    printf("pushing val %d to pos %d\n", val, stack->i);
    stack->array[stack->i++] = val;
    printf("pushed\n");
}

int pop(STACK *stack) {
    return stack->array[--stack->i];
}

void print(STACK *s) {
    int i, c;
    for (i = 0; (c = s->array[i]) != EOF; i++) {
        putchar(c);
    }
    putchar('\n');
}

/*
int main() {
    STACK *s = new_stack(400);
    int i;
    for (i = 0; i < 1000; i++) {
        push(s, i-500);
    }
    for (i = 0; i < 10000; i++) {
        printf("%d,", pop(s));
    }
    putchar('\n');
}
*/
