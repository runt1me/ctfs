# Description
Format-string challenge. Pretty difficult in that there is no easy symbol to jump to, and it's 64-bit, so the addresses that we need to work with all contain null bytes. I didn't figure it out, but the general principle is that you need to use %p specifies to get a libc address, use %n to somehow (?) overwrite the GOT address of exit() with system(), and then overwrite an argument with /bin/sh.

Someone else's writeup here:
https://ctftime.org/writeup/25903
