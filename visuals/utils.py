import visual_constants
import engine_constants
import numpy as np

BAD_LOCATION = (-1, -1)


def mouse_location_to_grid_location(mouse_loc):
    # bounds mouse location between the padding and the rest of the screen.
    shifted_mouse_x = mouse_loc[0] - visual_constants.HORIZONTAL_PADDING
    shifted_mouse_y = mouse_loc[1] - visual_constants.VERTICAL_PADDING

    tile_x, tile_y = BAD_LOCATION

    # If the mouse location is within the radius of a piece, we select it.
    for x in range(engine_constants.N_RANKS+1):
        for y in range(engine_constants.N_FILES+1):
            if np.sqrt((shifted_mouse_x - x*visual_constants.HORIZONTAL_TILE_SIZE)**2 +
                       (shifted_mouse_y - y*visual_constants.VERTICAL_TILE_SIZE)**2) <= visual_constants.PIECE_RADIUS:
                tile_x, tile_y = x, y
                break

    return tile_x, tile_y
