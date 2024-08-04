#include <math.h>
#include <stdio.h>

struct point {
    int x;
    int y;
};

struct rect {
    struct point p1;
    struct point p2;
};

struct point mkpoint(int x, int y) {
    struct point tmp;
    tmp.x = x;
    tmp.y = y;
    return tmp;
}

double distance(struct point a, struct point b) {
    return sqrt(pow((b.x-a.x), 2) + pow((b.y-a.y), 2));
}

int main() {
    struct point a = mkpoint(2, 5);
    struct point b = mkpoint(1, 8);
    printf("distance: %.3f\n", distance(a, b));
}
