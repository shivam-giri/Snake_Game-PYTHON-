import pyttsx3 #text to speech
import pygame
import random
import os
pygame.mixer.init()
pygame.init()

#Getting voices
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')

engine.setProperty('voice', voices[0].id)

# setting of Colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
green = (0,255,0)
# Creating window for Game
screen_width = 900
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width, screen_height))

# Adding Game images:-
GameBgPic = pygame.image.load("gbgimg.jpg") #game background screen
GameOverPic = pygame.image.load("gameOverScreeen.jpg") #game over Sreen
WelcomePic = pygame.image.load("WelcomeScreen.jpg")  #welcome screen
GameBgPic= pygame.transform.scale(GameBgPic,(screen_width, screen_height)).convert_alpha()
GameOverPic= pygame.transform.scale(GameOverPic,(screen_width, screen_height)).convert_alpha()
WelcomePic= pygame.transform.scale(WelcomePic,(screen_width, screen_height)).convert_alpha()


# Creating Game Title
pygame.display.set_caption("Snakes__With__Shivam")
pygame.display.update()
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 55)

def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x,y])

def plot_snake(gameWindow, color, snk_list, snake_size):
    for x,y in snk_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])

# writing speak function:
def speak(audio):
    engine.say(audio)
    engine.runAndWait()
    
# defining Welcome screen:
def welcom():
    exit_game = False
    while not exit_game:
        speak("Welcome to Snake Ninja created by SHIVAM, Press Space Key to Play")
        gameWindow.fill(green)
        gameWindow.blit(WelcomePic,(0,0))                                       #welcome pic
        text_screen("Welcome to Snake Ninja created by SHIVAM",red,70,250)
        text_screen("\"Press Space Key to Play\"",white,245,300)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # backgraund music file ----
                    pygame.mixer.music.load("back2.mp3")
                    pygame.mixer.music.play()
                    gameloop()

        pygame.display.update()
        clock.tick(60)


# Game Loop
def gameloop():
    # Game specific variables
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    velocity_x = 0
    velocity_y = 0
    snk_list = []
    snk_length = 1
    # chec if high score file is exist:-
    if(not os.path.exists("hiscore.txt")):
        with open("hiscore.txt", "w") as f:
            f.write("0")
    with open("hiscore.txt", "r") as f:
        hiscore = f.read()

    food_x = random.randint(20, screen_width / 2)
    food_y = random.randint(20, screen_height / 2)
    score = 0
    init_velocity = 5
    snake_size = 30
    fps = 60
    while not exit_game:
        if game_over:
            with open("hiscore.txt", "w") as f:
                f.write(str(hiscore))
            gameWindow.fill(white)
            gameWindow.blit(GameOverPic,(0,0)) # game over wallpaper--
            text_screen("Game Over! Press Enter To Continue", red, 100, 250)
# setting arrow keys working:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcom()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_LEFT:
                        velocity_x = - init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_UP:
                        velocity_y = - init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0

            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y
#management of score:
            if abs(snake_x - food_x)<20 and abs(snake_y - food_y)<20:
                score +=10
                food_x = random.randint(20, screen_width / 2)
                food_y = random.randint(20, screen_height / 2)
                snk_length +=5
                if score>int(hiscore):
                    hiscore = score

            gameWindow.fill(white)
            gameWindow.blit(GameBgPic,(0,0)) #game background wallpaper
            text_screen("Score: " + str(score) + "  Hiscore: "+str(hiscore), red, 5, 5)
            pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size, snake_size])

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list)>snk_length:
                del snk_list[0]

            if head in snk_list[:-1]:
                game_over = True
                pygame.mixer.music.load("gameOver2.mp3")
                pygame.mixer.music.play()

            if snake_x<0 or snake_x>screen_width or snake_y<0 or snake_y>screen_height:
                game_over = True
                pygame.mixer.music.load("gameOver2.mp3")
                pygame.mixer.music.play()

            plot_snake(gameWindow, black, snk_list, snake_size)
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()
welcom()