from csp import *
# from notebook import *


def different_values_constraint(A, a, B, b):
    """A constraint saying two neighboring variables must differ in value."""
    return a != b


def flatten(seqs):
    return sum(seqs, [])


_SIZEA = 4
_RA = list(range(_SIZEA))
_CELLA = itertools.count().__next__
_BGRIDA = [[[[_CELLA() for x in _RA] for y in _RA] for bx in _RA] for by in _RA]
_BOXESA = flatten([list(map(flatten, brow)) for brow in _BGRIDA])
_ROWSA = flatten([list(map(flatten, zip(*brow))) for brow in _BGRIDA])
_COLSA = list(zip(*_ROWSA))

_NEIGHBORSA = {v: set() for v in flatten(_ROWSA)}
for unit in map(set, _BOXESA + _ROWSA + _COLSA):
    for v in unit:
        _NEIGHBORSA[v].update(unit - {v})


class SudokuParam(CSP):
    Size = _SIZEA
    R = _RA
    Cell = _CELLA
    bgrid = _BGRIDA
    boxes = _BOXESA
    rows = _ROWSA
    cols = _COLSA
    neighbors = _NEIGHBORSA

    def __init__(self, grid):
        """Build a Sudoku problem from a string representing the grid:
        the digits 1-9 denote a filled cell, '.' or '0' an empty one;
        other characters are ignored."""

        numStr = [str(x) for x in
                  ['01', '02', '03', '04', '05', '06', '07', '08', '09'] + list(range(10, (_SIZEA * _SIZEA) + 1))]
        squares = iter(re.findall(r'\d\d|\.', grid))
        domains = {var: [ch] if ch in numStr else numStr
                   for var, ch in zip(flatten(self.rows), squares)}
        for _ in squares:
            raise ValueError("Not a Sudoku grid", grid)  # Too many squares
        CSP.__init__(self, None, domains, self.neighbors, different_values_constraint)

    def display(self, assignment):
        def show_box(box): return [' '.join(map(show_cell, row)) for row in box]

        def show_cell(cell): return str(assignment.get(cell, '.'))

        def abut(lines1, lines2): return list(
            map(' | '.join, list(zip(lines1, lines2))))

        print('\n------+-------+------\n'.join(
            '\n'.join(reduce(
                abut, map(show_box, brow))) for brow in self.bgrid))


_SIZEB = 10
_RB = list(range(_SIZEB))
_CELLB = itertools.count().__next__
_BGRIDB = [[[[_CELLB() for x in _RB] for y in _RB] for bx in _RB] for by in _RB]
_BOXESB = flatten([list(map(flatten, brow)) for brow in _BGRIDB])
_ROWSB = flatten([list(map(flatten, zip(*brow))) for brow in _BGRIDB])
_COLSB = list(zip(*_ROWSB))

_NEIGHBORSB = {v: set() for v in flatten(_ROWSB)}
for unit in map(set, _BOXESB + _ROWSB + _COLSB):
    for v in unit:
        _NEIGHBORSB[v].update(unit - {v})


class Sudoku100x100(CSP):
    Size = _SIZEB
    R = _RB
    Cell = _CELLB
    bgrid = _BGRIDB
    boxes = _BOXESB
    rows = _ROWSB
    cols = _COLSB
    neighbors = _NEIGHBORSB

    def __init__(self, grid):
        """Build a Sudoku problem from a string representing the grid:
        the digits 1-9 denote a filled cell, '.' or '0' an empty one;
        other characters are ignored."""
        numStr = ['0'+str(x) for x in
                  ['01', '02', '03', '04', '05', '06', '07', '08', '09'] + list(range(10, (_SIZEB * _SIZEB) + 1)) + ['100']]
        squares = iter(re.findall(r'\d\d\d|\.', grid))
        domains = {var: [ch] if ch in numStr else numStr
                   for var, ch in zip(flatten(self.rows), squares)}
        for _ in squares:
            raise ValueError("Not a Sudoku grid", grid)  # Too many squares
        CSP.__init__(self, None, domains, self.neighbors, different_values_constraint)

    def display(self, assignment):
        def show_box(box): return [' '.join(map(show_cell, row)) for row in box]

        def show_cell(cell): return str(assignment.get(cell, '.'))

        def abut(lines1, lines2): return list(
            map(' | '.join, list(zip(lines1, lines2))))

        print('\n------+-------+------\n'.join(
            '\n'.join(reduce(
                abut, map(show_box, brow))) for brow in self.bgrid))