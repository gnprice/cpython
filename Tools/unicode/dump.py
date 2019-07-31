
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


# Size of grid in one Braille character.
cell_dots = Dims(2, 4)

# Display choices we make: shape/size of each level of block.
block0_cells = Dims(2, 1)
block1_block0 = Dims(4, 4)
block2_block1 = Dims(4, 4)
block3_block2 = Dims(4, 4)

sepx = ['', '', ' ', '   ']
sepy = ['', '', '\n', '\n\n']


predicate = lambda ch: ch.isalnum()

base_codepoint = 0x0000


braille_base = ord('\u2800')  # BRAILLE PATTERN BLANK

# More facts about Braille in Unicode: the display coordinates
# of the single dot in the glyph for `chr(braille_base + (1 << i))`.
cell_offsets_yx = [(0,0), (1,0), (2,0), (0,1), (1,1), (2,1), (3,0), (3,1)]



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


block0_dots = block0_cells * cell_dots
block1_dots = block1_block0 * block0_dots
block2_dots = block2_block1 * block1_dots

block1_cells = block1_block0 * block0_cells
block2_cells = block2_block1 * block1_cells
block3_cells = block3_block2 * block2_cells

cell_offsets = [y*block0_dots.w + x for y, x in cell_offsets_yx]

grid = [
    Grid(block0_cells, cell_dots),
    Grid(block1_block0, block0_dots),
    Grid(block2_block1, block1_dots),
    Grid(block3_block2, block2_dots),
]

width = []
width.append((1 + len(sepx[0])) * block0_cells.w - len(sepx[0]))
width.append((width[-1] + len(sepx[1])) * block1_block0.w - len(sepx[1]))
width.append((width[-1] + len(sepx[2])) * block2_block1.w - len(sepx[2]))
width.append((width[-1] + len(sepx[3])) * block3_block2.w - len(sepx[3]))


def u_plus(codepoint: int) -> str:
    return 'U+{:04x}'.format(codepoint)


def show_cell(base: int) -> str:
    cell_codepoints = (base + offset for offset in cell_offsets)
    cell_bits = sum(predicate(chr(c)) << i
                    for i, c in enumerate(cell_codepoints))
    return chr(braille_base + cell_bits)


def show_block0(base: int) -> str:
    return sepx[0].join(show_cell(cell_base)
                        for cell_base in range(base, base + block0_dots.w, cell_dots.w))


def assemble_line(lvl: int, base: int, each: Callable[[int], str]) -> str:
    if lvl > 3:
        return ' {}\n'.format(each(base))
    assert(1 <= lvl <= 3)
    return assemble_line(lvl + 1, base,
        lambda base: sepx[lvl].join(
            each(inner_base) for inner_base in grid[lvl].iterx(base)))


def header_block1(base: int) -> str:
    return '{:{}}'.format(u_plus(base), width[1])


def header_block2(base: int) -> str:
    last = base + block2_dots.len - 1
    # return '{:^{}}'.format(u_plus(base), width[2])
    # return '{:^{}}'.format(' /== {} ==\\'.format(u_plus(base)), width[2])
    return '{:^{}}'.format(
        ' {} .. {}'.format(u_plus(base), u_plus(last)), width[2])
    #return '{:>{}}'.format(
    #    '....{}'.format(u_plus(last)), width[2])


def header(lvl: int, base: int) -> str:
    if lvl == 2:
        return assemble_line(lvl + 1, base, header_block2)
    elif lvl == 1:
        return assemble_line(lvl + 1, base, header_block1)
    else:
        return ''


def assemble_y(lvl: int, base: int, each: Callable[[int], str]) -> str:
    return sepy[lvl].join(each(inner_base) for inner_base in grid[lvl].itery(base))


def show_block3l(lvl: int, base: int) -> str:
    if lvl < 0:
        return assemble_line(1, base, show_block0)
    return header(lvl, base) + assemble_y(lvl, base,
                                          lambda base: show_block3l(lvl - 1, base))


print(show_block3l(3, base_codepoint))
