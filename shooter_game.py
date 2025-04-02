from pygame import *
from random import randint
from time import time as timer
mixer.init()



font.init()
font2 = font.SysFont('Arial', 35)
lost = 0
score = 0

font = font.SysFont('Arial', 70)
win = font.render('YOU WIN', True, (0, 255, 0))
lose_br = font.render('YOU LOSE', True, (255, 0, 0))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, w, h):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (w, h))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, self.rect)

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()
            

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        #global lost
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(0, 620)
            #lost += 1

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
    
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < 595:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 15, 20)
        bullets.add(bullet)

rocket = Player('rocket.png', 290, 400, 5 , 80, 100)

bullets = sprite.Group()

monsters = sprite.Group()
for i in range(5):
    monster = Enemy('ufo.png', randint(0, 620), -40, randint(1, 3), 80, 50)
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(3):
    asteroid = Enemy('asteroid.png', randint(0, 620), -40, randint(1, 2), 80, 50)
    asteroids.add(asteroid)

win_wight = 700
win_height = 500

window = display.set_mode((win_wight, win_height))
display.set_caption('Shooter')

bg = transform.scale(image.load('galaxy.jpg'), (win_wight, win_height))

fire_sound = mixer.Sound('fire.ogg')

mixer.music.load('space.ogg')
mixer.music.play()
mixer.music.set_volume(0.1)

game = True
finish = False
clock = time.Clock()

num_fire = 0
rel_time = False
bull = 5

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire += 1
                    bull -= 1
                    fire_sound.play()
                    rocket.fire()
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True
            elif finish and e.key == K_r:  # Нажмите "R" для перезапуска
                finish = False
                #lost = 0
                score = 0
                monsters.empty()
                bullets.empty()
                asteroids.empty()
                for i in range(5):
                    monster = Enemy('ufo.png', randint(0, 620), -40, randint(1, 3), 80, 50)
                    monsters.add(monster)
                for i in range(3):
                    asteroid = Enemy('asteroid.png', randint(0, 620), -40, randint(1, 2), 80, 50)
                    asteroids.add(asteroid)
    
    if not finish:
        window.blit(bg, (0, 0))

        if rel_time:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font2.render('Wait, reload..', True, (150, 0, 0))
                window.blit(reload, (250, 350))
            else:
                num_fire = 0
                bull = 5
                rel_time = False

        text_lost = font2.render('Пропущено: ' + str(lost) , 1, (255, 255, 255))
        text_score = font2.render('Счет: ' + str(score), 1, (255, 255, 255))
        text_bull = font2.render('Патроны: ' + str(bull), 1, (255, 255, 255))

        #window.blit(text_lost, (0, 35))
        window.blit(text_score, (0, 0))
        window.blit(text_bull, (0, 35))

        rocket.reset()
        rocket.update()

        monsters.draw(window)
        monsters.update()

        asteroids.draw(window)
        asteroids.update()

        bullets.draw(window)
        bullets.update()

        if sprite.groupcollide(bullets, monsters, True, True):
            score += 1
            monster = Enemy('ufo.png', randint(0, 620), -40, randint(1, 3), 80, 50)
            monsters.add(monster)
        
        if score > 9:
            finish = True
            window.blit(win, (200, 200))

        #if lost > 2:
         #   finish = True
          #  window.blit(lose_br, (200, 200))
        elif sprite.spritecollide(rocket, monsters, False):
            finish = True
            window.blit(lose_br, (200, 200))

        if sprite.spritecollide(rocket, asteroids, False):
            finish = True
            window.blit(lose_br, (200, 200))
            
    else:
        restart_text = font2.render('Нажмите R для перезапуска', 1, (255, 255, 255))
        window.blit(restart_text, (0, 450))
                    

    display.update()
    clock.tick(60)