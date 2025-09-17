# get rid of gross percent signs
set disassembly-flavor intel

# Breakpoint on shared library load
# catch load

# Run until the .so is loaded
break *main+70
run < <(python challenge.py)

# Break on my patch byte gadget
# break *0x080485b8

# other commands
# info proc mappings
# maintenance info sections
