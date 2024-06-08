import pygame
import random

# Initialize required game modules
pygame.init()
pygame.font.init()
pygame.mixer.init()

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Set up Play Area
screen_width = 1920
screen_height = 1080
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Catch the Beat")

# Initialize Images
bg = pygame.image.load('Images/background.jpg')
basket_img = pygame.image.load('Images/catcher.png')
basket_img = pygame.transform.scale(basket_img, (150, 150))
gameover_img = pygame.image.load('Images/gameover.webp') 
watermelon_img = pygame.image.load('Sprites/Watermelon.png')
grape_img = pygame.image.load('Sprites/Grape.png')  
cherry_img = pygame.image.load('Sprites/Cherry.png') 
chili_img = pygame.image.load('Sprites/Chili.png') 
pineapple_img = pygame.image.load('Sprites/Pineapple.png')

# Initialize Sounds
catch_sound = pygame.mixer.Sound('Sounds/item00.wav')
gameover_sound = pygame.mixer.Sound('Sounds/pldead00.wav')
dash_sound = pygame.mixer.Sound('Sounds/ok00.wav')
pygame.mixer.music.load('Sounds/bgm.wav')
pygame.mixer.music.play(-1)

# Initialize Game Variables
basket_width = 100
basket_height = 100
basket_x = screen_width // 2 - basket_width // 2
basket_y = screen_height - basket_height - 20
basket_speed = 10
dash_speed = 30
score = 0
clock = pygame.time.Clock()

# Define Fruit Properties
fruits = [
    {'image': watermelon_img, 'width': 50, 'height': 50, 'speed': 5, 'score': 10},
    {'image': grape_img, 'width': 50, 'height': 50, 'speed': 6, 'score': 20},
    {'image': pineapple_img, 'width': 50, 'height': 50, 'speed': 7, 'score': 30},
    {'image': cherry_img, 'width': 50, 'height': 50, 'speed': 8, 'score': 40},
    {'image': chili_img, 'width': 50, 'height': 50, 'speed': 10, 'score': 50}
    
]

# Initialize Fruit Variables
current_fruit_index = 0
fruit_x = random.randint(0, screen_width - fruits[current_fruit_index]['width'])
fruit_y = -fruits[current_fruit_index]['height']

# Start of Functions
def draw_basket(x, y):
    screen.blit(basket_img, (x, y, basket_width, basket_height))

def draw_fruit(x, y):
    fruit = fruits[current_fruit_index]
    screen.blit(fruit['image'], (x, y, fruit['width'], fruit['height']))

def display_score(score):
    font = pygame.font.SysFont(None, 36)
    text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(text, (10, 10))

def game_over():
    gameover_sound.play()  
    pygame.mixer.music.stop() 
    
    # Blit the background
    screen.blit(bg, (0, 0))

    # Blit the game over image
    gameover_x = (screen_width - gameover_img.get_width()) // 2
    gameover_y = (screen_height - gameover_img.get_height()) // 2
    screen.blit(gameover_img, (gameover_x, gameover_y))
    
    # Render and blit the game over text
    font = pygame.font.SysFont(None, 72)
    text = font.render("Game Over", True, WHITE)
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2 + gameover_img.get_height() // 2 + 50))
    screen.blit(text, text_rect)
    
    pygame.display.update()
    pygame.time.delay(2000)
    pygame.quit()
    quit()

def game_loop():
    global score
    global basket_x
    global fruit_x
    global fruit_y
    global current_fruit_index

    running = True
    dash_sound_played = False

    while running:
        screen.blit(bg, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            if not dash_sound_played:
                dash_sound.play()  # Play dash sound
                dash_sound_played = True
            speed = dash_speed
        else:
            dash_sound_played = False
            speed = basket_speed

        if keys[pygame.K_LEFT]:
            basket_x -= speed
        if keys[pygame.K_RIGHT]:
            basket_x += speed

        # Keep the basket within the screen bounds
        if basket_x < 0:
            basket_x = 0
        elif basket_x > screen_width - basket_width:
            basket_x = screen_width - basket_width

        fruit_y += fruits[current_fruit_index]['speed']

        # Check if the fruit is caught
        if (fruit_y + fruits[current_fruit_index]['height'] > basket_y and
                basket_x < fruit_x < basket_x + basket_width):
            score += fruits[current_fruit_index]['score']
            catch_sound.play()  # Play catch sound
            current_fruit_index = random.randint(0, len(fruits) - 1)  # Randomize next fruit
            fruit_x = random.randint(0, screen_width - fruits[current_fruit_index]['width'])
            fruit_y = -fruits[current_fruit_index]['height']

        draw_basket(basket_x, basket_y)
        draw_fruit(fruit_x, fruit_y)
        display_score(score)

        # Game over if fruit reaches the bottom
        if fruit_y > screen_height:
            game_over()

        pygame.display.update()
        clock.tick(60)

game_loop()
