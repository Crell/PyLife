import unittest
import pytest

import world


neighborTestData = [
    [[world.Organism(True)], False]

]

# Organism tests


def test_is_alive():
    default = world.Organism()
    assert default.isAlive()

    dead = world.Organism(False)
    assert not dead.isAlive()

    alive = world.Organism(True)
    assert alive.isAlive()


@pytest.mark.parametrize("start,neighbors,expected",  [
    (False, [world.Organism(True)], False),
    (False, [world.Organism(False)], False),
    (False, [world.Organism(False), world.Organism(True)], False),
    (False, [world.Organism(False), world.Organism(True)], False),
    (False, [world.Organism(True), world.Organism(True)], False),
    (False, [world.Organism(True), world.Organism(True)], False),
    (True, [world.Organism(True), world.Organism(True)], True),
    (False, [world.Organism(True), world.Organism(True), world.Organism(True)], True),
    (True, [world.Organism(True), world.Organism(True), world.Organism(True), world.Organism(True)], False),
])
def test_update_value(start, neighbors, expected):
        o = world.Organism(start)

        o.setSourceNeighbors(neighbors)
        o.updateValue()
        assert expected == o.isAlive()


class TestWorld(unittest.TestCase):

    def test_createWorld(self):
        w = world.World(5, 10)
        assert isinstance(w.grid, dict)
        assert isinstance(w.grid[0], dict)
        assert isinstance(w.grid[1], dict)

    def test_populateRocks(self):
        w = world.World(5, 10)
        w.placeRock(2, 3) \
            .placeRock(1, 1) \
            .placeRock(5, 10)
        assert isinstance(w.cellAt(2, 3), world.Rock)
        assert isinstance(w.cellAt(1, 1), world.Rock)
        assert isinstance(w.cellAt(5, 10), world.Rock)

    def test_populateOrganisms(self):
        w = world.World(5, 10)
        w.placeOrganism(2, 3) \
            .placeOrganism(1, 1, world.Organism(False)) \
            .placeOrganism(5, 10)

        self.assertTrue(w.cellAt(2, 3).isAlive())
        self.assertFalse(w.cellAt(1, 1).isAlive())
        self.assertTrue(w.cellAt(5, 10).isAlive())

    def test_step(self):
        w = world.World(5, 10)
        w.placeOrganism(2, 2).placeOrganism(2, 3).placeOrganism(2, 4)
        w.step()

        # Two cells should have died
        self.assertFalse(w.cellAt(2, 2).isAlive())
        self.assertFalse(w.cellAt(2, 4).isAlive())

        # Two cells should be born
        self.assertTrue(w.cellAt(1, 3).isAlive())
        self.assertTrue(w.cellAt(3, 3).isAlive())

        # One cell doesn't change
        self.assertTrue(w.cellAt(2, 3).isAlive())


if __name__ == '__main__':
    unittest.main()
