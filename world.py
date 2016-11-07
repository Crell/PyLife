
import copy
import operator

"""

Occupants:
- F: Food
- R: Rock
- E: Empty (Changeable)
- Digit: A player, each species is a different digit

Rules:

Living cell survives if:
(friends + enemies) < 4
friends+food >=2

Cell is born if:
friends + food = 3

@todo Create a coord named-tuple and use that instead of the anonymous coord tuples.

"""


class Cell(object):
    neighbors = []

    def __init__(self, state = 'E', mirror = None):
        self._state = state
        self.mirror_cell = mirror

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        self._state = state

    @property
    def mirror_cell(self):
        return self._mirror_cell

    @mirror_cell.setter
    def mirror_cell(self, cell):
        self._mirror_cell = cell

    def set_source_neighbors(self, cells):
        self.neighbors = cells
        return self

    def update_value(self):
        # The current state is actually the state of the mirror cell, since that determines
        # whether we may die or may be born.
        currentState = self.mirror_cell.state

        # Rocks and Food never change.
        if currentState in ['R', 'F']:
            self.state = currentState
            return self

        # Precompute the neighborStates for performance.
        neighborStates = [str(n) for n in self.neighbors]
        counts = {item: neighborStates.count(item) for item in neighborStates}

        # Ensure certain keys are mentioned so there's no missing key error later.
        for key in ['F', 'R', 'E', currentState]:
            if not key in counts:
                counts[key] = 0

        liveNeighbors = len([n for n in self.neighbors if n.state.isdigit()])

        # See if a cell should be born.
        if currentState == 'E' and liveNeighbors in xrange(1, 4) and liveNeighbors + counts['F'] >=3:
            speciesCounts = {species: counts[species] for species in counts if species.isdigit()}
            candidateState = max(speciesCounts.iteritems(), key=operator.itemgetter(1))[0]
            if (speciesCounts[candidateState] + counts['F']) >= 3:
                self.state = candidateState
        # Otherwise, see if it dies.
        elif currentState.isdigit() and (liveNeighbors >= 4 or (counts[currentState] + counts['F']) < 2):
                self.state = 'E'
        else:
            self.state = currentState

        return self

    def __str__(self):
        return self.state


class World(object):

    grid = dict()
    current = 0
    rows = 0
    cols = 0

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols

        # Initialize a rowsXcols grid of Cells with default values.
        grid = {(x, y): Cell() for x in xrange(self.rows) for y in xrange(self.cols)}

        self.grid[0] = copy.deepcopy(grid)
        self.grid[1] = copy.deepcopy(grid)

        self.set_grid_sources(self.grid[0], self.grid[1])
        self.set_grid_sources(self.grid[1], self.grid[0])

    def set_grid_sources(self, grid, target):
        for (x, y), cell, in grid.iteritems():
            cell.mirror_cell = target[(x, y)]
            cell.set_source_neighbors(self.get_cell_neighbors(target, (x, y)))

    def get_cell_neighbors(self, target, coord):
        x, y = coord
        return [target[(i, j)]
                     for i in xrange(max(x-1, 0), min(x+1, self.rows-1)+1)
                     for j in xrange(max(y-1, 0), min(y+1, self.cols-1)+1)
                     if not (i == x and j == y)]

    @property
    def active_grid(self):
        return self.grid[self.current]

    @property
    def inactive_grid(self):
        return self.grid[(self.current + 1) % 2]

    def cell_at(self, coord):
        return self.active_grid[coord]

    def place(self, state, coord):
        self.active_grid[coord].state = state
        # Food and Rocks are persistent, so set them on both grids.
        if state in ['F', 'R']:
            self.inactive_grid[coord].state = state

        return self

    def step(self):
        # Update all cells in the inactive grid.
        [cell.update_value() for coord, cell in self.inactive_grid.iteritems()]
        # Now set that grid active.
        self.current = (self.current + 1) % 2
        return

    def __str__(self):
        out = ''
        out += 'On grid {}:\n'.format(self.current)
        for x in xrange(self.rows):
            for y in xrange(self.cols):
                out += str(self.active_grid[(x, y)])
            out += '\n'
        return out


if __name__ == '__main__':

    w = World(5, 10)
    w.place('1', (2, 2)) \
        .place('2', (2, 3)) \
        .place('1', (2, 4))

    w.step()

    print w

    # No one should be born.
    assert w.cell_at((1, 3)).state == 'E'
