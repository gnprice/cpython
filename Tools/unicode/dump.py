

class Grid:
    def __init__(self, w: int, h: int) -> None:
        self.w = w
        self.h = h
        self.len = w * h

    def __mul__(self, other: 'Grid') -> 'Grid':
        return Grid(self.w * other.w,
                    self.h * other.h)

    def __floordiv__(self, other: 'Grid') -> 'Grid':
        return Grid(self.w // other.w,
                    self.h // other.h)

    def __repr__(self) -> str:
        return f'Grid({self.w}, {self.h})'


# Display choice we make: shape/size of a block.  Powers of 2.
block1_runes = Grid(0x20, 0x20)  # min 2, 4
block2_block1 = Grid(2, 2)
num_block2 = 0x2


braille_base = ord('\u2800')  # BRAILLE PATTERN BLANK

# Size of grid in one Braille character.
braille_dots = Grid(2, 4)

# More facts about Braille in Unicode: the display coordinates
# of the single dot in the glyph for `chr(braille_base + (1 << i))`.
cell_offsets_yx = [(0,0), (1,0), (2,0), (0,1), (1,1), (2,1), (3,0), (3,1)]


cell_offsets = [y*block1_runes.w + x for y, x in cell_offsets_yx]

block1_cells = block1_runes // braille_dots


row_size_codepoints = braille_dots.h * block1_runes.w
block_size_codepoints = block1_runes.len
assert(block_size_codepoints == block1_cells.h * row_size_codepoints)


block2_cells = block2_block1 * block1_cells
block2_runes = block2_block1 * block1_runes

gridline_size_codepoints = block2_block1.w * row_size_codepoints
gridrow_size_codepoints = block2_block1.w * block1_runes.len
assert(gridrow_size_codepoints == block1_cells.h * gridline_size_codepoints)
grid_size_codepoints = block2_runes.len


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
        for cell_base in range(base, base + block1_runes.w, braille_dots.w))


def grid_row(base: int) -> str:
    heading = ' {}\n'.format(
        ' '.join('{:{}}'.format(u_plus(base + x * block1_runes.len),
                                block1_cells.w)
                 for x in range(block2_block1.w)))
    return heading \
        + ''.join(' {}\n'.format(
            ' '.join(braille_row(base
                                 + x * block1_runes.len
                                 + y * braille_dots.h * block1_runes.w)
                     for x in range(block2_block1.w)))
                  for y in range(block1_cells.h))


def grid(base: int) -> str:
    return '\n'.join(grid_row(base + i * block1_runes.h * block2_runes.w)
                     for i in range(block2_block1.h)) \
        + '\n'


for i_block2 in range(num_block2):
    print(grid(i_block2 * block2_runes.len))
