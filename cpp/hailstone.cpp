
// C++17 implementation of Collatz conjecture (hailstone sequence)

#include <iostream>
#include <vector>

auto collatz(std::vector<int>& sequence, int start) -> void {
    int value = start;
    while (value != 1) {
        if (value % 2 == 0) {
            value /= 2;
        } else {
            value = 3 * value + 1;
        }
        sequence.push_back(value);
    }
}

int main() {
    constexpr int start_value = 27;

    int longest_number = 0;
    std::size_t longest_length = 0;

    std::vector<int> sequence;
    sequence.reserve(1000); // avoid frequent reallocations

    // Example for 27
    sequence.push_back(start_value);
    collatz(sequence, start_value);

    std::cout << "First four values in sequence for 27:\n";
    for (std::size_t i = 0; i < 4 && i < sequence.size(); ++i) {
        std::cout << sequence[i] << '\n';
    }

    std::cout << "Last four values in sequence for 27:\n";
    for (std::size_t i = sequence.size() > 4 ? sequence.size() - 4 : 0; i < sequence.size(); ++i) {
        std::cout << sequence[i] << '\n';
    }

    std::cout << "Length of sequence for 27:\n" << sequence.size() << '\n';

    sequence.clear();

    // Find number under 1,000,000 with longest sequence
    for (int n = 1; n < 1'000'000; ++n) {
        sequence.push_back(n);
        collatz(sequence, n);

        if (sequence.size() > longest_length) {
            longest_number = n;
            longest_length = sequence.size();
        }

        sequence.clear();
    }

    std::cout << "Number with longest sequence:\n" << longest_number << '\n';
    std::cout << "Length of longest sequence:\n" << longest_length << '\n';

    return 0;
}
