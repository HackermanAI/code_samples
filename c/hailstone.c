
// C99 implementation of Collatz conjecture (hailstone sequence)

#include <stdio.h>
#include <stdlib.h>

typedef struct IntArray {
    int *data;
    size_t size;
    size_t capacity;
} IntArray;

void init_array(IntArray *arr) {
    arr->size = 0;
    arr->capacity = 16;
    arr->data = malloc(arr->capacity * sizeof(int));
    if (!arr->data) {
        fprintf(stderr, "Memory allocation failed\n");
        exit(EXIT_FAILURE);
    }
}

void free_array(IntArray *arr) {
    free(arr->data);
    arr->data = NULL;
    arr->size = arr->capacity = 0;
}

void append(IntArray *arr, int value) {
    if (arr->size >= arr->capacity) {
        arr->capacity *= 2;
        arr->data = realloc(arr->data, arr->capacity * sizeof(int));
        if (!arr->data) {
            fprintf(stderr, "Memory allocation failed\n");
            exit(EXIT_FAILURE);
        }
    }
    arr->data[arr->size++] = value;
}

void clear(IntArray *arr) {
    arr->size = 0;
}

void collatz(IntArray *sequence, int start) {
    int value = start;
    while (value != 1) {
        if (value % 2 == 0) {
            value = value / 2;
        } else {
            value = 3 * value + 1;
        }
        append(sequence, value);
    }
}

int main(void) {
    const int start_value = 27;
    int longest_number = 0;
    size_t longest_length = 0;

    IntArray sequence;
    init_array(&sequence);

    // Example for 27
    append(&sequence, start_value);
    collatz(&sequence, start_value);

    printf("First four values in sequence for 27:\n");
    for (size_t i = 0; i < 4 && i < sequence.size; i++) {
        printf("%d\n", sequence.data[i]);
    }

    printf("Last four values in sequence for 27:\n");
    for (size_t i = sequence.size > 4 ? sequence.size - 4 : 0; i < sequence.size; i++) {
        printf("%d\n", sequence.data[i]);
    }

    printf("Length of sequence for 27:\n%zu\n", sequence.size);

    clear(&sequence);

    // Find number under 1,000,000 with longest sequence
    for (int n = 1; n < 1'000'000; n++) {  // use 1000000 in C if your compiler doesn't allow digit separators
        append(&sequence, n);
        collatz(&sequence, n);

        if (sequence.size > longest_length) {
            longest_number = n;
            longest_length = sequence.size;
        }

        clear(&sequence);
    }

    printf("Number with longest sequence:\n%d\n", longest_number);
    printf("Length of longest sequence:\n%zu\n", longest_length);

    free_array(&sequence);
    return 0;
}
