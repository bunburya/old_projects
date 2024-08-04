#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "brainfuck.h"

// it works yay!

void push(struct list *ls, int i) {
    //printf("adding %d\n", i);
    if (ls->len >= ls->size) {
        ls->size *= 2;
        ls->contents = realloc(ls->contents, (ls->size) * sizeof(int));
    }
    ls->contents[ls->len++] = i;
}

void assign(struct list *ls, int i, int newval) {
    ls->contents[i] = newval;
}

int pop(struct list *ls) {
    return ls->contents[--(ls->len)];
}

int peek(struct list *ls, int i) {
    return ls->contents[i];
}

void print_ls(struct list *ls) {
    int i, j;
    for (i = 0; i < ls->len; i++) {
        j = peek(ls, i);
        putchar(j);
    }
}

void add_str(struct list *ls, int *str) {
    int i = 0, j;
    while ((j = str[i++]) != '\0') {
        push(ls, j);
    }
}

void incr(struct list *ls, int i) {
    (ls->contents[i])++;
}

void decr(struct list *ls, int i) {
    (ls->contents[i])--;
}

struct list *new_list(int size) {
    struct list *ls = malloc(sizeof(struct list));
    ls->size = size;
    ls->len = 0;
    int *i = malloc(size * sizeof(int));
    ls->contents = i;
    return ls;
}
/*
void main() {
    struct list *ls = new_list(1000);
    int i[11] = {104, 101, 108, 108, 111, 32, 119, 111, 114, 108, 100};
    add_str(ls, i);
    incr(ls, 0);
    decr(ls, 1);
    print_ls(ls);
    putchar('\n');
}*/
