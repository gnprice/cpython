
for line in range(0x20):
    line_base = line * 0x100
    s = f'U+{line:02x}··:\n'
    for row in range(4):
        for stick in range(4):
            s += ' '
            for i in range(0x10):
                char = chr(line_base + 0x40 * row + 0x10 * stick + i)
                s += ".X"[char.isprintable()]
        s += '\n'
    print(s)
