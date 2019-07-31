
from typing import *


class Dims:
    def __init__(self, w: int, h: int) -> None:
        self.w = w
        self.h = h
        self.len = w * h

    def __mul__(self, other: 'Dims') -> 'Dims':
        return Dims(self.w * other.w,
                    self.h * other.h)

    def __floordiv__(self, other: 'Dims') -> 'Dims':
        return Dims(self.w // other.w,
                    self.h // other.h)

    def __repr__(self) -> str:
        return f'Dims({self.w}, {self.h})'


# Display choice we make: shape/size of a block.  Powers of 2.
block1_dots = Dims(0x20, 0x20)  # min 2, 4
block2_block1 = Dims(2, 2)
num_block2 = 0x2


braille_base = ord('\u2800')  # BRAILLE PATTERN BLANK

# Size of grid in one Braille character.
cell_dots = Dims(2, 4)

# More facts about Braille in Unicode: the display coordinates
# of the single dot in the glyph for `chr(braille_base + (1 << i))`.
cell_offsets_yx = [(0,0), (1,0), (2,0), (0,1), (1,1), (2,1), (3,0), (3,1)]


cell_offsets = [y*block1_dots.w + x for y, x in cell_offsets_yx]


class Grid:
    def __init__(self, outer: Dims, inner: Dims) -> None:
        self.outer = outer
        self.inner = inner
        self.whole = outer * inner
        self.row_len = self.whole.w * self.inner.h
        assert(self.row_len == self.outer.w * self.inner.len)

    def iterx(self, base: int) -> Iterable[int]:
        return range(base, base + self.row_len, self.inner.len)

    def itery(self, base: int) -> Iterable[int]:
        return range(base, base + self.whole.len, self.row_len)


block1_cells = block1_dots // cell_dots
block2_cells = block2_block1 * block1_cells
block2_dots = block2_block1 * block1_dots

block1_grid = Grid(block1_cells, cell_dots)
block2_grid = Grid(block2_block1, block1_dots)
whole_grid = Grid(Dims(1, num_block2), block2_dots)


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


def assemble_x2(base: int, each: Callable[[int], str]) -> str:
    return ' {}\n'.format(
        ' '.join(each(inner_base) for inner_base in block2_grid.iterx(base)))


def assemble_y1(base: int, each: Callable[[int], str]) -> str:
    return ''.join(each(inner_base) for inner_base in block1_grid.itery(base))


def show_block21(base: int) -> str:
    return (
        assemble_x2(base,
                    lambda base: '{:{}}'.format(u_plus(base), block1_cells.w)) 
        + assemble_y1(base, lambda base: assemble_x2(base, show_block10))
    )


def assemble_y2(base: int, each: Callable[[int], str]) -> str:
    return '\n'.join(each(inner_base) for inner_base in block2_grid.itery(base))


def assemble_all(base: int, each: Callable[[int], str]) -> str:
    return '\n\n'.join(each(inner_base) for inner_base in whole_grid.itery(base))


def show_all(base: int) -> str:
    return assemble_all(base, lambda base: assemble_y2(base, show_block21))


print(show_all(0))
