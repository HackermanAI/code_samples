
// smart pointers

#include <memory>
#include <iostream>
#include <vector>

class MyClass {
    // unique_ptr is a smart pointer
    std::unique_ptr<std::vector<int>> data;
public:
    // allocate memory with make_unique
    MyClass(const int size) { data = std::make_unique<std::vector<int>>(size); }
    void print_data() {
        for (auto i : *data) { std::cout << i << std::endl; }
    }
};

void function_using_data() {
    // lifetime tied to scope
    MyClass my_class(5);
    my_class.print_data();
} // my_class is destroyed here

int main() {
    function_using_data(); // 0 0 0 0 0
}
