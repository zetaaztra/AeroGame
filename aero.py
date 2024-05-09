import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set screen dimensions
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 666

# Set colors
BLACK = (60, 60, 60)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Set airplane properties
airplane_size = 40
airplane_speed = 5

# Set obstacle properties
obstacle_width = 60
obstacle_speed = 5

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Airplane Flying Game")

# Load images
airplane_image = pygame.Surface((airplane_size, airplane_size), pygame.SRCALPHA)
pygame.draw.polygon(airplane_image, BLUE, [(0, airplane_size // 2), (airplane_size, 0), (airplane_size, airplane_size)])

# Set airplane initial position
airplane_pos = [50, SCREEN_HEIGHT // 2 - airplane_size // 2]

# Function to create obstacles
def create_obstacle():
    obstacle_height = random.randint(50, 200)
    obstacle_pos = [SCREEN_WIDTH, 0]
    obstacle_gap = random.randint(200, 300)
    return obstacle_pos, obstacle_height, obstacle_gap

# Function to move obstacles
def move_obstacles(obstacles):
    for obstacle in obstacles:
        obstacle[0][0] -= obstacle_speed

# Function to draw obstacles
def draw_obstacles(obstacles):
    for obstacle in obstacles:
        pygame.draw.rect(screen,RED, (obstacle[0][0], obstacle[0][1], obstacle_width, obstacle[1]))
        pygame.draw.rect(screen,RED, (obstacle[0][0], obstacle[0][1] + obstacle[1] + obstacle[2], obstacle_width, SCREEN_HEIGHT))

# Function to check for collisions
def check_collision(airplane_pos, obstacles):
    for obstacle in obstacles:
        if (airplane_pos[0] < obstacle[0][0] + obstacle_width and
            airplane_pos[0] + airplane_size > obstacle[0][0] and
            (airplane_pos[1] < obstacle[0][1] + obstacle[1] or
             airplane_pos[1] + airplane_size > obstacle[0][1] + obstacle[1] + obstacle[2])):
            return True
    return False

# Main game loop
running = True
clock = pygame.time.Clock()
obstacles = []

score = 0

while running:
    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move airplane
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        airplane_pos[1] -= airplane_speed
    if keys[pygame.K_DOWN]:
        airplane_pos[1] += airplane_speed

    # Generate obstacles
    if len(obstacles) == 0 or obstacles[-1][0][0] < SCREEN_WIDTH - random.randint(200, 300):
        obstacles.append(create_obstacle())

    # Move obstacles
    move_obstacles(obstacles)

    # Check for collisions
    if check_collision(airplane_pos, obstacles):
        print("Game Over! Final Score:", score)
        running = False

    # Check for points scored
    for obstacle in obstacles:
        if obstacle[0][0] + obstacle_width < airplane_pos[0]:
            score += 1
            obstacles.remove(obstacle)

    # Clear the screen
    screen.fill(BLACK)

    # Draw obstacles
    draw_obstacles(obstacles)

    # Draw airplane
    screen.blit(airplane_image, airplane_pos)

    # Update the display
    pygame.display.update()

    # Limit frames per second
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()

