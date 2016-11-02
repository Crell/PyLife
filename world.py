
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

"""

class Cell(object):
    neighbors = []

    def __init__(self, state = 'E', mirror = None):
        self._state = state
        self.mirrorCell = mirror

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        self._state = state

    @property
    def mirrorCell(self):
        return self._mirror_cell

    @mirrorCell.setter
    def mirrorCell(self, cell):
        self._mirror_cell = cell

    def setSourceNeighbors(self, cells):
        self.neighbors = cells
        return self

    def updateValue(self):
        # The current state is actually the state of the mirror cell, since that determines
        # whether we may die or may be born.
        currentState = self.mirrorCell.state

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

        self.setGridSources(self.grid[0], self.grid[1])
        self.setGridSources(self.grid[1], self.grid[0])

    def setGridSources(self, grid, target):
        for (x, y), cell, in grid.iteritems():
            cell.mirrorCell = target[(x, y)]
            cell.setSourceNeighbors(self.getCellNeighbors(target, (x, y)))

    def getCellNeighbors(self, target, coord):
        x, y = coord
        return [target[(i, j)]
                     for i in xrange(max(x-1, 0), min(x+1, self.rows-1)+1)
                     for j in xrange(max(y-1, 0), min(y+1, self.cols-1)+1)
                     if not (i == x and j == y)]

    @property
    def activeGrid(self):
        return self.grid[self.current]

    @property
    def inactiveGrid(self):
        return self.grid[(self.current + 1) % 2]

    def cellAt(self, coord):
        return self.activeGrid[coord]

    def place(self, state, coord):
        self.activeGrid[coord].state = state
        # Food and Rocks are persistent, so set them on both grids.
        if state in ['F', 'R']:
            self.inactiveGrid[coord].state = state

        return self

    def step(self):
        # Update all cells in the inactive grid.
        [cell.updateValue() for coord, cell in self.inactiveGrid.iteritems()]
        # Now set that grid active.
        self.current = (self.current + 1) % 2
        return

    def __str__(self):
        out = ''
        out += 'On grid {}:\n'.format(self.current)
        for x in xrange(self.rows):
            for y in xrange(self.cols):
                out += str(self.activeGrid[(x, y)])
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
    assert w.cellAt((1, 3)).state == 'E'
