# Import required libraries
import pygame
import random

# Initialize required pygame modules
pygame.init()
pygame.font.init()
pygame.mixer.init()

# Set global variables
basket_speed = 10
dash_speed = 30
clock = pygame.time.Clock()
WHITE = (255, 255, 255)

# Set up boundaries of play area
screen_width = 1920
screen_height = 1080
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Catch the Beat")

# Load and initialize game sprites and images
bg = pygame.image.load('Images/background.jpg')
basket_img = pygame.image.load('Images/catcher.png')
basket_img = pygame.transform.scale(basket_img, (150, 150))
gameover_img = pygame.image.load('Images/gameover.webp') 
watermelon_img = pygame.image.load('Sprites/Watermelon.png')
grape_img = pygame.image.load('Sprites/Grape.png')  
cherry_img = pygame.image.load('Sprites/Cherry.png') 
chili_img = pygame.image.load('Sprites/Chili.png') 
pineapple_img = pygame.image.load('Sprites/Pineapple.png')

# Initialize game sounds and music
catch_sound = pygame.mixer.Sound('Sounds/item00.wav')
gameover_sound = pygame.mixer.Sound('Sounds/pldead00.wav')
dash_sound = pygame.mixer.Sound('Sounds/ok00.wav')
pygame.mixer.music.load('Sounds/bgm.wav')
pygame.mixer.music.play(-1)  # Play background music on loop

# Assign unique properties to each subcategory of fruit using list of dictioanries to store key value pairs.
fruits_data = [
    {'image': watermelon_img, 'width': 50, 'height': 50, 'speed': 6, 'score': 10},
    {'image': grape_img, 'width': 50, 'height': 50, 'speed': 7, 'score': 20},
    {'image': pineapple_img, 'width': 50, 'height': 50, 'speed': 8, 'score': 30},
    {'image': cherry_img, 'width': 50, 'height': 50, 'speed': 9, 'score': 40},
    {'image': chili_img, 'width': 50, 'height': 50, 'speed': 10, 'score': 50}
]

class Drawable:
    """
    Abstract base class for all drawable objects in the game.
    Provides a method to draw the object on the screen.
    """
    def draw(self, screen):
        raise NotImplementedError("Subclasses must implement draw method")

class Basket(Drawable):
    """
    Handles movement and drawing of the player controlled basket object.
    """
    def __init__(self, image, x, y, width, height, speed):
        self.image = image
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed

    def move(self, direction, dash):
        """
        Moves the basket left or right, with an optional dash for increased speed.
        Keeps the basket within the screen bounds.
        """
        speed = dash_speed if dash else self.speed
        if direction == "left":
            self.x -= speed
        elif direction == "right":
            self.x += speed

        # Keep the basket within the screen bounds
        if self.x < 0:
            self.x = 0
        elif self.x > screen_width - self.width:
            self.x = screen_width - self.width

    def draw(self, screen):
        """
        Draws the basket on the screen.
        """
        screen.blit(self.image, (self.x, self.y, self.width, self.height))

class Fruit(Drawable):
    """
    Handles the random spawning and drawing of the various subcategories of fruit.
    """
    def __init__(self, data):
        self.image = data['image']
        self.width = data['width']
        self.height = data['height']
        self.speed = data['speed']
        self.score = data['score']
        self.x = random.randint(0, screen_width - self.width)
        self.y = -self.height

    def fall(self):
        """
        Handles the falling of the fruit objects within the y axis of the play area.
        """
        self.y += self.speed

    def draw(self, screen):
        """
        Draws the fruit onjects on the screen.
        """
        screen.blit(self.image, (self.x, self.y, self.width, self.height))

class Game:
    """
    Manages the overall game logic and flow.
    Handles the game loop, event processing, and game state updates.
    """
    def __init__(self):
        self.basket = Basket(basket_img, screen_width // 2 - 75, screen_height - 120, 150, 150, basket_speed)
        self.fruit = Fruit(random.choice(fruits_data))
        self.score = 0
        self.running = True

    def check_collision(self):
        """
        Checks if the basket has caught the fruit.
        If caught, it triggers the catch sound, updates the score and spawns a new fruit object.
        """
        if (self.fruit.y + self.fruit.height > self.basket.y and
                self.basket.x < self.fruit.x < self.basket.x + self.basket.width):
            self.score += self.fruit.score
            catch_sound.play()
            self.fruit = Fruit(random.choice(fruits_data))

    def game_over(self):
        """
        Handles game over logic including displaying the game over screen.
        Terminitates the process on game over.
        """
        gameover_sound.play()
        pygame.mixer.music.stop()

        # Display game over screen and terminate game
        screen.blit(bg, (0, 0))
        gameover_x = (screen_width - gameover_img.get_width()) // 2
        gameover_y = (screen_height - gameover_img.get_height()) // 2
        screen.blit(gameover_img, (gameover_x, gameover_y))
        font = pygame.font.SysFont(None, 72)
        text = font.render("Game Over", True, WHITE)
        text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2 + gameover_img.get_height() // 2 + 50))
        screen.blit(text, text_rect)

        pygame.display.update()
        pygame.time.delay(2000)
        pygame.quit()
        quit()

    def display_score(self):
        """
        Displays the current score on the screen.
        """
        font = pygame.font.SysFont(None, 50)
        text = font.render("Score: " + str(self.score), True, WHITE)
        screen.blit(text, (10, 10))

    def display_instructions(self):
        """
        Displays instructions for the player on the screen.
        """
        font = pygame.font.SysFont(None, 25)
        text = font.render("Use the left and right arrows to control and shift to dash ", True, WHITE)
        screen.blit(text, (10, 50))

    def run(self):
        """
        The main game loop.
        Handles event processing, game logic, and screen updates.
        """
        dash_sound_played = False

        while self.running:
            screen.blit(bg, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            keys = pygame.key.get_pressed()
            dash = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]

            if dash and not dash_sound_played:
                dash_sound.play()
                dash_sound_played = True
            elif not dash:
                dash_sound_played = False

            if keys[pygame.K_LEFT]:
                self.basket.move("left", dash)
            if keys[pygame.K_RIGHT]:
                self.basket.move("right", dash)

            self.fruit.fall()
            self.check_collision()

            self.basket.draw(screen)
            self.fruit.draw(screen)
            self.display_score()
            self.display_instructions()

            if self.fruit.y > screen_height:
                self.game_over()

            pygame.display.update()
            clock.tick(60)

# Create and run the game process
game = Game()
game.run()
