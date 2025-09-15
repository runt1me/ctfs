# Description
Mostly just an annoying challenge having to deal with the dumb "game" interaction before sending the payload.

ret2libc. Returned to puts to leak a libc address, calculate libc base, go back to main, return to system("/bin/sh")
