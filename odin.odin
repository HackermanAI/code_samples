
// Comment
/* 
    Multi-line 
    comment
    
    /*
        Nested multi-line comment
    */
*/

package main

import "core:fmt"

DIRECTIVE :: #config(DIRECTIVE, 20)
Char_Set :: bit_set['A'..='Z'; u32]

@(cold)
main :: proc() {
    defer fmt.println("Hellope!")
    some_array : [4]int = { 4, 3, 2, 1 }

    for i in 0..<4 {
        some_array[i] += i + len(some_array)
    }

    some_struct : Structure = { true, `raw string` }
    
    foo :: proc() {
        // pass
    }
}

Structure :: struct {
    is_true: bool,
    text: string,
}
