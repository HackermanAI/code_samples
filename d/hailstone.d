
// D implementation of Collatz conjecture (hailstone sequence)

import std.stdio;
import std.algorithm;
import std.range;
import std.typecons;

// Generate hailstone sequence starting from n
auto hailstone(uint n) {
    return recurrence!q{
        // If previous element is odd, 3x+1, else divide by 2
        (a[n - 1] & 1) ? a[n - 1] * 3 + 1 : a[n - 1] / 2
    }(n)               // initial element
    .until!q{ a == 1 } // stop when we reach 1
    (OpenRight.no);    // include the 1
}

void main() {
    enum startValue = 27;

    // Compute sequence for 27
    auto seq = startValue.hailstone.array;

    writeln("Hailstone(", startValue, "):");
    writeln("  First 4: ", seq[0 .. 4]);
    writeln("  Last 4 : ", seq[$ - 4 .. $]);
    writeln("  Length : ", seq.length);

    // Find longest sequence under 100_000
    enum limit = 100_000;

    auto longest =
        iota(1, limit)
        .map!(n => tuple(n.hailstone.walkLength, n)) // (length, number)
        .reduce!max;                                 // pick tuple with largest length

    writeln("\nLongest sequence in [1, ", limit, "]:");
    writeln("  Number = ", longest[1]);
    writeln("  Length = ", longest[0]);
}
