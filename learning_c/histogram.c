#include <stdio.h>

#define IN      1   // Inside a word
#define OUT     0   // Outside a word

#define MAXLEN  10  // Number of elements in the length array (the last space
                    // in the array containing the number of words of length
                    // MAXLEN and above.
#define HEIGHT  20  // Height of histogram (feature not implemented)

/* Print a histogram of the lengths of words in input. */

main() {

    int c, state, wordlen, maxfreq, i;
    int lengths[MAXLEN];
    state = OUT;
    wordlen = 0;
    for (i=0;i<MAXLEN;i++) {
        lengths[i] = 0;
    }

    // Go through the input, find the length of each word, increment the
    // appropriate array element.
    while ((c = getchar()) != EOF) {
        if (c == ' ' || c == '\t' || c == '\n') {
            if (state == IN) {
                state = OUT;
                // We always subtract 1 to get the array index,
                // because there are no 0-length words.
                if (wordlen >= MAXLEN) {
                    ++lengths[MAXLEN-1];
                } else {
                    ++lengths[wordlen-1];
                }
                wordlen = 0;
            }
        } else {
            state = IN;
            wordlen++;
        }
    }
    
    // Print out the array as a vertical histogram.
    maxfreq = 0;
    // Find highest frequency, to determine height of histogram.
    for (i=0;i<MAXLEN;i++) {
        if (lengths[i] > maxfreq) {
            maxfreq = lengths[i];
        }
    }
    while (maxfreq) {
        for (i=0;i<MAXLEN;i++) {
            if (lengths[i] >= maxfreq) {
                putchar('_');
            } else {
                putchar(' ');
            }
            putchar('\t');
        }
        putchar('\n');
        maxfreq--;
    }
    putchar('\n');
    for (i=0;i<MAXLEN;i++) {
        printf("%d", i+1);
        if (i == MAXLEN-1) {
            putchar('+');
        } else {
            putchar('\t');
        }
    }
    putchar('\n');
}
