
; hello64.asm
; Assemble: nasm -felf64 hello64.asm && ld -o hello64 hello64.o
; Run:      ./hello64

section .data
    msg db "Hello, world!", 10
    len equ $ - msg

section .text
    global _start
_start:
    ; write(1, msg, len)
    mov rax, 1          ; sys_write
    mov rdi, 1          ; fd = stdout
    mov rsi, msg        ; buf
    mov rdx, len        ; count
    syscall

    ; exit(0)
    mov rax, 60         ; sys_exit
    xor rdi, rdi        ; status = 0
    syscall
