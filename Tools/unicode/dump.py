
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
block0_cells = Dims(2, 1); assert(block0_cells.h == 1)
block1_block0 = Dims(4, 4)
block2_block1 = Dims(4, 4)
block3_block2 = Dims(4, 4)

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

cell_offsets = [y*block0_dots.w + x for y, x in cell_offsets_yx]

block1_grid = Grid(block1_block0, block0_dots)
block2_grid = Grid(block2_block1, block1_dots)
block3_grid = Grid(block3_block2, block2_dots)


def u_plus(codepoint: int) -> str:
    return 'U+{:04x}'.format(codepoint)


def show_cell(base: int) -> str:
    cell_codepoints = (base + offset for offset in cell_offsets)
    cell_bits = sum(predicate(chr(c)) << i
                    for i, c in enumerate(cell_codepoints))
    return chr(braille_base + cell_bits)


def show_block0(base: int) -> str:
    assert(block0_cells.h == 1)
    return ''.join(show_cell(cell_base)
                   for cell_base in range(base, base + block0_dots.w, cell_dots.w))


def show_block10(base: int) -> str:
    return ''.join(show_block0(inner_base) for inner_base in block1_grid.iterx(base))


def assemble_x2(base: int, each: Callable[[int], str]) -> str:
    return ' '.join(each(inner_base) for inner_base in block2_grid.iterx(base))


def assemble_x3(base: int, each: Callable[[int], str]) -> str:
    return ' {}\n'.format(
        '   '.join(each(inner_base) for inner_base in block3_grid.iterx(base)))


def header_block1(base: int) -> str:
    return '{:{}}'.format(u_plus(base), block1_cells.w)


def assemble_y1(base: int, each: Callable[[int], str]) -> str:
    assert(block0_cells.h == 1)
    return ''.join(each(inner_base) for inner_base in block1_grid.itery(base))


def show_block31(base: int) -> str:
    return (
        assemble_x3(base, lambda base: assemble_x2(base, header_block1))
        + assemble_y1(base, lambda base:
            assemble_x3(base, lambda base: assemble_x2(base, show_block10)))
    )


def header_block2(base: int) -> str:
    width = block2_cells.w + (block2_block1.w - 1)
    last = base + block2_dots.len - 1
    # return '{:^{}}'.format(' /== {} ==\\'.format(u_plus(base)), width)
    return '{:^{}}'.format(
        ' {} .. {}'.format(u_plus(base), u_plus(last)), width)
    #return '{:>{}}'.format(
    #    '....{}'.format(u_plus(last)), width)


def assemble_y2(base: int, each: Callable[[int], str]) -> str:
    return '\n'.join(each(inner_base) for inner_base in block2_grid.itery(base))


def show_block32(base: int) -> str:
    return (assemble_x3(base, header_block2) + assemble_y2(base, show_block31))


def assemble_y3(base: int, each: Callable[[int], str]) -> str:
    return '\n\n'.join(each(inner_base) for inner_base in block3_grid.itery(base))


def show_block3(base: int) -> str:
    return assemble_y3(base, show_block32)


print(show_block3(base_codepoint))
