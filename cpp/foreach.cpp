
// for each in vector

#include <algorithm>
#include <vector>
#include <iostream>

int main() {
    std::vector<int> numbers = { 1, 2, 3, 4, 5 };

    std::for_each(numbers.begin(), numbers.end(), [](int &number) {
        number *= 2;
    });

    std::for_each(numbers.begin(), numbers.end(), [](int number) {
        std::cout << number << std::endl;
    });
}
