BAD_LOCATION = (-1, -1)


def mouse_location_to_grid_location(mouse_loc):
    from .visual_constants import WINDOW_HEIGHT, WINDOW_WIDTH, PIECE_RADIUS, HORIZONTAL_PADDING, \
        VERTICAL_PADDING, VERTICAL_TILE_SIZE, HORIZONTAL_TILE_SIZE
    from engine.engine_constants import N_RANKS, N_FILES
    import numpy as np

    if mouse_loc[0] > (WINDOW_WIDTH - HORIZONTAL_PADDING + PIECE_RADIUS) or \
            mouse_loc[0] < (HORIZONTAL_PADDING - PIECE_RADIUS) or \
            mouse_loc[1] > (WINDOW_HEIGHT - VERTICAL_PADDING + PIECE_RADIUS) or \
            mouse_loc[1] < VERTICAL_PADDING - PIECE_RADIUS:
        return BAD_LOCATION

    # bounds mouse location between the padding and the rest of the screen.
    shifted_mouse_x = mouse_loc[0] - HORIZONTAL_PADDING
    shifted_mouse_y = mouse_loc[1] - VERTICAL_PADDING

    tile_x, tile_y = BAD_LOCATION

    # If the mouse location is within the radius of a piece, we select it.
    for x in range(N_RANKS + 1):
        for y in range(N_FILES + 1):
            if np.sqrt((shifted_mouse_x - x * HORIZONTAL_TILE_SIZE) ** 2 +
                       (shifted_mouse_y - y * VERTICAL_TILE_SIZE) ** 2) <= PIECE_RADIUS:
                tile_x, tile_y = x, y
                break

    return tile_x, tile_y
