
// Comment

/* 
    Multi-line
    comment
*/

#include <stdio.h>
#include <stdbool.h>
#define length(x) sizeof(x) / sizeof(x[0])

typedef struct Structure {
    bool is_true;
    char text[20];
} Structure;

int main() {
    printf("Hello World!");
    unsigned int some_array[4] = { 4, 3, 2, 1 };

    for (int i = 0; i < length(some_array); i++)
    {
        some_array[i] += i + sizeof(some_array);
    }

    Structure some_struct = { true, "string" };
    char some_char = 'c';
}
