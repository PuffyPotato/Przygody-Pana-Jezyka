import pygame
import random
import pygame_menu
import time

from pygame import mixer
from pygame_menu import sound

pygame.init()
counter = 0

#definiowanie okna gry
SCREEN_HEIGHT = 720
SCREEN_WIDTH = 1080
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#rozmiar obrazków
IMG_SIZE = 64

#maxX
MAX_X = SCREEN_WIDTH - IMG_SIZE

#muzyka w tle
mixer.music.load('AutumnDay.mp3')
pygame.mixer.music.play(-1)


# wyświetlanie okna gry
pygame.display.set_caption("Przygody Pana Jeżyka")

class oobject:
    def __init__(self, X, Y, Img, change):
        self.X = X
        self.Y = Y
        self.Img = Img
        self.change = change

#gracz (jeż)
hedgehog = oobject( (SCREEN_WIDTH - IMG_SIZE) / 2, SCREEN_HEIGHT - 120 - (IMG_SIZE / 2), pygame.image.load("hedgehog.png"), 0)

hedgehog_speed = 2.5
hedgehog_mul = 1.0

# jablko
apple = oobject([random.randint(0, MAX_X), random.randint(0, MAX_X), random.randint(0, MAX_X)], [-110, -210, -510], pygame.image.load("apple.png"), [2.1, 1.9, 2.0])

# gruszka
pear = oobject(random.randint(0, MAX_X), -10, pygame.image.load("pear.png"), 2.3)

#wynik
score_val = 0
font = pygame.font.Font('Lato-Bold.ttf', 32)
textX = 5
textY = 5
timeX = 5
timeY = 42

def show_time(x, y, t):
    timee = font.render("Czas: " + str(t), True, (255,255,255))
    screen.blit(timee, (x, y))

def show_score(x, y):
    score = font.render("Wynik: " + str(score_val), True, (255,255,255))
    screen.blit(score, (x, y))

def hedgehog_move():
    global hedgehog

    hedgehog.X += hedgehog.change
        
    if hedgehog.X <= 0:
        hedgehog.X = 0
    elif hedgehog.X >= MAX_X:
        hedgehog.X = MAX_X
    draw(hedgehog.X, hedgehog.Y, hedgehog.Img)

def apple_m(X, Y, C, i):

    global apple

    draw(X[i], Y[i], apple.Img)
    Y[i] += C[i]

def apple_move():

    global apple

    for i in range(3):
        apple_m(apple.X, apple.Y, apple.change, i)
        if apple.Y[i] > SCREEN_HEIGHT:
            apple.X[i] = random.randint(0, MAX_X)
            apple.Y[i] = -10 + (i * -100)
            apple_m(apple.X, apple.Y, apple.change, i)

def pear_m(): 
    global pear
    draw(pear.X, pear.Y, pear.Img)
    pear.Y += pear.change

def pear_move():
    global pear
    global counter
    pear_m()
    if pear.Y > SCREEN_HEIGHT:
        pear.X = random.randint(0, MAX_X)
        counter = 0
        pear.Y = -10
        pear_m()

def draw(x, y, Img):
    screen.blit(Img, (x, y))

def get_speed():
    global pear
    global hedgehog

    if hedgehog.X > pear.X-64 and hedgehog.X < pear.X+64 and pear.Y+64-hedgehog.Y <= 64 and pear.Y+64-hedgehog.Y > 0:
        return True
    else:
        return False

def get_point(i):

    global apple
    global hedgehog

    if hedgehog.X > apple.X[i]-64 and hedgehog.X < apple.X[i]+64 and apple.Y[i]+64-hedgehog.Y <= 64 and apple.Y[i]+64-hedgehog.Y > 0:
        return True

    else:
        return False

def quit_the_game():
    quit()

def reset():

    global counter
    global score_val
    global pear
    global apple
    global hedgehog

    counter = 0
    score_val = 0
    pear.Y = -20
    for i in range(3):
        apple.Y[i] = (i+1) * -70
    hedgehog.X = (SCREEN_WIDTH - IMG_SIZE) / 2



def start_the_game():

    global hedgehog
    global hedgehog_speed
    global hedgehog_mul

    global apple

    global pear

    global score_val
    global counter
    delta = 0
    T = 0
    max_tps = 144
    clock = pygame.time.Clock()

    ready_pear = random.randint(220, 460)

    run = True
    while run:
        screen.fill((0,82,33))
        pygame.draw.rect(screen, (87,65,47), (0, SCREEN_HEIGHT - 120 - (IMG_SIZE / 2) + 57, SCREEN_WIDTH, 100))

        for event in pygame.event.get():

            #klawisze
            keys = pygame.key.get_pressed() #zwraca stan klawiszy na klawiaturze jako wartość logiczną
            if keys[pygame.K_RIGHT] and keys[pygame.K_LEFT]:
                hedgehog.change = 0
            elif keys[pygame.K_RIGHT]:
                hedgehog.change = hedgehog_speed * hedgehog_mul
                hedgehog.Img = pygame.image.load("hedgehog.png")
                screen.blit(hedgehog.Img, (hedgehog.X, hedgehog.Y))
            elif keys[pygame.K_LEFT]:
                hedgehog.change = -1 * hedgehog_speed * hedgehog_mul
                hedgehog.Img = pygame.image.load("hedgehog_rev.png")
                screen.blit(hedgehog.Img, (hedgehog.X, hedgehog.Y))
            else:
                hedgehog.change = 0


            #zamykanie gry
            if event.type == pygame.QUIT:
                run = False
                reset()


        #Ticking
        delta += clock.tick()/1000.0   
        while delta > 1 / max_tps:
            counter += 1
            #print(counter)
            T += 1 / max_tps
            delta -= 1 / max_tps 


            #ruch gracza
            hedgehog_move()
            #ruch jabłka
            apple_move()

            for i in range(3):
                if get_point(i):
                    bite_sound = mixer.Sound('AppleBite.wav')
                    bite_sound.play()
                    apple.Y[i] = SCREEN_HEIGHT + 1
                    score_val += 1

            if counter == ready_pear:
                #ruch gruszki
                counter = ready_pear - 1
                pear_move()

            if pear.Y > SCREEN_HEIGHT:
                pear.X = random.randint(0, MAX_X)
                counter = 0
                pear.Y = -10

            if get_speed():
                hedgehog_mul += 0.15
                pear.Y = SCREEN_HEIGHT + 1
                pear.Y = -10
                pear.X = random.randint(0, MAX_X)

                counter = 0
                ready_pear = random.randint(220, 460)

            show_score(textX, textY)
            show_time(timeX, timeY, round(T, 2))

            if score_val == 23:
                reset()
                while run:
                    screen.fill((0,0,0))
                    show_time(SCREEN_HEIGHT/2-16, SCREEN_HEIGHT/2-32, round(T, 2))
                    pygame.display.update()
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            run = False



            pygame.display.update()

    pass


#menu
menu = pygame_menu.Menu(300, 400, 'Witaj', theme=pygame_menu.themes.THEME_BLUE)
menu.add_text_input('Imię: ', default='Jacuś')
menu.add_button('Graj', start_the_game)
menu.add_button('Wyjdź', quit_the_game)
menu.mainloop(screen)