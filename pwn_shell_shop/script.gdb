# get rid of gross percent signs
set disassembly-flavor intel

# Breakpoint on shared library load
# catch load

# Run until the .so is loaded
break *main+372
