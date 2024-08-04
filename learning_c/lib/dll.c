#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct link {
    struct link *prev;
    struct link *next;
    int val;
} LINK;

typedef struct list {
    struct link *first;
    struct link *last;
    int len;
} LIST;

LIST *new_list() {
    LIST *new = (LIST *) malloc(sizeof(LIST));
    if (new) {
        memset(new, 0, sizeof(LINK));
    }
    return new;
}

LINK *new_link() {
    LINK *new = (LINK *) malloc(sizeof(LINK));
    if (new) {
        memset(new, 0, sizeof(LINK));
    }
    return new;
}

void append(LIST *dll, int val) {
    LINK *new = new_link();
    new->val = val;
    new->prev = dll->last;
    new->next = 0;
    if (dll->first == 0) {
        dll->first = new;
        dll->last = new;
    } else {
        dll->last->next = new;
        dll->last = new;
        dll->len++;
    }
}

int main() {
    LIST *dll = new_list();
    int i;
    append(dll, 44);
    append(dll, 52);
    append(dll, 665);
    LINK *cur = dll->first;
    for (i = 0; i <= dll->len; i++) {
        printf("%d\n", cur->val);
        if (cur->next != 0) {
        cur = cur->next;
        }
    }
}
