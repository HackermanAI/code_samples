// Comment
/* Multi-line comment */

#include <iostream>
#include <string>
#define length(x) sizeof(x) / sizeof(x[0])

typedef struct
{
    [[deprecated]] bool is_true;
    std::string text;
} Structure;

int main()
{
    std::cout << "Hello world!" << std::endl;
    unsigned int some_array[4] = { 4, 3, 2, 1 };

    for (int i = 0; i < length(some_array); i++)
    {
        some_array[i] += i + sizeof(some_array);
    }

    Structure some_struct;
    some_struct.is_true = true;
    some_struct.text = R"(raw string)";
    char some_char = 'c';
}

