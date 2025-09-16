import ctypes
from pwn import *

# Create a mapping of all srand seeds to libc rand values
libc = ctypes.CDLL('libc.so.6')
mapping = {}
for i in range(255):
    libc.srand(i)
    mapping[libc.rand()] = chr(i)

for k in mapping.keys():
    print(k)
    print(mapping[k])
    print()

flag = ""
casino = ELF("./casino", checksec=False)
for b in range(29):
    val = casino.u32(casino.sym["check"] + b * 4)
    flag += mapping[val]
print(flag)

