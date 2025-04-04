#создай игру "Лабиринт"!
from pygame import *
font.init()
mixer.init()
mixer.music.load('jungles.ogg')
mixer.music.play()
kick = mixer.Sound('kick.ogg') #kick.play()
money = mixer.Sound('money.ogg') #money.play()
clock = time.Clock()

finish = False

LIGHT_GREEN = (124, 252, 0)

#class

class GameSprite(sprite.Sprite):
    def __init__(self, imageg, speed, x, y):
        super().__init__()
        self.image = transform.scale(image.load(imageg), (65, 65))
        self.robot_left = transform.scale(image.load('cyborg_left.png'), (65, 65))
        self.robot_right = transform.scale(image.load('cyborg_right.png'), (65, 65))
        self.hero_left = transform.scale(image.load('hero_left.png'), (65, 65))
        self.hero_right = transform.scale(image.load('hero_right.png'), (65, 65))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y 
        self.position = 'right'
        self.direction = 'right'
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

#hero movement
    def move_hero(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_w] and self.rect.y > 0:
            self.rect.y-=self.speed
        if keys_pressed[K_a] and self.rect.x > 0:
            if self.position != 'left' and not keys_pressed[K_d]:
                self.image = self.hero_left
                self.position = 'left'
            self.rect.x-=self.speed
        if keys_pressed[K_s] and self.rect.y < 435:
            self.rect.y+=self.speed
        if keys_pressed[K_d] and self.rect.x < 635:
            if self.position != 'right' and not keys_pressed[K_a]:
                self.image = self.hero_right
                self.position = 'right'
            self.rect.x+=self.speed

#enemy movement
    def move_cyborg(self):
        if self.rect.x <= 470:
            self.direction = 'right'
            self.position = 'left'
        if self.rect.x >= win_width - 85:
            self.direction = 'left'
            self.position = 'right'

        
        if self.direction == 'left':
            if self.position != 'left':
                self.image = self.robot_left
                self.position = 'left'
            self.rect.x -= self.speed
        else:
            if self.position != 'right':
                self.image = self.robot_right
                self.position = 'right'
            self.rect.x += self.speed

class Wall(sprite.Sprite):
    def __init__(self, color, width, height, x, y):
        super().__init__()
        self.color = color
        self.width = width
        self.height = height
        self.image = Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
    

#def
def resetgame():
    hero.rect.x = 5 
    hero.rect.y = win_height - 80


#создай окно игры
win_width = 700
win_height = 500

window = display.set_mode((win_width, win_height))
display.set_caption('Maze')

#dich
font = font.SysFont('Arial', 70)
lose = font.render('YOU LOSE!', True, (255, 0, 0))
win = font.render('YOU WIN!', True, (255, 215, 0))

#bg hero cybrog and everything

background = transform.scale(image.load('background.jpg'), (700, 500))
hero = GameSprite('hero.png', 4, 5, win_height - 80)
cyborg = GameSprite('cyborg.png', 2, win_width - 80, 275)
treasure = GameSprite('treasure.png', 0, win_width - 120, win_height - 80)
# walls
w1 = Wall(LIGHT_GREEN, 450, 10, 100, 20)
w2 = Wall(LIGHT_GREEN, 350, 10, 100, 480)
w3 = Wall(LIGHT_GREEN, 10, 380, 100, 20)
w4 = Wall(LIGHT_GREEN, 10, 350, 200, 130)
w5 = Wall(LIGHT_GREEN, 10, 360, 450, 130)
w6 = Wall(LIGHT_GREEN, 10, 350, 300, 20)
w7 = Wall(LIGHT_GREEN, 130, 10, 390, 120)
walls = [w1,w2,w3,w4,w5,w6,w7]

#обработай событие «клик по кнопке "Закрыть окно"»

game = True
while game:
    keys_pressed = key.get_pressed()
    for e in event.get():
        if e.type == QUIT:
            game = False
        if keys_pressed[K_SPACE]:
            resetgame()
            finish = False

    if finish != True:
        window.blit(background, (0, 0))
        for wall in walls:
            wall.reset()
            if sprite.collide_rect(hero, wall):
                window.blit(lose, (200, 200))
                kick.play()
                finish = True
        treasure.reset()
        hero.reset()
        cyborg.reset()

        hero.move_hero()
        cyborg.move_cyborg()
        
        if sprite.collide_rect(hero, cyborg):
            window.blit(lose, (200, 200))
            kick.play()
            finish = True
        if sprite.collide_rect(hero, treasure):
            window.blit(win, (200, 200))
            money.play()
            finish = True

        display.update()
        clock.tick(60)
display.update()
