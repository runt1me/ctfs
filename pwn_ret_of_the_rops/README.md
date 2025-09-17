# Description
ret2libc with puts to leak the address. The only bit that's slightly tricky is parsing the leak address, as it comes back as part of the same line that contains my payload.


