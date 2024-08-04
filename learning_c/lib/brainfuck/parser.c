#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include "brainfuck.h"
#define MAXLINE 998

int read_file(FILE *, struct list *);
void parse_prog(struct list *);
void parse_char(char, struct list *, struct list *, int *, int *);

struct list *prog;
FILE *fp;

int main(int argc, char *argv[]) {
    fp = fopen(argv[1], "r");
    prog = new_list(1000);
    read_file(fp, prog);
    parse_prog(prog);
    return 0;
}

int read_file(FILE *fp, struct list *ls) {
    // Read file into memory
    char c;
    while ((c = fgetc(fp)) != EOF) {
        push(ls, c);
    }
    push(ls, '\0');
    // TODO: return 1 if problem reading from file
    return 0;
}

void parse_prog(struct list *prog) {
    struct list *cells = new_list(30000);
    struct list *loops = new_list(1000);
    int *cell_i = malloc(sizeof(int)); // current cell
    int *prog_i = malloc(sizeof(int)); // current position in program
    *cell_i = 0;
    *prog_i = 0;
    char c;
    while ((c = peek(prog, *prog_i))) {
        parse_char(c, cells, loops, cell_i, prog_i);
        //sleep(1);
    }
}
        
void parse_char(char c, struct list *cells, struct list *loops, int *cell_i, int *prog_i) {
    //printf("handling char ");
    //putchar(c);
    //putchar('\n');
    switch (c) {
        case '>':
            (*cell_i)++;
            break;
        case '<':
            (*cell_i)--;
            break;
        case '+':
            incr(cells, *cell_i);
            break;
        case '-':
            decr(cells, *cell_i);
            break;
        case '.':
            putchar(peek(cells, *cell_i));
            break;
        case ',':
            assign(cells, *cell_i, getchar());
            break;
        case '[':
            push(loops, *prog_i);
            break;
        case ']':
            if (peek(cells, *cell_i)) {
                *prog_i = peek(loops, (loops->len)-1);
            } else {
                pop(loops);
                (*prog_i)++;
            }
            break;
        }
    if (c != ']') {
        (*prog_i)++;
    }
}
