#include <stdio.h>
#define swap(t, x, y) t tmp = y; y = x; x = tmp

int main() {
    int a = 1, b = 2;
    printf("Initial values: x %d, y %d\n", a, b);
    swap(int, a, b);
    printf("Final values: x %d, y %d\n", a, b);
}
