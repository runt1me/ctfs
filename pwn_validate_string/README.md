# Description

With no ASLR, this is not too hard, but with ASLR, I haven't figured it out yet. Basic idea is to try and leak a libc address using puts, but then trying to jump back to main() doesn't work easily because the input buffer is taken as argv[1], so I can't provide a new one without restarting the program and thus getting a new address space. Next idea would be to somehow leak the address, return to read@plt, and send a stage two payload into stdin that way, but seems complicated.
