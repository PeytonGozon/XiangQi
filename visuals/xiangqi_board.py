import pygame
import engine
import utils
import engine_util
from visual_constants import *
import piece_movement


class Board(object):
    def __init__(self, chess_engine: engine.ChessEngine, special_board=None):
        self._running = True
        self._display_surf = None
        self._size = WINDOW_WIDTH, WINDOW_HEIGHT
        self._chess_engine = chess_engine
        self._font = None
        self._clock = None
        self._text_displacement = None
        # whether we are currently moving a piece or not.
        self._piece_hovering = False
        self._piece_locations = []

    def on_init(self):
        # Initialize pygame, the visual backend
        pygame.init()
        pygame.font.init()

        # Create the window
        self._display_surf = pygame.display.set_mode(self._size, pygame.HWACCEL | pygame.DOUBLEBUF)
        pygame.display.set_caption("象棋 - XiangQi")

        # Initialize a timer to maintain consistent FPS (and to limit CPU usage)
        self._clock = pygame.time.Clock()

        # Load the font for drawing text to the pieces, and determine the optimal text displacement
        self._font = pygame.font.Font('font.ttf', 48)
        temp = self._font.render('车', True, BLACK_TEXT)
        text_size = temp.get_size()
        self._text_displacement = (0.5 * text_size[0], 0.5 * text_size[1])

        # Initialize the green circle that show legal moves
        pygame.draw.circle(POTENTIAL_LOCATION_SURF, POTENTIAL_COLOR, (PIECE_RADIUS, PIECE_RADIUS), PIECE_RADIUS)

        # Start the game
        self._running = True

    def on_event(self, event):
        # depending on event, update screen
        # TODO: Add the ability to move pieces
        if event.type == pygame.QUIT:
            self._running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_move_piece(pygame.mouse.get_pos())

    def on_loop(self):
        pass

    def on_render(self):
        # render the board and the pieces
        self.render_board_background()
        self.render_pieces()

        if self._piece_hovering:
            self.render_valid_moves()

        # Update the screen and the clock
        pygame.display.update()
        self._clock.tick(FPS)

    def on_cleanup(self):
        pygame.font.quit()
        pygame.quit()

    def on_execute(self):
        self.on_init()

        while self._running:
            for event in pygame.event.get():
                self.on_event(event)

            self.on_loop()
            self.on_render()

        self.on_cleanup()

    def handle_move_piece(self, mouse_location, verbose=False):
        # Convert the mouse's location into grid coordinates
        grid_location = utils.mouse_location_to_grid_location(mouse_location)

        if grid_location != utils.BAD_LOCATION:
            self._piece_hovering = not self._piece_hovering
            self._piece_locations.append(grid_location)

            # Update the game window's title to let the user know they are hovering
            if self._piece_hovering:
                piece_class = engine_util.piece_class_by_location(self._chess_engine.bit_board, grid_location)
                pygame.display.set_caption(f'棋 - XiangQi [MOVING  {piece_class} from location {grid_location}]')

            # If the piece is no longer hovering, move its location
            if not self._piece_hovering:
                success = self.move_piece(True)
                if success:
                    self._piece_locations = []
                    pygame.display.set_caption("象棋 - XiangQi")
                else:
                    self._piece_hovering = True
                    if len(self._piece_locations) > 1:
                        self._piece_locations.pop(-1)



    def move_piece(self, verbose=False):
        # Need an even number of locations to know where we're moving from to where we're moving to.
        assert (len(self._piece_locations) % 2 == 0)

        success = engine_util.move_piece_by_location(self._chess_engine.bit_board, self._piece_locations[0],
                                                     self._piece_locations[1])

        if success:
            if verbose:
                print("Moved piece: ", self._piece_locations)
            # Clean the piece locations to maintain memory
            return True

        return False

    def render_valid_moves(self):
        # Obtain the location of the piece we're moving
        location = self._piece_locations[0]

        # obtain the piece class:
        piece_class = engine_util.piece_class_by_location(self._chess_engine.bit_board, location, just_class=True)

        # Find the correct set of valid moves
        valid_moves = []

        # Generate all the valid moves for it
        # if piece_class == 'g':  # Black General
        #     valid_moves = engine_util.bitboard_to_locations(
        #         piece_movement.black_general_valid_movements(self._chess_engine.bit_board))
        #     print(valid_moves)

        valid_moves = engine_util.bitboard_to_locations(
            piece_movement.return_valid_moves_by_type(self._chess_engine.bit_board, piece_class)
        )

        # Render green circles at all valid locations
        self.render_piece_class('potential', valid_moves)

    def render_piece_class(self, piece_class, locations):
        if piece_class != 'potential':
            text, team = PIECE_CLASS_TO_TEXT[piece_class]
            text_image = self._font.render(text, True, RED_TEXT if team is 'r' else BLACK_TEXT)

        for location in locations:
            if piece_class != 'potential':
                x = (location % N_FILES) * HORIZONTAL_TILE_SIZE + HORIZONTAL_PADDING
                y = int(location / N_FILES) * VERTICAL_TILE_SIZE + VERTICAL_PADDING
                pygame.draw.circle(self._display_surf, center=(x, y), color=PIECE_COLOR, radius=PIECE_RADIUS)
                self._display_surf.blit(text_image, (x - self._text_displacement[0], y - self._text_displacement[1]))
            else:
                # If we're not rendering a piece, we're rendering potential locations for a piece.
                x = location[0] * HORIZONTAL_TILE_SIZE + HORIZONTAL_PADDING - PIECE_RADIUS
                y = location[1] * VERTICAL_TILE_SIZE + VERTICAL_PADDING - PIECE_RADIUS
                self._display_surf.blit(POTENTIAL_LOCATION_SURF, (x, y))

    def render_pieces(self):
        # Obtain the location of every piece from its bit board and render it.
        locations = self._chess_engine.bit_board.get_locations_by_piece_class()
        for k, v in locations.items():
            # v is a tuple in the form (important,), so v[0] obtains the important information.
            self.render_piece_class(k, v[0])

    def render_board_background(self):
        # begin by cleaning the board
        self._display_surf.fill(BACKGROUND_COLOR)

        # Draw the game's boarder (with rounded corners)
        pygame.draw.rect(self._display_surf, LINE_COLOR, GAME_BOARD_RECTANGLE, OUTER_LINE_THICKNESS,
                         border_radius=OUTER_LINE_THICKNESS)

        # Draw the ranks (left-right lines)
        for i in range(1, (N_RANKS - 1)):
            pygame.draw.line(self._display_surf, LINE_COLOR,
                             (HORIZONTAL_PADDING, VERTICAL_PADDING + i * VERTICAL_TILE_SIZE),
                             (WINDOW_WIDTH - HORIZONTAL_PADDING - 10, VERTICAL_PADDING + i * VERTICAL_TILE_SIZE),
                             INNER_LINE_THICKNESS)

        # Draw the files (top-down lines, with a river in rank 5).
        for i in range(1, (N_FILES - 1)):
            # portion of line above the river
            pygame.draw.line(self._display_surf, LINE_COLOR,
                             (HORIZONTAL_PADDING + i * HORIZONTAL_TILE_SIZE, VERTICAL_PADDING),
                             (HORIZONTAL_PADDING + i * HORIZONTAL_TILE_SIZE, VERTICAL_PADDING + 4 * VERTICAL_TILE_SIZE),
                             INNER_LINE_THICKNESS)
            # portion of line below the river
            pygame.draw.line(self._display_surf, LINE_COLOR,
                             (HORIZONTAL_PADDING + i * HORIZONTAL_TILE_SIZE, VERTICAL_PADDING + 5 * VERTICAL_TILE_SIZE),
                             (HORIZONTAL_PADDING + i * HORIZONTAL_TILE_SIZE, WINDOW_HEIGHT - VERTICAL_PADDING - 10),
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
    xiangqi_engine = engine.ChessEngine()
    xiangqi_board = Board(xiangqi_engine)
    xiangqi_board.on_execute()
