import pygame
from pygame.locals import *
from visuals.constants import *


class Board:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = WINDOW_WIDTH, WINDOW_HEIGHT

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWACCEL | pygame.DOUBLEBUF)
        pygame.display.set_caption("象棋 - XiangQi")
        self._running = True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def on_loop(self):
        pass

    def on_render(self):
        self.render_board()

        pygame.display.update()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        self.on_init()

        while self._running:
            for event in pygame.event.get():
                self.on_event(event)

            self.on_loop()
            self.on_render()

        self.on_cleanup()

    def render_board(self):
        # begin by cleaning the board
        self._display_surf.fill(BACKGROUND_COLOR)

        # Draw the game's boarder (with rounded corners)
        pygame.draw.rect(self._display_surf, LINE_COLOR, GAME_BOARD_RECTANGLE, OUTER_LINE_THICKNESS,
                         border_radius=OUTER_LINE_THICKNESS)

        # Draw the ranks (left-right lines)
        for i in range(1, N_VERTICAL_TILES):
            pygame.draw.line(self._display_surf, LINE_COLOR,
                             (HORIZONTAL_PADDING, VERTICAL_PADDING + i * VERTICAL_TILE_SIZE),
                             (WINDOW_WIDTH-HORIZONTAL_PADDING-10, VERTICAL_PADDING + i * VERTICAL_TILE_SIZE),
                             INNER_LINE_THICKNESS)

        # Draw the files (top-down lines, with a river in rank 5).
        for i in range(1, N_HORIZONTAL_TILES):
            # portion of line above the river
            pygame.draw.line(self._display_surf, LINE_COLOR,
                             (HORIZONTAL_PADDING+i*HORIZONTAL_TILE_SIZE, VERTICAL_PADDING),
                             (HORIZONTAL_PADDING+i*HORIZONTAL_TILE_SIZE, VERTICAL_PADDING+4*VERTICAL_TILE_SIZE),
                             INNER_LINE_THICKNESS)
            # portion of line below the river
            pygame.draw.line(self._display_surf, LINE_COLOR,
                             (HORIZONTAL_PADDING + i * HORIZONTAL_TILE_SIZE, VERTICAL_PADDING+5*VERTICAL_TILE_SIZE),
                             (HORIZONTAL_PADDING + i * HORIZONTAL_TILE_SIZE, WINDOW_HEIGHT - VERTICAL_PADDING-10),
                             INNER_LINE_THICKNESS)

        # Draw in the diagonal lines for advisors
        # Top
        pygame.draw.line(self._display_surf, LINE_COLOR, (BOARD_LEFT + 3 * HORIZONTAL_TILE_SIZE, BOARD_TOP),
                         (BOARD_LEFT + 5 * HORIZONTAL_TILE_SIZE, BOARD_TOP + 2 * VERTICAL_TILE_SIZE),
                         INNER_LINE_THICKNESS)
        pygame.draw.line(self._display_surf, LINE_COLOR,
                         (BOARD_LEFT + 3 * HORIZONTAL_TILE_SIZE, BOARD_TOP + 2 * VERTICAL_TILE_SIZE),
                         (BOARD_LEFT + 5 * HORIZONTAL_TILE_SIZE, BOARD_TOP),
                         INNER_LINE_THICKNESS)

        # Bottom
        pygame.draw.line(self._display_surf, LINE_COLOR,
                         (BOARD_LEFT + 3 * HORIZONTAL_TILE_SIZE - 4, BOARD_TOP + BOARD_HEIGHT),
                         (BOARD_LEFT + 5 * HORIZONTAL_TILE_SIZE, BOARD_TOP + BOARD_HEIGHT - 2 * VERTICAL_TILE_SIZE),
                         INNER_LINE_THICKNESS)
        pygame.draw.line(self._display_surf, LINE_COLOR,
                         (BOARD_LEFT + 3 * HORIZONTAL_TILE_SIZE, BOARD_TOP + BOARD_HEIGHT - 2 * VERTICAL_TILE_SIZE),
                         (BOARD_LEFT + 5 * HORIZONTAL_TILE_SIZE, BOARD_TOP + BOARD_HEIGHT - 4),
                         INNER_LINE_THICKNESS)


if __name__ == "__main__":
    xiangqi_board = Board()
    xiangqi_board.on_execute()
