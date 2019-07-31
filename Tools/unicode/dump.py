
# A "plane" is size 0x10000;
# and a "stick" was size 0x10, for the designers of ASCII.
# Call size 0x100... a "line"?

# Display choice we make: shape/size of a block.  Powers of 2.
block_width_codepoints = 0x20  # min 2
block_height_codepoints = 0x20  # min 4

num_blocks = 0x10


braille_base = ord('\u2800')  # BRAILLE PATTERN BLANK

# Size of grid in one Braille character.
braille_width = 2
braille_height = 4

# More facts about Braille in Unicode: the display coordinates
# of the single dot in the glyph for `chr(braille_base + (1 << i))`.
cell_offsets_yx = [(0,0), (1,0), (2,0), (0,1), (1,1), (2,1), (3,0), (3,1)]


block_width_cells = block_width_codepoints // braille_width
block_height_cells = block_height_codepoints // braille_height

cell_offsets = [y*block_width_codepoints + x for y, x in cell_offsets_yx]

row_size_codepoints = braille_height * block_width_codepoints
block_size_codepoints = block_height_codepoints * block_width_codepoints
assert(block_size_codepoints == block_height_cells * row_size_codepoints)


def braille_cell(base: int) -> str:
    cell_codepoints = (base + offset for offset in cell_offsets)
    cell_bits = sum(chr(c).isprintable() << i
                    for i, c in enumerate(cell_codepoints))
    return chr(braille_base + cell_bits)


def braille_row(base: int) -> str:
    return ''.join(
        braille_cell(cell_base)
        for cell_base in range(base, base + block_width_codepoints,
                               braille_width))


for block in range(num_blocks):
    block_base = block * block_size_codepoints
    print('U+{:04x}..U+{:04x}:'.format(
        block_base, block_base + block_size_codepoints - 1))
    print(''.join(
        ' {}\n'.format(
            braille_row(block_base + row_size_codepoints * row))
        for row in range(block_height_cells)))
