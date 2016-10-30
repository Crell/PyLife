import unittest
import pytest

import world

# Organism tests

def test_is_alive():
    default = world.Organism()
    assert default.isAlive()

    dead = world.Organism(False)
    assert not dead.isAlive()

    alive = world.Organism(True)
    assert alive.isAlive()

# Cell tests

@pytest.mark.parametrize("start,neighbors,expected",  [
    (False, [world.Cell(world.Organism(True))], False),
    (False, [world.Cell(world.Organism(False))], False),
    (False, [world.Cell(world.Organism(False)), world.Cell(world.Organism(True))], False),
    (False, [world.Cell(world.Organism(False)), world.Cell(world.Organism(True))], False),
    (False, [world.Cell(world.Organism(True)), world.Cell(world.Organism(True))], False),
    (False, [world.Cell(world.Organism(True)), world.Cell(world.Organism(True))], False),
    (True, [world.Cell(world.Organism(True)), world.Cell(world.Organism(True))], True),
    (False, [world.Cell(world.Organism(True)), world.Cell(world.Organism(True)), world.Cell(world.Organism(True))], True),
    (True, [world.Cell(world.Organism(True)), world.Cell(world.Organism(True)), world.Cell(world.Organism(True)), world.Cell(world.Organism(True))], False),
])
def test_update_value(start, neighbors, expected):
        # The state of the local organism doesn't matter, it's the mirror organism that matters.
        c = world.Cell(None, world.Organism(start))

        c.setSourceNeighbors(neighbors)
        c.updateValue()
        assert expected == c.isAlive()


# World tests

def test_create_world():
    w = world.World(5, 10)
    assert isinstance(w.grid, dict)
    assert isinstance(w.grid[0], dict)
    assert isinstance(w.grid[1], dict)
    assert isinstance(w.grid[0][(1, 1)], world.Cell)
    assert isinstance(w.grid[0][(1, 1)].occupant, world.Organism)


def test_populateRocks():
    w = world.World(5, 10)
    w.placeRock(2, 3) \
        .placeRock(1, 1) \
        .placeRock(4, 9)

    assert isinstance(w.cellAt(4, 4), world.Occupant)
    assert isinstance(w.cellAt(2, 3), world.Rock)
    assert isinstance(w.cellAt(1, 1), world.Rock)
    assert isinstance(w.cellAt(4, 9), world.Rock)


def test_populateOrganisms():
    w = world.World(5, 10)
    w.placeOrganism(2, 3) \
        .placeOrganism(1, 1, world.Organism(False)) \
        .placeOrganism(4, 9)

    assert w.cellAt(2, 3).isAlive()
    assert not w.cellAt(1, 1).isAlive()
    assert w.cellAt(4, 9).isAlive()

def test_get_cell_neighbors():
    w = world.World(3, 3)
    assert len(w.getCellNeighbors(w.grid[1], 0, 0)) == 3
    assert len(w.getCellNeighbors(w.grid[1], 0, 1)) == 5
    assert len(w.getCellNeighbors(w.grid[1], 0, 2)) == 3
    assert len(w.getCellNeighbors(w.grid[1], 1, 0)) == 5
    assert len(w.getCellNeighbors(w.grid[1], 1, 1)) == 8
    assert len(w.getCellNeighbors(w.grid[1], 1, 2)) == 5
    assert len(w.getCellNeighbors(w.grid[1], 2, 0)) == 3
    assert len(w.getCellNeighbors(w.grid[1], 2, 1)) == 5
    assert len(w.getCellNeighbors(w.grid[1], 2, 2)) == 3



def test_step():
    w = world.World(5, 10)
    w.placeOrganism(2, 2)\
        .placeOrganism(2, 3)\
        .placeOrganism(2, 4)
    w.step()

    # Two cells should have died
    assert not w.cellAt(2, 2).isAlive()
    assert not w.cellAt(2, 4).isAlive()

    # Two cells should be born
    assert w.cellAt(1, 3).isAlive()
    assert w.cellAt(3, 3).isAlive()

    # One cell doesn't change
    assert w.cellAt(2, 3).isAlive()


if __name__ == '__main__':
    unittest.main()
