#!/usr/bin/env python3

import pygame
import random
import sys

class Overlay(pygame.sprite.Sprite):
    def __init__(self):
        # Equivalent statements:
        #pygame.sprite.Sprite.__init__(self)
        super(pygame.sprite.Sprite, self).__init__()
        self.image = pygame.Surface((800, 20))
        #self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()

        WHITE = (255, 255, 255)
        self.font = pygame.font.Font('freesansbold.ttf', 18)
        #self.xyxy = self.font.render('Score: 0        Lives: 5', True, WHITE)
        self.render('Score: 0        Lives: 5')

    def draw(self, screen):
        screen.blit(self.text, (0, 0))

    def render(self, text):
        self.text = self.font.render(text, True, (255, 255, 255))
        self.image.blit(self.text, self.rect)

    def update(self, score, lives):
        self.render('Score: ' + str(score) + '        Lives: ' + str(lives))

class Paddle(pygame.sprite.Sprite):
    player_image = pygame.image.load('assets/player.png')
    left = False
    right = False

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(self.player_image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = 375
        self.rect.y = 540

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        if self.left == True:
            self.rect.x -= 5
            if self.rect.x <= 0:
                self.rect.x = 0
        if self.right == True:
            self.rect.x += 5
            if self.rect.x >= 750:
                self.rect.x = 750

class Star(pygame.sprite.Sprite):
    inity =0
    initx =0
    tillBorder = 0
    starImage = pygame.image.load('assets/star.jpg')

    def __init__(self,xpos,ypos,size):
        pygame.sprite.Sprite.__init__(self)
        self.xpos = xpos
        self.ypos = ypos
        self.initx= xpos
        self.inity = ypos
        self.image = pygame.transform.scale(self.starImage,(size,size))
        self.vector = [-2, -2]

    def update(self,screen):
        if self.xpos <= 0:
            self.xpos += (600-self.ypos)
            self.ypos += (600-self.ypos)
        elif self.ypos <=0:
            self.ypos += (800 - self.xpos)
            self.xpos += (800 - self.xpos)
        self.xpos += self.vector[0]
        self.ypos += self.vector[1]
        screen.blit(self.image, (self.xpos, self.ypos))


class Block(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((25, 25))
        self.color = ( random.randint(0, 255), random.randint(0, 255), random.randint(0, 255) )
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.vector = [2,0]

    def update(self, game, bool):
        if bool == True:
            self.vector[0] *= -1
        self.rect.x += self.vector[0]

class Boss(pygame.sprite.Sprite):
    hitpoint = 15
    boss_image = pygame.image.load(r"assets/enemyBlack1.png")


    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(self.boss_image, (150, 100))
        self.rect = self.image.get_rect()
        self.rect.x = 325
        self.rect.y = 50
        self.vector = [5,0]

    def shoot(self,game):
        print("shoot")
        Lball = Ball(True)
        Rball = Ball(True)
        Lball.rect.x = (self.rect.x + 45)
        Lball.rect.y = 145
        Rball.rect.x = (self.rect.x + 105)
        Rball.rect.y = 145
        game.balls.add(Lball)
        game.balls.add(Rball)

    def is_hit(self):
        self.hitpoint -= 1
        if self.hitpoint == 0:
            game.game_over()

    def update(self,game):
        if random.randint(0,250) < 6:
            self.shoot(game)

        if (self.rect.x >= 650) or self.rect.x <= 5:
            self.vector[0] *= -1
        self.rect.x += self.vector[0]

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Ball(pygame.sprite.Sprite):
    enemy = False
    def __init__(self,enemy):
        self.enemy = enemy
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((5, 5))
        if self.enemy == False:
            pygame.draw.circle(self.image, (0, 0, 255), (5, 5),10)
        else:
            pygame.draw.circle(self.image, (255, 0, 0), (5, 5),10)

        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = 560
        self.vector = [ 0, 0 ]
        self.thud_sound = pygame.mixer.Sound('assets/thud.wav')

    def update(self, game, blocks, paddle):
        if self.rect.y < 0:
            self.kill()
            game.readyCannon(True)
        if self.rect.y > paddle.rect.y + 20:
            game.balls.remove(self)
            pygame.event.post(game.new_life_event)

        hitPlayer = pygame.sprite.spritecollideany(self, game.paddle_group)

        if hitPlayer:
            self.kill()
            game.lives -= 1

        if self.enemy == False:
            hitObject = pygame.sprite.spritecollideany(self, blocks)

            if hitObject and game.wave < 4:
                self.thud_sound.play()
                self.kill()
                game.readyCannon(True)
                hitObject.kill()
                game.score += 1
                if not bool(game.blocks):
                    if game.wave < 3:
                        game.load_enemies()
                    else:
                        game.load_boss()
                    game.wave +=1
            elif hitObject:
                self.thud_sound.play()
                self.kill()
                game.readyCannon(True)
                for boss in blocks:
                    boss.is_hit()

        else:
            self.vector = [(((paddle.rect.x )- (self.rect.x)) / 48), 3]

        self.rect.x += self.vector[0]
        self.rect.y += self.vector[1]

class Game:
    wave = 1

    def game_over(self):
        sys.exit()

    def readyCannon(self, Bool):
        self.canShoot = Bool

    def __init__(self):
        pygame.init()
        pygame.key.set_repeat(50)
        pygame.mixer.music.load('assets/loop.wav')
        pygame.mixer.music.play(-1)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((800, 600))
        self.balls = pygame.sprite.Group()
        self.bosses = pygame.sprite.Group()
        self.paddle = Paddle()
        self.paddle_group = pygame.sprite.Group()
        self.paddle_group.add(self.paddle)
        self.new_life_event = pygame.event.Event(pygame.USEREVENT + 1)
        self.blocks = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()
        self.overlay = Overlay()
        self.screen.fill((255, 255, 255))
        self.ready = True 
        self.score = 0
        self.lives = 3
        self.canShoot = True

        for s in range(0,75):
            star = Star(random.randint(0,800),random.randint(0,600),random.randint(0,10))
            self.stars.add(star)
        self.load_enemies()

    def load_enemies(self):
        for i in range(0,2):
            block = Block()
            block.rect.x = 325 + (i * 150)
            block.rect.y = 50
            self.blocks.add(block)
        for j in range(0,8):
            block = Block()
            block.rect.x = 225 + (j * 50)
            block.rect.y = 100
            self.blocks.add(block)
        for k in range(0, 10):
            block = Block()
            block.rect.x = 175 + (k * 50)
            block.rect.y = 150
            self.blocks.add(block)

    def load_boss(self):
        boss = Boss()
        self.bosses.add(boss)

    def run(self):
        self.done = False
        while not self.done:
            self.screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if self.lives <= 0:
                    pygame.quit()
                    sys.exit(0)
                #if event.type == self.new_life_event.type:
                    #self.lives -= 1
                    #if self.lives > 0:
                        #self.ready = True
                    #else:
                        #pygame.quit()
                        #sys.exit(0)

                if event.type == pygame.QUIT:
                    self.done = True
                if event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_SPACE) & self.canShoot:
                        ball = Ball(False)
                        ball.rect.x = (self.paddle.rect.x) + 25
                        ball.rect.y = (self.paddle.rect.y) + -20
                        ball.vector = [0, -10]
                        self.balls.add(ball)
                        self.readyCannon(False)
                    if event.key == pygame.K_f:
                        self.lives = 100
                    if event.key == pygame.K_LEFT:
                        self.paddle.left = True
                    if event.key == pygame.K_RIGHT:
                        self.paddle.right = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.paddle.left = False
                    if event.key == pygame.K_RIGHT:
                        self.paddle.right = False

            if random.randint(0,100) < 2:
                ball = Ball(True)
                ships = list(self.blocks)
                if len(ships) > 0:
                    attackShip = random.randint(0,len(ships)-1)
                    ball.rect.x = (ships[attackShip].rect.x) + 12
                    ball.rect.y = (ships[attackShip].rect.y) + 10
                    self.balls.add(ball)
                    ball.enemy = True

            bool = False
            for sprite in self.blocks.sprites():
                if sprite.rect.x <= 50 or sprite.rect.x >= 750:
                    bool = True


            self.blocks.update(game, bool)
            if self.wave == 4:
                self.balls.update(self, self.bosses, self.paddle)
            else:
                self.balls.update(self, self.blocks, self.paddle)
            self.stars.update(self.screen)
            self.overlay.update(self.score, self.lives)
            self.paddle.update()
            self.bosses.update(game)

            self.bosses.draw(self.screen)
            self.balls.draw(self.screen)
            self.paddle.draw(self.screen)
            self.blocks.draw(self.screen)
            self.overlay.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)

class Intro(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((800, 120))
        self.font = pygame.font.Font('freesansbold.ttf', 96)
        self.text = self.font.render('Galaxian!', True, (0, 0, 0))
        self.rect = self.image.get_rect()
        self.image.blit(self.text, self.rect)

    def draw(self, screen):
        screen.blit(self.text, (0, 0))

if __name__ == "__main__":
    game = Game()
    game.run()
