import random


class Minesweeper:
    def __init__(self, difficulty):
        columns, rows, mines_number = difficulty
        self.board = [(x, y) for x in range(columns) for y in range(rows)]
        self.neighbours = self.get_neighbours()
        self.mines = self.set_mines(columns, rows, mines_number)
        self.empty_field = columns * rows - mines_number

        self.opened = []
        self.flagged = set()

        self.mines_near = {}

    def get_neighbours(self):
        """Return all neighbours of one cell"""
        neighbours = {}
        for (x, y) in self.board:
            neighbours[(x, y)] = [(a, b) for a in [x-1, x, x+1]
                                  for b in [y-1, y, y+1]
                                  if (a, b) != (x, y) if (a, b) in self.board]
        return neighbours

    def set_mines(self, columns, rows, mines_number):
        """Return where are the mines"""
        mine_fields = []
        while len(mine_fields) < mines_number:
            random_mine = (random.randrange(columns),
                           random.randrange(rows))
            while random_mine in mine_fields:
                random_mine = (random.randrange(columns),
                               random.randrange(rows))

            mine_fields.append(random_mine)

        return mine_fields

    def open(self, cell):
        if cell in self.opened:
            return

        if cell in self.mines:
            return False
        else:
            mines_around = 0
            for spot in self.mines:
                if spot in self.neighbours[cell]:
                    mines_around += 1
            self.mines_near[cell] = mines_around
            self.opened.append(cell)
            if self.mines_near[cell] == 0:
                for field in self.neighbours[cell]:
                    self.open(field)
            return True

    def flag(self, cell):
        self.flagged.add(cell)

    def check_for_win(self):
        unopened_fields = set([field for field in self.board
                              if field not in self.opened
                              if field not in self.flagged])
        mines_left = set([field for field in self.mines
                         if field not in self.flagged])
        if unopened_fields == mines_left:
            for mine in mines_left:
                self.flagged.add(mine)
        return self.flagged == set(self.mines) and \
            len(self.opened) == self.empty_field

    def smart_open(self, cell):
        if cell in self.opened or cell in self.mines:
            return
        self.open(cell)
        self.smart_check(cell)
        for field in self.neighbours[cell]:
            self.smart_check(field)

    def smart_flag(self, cell):
        if cell in self.flagged:
            return
        self.flag(cell)
        for field in self.neighbours[cell]:
            self.smart_check(field)

    def smart_check(self, cell):
        """Open/Flag neighbours of cell if possible."""
        if cell not in self.opened:
            return
        flagged_neighbours = []
        unopened = []
        other_cells = []
        for field in self.neighbours[cell]:
            if field in self.flagged:
                flagged_neighbours.append(field)
            if field not in self.opened:
                unopened.append(field)
            if field not in self.opened and field not in self.flagged:
                other_cells.append(field)

        if self.mines_near[cell] == len(flagged_neighbours):
            for field in other_cells:
                self.smart_open(field)
            return
        if self.mines_near[cell] == len(flagged_neighbours) or \
           self.mines_near[cell] == len(unopened):
            for field in unopened:
                self.smart_flag(field)
