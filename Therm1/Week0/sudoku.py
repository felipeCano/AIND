

class Sudoku:

    def __init__(self):
        self.rows = 'ABCDEFGHI'
        self.cols = '123456789'
        self.boxes = self.cross(self.rows, self.cols)
        self.row_units = [self.cross(r, self.cols) for r in self.rows]
        self.column_units = [self.cross(self.rows, c) for c in self.cols]
        self.square_units = [
            self.cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI')
            for cs in ('123', '456', '789')
        ]
        self.unitlist = self.row_units + self.column_units + self.square_units
        self.units = dict((s, [u for u in self.unitlist if s in u]) for s in self.boxes)
        self.peers = dict((s, set(sum(self.units[s], [])) - set([s])) for s in self.boxes)
        self.values = None
        self.stalled = False

    def cross(self, a, b):
        return [s + t for s in a for t in b]

    def grid_values(self, values):
        values = dict(zip(self.boxes, values))
        values = {k: self.cols if v == '.' else v for (k, v) in values.items()}
        return values

    def eliminate(self, values):
        if not values:
            values = self.values

        solved_boxes = [box for box in values.keys() if len(values[box]) == 1]
        for box in solved_boxes:
            n = values[box]
            for peer in self.peers[box]:
                values[peer] = values[peer].replace(n, '')
        return values

    def one_choice(self, values):
        if not values:
            values = self.values

        for unit in self.unitlist:
            for n in '123456789':
                boxes = [box for box in unit if n in values[box]]
                if len(boxes) == 1:
                    values[boxes[0]] = n
        return values

    def reduce_puzzle(self, values):
        if not values:
            values = self.values

        while not self.stalled:
            # Check how many boxes have a determined value
            solved_values_before = len([box for box in values.keys() if len(values[box])])

            # Eliminate strategy
            self.eliminate()

            # One choice strategy
            self.one_choice()

        return

    def display(self, values):
        """
        Display the values as a 2-D grid.
        Input: The sudoku in dictionary form
        Output: None
        """
        if not values:
            values = self.values

        width = 1 + max(len(values[s]) for s in self.boxes)
        line = '+'.join(['-' * (width * 3)] * 3)
        for r in self.rows:
            g = ''.join(values[r + c].center(width) + ('|' if c in '36' else '') for c in self.cols)
            print(g)
            if r in 'CF':
                print(line)
        return

    def solve(self, values):
        self.values = values
        self.reduce_puzzle()
        return True


if __name__ == '__main__':
    sudoku = Sudoku()
    print(sudoku.display('..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'))
    # import ipdb; ipdb.set_trace()
