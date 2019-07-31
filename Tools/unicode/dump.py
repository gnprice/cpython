
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
block_rel = [
    Dims(2, 1),
    Dims(4, 4),
    Dims(2, 2),
    Dims(2, 2),
    Dims(2, 2),
    Dims(2, 2),
]
num_levels = len(block_rel)

sepx = ['', '', ' ', '   ', '     ', '       ']
sepy = ['', '', '\n', '\n\n', '\n\n\n', '\n\n\n\n\n']


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


block_dots = [cell_dots]
for i in range(num_levels - 1):
    block_dots.append(block_dots[-1] * block_rel[i])

cell_offsets = [y*block_dots[1].w + x for y, x in cell_offsets_yx]

grid = [Grid(block_rel[i], block_dots[i])
        for i in range(num_levels)]

width = []; last_width = 1
for i in range(num_levels):
    width.append((last_width + len(sepx[i])) * block_rel[i].w - len(sepx[i]))
    last_width = width[-1]


def u_plus(codepoint: int) -> str:
    return 'U+{:04x}'.format(codepoint)


def show_cell(base: int) -> str:
    cell_codepoints = (base + offset for offset in cell_offsets)
    cell_bits = sum(predicate(chr(c)) << i
                    for i, c in enumerate(cell_codepoints))
    return chr(braille_base + cell_bits)


def show_block0(base: int) -> str:
    return sepx[0].join(show_cell(cell_base)
                        for cell_base in range(base, base + block_dots[1].w, block_dots[0].w))


def assemble_line(lvl: int, base: int, each: Callable[[int], str]) -> str:
    if lvl >= num_levels:
        return ' {}\n'.format(each(base))
    assert(1 <= lvl < num_levels)
    return assemble_line(lvl + 1, base,
        lambda base: sepx[lvl].join(
            each(inner_base) for inner_base in grid[lvl].iterx(base)))


def header_small(lvl: int, base: int) -> str:
    return '{:{}}'.format(u_plus(base), width[lvl])


def header_big(lvl: int, base: int) -> str:
    last = base + block_dots[lvl + 1].len - 1
    # return '{:^{}}'.format(u_plus(base), width[lvl])
    # return '{:^{}}'.format(' /== {} ==\\'.format(u_plus(base)), width[lvl])
    return '{:^{}}'.format(
        ' {} .. {}'.format(u_plus(base), u_plus(last)), width[lvl])
    #return '{:>{}}'.format(
    #    '....{}'.format(u_plus(last)), width[lvl])


header_type = {
    3: header_big,
    1: header_small,
}


def header(lvl: int, base: int) -> str:
    tp = header_type.get(lvl)
    if tp is None:
        return ''
    return assemble_line(lvl + 1, base, lambda base: tp(lvl, base))


def assemble_y(lvl: int, base: int, each: Callable[[int], str]) -> str:
    return sepy[lvl].join(each(inner_base) for inner_base in grid[lvl].itery(base))


def show_block3l(lvl: int, base: int) -> str:
    if lvl < 0:
        return assemble_line(1, base, show_block0)
    return header(lvl, base) + assemble_y(lvl, base,
                                          lambda base: show_block3l(lvl - 1, base))


print(show_block3l(num_levels - 1, base_codepoint))
