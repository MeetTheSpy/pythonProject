import pygame
import os
import sys
import time


class Board:
    def __init__(self, width, height, fname):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 3

        # поле кругов
        self.circles = self.load_level(fname)
        self.lines = [[0] * len(self.circles) for _ in range(len(self.circles))]
        colors = set([x for row in self.circles for x in row if x != 0])
        self.ways = {}
        for c in colors:
            self.ways[c] = []

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def load_image(name, colorkey=None):
        fullname = os.path.join('data', name)
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{fullname}' не найден")
            sys.exit()
        image = pygame.image.load(fullname)
        if colorkey is not None:
            image = image.convert()
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        else:
            image = image.convert_alpha()
        return image

    def render(self, screen):
        colors = ['black', 'red', 'yellow', 'blue', 'green', 'purple', 'pink']
        for i in range(self.height):
            for j in range(self.width):
                pygame.draw.rect(screen, 'white',
                                 ((self.left + j * self.cell_size, self.top + i * self.cell_size),
                                  (self.cell_size, self.cell_size)), 1)
                pygame.draw.rect(screen, colors[self.board[i][j]],
                                 ((self.left + j * self.cell_size + 1, self.top + i * self.cell_size + 1),
                                  (self.cell_size - 2, self.cell_size - 2)))
                if self.circles[i][j] != 0:
                    pygame.draw.circle(screen, colors[self.circles[i][j]],
                                       ((self.left + j * self.cell_size + self.cell_size // 2,
                                         self.top + i * self.cell_size + self.cell_size // 2)), 30)
                if self.lines[i][j] != 0:
                    pygame.draw.circle(screen, colors[self.lines[i][j]],
                                       ((self.left + j * self.cell_size + self.cell_size // 2,
                                         self.top + i * self.cell_size + self.cell_size // 2)), 10)

        # print(self.ways)
        for col in self.ways:
            if len(self.ways[col]) > 1:
                k = len(self.ways[col])
                if self.ways[col][-1] == 'end':
                    k -= 1
                for i in range(1, k):
                    i0, j0 = self.ways[col][i - 1]
                    i1, j1 = self.ways[col][i]
                    if i1 != i0:

                        pygame.draw.rect(screen, colors[col],
                                         (self.left + j0 * self.cell_size + self.cell_size // 2 - 10,
                                          self.top + min(i0, i1) * self.cell_size + self.cell_size // 2, 20, self.cell_size))
                    if j1 != j0:
                        pygame.draw.rect(screen, colors[col],
                                         (self.left + min(j0, j1) * self.cell_size + self.cell_size // 2,
                                          self.top + i0 * self.cell_size + self.cell_size // 2 - 10, self.cell_size, 20))



    def load_level(self, filename):
        filename = 'levels\\' + filename
        with open(filename, 'r') as mapFile:
            level_map = [list(map(int, line.strip())) for line in mapFile]

        max_width = max(map(len, level_map))

        return level_map

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        j, i = (x - self.left) // self.cell_size, (y - self.top) // self.cell_size
        if 0 <= j < self.width and 0 <= i < self.height:
            return i, j
        else:
            return None

    def clear_lines(self, cur_color):
        for i in range(len(self.lines)):
            for j in range(len(self.lines[i])):
                if self.lines[i][j] == cur_color:
                    self.lines[i][j] = 0


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Соединяй точки')
    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)
    running = True

    n = 10 # количество уровней

    for level in range(n):
        if not running:
            break

        fname = 'level' + str(level + 1) +'.txt'
        board = Board(5, 5, fname)
        board.set_view(190, 70, 80)


        drawing = False
        while running:

            # проверка на окончание раунда
            ok = True
            for row in board.lines:
                for x in row:
                    if x == 0:
                        ok = False
            if ok:
                time.sleep(2)
                break

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = event.pos
                    if board.get_cell(pos):
                        i, j = board.get_cell(pos)
                        cur_color = board.circles[i][j]
                        if board.circles[i][j] != 0 and board.lines[i][j] == 0:
                            drawing = True
                            board.lines[i][j] = cur_color
                            if not board.ways[cur_color]:
                                board.ways[cur_color].append((i,j))
     #                   if board.lines[i][j] == cur_color and (i, j) in board.ways[cur_color]:
     #                       k = board.ways[cur_color].index((i, j))
     #                       board.ways[cur_color] = board.ways[cur_color][:k + 1]

                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if not drawing:
                        board.clear_lines(cur_color)
                        board.ways[cur_color] = []

                    drawing = False

                if event.type == pygame.MOUSEMOTION and drawing:
                    pos = event.pos
                    if board.get_cell(pos):
                        i, j = board.get_cell(pos)
                        if board.circles[i][j] == 0 and board.lines[i][j] == 0 or board.circles[i][j] == cur_color:
                            if board.ways[cur_color][-1] != 'end':
                                i0, j0 = board.ways[cur_color][-1]
                                if abs(i - i0) == 1 and j == j0 or abs(j - j0) == 1 and i == i0:
                                    board.ways[cur_color].append((i, j))
                                    board.lines[i][j] = cur_color
                                    if board.circles[i][j] == cur_color:
                                        board.ways[cur_color].append('end')

            screen.fill((0, 0, 0))
            board.render(screen)
            pygame.display.flip()

    pygame.quit()

