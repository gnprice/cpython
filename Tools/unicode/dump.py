
# A "plane" is size 0x10000;
# and a "stick" was size 0x10, for the designers of ASCII.
# Call size 0x100... a "line"?

braille_base = ord('\u2800')  # BRAILLE PATTERN BLANK

# Display coordinates of the single dot in glyph of chr(braille_base + (1 << i)).
cell_offsets_yx = [(0,0), (1,0), (2,0), (0,1), (1,1), (2,1), (3,0), (3,1)]

row_len = 0x10  # In codepoints
cell_offsets = [y*row_len + x for y, x in cell_offsets_yx]

def braille_row(base: int) -> str:
    s = ''
    for cell_base in range(base, base + row_len, 2):
        cell_codepoints = (cell_base + offset for offset in cell_offsets)
        cell_bits = sum(chr(c).isprintable() << i
                        for i, c in enumerate(cell_codepoints))
        cell_repr = chr(braille_base + cell_bits)
        s += cell_repr
    return s

for line in range(0x10):
    line_base = line * 0x100
    s = f'U+{line:02x}··:\n'
    for row in range(0x100 // 4 // row_len):
        s += ' '
        s += braille_row(line_base + 4 * row_len * row)
        s += '\n'
    print(s)
