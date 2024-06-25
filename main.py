import pygame
import sys
import random
import time

# Initialize pygame
pygame.init()

# Set up the game window
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Pacman')

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Load images
pacman_image = pygame.image.load('assets/PNG_transparency_demonstration_1.png')
pacman_image = pygame.transform.scale(pacman_image, (50, 50))  # Resize player image
ghost_image = pygame.image.load('assets/alien1.png')
wall_image = pygame.image.load('assets/brick.png')
pellet_image = pygame.image.load('assets/Google-flutter-logo.png')

# Define the Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pacman_image
        self.rect = self.image.get_rect()
        self.rect.center = (400, 300)
        self.speed = 2  # Reduced speed
        self.score = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

# Define the Ghost class
class Ghost(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = ghost_image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 0.5  # Further reduced speed

    def update(self):
        directions = [(self.speed, 0), (-self.speed, 0), (0, self.speed), (0, -self.speed)]
        direction = random.choice(directions)
        self.rect.x += direction[0]
        self.rect.y += direction[1]

        # Keep the ghost within the screen bounds
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 800:
            self.rect.right = 800
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > 600:
            self.rect.bottom = 600

# Define the Wall class
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.transform.scale(wall_image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Define the Pellet class
class Pellet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(pellet_image, (10, 10))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

# Create a player instance
player = Player()

# Create ghost instances
ghosts = pygame.sprite.Group()
ghost_positions = [(100, 100), (700, 500)]  # Initial positions to avoid collision
for pos in ghost_positions:
    ghost = Ghost(*pos)
    ghosts.add(ghost)

# Create wall instances
walls = pygame.sprite.Group()
wall_positions = [
    (100, 100, 600, 20),
    (100, 200, 20, 400),
    (100, 580, 600, 20),
    (680, 200, 20, 400)
]
for pos in wall_positions:
    wall = Wall(*pos)
    walls.add(wall)

# Create pellet instances
pellets = pygame.sprite.Group()
for i in range(150, 650, 50):
    for j in range(150, 550, 50):
        pellet = Pellet(i, j)
        pellets.add(pellet)

# Create a sprite group
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(ghosts)
all_sprites.add(walls)
all_sprites.add(pellets)

# Add a delay at the start of the game
pygame.display.flip()
time.sleep(2)  # 2-second delay

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update all sprites
    all_sprites.update()

    # Check for collisions between player and pellets
    pellet_collisions = pygame.sprite.spritecollide(player, pellets, True)
    player.score += len(pellet_collisions)

    # Check for collisions between player and ghosts
    if pygame.sprite.spritecollideany(player, ghosts):
        print(f'Game Over! Your score: {player.score}')
        pygame.quit()
        sys.exit()

    # Fill the screen with black color
    screen.fill(BLACK)

    # Draw all sprites
    all_sprites.draw(screen)

    # Display the score
    font = pygame.font.Font(None, 36)
    score_text = font.render(f'Score: {player.score}', True, WHITE)
    screen.blit(score_text, (10, 10))

    # Update the display
    pygame.display.flip()
