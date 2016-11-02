
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

    occupant = None
    mirrorCell = None

    # In Python 3.4 we'd use an Enum here
    state = 'E'

    def __init__(self, state = 'E', mirror = None):
        self.state = state
        self.mirrorCell = mirror

    def setMirrorCell(self, cell):
        self.mirrorCell = cell
        return self

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
        neighborStates = map(str, self.neighbors)
        counts = {item: neighborStates.count(item) for item in neighborStates}

        # Ensure certain keys are mentioned so there's no missing key error later.
        for key in ['F', 'R', 'E', currentState]:
            if not key in counts:
                counts[key] = 0

        liveNeighbors = len([n for n in self.neighbors if n.state.isdigit()])

        # See if a cell should be born.
        if currentState == 'E' and liveNeighbors in range(1, 4) and liveNeighbors + counts['F'] >=3:
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
        grid = self.newgrid(rows, cols)

        self.grid[0] = copy.deepcopy(grid)
        self.grid[1] = copy.deepcopy(grid)

        self.setGridSourceNeighbors(self.grid[0], self.grid[1])
        self.setGridSourceNeighbors(self.grid[1], self.grid[0])

        self.setGridMirrors(self.grid[0], self.grid[1])
        self.setGridMirrors(self.grid[1], self.grid[0])

    def setGridMirrors(self, source, target):
        for (x, y), cell, in source.iteritems():
            cell.setMirrorCell(target[(x, y)])

    def setGridSourceNeighbors(self, grid, target):
        for (x, y), cell, in grid.iteritems():
            cell.setSourceNeighbors(self.getCellNeighbors(target, (x, y)))

    def getCellNeighbors(self, target, coord):
        x = coord[0]
        y = coord[1]
        x_range = range(max(x-1, 0), min(x+1, self.rows-1)+1)
        y_range = range(max(y-1, 0), min(y+1, self.cols-1)+1)

        neighbors = [target[(i, j)]
                     for i in x_range
                     for j in y_range
                     if not (i == x and j == y)]
        return neighbors

    def activeGrid(self):
        return self.grid[self.current]

    def inactiveGrid(self):
        return self.grid[(self.current + 1) % 2]

    def cellAt(self, coord):
        active = self.activeGrid()
        return active[coord]

    def place(self, state, coord):
        cell = self.activeGrid()[coord].state = state
        # Food and Rocks are persistent, so set them on both grids.
        if state in ['F', 'R']:
            self.inactiveGrid()[coord].state = state

        return self

    def step(self):
        nextCurrent = (self.current + 1) % 2
        nextGrid = self.grid[nextCurrent]
        # @todo Turn this into a map call if possible.
        for coord, cell in nextGrid.iteritems():
            cell.updateValue()

        self.current = nextCurrent
        return

    def newgrid(self, rows, cols):
        grid = {}
        # @todo There is probably a comprehension version of this.
        for r in range(0, rows):
            for c in range(0, cols):
                grid[(r, c)] = Cell()
        return grid

    def __str__(self):
        grid = self.activeGrid()
        out = ''
        out += 'On grid ' + str(self.current) + ':\n'
        for x in range(self.rows):
            for y in range(self.cols):
                out += str(grid[(x, y)])
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
