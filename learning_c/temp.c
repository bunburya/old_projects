#include <stdio.h>

main() {
    float fahr, celsius;
    int lower, upper, step;

    lower = 0;      // lower limit of temperature scale
    upper = 300;    // upper limit
    step = 20;      // step size

    printf("Fahr\tCels\n");

    for (fahr = lower; fahr <= upper; fahr += step) {
        celsius = (5*(fahr-32))/9;
        printf("%3.0f\t%6.2f\n", fahr, celsius);
    }
}
