import pygame
import Minesweeper
from pygame.locals import *
import time


pygame.init()

SCREENWIDTH = 800
SCREENHEIGHT = 600
SQUARE = 25

#difficulties
BEGINNER = (9, 9, 10)
INTERMEDIATE = (16, 16, 40)
ADVANCED = (30, 16, 99)

X_OFF = {BEGINNER: (SCREENWIDTH/2)-(SQUARE*BEGINNER[0]/2),
         INTERMEDIATE: (SCREENWIDTH/2)-(SQUARE*INTERMEDIATE[0]/2),
         ADVANCED: (SCREENWIDTH/2)-(SQUARE*ADVANCED[0]/2)}

Y_OFF = {BEGINNER: (SCREENHEIGHT/2)-(SQUARE*BEGINNER[1]/2),
         INTERMEDIATE: (SCREENHEIGHT/2)-(SQUARE*INTERMEDIATE[1]/2),
         ADVANCED: (SCREENHEIGHT/2)-(SQUARE*ADVANCED[1]/2)}

MINE = pygame.image.load('images\mine_1.png')
FLAG = pygame.image.load('images\mflag.png')
FIELD = (75, 103, 213)
EMPTY = (207, 238, 245)
DIFF_BACKGROUND = pygame.image.load('images\Capture.JPG')

#Colors
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
WHITE = (255, 255, 255)
BACK = (155, 170, 199)
BLUE = (35, 58, 150)
RED = (165, 0, 0)
VIOLET = (64, 0, 128)
SEA_BLUE = (0, 157, 157)
DARK_RED = (169, 0, 0)
BORDO = (81, 0, 0)
ORANGE = (213, 106, 0)
NUM_COLOR = (175, 226, 239)

FONT = pygame.font.SysFont('calibri', 25, True)
FONT_TITLE = pygame.font.SysFont('calibri', 65, True)

NUMBERS = {'0': WHITE, '1': BLUE, '2': GREEN, '3': RED, '4': VIOLET,
           '5': BORDO, '6': SEA_BLUE, '7': DARK_RED, '8': ORANGE}

#messages
TITLE = 'MINESWEEPER'
FIN = 'GAME OVER'
WIN = '!!! WIN !!!'
LOST = 'Sorry, you lost the game. Better luck next time!'
WINNING = 'Congratulations, you won the game!'
RESTART = 'To play again press "R" or press "Esc" for quit!'
CONFIRM = 'If you really want to restart press "R" again'
HELP = "Do you want to play with computer's help:"
CHOOSE = 'CHOOSE DIFFICULTY:'
PRESS_1 = 'For Beginner press 1'
PRESS_2 = 'For Intermediate press 2'
PRESS_3 = 'For Advanced press 3'
Y_N = '(Y)es / (N)o'


class MinesweeperGUI:
    def __init__(self):
        self.field = None
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill(BACK)
        pygame.display.set_caption('Minesweeper')
        self.difficulty = None
        self.smart_player = False

        while self.play_game():
            pass

    def play_game(self):
        self.select_smart_player()
        self.select_difficulty()

        while True:
            self.start_game()

            if self.field.check_for_win() is True:
                self.draw_squares()
                self.draw_lines()
                pygame.display.update()

                break

            for event in pygame.event.get():
                self.quit_restart(event)
                self.move_play(event)
        self.win()

    def start_game(self):
        mines_left_number = len(self.field.mines)-len(self.field.flagged)
        mines_left = 'Mines Left: '+str(mines_left_number)
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(FONT_TITLE.render(TITLE, True, WHITE), (200, 15))
        self.screen.blit(FONT.render(mines_left, True, WHITE), (20, 40))
        self.draw_squares()
        self.draw_lines()
        self.clock.tick(100)
        pygame.display.update()

    def quit_restart(self, event):
        escape = event.type == KEYDOWN and event.key == K_ESCAPE
        if event.type == QUIT or escape:
            exit()

        elif event.type == KEYDOWN:
            if event.key == K_r:
                self.restart()

    def move_play(self, event):
        if event.type == MOUSEBUTTONUP:
            move = self.coord_to_pixel(event.pos[0], event.pos[1])
            if move:
                if event.button == 1 and \
                   move not in self.field.opened:
                    x, y = ((move[0]*SQUARE+X_OFF[self.difficulty],
                             move[1]*SQUARE+Y_OFF[self.difficulty]))
                    if not self.field.open(move) and \
                        move not in self.field.flagged:
                        self.screen.blit(MINE, (x, y))
                        pygame.display.update()
                        time.sleep(0.5)
                        self.show_mines(move)
                        time.sleep(1)
                        pygame.display.update()
                        self.play_again()
                        return False
                    else:
                        if self.smart_player is True:
                            self.field.smart_open(move)
                        else:
                            self.field.open(move)

                if event.button == 3:
                    if move in self.field.flagged:
                        self.field.flagged.remove(move)
                    elif move not in self.field.opened:
                        if self.smart_player is True:
                            self.field.smart_flag(move)
                        else:
                            self.field.flag(move)

    def select_difficulty(self):
        """Player can choose game's difficulty"""
        while True:
            for event in pygame.event.get():
                escape = event.type == KEYDOWN and event.key == K_ESCAPE
                if event.type == QUIT or escape:
                    exit()
                elif event.type == KEYDOWN:
                    if event.key == K_KP1 or event.key == K_1:
                        self.field = Minesweeper.Minesweeper(BEGINNER)
                        self.difficulty = BEGINNER
                        return
                    if event.key == K_KP2 or event.key == K_2:
                        self.field = Minesweeper.Minesweeper(INTERMEDIATE)
                        self.difficulty = INTERMEDIATE
                        return
                    if event.key == K_KP3 or event.key == K_3:
                        self.field = Minesweeper.Minesweeper(ADVANCED)
                        self.difficulty = ADVANCED
                        return

            self.screen.blit(DIFF_BACKGROUND, (0, 0))
            self.screen.blit(FONT_TITLE.render(TITLE, True, WHITE), (200, 15))
            self.screen.blit(FONT.render(CHOOSE, True, WHITE), (300, 245))
            self.screen.blit(FONT.render(PRESS_1, True, WHITE), (300, 280))
            self.screen.blit(FONT.render(PRESS_2, True, WHITE), (300, 315))
            self.screen.blit(FONT.render(PRESS_3, True, WHITE), (300, 350))
            pygame.display.update()


    def draw_squares(self):
        for cell in self.field.board:

            x, y = ((cell[0]*SQUARE)+X_OFF[self.difficulty],
                    (cell[1]*SQUARE)+Y_OFF[self.difficulty])

            if cell not in self.field.opened and \
               cell not in self.field.flagged:
                pygame.draw.rect(self.screen, FIELD, (x, y, SQUARE, SQUARE))
            elif cell in self.field.flagged:
                pygame.draw.rect(self.screen, FIELD, (x, y, SQUARE, SQUARE))
                self.screen.blit(FLAG, (x, y))
            elif cell in self.field.opened:
                number = str(self.field.mines_near[cell])
                if self.field.mines_near[cell] == 0:
                    pygame.draw.rect(self.screen,
                                     EMPTY, (x, y, SQUARE, SQUARE))
                else:
                    pygame.draw.rect(self.screen, NUM_COLOR,
                                     (x, y, SQUARE, SQUARE))
                    self.screen.blit(FONT.render(number, True,
                                     NUMBERS[number]), (x+int(SQUARE/4),
                                                        y+int(SQUARE/8)))

    def draw_lines(self):
        lines = [(x, y) for x in range(self.difficulty[0]+1)
                 for y in range(self.difficulty[1]+1)]

        for cell in lines:

            vertic_start = (cell[0]*SQUARE+X_OFF[self.difficulty],
                            Y_OFF[self.difficulty])

            vertic_end = (cell[0]*SQUARE+X_OFF[self.difficulty],
                         (SQUARE*self.difficulty[1])+Y_OFF[self.difficulty])

            horizon_start = (X_OFF[self.difficulty],
                            (cell[1]*SQUARE)+Y_OFF[self.difficulty])

            horizon_end = (SQUARE*self.difficulty[0]+X_OFF[self.difficulty],
                          (cell[1]*SQUARE)+Y_OFF[self.difficulty])

            pygame.draw.line(self.screen, BLACK, vertic_start, vertic_end)
            pygame.draw.line(self.screen, BLACK, horizon_start, horizon_end)

    def coord_to_pixel(self, x, y):
        for cell in self.field.board:
            if x > cell[0]*SQUARE+X_OFF[self.difficulty] and \
               y > cell[1]*SQUARE+Y_OFF[self.difficulty] and \
               x < (cell[0]+1)*SQUARE+X_OFF[self.difficulty] and \
               y < (cell[1]+1)*SQUARE+Y_OFF[self.difficulty]:
                return cell
        return None

    def show_mines(self, cell):
        """Show the mine when the button is pressed"""
        for mine in self.field.mines:
            x, y = ((mine[0]*SQUARE)+X_OFF[self.difficulty],
                    (mine[1]*SQUARE)+Y_OFF[self.difficulty])
            if mine is not cell:
                self.screen.blit(MINE, (x, y))
        return True

    def play_again(self):
        while True:
            for event in pygame.event.get():
                escape = event.type == KEYDOWN and event.key == K_ESCAPE
                if event.type == QUIT or escape:
                    exit()

                elif event.type == KEYDOWN:
                    if event.key == K_r:
                        new_game = self.play_game()
                        return new_game

            time.sleep(2)
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(FONT_TITLE.render(FIN, True, BLACK), (230, 15))
            self.screen.blit(FONT.render(LOST, True, BLACK), (170, 225))
            self.screen.blit(FONT.render(RESTART, True, BLACK), (170, 255))
            pygame.display.update()

    def restart(self):
        while True:
            for event in pygame.event.get():
                escape = event.type == KEYDOWN and event.key == K_ESCAPE
                if event.type == QUIT or escape:
                    exit()

                if event.type == KEYDOWN:
                    if event.key == K_r:
                        new_game = self.play_game()
                        return new_game
            self.screen.blit(FONT.render(CONFIRM, True, WHITE), (175, 75))
            pygame.display.update()

    def win(self):
        while True:
            for event in pygame.event.get():
                escape = event.type == KEYDOWN and event.key == K_ESCAPE
                if event.type == QUIT or escape:
                    exit()

                elif event.type == KEYDOWN:
                    if event.key == K_r:
                        new_game = self.play_game()
                        return new_game

            time.sleep(2)
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(FONT_TITLE.render(WIN, True, BLUE), (280, 15))
            self.screen.blit(FONT.render(WINNING, True, BLUE), (215, 225))
            self.screen.blit(FONT.render(RESTART, True, BLUE), (170, 255))
            pygame.display.update()

    def select_smart_player(self):
        while True:
            for event in pygame.event.get():
                escape = event.type == KEYDOWN and event.key == K_ESCAPE
                if event.type == QUIT or escape:
                    exit()
                elif event.type == KEYDOWN:
                    if event.key == K_y:
                        self.smart_player = True
                        return
                    if event.key == K_n:
                        self.smart_player = False
                        return

            self.screen.blit(DIFF_BACKGROUND, (0, 0))
            self.screen.blit(FONT_TITLE.render(TITLE, True, WHITE), (200, 15))
            self.screen.blit(FONT.render(HELP, True, WHITE), (180, 245))
            self.screen.blit(FONT.render(Y_N, True, WHITE), (300, 280))
            pygame.display.update()


def main():
    main = MinesweeperGUI()

    return main


if __name__ == '__main__':
    main()
