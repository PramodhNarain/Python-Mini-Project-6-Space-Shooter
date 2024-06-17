import pygame
import random

# Initialize Pygame
pygame.init()
pygame.font.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_NAME = pygame.font.match_font('arial')
ALIEN_SPAWN_EVENT = pygame.USEREVENT + 1  # Custom event for alien spawning
ALIEN_SPAWN_INTERVAL = 1000  # Spawn a new alien every 1000 milliseconds (1 second)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter Game")
clock = pygame.time.Clock()

# Load images
player_img = pygame.image.load('player.png')  # Replace 'player.png' with your player image
alien_img = pygame.image.load('alien.png')  # Replace 'alien.png' with your alien image
bullet_img = pygame.image.load('bullet.png')  # Replace 'bullet.png' with your bullet image

# Scale images
player_img = pygame.transform.scale(player_img, (50, 50))
alien_img = pygame.transform.scale(alien_img, (50, 50))
bullet_img = pygame.transform.scale(bullet_img, (10, 30))

# Player
player = pygame.Rect(WIDTH // 2 - 25, HEIGHT - 70, 50, 50)

# Lists to hold alien and bullet objects
aliens = []
bullets = []

# Player name and score
score = 0

def spawn_alien():
    alien = pygame.Rect(random.randint(0, WIDTH - 50), random.randint(-200, -50), 50, 50)
    aliens.append(alien)

def draw_objects():
    screen.fill(BLACK)
    screen.blit(player_img, player)

    for alien in aliens:
        screen.blit(alien_img, alien)

    for bullet in bullets:
        screen.blit(bullet_img, bullet)

def move_objects():
    for alien in aliens:
        alien.y += 1  # Adjust speed
        if alien.y > HEIGHT:
            aliens.remove(alien)

    for bullet in bullets:
        bullet.y -= 5  # Adjust speed
        if bullet.y < 0:
            bullets.remove(bullet)

def draw_text(surface, text, size, x, y, center=False):
    font = pygame.font.Font(FONT_NAME, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topright = (x, y)
    surface.blit(text_surface, text_rect)

def get_player_name():
    input_box = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 32, 200, 64)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    done = False

    font = pygame.font.Font(FONT_NAME, 32)

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill(BLACK)
        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)

        pygame.display.flip()
        clock.tick(30)

    return text

def game_over_screen(player_name, score):
    screen.fill(BLACK)
    draw_text(screen, "Game Over", 64, WIDTH // 2, HEIGHT // 4, center=True)
    draw_text(screen, f"Congratulations, {player_name}!", 32, WIDTH // 2, HEIGHT // 2, center=True)
    draw_text(screen, f"Your Score: {score}", 32, WIDTH // 2, HEIGHT // 2 + 50, center=True)
    draw_text(screen, "Press Enter to Play Again or Esc to Quit", 24, WIDTH // 2, HEIGHT // 2 + 100, center=True)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

def main_game(player_name):
    global score
    pygame.time.set_timer(ALIEN_SPAWN_EVENT, ALIEN_SPAWN_INTERVAL)
    score = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet = pygame.Rect(player.centerx - 5, player.top - 30, 10, 30)
                    bullets.append(bullet)
            if event.type == ALIEN_SPAWN_EVENT:
                spawn_alien()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.left > 0:
            player.x -= 5
        if keys[pygame.K_RIGHT] and player.right < WIDTH:
            player.x += 5

        draw_objects()
        move_objects()

        # Collision detection for bullets
        for bullet in bullets:
            for alien in aliens:
                if bullet.colliderect(alien):
                    bullets.remove(bullet)
                    aliens.remove(alien)
                    score += 1  # Increase score
                    break  # Avoid modifying the list while iterating

        # Collision detection for player and aliens
        for alien in aliens:
            if player.colliderect(alien):
                running = False

        # Draw player name and score
        draw_text(screen, f"{player_name}: {score}", 24, WIDTH - 10, 10)

        pygame.display.update()
        clock.tick(FPS)

    game_over_screen(player_name, score)

if __name__ == "__main__":
    player_name = get_player_name()
    while True:
        main_game(player_name)
        game_over_screen(player_name, score)
