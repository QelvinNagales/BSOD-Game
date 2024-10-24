import pygame
import sys
import pyautogui

# Initialize pygame
pygame.init()

# Set screen dimensions and colors for a scary theme
def get_screen_dimensions():
    width, height = pyautogui.size()
    return width, height

SCREEN_WIDTH, SCREEN_HEIGHT = get_screen_dimensions()
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PLAYER_COLOR = (64, 224, 208)
WALL_COLOR = (139, 0, 0)
FINISH_COLOR = (44, 195, 27)
PATH_COLOR = (100, 100, 100)

# Background music
pygame.mixer.music.load('assets/limbo.mp3')
pygame.mixer.music.play(-1)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Scary Maze")

# Clock to control frame rate
clock = pygame.time.Clock()

# Define the player
player_size = 20
player_x = 91
player_y = 113
player_speed = 7

# Maze walls (list of pygame.Rect objects) - Complex maze
walls = [
    pygame.Rect(-2, 34, 70, 125), #left border
    pygame.Rect(0, 0, 1920, 99),  #Upmost border
    pygame.Rect(75, 1053, 1845, 27), #Bottom border 
    pygame.Rect(0, 159, 571, 211), #Left
    pygame.Rect(0, 370, 449, 235), #Left 
    pygame.Rect(0, 605, 571, 139), #Left   
    pygame.Rect(0, 700, 100, 400), #Left
    pygame.Rect(504, 407, 133, 159),#middle small
    pygame.Rect(449, 578, 26, 27),#middle smaller  
    pygame.Rect(637, 65, 424, 940), #middle big  
    pygame.Rect(146, 794, 491, 211), #middle bot
    pygame.Rect(1097, 470, 49, 65), #Right mid small
    pygame.Rect(1127, 142, 385, 938), #Right mid
    pygame.Rect(1512, 142, 82, 362), #Right medium
    pygame.Rect(1512, 504, 257,342), #Right medium
    pygame.Rect(1647, 84, 273, 342), #Right upper
    pygame.Rect(1847, 422, 97, 593), #Right most middle 
    pygame.Rect(1578, 889, 270, 126), #Right most middle
]

# Define the finish line
finish_line = pygame.Rect(1889, 1015, 31, 38)

# Load the BSOD image for when the player dies
bsod_image = pygame.image.load('assets/BSOD.bmp')
bsod_image = pygame.transform.scale(bsod_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load the celebration image and sound for the finish line
celebration_image = pygame.image.load('assets/Hackerman.bmp')
celebration_image = pygame.transform.scale(celebration_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
celebration_sound = 'assets/congratulations.mp3'

# Limited visibility effect (flashlight)
visibility_radius = 0.1

# BSOD sound
bsod_sound = 'assets/BSOD sound.mp3'

def draw_bsod():
    pygame.mixer.music.stop()
    pygame.mixer.music.load(bsod_sound)
    pygame.mixer.music.play()
    screen.blit(bsod_image, (0, 0))
    pygame.display.flip()
    pygame.time.wait(10000)

def draw_flashlight(player_x, player_y):
    darkness = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    darkness.fill(BLACK)
    pygame.draw.circle(darkness, (0, 0, 0, 0), (player_x + player_size//2, player_y + player_size//2), visibility_radius)
    screen.blit(darkness, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)

def check_collision(player_rect, walls):
    for wall in walls:
        if player_rect.colliderect(wall):
            return True
    return False

def check_finish(player_rect, finish_line):
    if player_rect.colliderect(finish_line):
        return True
    return False

def player_die():
    pygame.mixer.music.stop()
    draw_bsod()
    pygame.quit()
    sys.exit()

def celebrate():
    pygame.mixer.music.stop()
    pygame.mixer.music.load(celebration_sound)
    pygame.mixer.music.play()
    screen.blit(celebration_image, (0, 0))
    pygame.display.flip()
    pygame.time.wait(5000)
    pygame.quit()
    sys.exit()

def close_game():
    pygame.quit()
    sys.exit()

def game_loop():
    global player_x, player_y
    
    # Start timer
    start_ticks = pygame.time.get_ticks() # Uses miliseconds
    total_time = 30

    # Game loop and event handling
    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close_game()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                close_game()
        
        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            player_x -= player_speed
        if keys[pygame.K_d]:
            player_x += player_speed
        if keys[pygame.K_w]:
            player_y -= player_speed
        if keys[pygame.K_s]:
            player_y += player_speed
        
        # Create player rectangle
        player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
        
        # Check collision with walls
        if check_collision(player_rect, walls):
            player_die()
        
        # Check if player reaches the finish line
        if check_finish(player_rect, finish_line):
            celebrate()  # Celebrate when reaching the finish line
        
        # Drawing the game
        screen.fill(BLACK)
        
        # Draw walls
        for wall in walls:
            pygame.draw.rect(screen, WALL_COLOR, wall)
        
        # Draw the finish line
        pygame.draw.rect(screen, FINISH_COLOR, finish_line)
        
        # Draw player
        pygame.draw.rect(screen, PLAYER_COLOR, player_rect)
        
        # Draw limited visibility (flashlight effect)
        draw_flashlight(player_x, player_y)
        
        # Calculate the remaining time
        seconds = (pygame.time.get_ticks() - start_ticks) / 1000 # ms to s since start_ticks is in ms
        remaining_time = total_time - seconds
        font = pygame.font.Font(None, 36)
        timer_text = font.render(f"Time: {int(remaining_time)}", True, WHITE)
        screen.blit(timer_text, (SCREEN_WIDTH - 150, 10))
        
        # Check if time is up
        if remaining_time <= 0:
            player_die()
        
        # Update display
        pygame.display.flip()
        
        # Frame rate
        clock.tick(30)

# Start the game
game_loop()