import pygame
import sys




pygame.init()

bullets=[]
players=[]

font1=pygame.font.SysFont('arial',16,True)

window=pygame.display.set_mode((800,500))
clock=pygame.time.Clock()

pygame.event.pump()



class Player(object):
    def __init__(self, name, x, y, width, height, vel, up, down, shootkey, bulletcolor, sprite):
        self.name=name
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = vel
        self.sprite = pygame.image.load(f"assets/{sprite}")
        self.down=down
        self.up=up
        self.score=0
        self.shootkey=shootkey
        self.bulletcolor=bulletcolor
        self.shootratelimit=0
        players.append(self)


    def draw(self, win):
        self.movement()
        win.blit(self.sprite, (self.x, self.y))
        self.hitbox = (self.x + 20, self.y + 10, 96, 80)
        if self.shootratelimit > 0:
            self.shootratelimit -= 1
            print(self.shootratelimit)
#        pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)
        if self.score >= 100:
            winscreen(self)
            self.score=0

    def movement(self):
        # Goingup
        keys = pygame.key.get_pressed()
        if keys[self.up] and self.y > 50:
            self.y -= self.vel
            # Goingdown
        if keys[self.down] and self.y < 750:
            self.y += self.vel
        if keys[self.shootkey] and self.shootratelimit == 0:
            global shot
            shot=bullet((self.bulletcolor),10,self.x,self.y+30, self)
            self.shootratelimit = 10


class bullet(object):
    def __init__(self, color, speed, x, y, shooter):
        self.color=color
        self.speed=speed
        self.x=x
        self.y=y
        self.shooter=shooter
        if self.x < 400:
            self.moveleft=True
        else:
            self.moveleft=False
        bullets.append(self)


    def move(self):
        if self.x < 800 and self.x > 0:

            if self.moveleft:
                self.x += self.speed
            else:
                self.x -= self.speed
        else:
            bullets.pop(bullets.index(self))

    def draw(self, window):
        pygame.draw.circle(window, (self.color),(self.x,self.y),15)

        self.move()
        self.hitcontrol()

    def hitcontrol(self):
        for player in players:
            if self.y  < player.hitbox[1] + player.hitbox[3] and self.y  > player.hitbox[
                1]:
                if self.x  > player.hitbox[0] and self.x  < player.hitbox[0] + player.hitbox[2]:
                    if self.shooter != player:
                        self.shooter.score += 1
                        bullets.pop(bullets.index(self))


def displaydraw():
    window.fill((0,0,0))
    for player in players:
        player.draw(window)
        scorecounter=font1.render(f"{player.name}'s score: {player.score}", 1 , player.bulletcolor)
        window.blit(scorecounter, (player.x,50))
    for shoot in bullets:
        shoot.draw(window)
    pygame.display.update()


def winscreen(winner):
    pygame.event.get()
    pygame.display.update()
    window.fill((0,0,0))
    bullets=[]
    for player in players:
        player.score=0
    message=font1.render(f"{winner.name} has won with {winner.score} points! Press SPACE to play again",1,(255,255,255))
    window.blit(message,(200,250))
    while True:
        pygame.event.get()
        keys=pygame.key.get_pressed()
        pygame.display.update()
        if keys[pygame.K_SPACE]:
            break







Player('Player1',100,200,96,96,6,pygame.K_w,pygame.K_s,pygame.K_e,(255,0,0),'redplane.png')
Player('Player2',600,200,96,96,6,pygame.K_UP,pygame.K_DOWN,pygame.K_RSHIFT,(0,0,255), 'blueplane.png')


if __name__=='__main__':
    while True:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        clock.tick(60)
        displaydraw()
