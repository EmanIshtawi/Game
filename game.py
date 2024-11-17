import pygame
import random

# Initialize Pygame
pygame.init()

# Set up game window
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Number Puzzle Game")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (220, 220, 220)
LIGHT_BLUE = (173, 216, 230)
DARK_BLUE = (0, 0, 128)

# Define font
font = pygame.font.SysFont('Arial', 50)
message_font = pygame.font.SysFont('Arial', 30)

# Function to create a shuffled puzzle for a given size
def create_puzzle(grid_size):
    numbers = [i for i in range(1, grid_size ** 2 + 1)]
    random.shuffle(numbers)
    return numbers

# Function to draw the puzzle grid
def draw_puzzle(numbers, grid_size, selected_index=None):
    block_size = WIDTH // grid_size  # Dynamically calculate block size
    for i, num in enumerate(numbers):
        row = i // grid_size
        col = i % grid_size
        x = col * block_size
        y = row * block_size

        # Draw the block
        pygame.draw.rect(screen, LIGHT_BLUE if selected_index != i else (255, 0, 0), (x, y, block_size, block_size))
        pygame.draw.rect(screen, DARK_BLUE, (x, y, block_size, block_size), 5)  # border

        # Render the number
        text = font.render(str(num), True, BLACK)
        screen.blit(text, (x + block_size // 3, y + block_size // 3))

# Function to check if the puzzle is solved
def is_solved(numbers, grid_size):
    return numbers == list(range(1, grid_size ** 2 + 1))

# Function to display message
def display_message(message):
    text = message_font.render(message, True, DARK_BLUE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 + 100))

# Main game loop
def play_game():
    level = 1
    grid_size = 2
    numbers = create_puzzle(grid_size)
    selected_index = None
    running = True
    clock = pygame.time.Clock()

    while running:
        screen.fill(WHITE)  # Background color

        # Draw puzzle
        draw_puzzle(numbers, grid_size, selected_index)

        # Display level and message
        level_text = message_font.render(f"Level: {level}", True, DARK_BLUE)
        screen.blit(level_text, (10, 10))

        if is_solved(numbers, grid_size):
            display_message("Puzzle Solved! Proceeding to next level...")

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Get the position of the mouse click
                x, y = pygame.mouse.get_pos()
                col = x // (WIDTH // grid_size)  # Adjust for grid size
                row = y // (HEIGHT // grid_size)
                selected_index = row * grid_size + col

            if event.type == pygame.MOUSEBUTTONUP and selected_index is not None:
                # Get the position of the mouse release
                x, y = pygame.mouse.get_pos()
                col = x // (WIDTH // grid_size)  # Adjust for grid size
                row = y // (HEIGHT // grid_size)
                new_index = row * grid_size + col

                if new_index != selected_index:
                    # Swap the blocks
                    numbers[selected_index], numbers[new_index] = numbers[new_index], numbers[selected_index]
                    selected_index = None

        # Check if puzzle is solved
        if is_solved(numbers, grid_size):
            pygame.time.wait(1000)  # Wait for 1 second to show the solved message
            level += 1
            grid_size += 1  # Increase grid size with each level
            numbers = create_puzzle(grid_size)  # Shuffle for the next level

        clock.tick(30)  # FPS

    pygame.quit()

if __name__ == "__main__":
    play_game()