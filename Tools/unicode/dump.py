
# A "plane" is size 0x10000;
# and a "stick" was size 0x10, for the designers of ASCII.
# Call size 0x100... a "line"?

# Display choice we make: shape/size of a block.  Powers of 2.
block_width_codepoints = 0x20  # min 2
block_height_codepoints = 0x20  # min 4

grid_width_blocks = 0x4
grid_height_blocks = 0x4

num_grids = 0x1


braille_base = ord('\u2800')  # BRAILLE PATTERN BLANK

# Size of grid in one Braille character.
braille_width = 2
braille_height = 4

# More facts about Braille in Unicode: the display coordinates
# of the single dot in the glyph for `chr(braille_base + (1 << i))`.
cell_offsets_yx = [(0,0), (1,0), (2,0), (0,1), (1,1), (2,1), (3,0), (3,1)]


cell_offsets = [y*block_width_codepoints + x for y, x in cell_offsets_yx]

block_width_cells = block_width_codepoints // braille_width
block_height_cells = block_height_codepoints // braille_height

row_size_codepoints = braille_height * block_width_codepoints
block_size_codepoints = block_height_codepoints * block_width_codepoints
assert(block_size_codepoints == block_height_cells * row_size_codepoints)


gridline_size_codepoints = grid_width_blocks * row_size_codepoints
gridrow_size_codepoints = grid_width_blocks * block_size_codepoints
assert(gridrow_size_codepoints == block_height_cells * gridline_size_codepoints)
grid_size_codepoints = grid_height_blocks * gridrow_size_codepoints


def u_plus(codepoint: int) -> str:
    return 'U+{:04x}'.format(codepoint)


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


def grid_row(base: int) -> str:
    heading = ' {}\n'.format(
        ' '.join('{:{}}'.format(u_plus(base + i * block_size_codepoints),
                                block_width_cells)
                 for i in range(grid_width_blocks)))
    return heading \
        + ''.join(' {}\n'.format(
            ' '.join(braille_row(base
                                 + y * row_size_codepoints
                                 + x * gridline_size_codepoints)
                     for x in range(grid_width_blocks)))
                  for y in range(block_height_cells))


def grid(base: int) -> str:
    return '\n'.join(grid_row(base + i * gridrow_size_codepoints)
                     for i in range(grid_height_blocks)) \
        + '\n'


for i_grid in range(num_grids):
    print(grid(i_grid * grid_size_codepoints))
