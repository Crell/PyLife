import unittest

import world

class TesteOrganism(unittest.TestCase):
    def test_is_alive(self):
        default = world.Organism()
        self.assertTrue(default.isAlive())

        dead = world.Organism(False)
        self.assertFalse(dead.isAlive())

        alive = world.Organism(True)
        self.assertTrue(alive.isAlive())


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

if __name__ == '__main__':
    unittest.main()
