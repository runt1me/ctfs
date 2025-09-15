# Description
A decent number of ROP gadgets available here, but no easy read/write primitive.

ret2libc. ret2plt (libc.write) to write a runtime address to stdout, jump back to main, use the leaked address to get the libc base, ret to system("/bin/sh"). execve("/bin/sh") did not work and I didn't take the time to figure out why, probably an issue with the state of the registers.
