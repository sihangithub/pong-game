from turtle import Screen
import pygame
import sys

from pygame.cursors import ball

score = 0

# Initialize Pygame
pygame.init()

# Initialize font
font = pygame.font.Font(None, 36)

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
PLAYER_SIZE = 50
PLAYER_SPEED = 5

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Set up the display
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("2D Game")
clock = pygame.time.Clock()

# Create rectangles for hitter and wall
hitter = pygame.Rect(WINDOW_WIDTH - 30, WINDOW_HEIGHT // 2, 10, 60)  # Moved hitter to right side and made it taller
leftWall = pygame.Rect(0, 0, 10, WINDOW_HEIGHT)

# For the ball, we need to track its position separately since pygame.draw.circle doesn't return a rect
ball_pos = [WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2]
ball_radius = 10

def handle_hitter():
    """Handle keyboard input for hitter movement"""
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        hitter.y -= PLAYER_SPEED
    if keys[pygame.K_DOWN]:
        hitter.y += PLAYER_SPEED
    
    # Keep hitter within screen bounds
    if hitter.top < 0:
        hitter.top = 0
    if hitter.bottom > WINDOW_HEIGHT:
        hitter.bottom = WINDOW_HEIGHT

def main():
    """Main game loop"""
    running = True
    
    start_time = pygame.time.get_ticks()/1000
    
    # Ball movement
    ball_speed_x = PLAYER_SPEED
    ball_speed_y = PLAYER_SPEED
    speed_multiplier = 1.0  # Add this to control ball speed
    
    while running:
        global score
        current_time = pygame.time.get_ticks()/1000
        elapsed_time = current_time - start_time
        
        # Increase speed over time
        speed_multiplier = 1.0 + (elapsed_time * 0.1)  # Increase by 10% every second
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Move ball
        ball_pos[0] += ball_speed_x * speed_multiplier
        ball_pos[1] += ball_speed_y * speed_multiplier
        
        # Handle hitter movement
        handle_hitter()
        
        # Keep ball within screen bounds
        if ball_pos[1] <= 0 or ball_pos[1] >= WINDOW_HEIGHT:
            ball_speed_y *= -1
        if ball_pos[0] <= 0 or ball_pos[0] >= WINDOW_WIDTH:
            ball_speed_x *= -1
        
        # Clear screen
        screen.fill(WHITE)
        
        # Draw objects
        pygame.draw.rect(screen, RED, leftWall)
        pygame.draw.rect(screen, BLACK, hitter)
        pygame.draw.circle(screen, BLACK, (int(ball_pos[0]), int(ball_pos[1])), ball_radius)
        screen.blit(font.render(str(score), True, (255, 0, 0)), (10, 10))
        screen.blit(font.render(f"Time: {int(elapsed_time)}s", True, RED), (10, 50))
        screen.blit(font.render(f"Speed: {speed_multiplier:.1f}x", True, RED), (10, 90))
        
        if ball_pos[0] <= 0:
            score += 1
        
        if ball_pos[0] >= WINDOW_WIDTH:
            score -= 1
        
        # Check for collision with hitter
        ball_rect = pygame.Rect(ball_pos[0] - ball_radius, ball_pos[1] - ball_radius, 
                              ball_radius * 2, ball_radius * 2)
        if ball_rect.colliderect(hitter) or ball_rect.colliderect(leftWall):
            ball_speed_x *= -1
        
        # Update display
        pygame.display.flip()
        
        # Control game speed
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
