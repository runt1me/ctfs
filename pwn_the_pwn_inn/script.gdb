# get rid of gross percent signs
set disassembly-flavor intel

# Breakpoint on shared library load
# catch load

# Set a value in gdb
# set {int}0x08049724=0x080484b4

# Run until the .so is loaded
break __stack_chk_fail
break *vuln+95
run < <(python challenge.py)

