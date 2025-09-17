
// Odin implementation of Collatz conjecture (hailstone sequence)

package main

import "core:fmt"

collatz :: proc(sequence: ^[dynamic]int, start: int) {
    value := start
    for value != 1 {
        if value % 2 == 0 {
            value = value / 2
        } else {
            value = 3 * value + 1
        }
        append(&sequence^, value)
    }
}

main :: proc() {
    start_value := 27

    longest_number := 0
    longest_length := 0

    sequence: [dynamic]int
    defer delete(sequence)

    // Example for 27
    append(&sequence, start_value)
    collatz(&sequence, start_value)

    fmt.println("First four values in sequence for 27:")
    for i := 0; i < 4; i += 1 {
        fmt.println(sequence[i])
    }

    fmt.println("Last four values in sequence for 27:")
    for i := 0; i < 4; i += 1 {
        fmt.println(sequence[len(sequence) - 4 + i])
    }

    fmt.println("Length of sequence for 27:")
    fmt.println(len(sequence))

    // Clear sequence for reuse
    for len(sequence) > 0 {
        pop(&sequence)
    }

    // Find number under 1_000_000 with longest sequence
    for n := 1; n < 1_000_000; n += 1 {
        append(&sequence, n)
        collatz(&sequence, n)

        if len(sequence) > longest_length {
            longest_number = n
            longest_length = len(sequence)
        }

        // Clear for next run
        for len(sequence) > 0 {
            pop(&sequence)
        }
    }

    fmt.println("Number with longest sequence:")
    fmt.println(longest_number)

    fmt.println("Length of longest sequence:")
    fmt.println(longest_length)
}
