import pygame
import os
import sys

print(1)
class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 3

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

    def load_level(filename):
        filename = 'levels\\' + filename
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]

        max_width = max(map(len, level_map))

        return list(map(lambda x: x.ljust(max_width, '.'), level_map))


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Соединяй точки')
    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)

    board = Board(5, 5)
    board.set_view(190, 70, 80)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))
        board.render(screen)
        pygame.display.flip()

    pygame.quit()