
from typing import *


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
block1_dots = Grid(0x20, 0x20)  # min 2, 4
block2_block1 = Grid(2, 2)
num_block2 = 0x2


braille_base = ord('\u2800')  # BRAILLE PATTERN BLANK

# Size of grid in one Braille character.
cell_dots = Grid(2, 4)

# More facts about Braille in Unicode: the display coordinates
# of the single dot in the glyph for `chr(braille_base + (1 << i))`.
cell_offsets_yx = [(0,0), (1,0), (2,0), (0,1), (1,1), (2,1), (3,0), (3,1)]


cell_offsets = [y*block1_dots.w + x for y, x in cell_offsets_yx]

block1_cells = block1_dots // cell_dots
block2_cells = block2_block1 * block1_cells
block2_dots = block2_block1 * block1_dots


def u_plus(codepoint: int) -> str:
    return 'U+{:04x}'.format(codepoint)


def show_cell(base: int) -> str:
    cell_codepoints = (base + offset for offset in cell_offsets)
    cell_bits = sum(chr(c).isprintable() << i
                    for i, c in enumerate(cell_codepoints))
    return chr(braille_base + cell_bits)


def show_block10(base: int) -> str:
    return ''.join(
        show_cell(cell_base)
        for cell_base in range(base, base + block1_dots.w, cell_dots.w))


def block20_block10_bases(base: int) -> Iterable[int]:
    return range(base, base + block2_block1.w * block1_dots.len, block1_dots.len)


def show_block20(base: int) -> str:
    return ' '.join(
        show_block10(block10_base)
        for block10_base in block20_block10_bases(base))


def block21_block20_bases(base: int) -> Iterable[int]:
    return range(base, base + block1_dots.len, block1_cells.w * cell_dots.len)


def show_block21(base: int) -> str:
    heading = ' {}\n'.format(
        ' '.join('{:{}}'.format(u_plus(block10_base),
                                block1_cells.w)
                 for block10_base in block20_block10_bases(base)))
    return heading \
        + ''.join(' {}\n'.format(show_block20(block20_base))
                  for block20_base in block21_block20_bases(base))


def block2_block21_bases(base: int) -> Iterable[int]:
    return range(base, base + block2_dots.len, block2_block1.w * block1_dots.len)


def show_block2(base: int) -> str:
    return '\n'.join(show_block21(block21_base)
                     for block21_base in block2_block21_bases(base)) \
        + '\n'


def all_block2_bases(base: int) -> Iterable[int]:
    return range(base, base + num_block2 * block2_dots.len, block2_dots.len)


def show_all(base: int) -> str:
    return '\n'.join(show_block2(block2_base)
                     for block2_base in all_block2_bases(base)) \


print(show_all(0))
