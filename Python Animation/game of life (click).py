import time
from xmlrpc.client import boolean
import pygame
import numpy as np

# Define colors
color_background = pygame.Color('black')
color_grid = pygame.Color('dimgray')
color_die_next = pygame.Color('green')
color_alive_next = pygame.Color('forestgreen')

# Function to simulate the Game of Life
def game_of_life(screen: pygame.Surface, cells: numpy.ndarray, 
                 size: int, with_progress=False) -> numpy.ndarray:

    """ Simulates the Game of Life on a grid of cells.

    Args:
    - screen: The surface to draw the cells on.
    - cells: 2D array representing the current state of cells.
    - size: Size of each cell in pixels.
    - with_progress : If True, displays color changes for cell updates.

    Returns:
    numpy.ndarray: Updated state of cells after one iteration.

    Functionality:
    - Iterates over each cell, calculates the number of alive neighbors, and updates cell states.
    - Implements Game of Life rules to determine cell life and death.
    - Draws rectangles on the screen to represent cell states.
    """

    # Create an empty array with the same shape as cells
    updated_cells = np.zeros((cells.shape[0], cells.shape[1]))

    # Iterate over each individual cell in the grid
    for row, col in np.ndindex(cells.shape):
        # Calculate the number of alive neighbors (excluding the current cell)
        alive = np.sum(cells[row - 1:row + 2, col - 1:col + 2]) - cells[row, col]
        
        # Determine the color based on the cell's state
        color = color_background if cells[row, col] == 0 else color_alive_next

        # Update cell state based on Game of Life rules
        if cells[row, col] == 1:
            if alive < 2 or alive > 3:
                if with_progress:
                    color = color_die_next
            elif 2 <= alive <= 3:
                updated_cells[row, col] = 1
                if with_progress:
                    color = color_alive_next
        else:
            if alive == 3:
                updated_cells[row, col] = 1
                if with_progress:
                    color = color_alive_next

        # Draw rectangles on the screen to represent cells
        pygame.draw.rect(screen, color, (col * size, row * size, size - 1, size - 1))

    return updated_cells

# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((1000, 600))
cells = np.zeros((60, 100))  # Initial state of the grid
size = 20  # Size of each cell

# Fill the screen with the grid color
screen.fill(color_grid)

# Display the initial state of the Game of Life
game_of_life(screen, cells, size)

# Update the Pygame display
pygame.display.flip()
pygame.display.update()

running = False

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            # Toggle the simulation on/off with the spacebar
            if event.key == pygame.K_SPACE:
                running = not running
                game_of_life(screen, cells, size)
                pygame.display.update()
        # Handle mouse clicks to set cell states
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            cells[pos[1] // size, pos[0] // size] = 1
            game_of_life(screen, cells, size)
            pygame.display.update()

    # Clear the screen and redraw the grid
    screen.fill(color_grid)

    # Run the simulation if it is in the running state
    if running:
        cells = game_of_life(screen, cells, size, with_progress=True)
        pygame.display.update()

    # Introduce a small delay for smoother simulation
    time.sleep(0.001)