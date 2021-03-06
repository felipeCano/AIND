from visualize import visualize_assignments


class Sudoku:

    def __init__(self, diagonal=False):
        self.rows = 'ABCDEFGHI'
        self.cols = '123456789'
        self.boxes = self.cross(self.rows, self.cols)
        self.diagonal_units = self.diagonal(self.rows, self.cols)
        self.row_units = [self.cross(r, self.cols) for r in self.rows]
        self.column_units = [self.cross(self.rows, c) for c in self.cols]
        self.square_units = [
            self.cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI')
            for cs in ('123', '456', '789')
        ]
        self.unitlist = self.row_units + self.column_units + self.square_units
        if diagonal is True:
            self.diagonal_units = self.diagonal(self.rows, self.cols)
            self.unitlist = self.unitlist + self.diagonal_units
        self.units = dict((s, [u for u in self.unitlist if s in u]) for s in self.boxes)
        self.peers = dict((s, set(sum(self.units[s], [])) - set([s])) for s in self.boxes)
        self.values = None
        self.assignments = []

    def assign_value(self, values, box, value):
        """
        Please use this function to update your values dictionary!
        Assigns a value to a given box. If it updates the board record it.
        """
        values[box] = value
        if len(value) == 1:
            self.assignments.append(values.copy())
        return values

    def cross(self, a, b):
        return [s + t for s in a for t in b]

    def diagonal(self, a, b):
        rows = list(a)
        cols = list(b)
        left_diag = []
        right_diag = []
        i = 0
        for e in rows:
            left_diag.append(e + cols[i])
            i += 1
        i = 8
        for e in rows:
            right_diag.append(e + cols[i])
            i -= 1
        return [left_diag, right_diag]

    def grid_values(self, values):
        values = dict(zip(self.boxes, values))
        # self.display(values)
        values = {k: self.cols if v == '.' else v for (k, v) in values.items()}
        return values

    def eliminate(self, values, n=None, value=None):
        solved_boxes = [box for box in values.keys() if len(values[box]) == 1]
        for box in solved_boxes:
            n = values[box]
            for peer in self.peers[box]:
                values[peer] = values[peer].replace(n, '')
        return values

    def one_choice(self, values):
        for unit in self.unitlist:
            for n in '123456789':
                boxes = [box for box in unit if n in values[box]]
                if len(boxes) == 1:
                    values[boxes[0]] = n
        return values

    def naked_twins(self, values):
        unit_values = [{box: values[box] for box in unit} for unit in self.unitlist]
        for unit in unit_values:
            twins = {k: v for (k, v) in unit.items() if len(v) == 2 if list(unit.values()).count(v) > 1}
            if len(twins) > 0:
                twin_boxes = list(twins.keys())
                for k, v in twins.items():
                    for box in unit.keys():
                        if box not in twin_boxes:
                            values[box] = values[box].replace(v[0], '')
                            values[box] = values[box].replace(v[1], '')
        return values

    def reduce_puzzle(self, values):
        stalled = False
        while not stalled:
            # Check how many boxes have a determined value
            solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

            # Eliminate strategy
            values = self.eliminate(values)

            # Naked twins strategy
            values = self.naked_twins(values)

            # One choice strategy
            values = self.one_choice(values)

            # Check how many boxes have a determined value, to compare
            solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
            # If no new values were added, stop the loop.
            stalled = solved_values_before == solved_values_after
            # Sanity check, return False if there is a box with zero available values:
            if len([box for box in values.keys() if len(values[box]) == 0]):
                return False
        return values

    def search(self, values):
        values = self.reduce_puzzle(values)
        if values is False:
            return False
        if all(len(values[s]) == 1 for s in self.boxes):
            return values
        n, s = min((len(values[s]), s) for s in self.boxes if len(values[s]) > 1)
        for value in values[s]:
            new_sudoku = values.copy()
            new_sudoku[s] = value
            attempt = self.search(new_sudoku)
            if attempt:
                return attempt

    def display(self, values=None):
        """
        Display the values as a 2-D grid.
        Input: The sudoku in dictionary form
        Output: None
        """
        width = 1 + max(len(values[s]) for s in self.boxes)
        line = '+'.join(['-' * (width * 3)] * 3)
        for r in self.rows:
            g = ''.join(values[r + c].center(width) + ('|' if c in '36' else '') for c in self.cols)
            print(g)
            if r in 'CF':
                print(line)
        try:
            visualize_assignments(self.assignments)
        except SystemExit:
            pass
        except:
            print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
        return

    def solve(self, values, display=False):
        self.values = self.grid_values(values)
        self.display(self.values)
        self.values = self.reduce_puzzle(self.values)
        self.values = self.search(self.values)
        if display is True:
            self.display(self.values)
        else:
            return self.values


if __name__ == '__main__':
    easy_unsolved = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'
    hard_unsolved = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
    diagonal_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    sudoku = Sudoku(diagonal=True)
    sudoku.solve(diagonal_grid, display=True)
