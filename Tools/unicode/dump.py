
# A "plane" is size 0x10000;
# and a "stick" was size 0x10, for the designers of ASCII.
# Call size 0x100... a "line"?

braille_base = ord('\u2800')
cell_offsets = [0x00, 0x10, 0x20, 0x01, 0x11, 0x21, 0x30, 0x31]

for line in range(0x10):
    line_base = line * 0x100
    s = f'U+{line:02x}··:\n'
    for row in range(4):
        s += ' '
        for cell in range(8):
            cell_base = line_base + 0x40 * row + 2 * cell
            cell_codepoints = (cell_base + offset for offset in cell_offsets)
            cell_bits = sum(chr(c).isprintable() << i
                            for i, c in enumerate(cell_codepoints))
            cell_repr = chr(braille_base + cell_bits)
            s += cell_repr
        s += '\n'
    print(s)
