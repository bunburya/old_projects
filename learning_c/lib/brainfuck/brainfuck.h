struct list {
    int *contents;
    int size;
    int len;
};

void push(struct list *, int);
void assign(struct list *, int, int);
int pop(struct list *);
int peek(struct list *, int);
void print_ls(struct list *);
void add_str(struct list *, int *);
void incr(struct list *, int);
void decr(struct list *, int);
struct list *new_list(int);
