# Description
A bit more interesting, there are no real ROP gadgets available here. Looks like it might not be glibc either, I didn't see __libc_csu_init available.

However, the stack is executable, and you get a stack address handed to you. So you can write shellcode as part of your payload and jump back to that address.

One other interesting trick with this one is that a lot of the normal shellcodes I found online did not play nicely with the fact that the shellcode was being executed on the stack. I had to modify them to sub rsp, 0x40 before executing the shellcode. Otherwise, I would get a segfault in the middle of my shellcode. Per ChatGPT, this is because having rsp == rip causes problems when a push instruction is executed. Each push writes 8 bytes below the current rsp, which collides with my instruction stream (shellcode) that hasn't been executed yet, corrupting it.

Assembling shellcode with nasm:
`nasm -f bin shellcode.asm -o shellcode.bin`
