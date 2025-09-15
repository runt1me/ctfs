# Description

Basic ret2win challenge, but with an annoying buffer size that turns out to be a giant PITA. fgets() reads 44 bytes into a 32-byte stack buffer, which creates the condition for the overflow. After sending 32 bytes, the next 8 will overwrite the saved frame pointer, and then the next 4-bytes will be used as the top half of the return address (read_secret). Fortunately, the bottom half of the return address will still just be null bytes anyways, so it doesn't matter that we can't overwrite that half of the address.
