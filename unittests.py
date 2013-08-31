import unittest

import random

import minesweeper


B = (9, 9, 10)


class MinesweeperTest(unittest.TestCase):
    def test_get_neighbours(self):
        A = minesweeper.Minesweeper(B)
        A.mines = [(4, 2), (0, 4), (2, 0), (5, 4), (4, 6),
                   (2, 1), (7, 2), (7, 8), (1, 1), (1, 7)]
        expected_neighbours = set([(2, 2), (2, 3), (2, 4), (3, 2),
                                   (3, 4), (4, 2), (4, 3), (4, 4)])

        self.assertEqual(set(A.neighbours[(3, 3)]), expected_neighbours)

    def test_set_mines(self):
        A = minesweeper.Minesweeper(B)
        A.mines = [(4, 2), (0, 4), (2, 0), (5, 4), (4, 6),
                   (2, 1), (7, 2), (7, 8), (1, 1), (1, 7)]
        self.assertEqual(len(A.mines), 10)

    def test_open(self):
        A = minesweeper.Minesweeper(B)
        A.mines = [(4, 2), (0, 4), (2, 0), (5, 4), (4, 6),
                   (2, 1), (7, 2), (7, 8), (1, 1), (1, 7)]

        self.assertTrue(A.open((3, 3)))
        self.assertFalse(A.open((3, 3)))

        mine = A.mines[5]

        self.assertFalse(A.open(mine))

        self.assertTrue(A.open((3, 5)))

    def test_flag(self):
        A = minesweeper.Minesweeper(B)
        A.mines = [(4, 2), (0, 4), (2, 0), (5, 4), (4, 6),
                   (2, 1), (7, 2), (7, 8), (1, 1), (1, 7)]
        A.flag((3, 3))

        self.assertTrue((3, 3) in A.flagged)

    def test_check_for_win(self):
        A = minesweeper.Minesweeper(B)
        A.mines = [(4, 2), (0, 4), (2, 0), (5, 4), (4, 6),
                   (2, 1), (7, 2), (7, 8), (1, 1), (1, 7)]
        for (x, y) in A.board:
            if (x, y) not in A.mines:
                A.open((x, y))

        self.assertTrue(A.check_for_win())

    def test_smart_open(self):
        A = minesweeper.Minesweeper(B)
        A.mines = [(4, 2), (0, 4), (2, 0), (5, 4), (4, 6),
                   (2, 1), (7, 2), (7, 8), (1, 1), (1, 7)]

        self.assertFalse(A.smart_open((4, 2)))

        A.smart_open((3, 3))
        self.assertTrue((3, 3) in A.opened)

    def test_smart_flag(self):
        A = minesweeper.Minesweeper(B)
        A.mines = [(4, 2), (0, 4), (2, 0), (5, 4), (4, 6),
                   (2, 1), (7, 2), (7, 8), (1, 1), (1, 7)]
        A.flag((2, 0))

        self.assertFalse(A.smart_flag((2, 0)))

        A.smart_flag((0, 4))
        self.assertTrue((0, 4) in A.flagged)

    def test_smart_check(self):
        A = minesweeper.Minesweeper(B)
        A.mines = [(4, 2), (0, 4), (2, 0), (5, 4), (4, 6),
                   (2, 1), (7, 2), (7, 8), (1, 1), (1, 7)]
        A.open((1, 4))
        A.flag((0, 4))
        A.smart_check((1, 4))

        self.assertTrue((1, 3) in A.opened)

if __name__ == '__main__':
    unittest.main()
