# get rid of gross percent signs
set disassembly-flavor intel

# Breakpoint on shared library load
catch load

# Breakpoints
break set_score
break *set_score+183

# other commands
# info proc mappings
# maintenance info sections
