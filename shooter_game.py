from pygame import *
from random import randint
import time as t

gamemode = 'easy'
if gamemode == 'easy':
    r_speed = 5
    speed = 1
    l_miss_c = 45
    w_score = 50
    lives = 40
elif gamemode == 'medium':
    r_speed = 5
    speed = 1
    l_miss_c = 30
    w_score = 75
    lives = 30
elif gamemode == 'hard':
    r_speed = 5
    speed = 2
    l_miss_c = 20
    w_score = 100
    lives = 20
elif gamemode == 'crazy':
    r_speed = 10
    speed = 10
    l_miss_c = 10000
    w_score = 10000
    lives = 100000

score, miss_c = 0, 0
font.init()
font1 = font.SysFont('Arial', 30)
font2 = font.SysFont('Arial', 70)
font3 = font.SysFont('Arial', 15)
score_l = font1.render(f'Счёт: {score}', True, (255, 255, 255))
miss_l = font1.render(f'Пропущено: {miss_c}', True, (255, 255, 255))
pause_l = font2.render('PAUSE', True, (255, 215, 0))


clip = 0

clock = time.Clock()
FPS = 60


mixer.init()
# mixer.music.load('zv.ogg')
# mixer.music.play()
explode = mixer.Sound('zvuk-vzryva.ogg')


mw = display.set_mode((700, 500))
display.set_caption('Shooter best in the world')
bg = transform.scale(image.load('galaxy.jpg'), (700, 500))
run = True

class GameSprite(sprite.Sprite):
    def __init__(self, im, pl_speed, x, y, width, height):
        super().__init__()
        self.height = height
        self.width = width
        self.image = transform.scale(image.load(im), (self.height, self.width))
        self.speed = pl_speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


    def reset(self):
        mw.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        sp = self.speed
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 10:
            self.rect.x -= sp
        if keys[K_RIGHT] and self.rect.x < 610:
            self.rect.x += sp
    def shoot(self):
        bullet = Bullet('bullet.png', 8, self.rect.centerx-7, self.rect.y, 20, 15)
        bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        global miss_c
        if self.rect.y > 500:
            miss_c += 1
            self.rect.y = -50
            self.rect.x = randint(10, 610)
        self.rect.y += self.speed

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < -100:
            self.kill()



player = Player('rocket.png', r_speed, 310, 400, 100, 80)
bullets = sprite.Group()
monsters = sprite.Group()
asteroids = sprite.Group()
for i in range(5):
    ufo = Enemy('ufo.png', speed, randint(1, 600), -50, 50, 80)
    monsters.add(ufo)
for i in range(2):
    asteroid = Enemy('asteroid.png', speed, randint(1, 600), -50, 50, 80)
    asteroids.add(asteroid)
finish = False
pause = False
rel_time = False

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_w:
                if 0 <= clip < 5 and rel_time == False:
                    player.shoot()
                    clip += 1
                elif clip == 5 and rel_time == False:
                    rel_time = True
                    t1 = t.time()




            elif e.key == K_SPACE:
                if pause == False: pause = True; mw.blit(pause_l, (260, 200)); 
                elif pause == True: pause = False
                
    if not finish and not pause:
        mw.blit(bg, (0, 0))
        score_l = font1.render(f'Счёт: {score}', True, (255, 255, 255))
        miss_l = font1.render(f'Пропущено: {miss_c}', True, (255, 255, 255))
        lives_l = font1.render(f'Жизней: {lives}', True, (255, 255, 255))   
        mw.blit(score_l, (10, 10))
        mw.blit(miss_l, (10, 40))
        mw.blit(lives_l, (10, 70))

        if rel_time == True:
            t2 = t.time()
            if t2 - t1 < 3:
                reload_l = font1.render(f'Wait, reload...', True, (255, 0, 0))
                mw.blit(reload_l, (285, 460))
            else:
                clip = 0
                rel_time = False
        

        player.update()
        player.reset()
        monsters.draw(mw)
        monsters.update()
        bullets.update()
        bullets.draw(mw)
        asteroids.update()
        asteroids.draw(mw)


        bul_ufo = sprite.groupcollide(monsters, bullets, True, True)
        pl_ufo = sprite.spritecollide(player, monsters, True)
        pl_as = sprite.spritecollide(player, asteroids, True)
        bul_as = sprite.groupcollide(asteroids, bullets, True, True)
        for ufo in bul_ufo:
            ufo = Enemy('ufo.png', speed, randint(1, 600), -50, 50, 80)
            score += 1
            monsters.add(ufo)
        if miss_c >= l_miss_c:
            lose_l = font2.render('YOU LOST', True, (255, 0, 0))
            mw.blit(lose_l, (200, 230))
            finish = True
        if score >= w_score:
            win_l = font2.render('YOU WON', True, (255, 215, 0))
            mw.blit(win_l, (200, 200))
            finish = True
        if lives <= 0: 
            lose_l = font2.render('YOU LOST', True, (255, 0, 0))
            mw.blit(lose_l, (200, 200))
            explode.play()
            finish = True
        for ufo in pl_ufo:
            ufo = Enemy('ufo.png', speed, randint(1, 600), -50, 50, 80)
            monsters.add(ufo)
            lives -= 1
        for asteroid in pl_as:
            asteroid = Enemy('asteroid.png', speed, randint(1, 600), -50, 50, 80)
            asteroids.add(asteroid)
            lives -= 1
        for asteroid in bul_as:
            asteroid = Enemy('asteroid.png', speed, randint(1, 600), -50, 50, 80)
            asteroids.add(asteroid)
        

        

    display.update()
    clock.tick(FPS)