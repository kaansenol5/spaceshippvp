import pygame
import sys
from threading import Thread



pygame.init()

bullets=[]
players=[]

font1=pygame.font.SysFont('arial',26,True)

window=pygame.display.set_mode((800,500))
clock=pygame.time.Clock()

pygame.event.pump()

def gamemodeselection():
    selected=0
    singlecolor=(255,0,0)
    pvpcolor=(0,0,255)
    while True:
        pygame.event.get()
        keys=pygame.key.get_pressed()
        window.fill((0,0,0))
        single=font1.render("SinglePlayer",1, singlecolor)
        pvp=font1.render("PvP",1 ,pvpcolor)
        window.blit(single,(50,250))
        window.blit(pvp,(700,250))
        if keys[pygame.K_LEFT]:
            selected=0
            singlecolor=(255,255,255)
            pvpcolor=((0,0,255))
        if keys[pygame.K_RIGHT]:
            pvpcolor=(255,255,255)
            singlecolor=((255,0,0))
            selected=1
        if keys[pygame.K_RETURN]:
            return selected
        pygame.display.update()
mode = gamemodeselection()

class Player(object):
    def __init__(self, name, x, y, width, height, vel, up, down, shootkey,supershotkey, bulletcolor,supershotcolor, sprite):
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
        self.supershotkey=supershotkey
        self.bulletcolor=bulletcolor
        self.supershotcolor=supershotcolor
        self.supershotratelimit=0
        self.shootratelimit=0
        if mode==0 and self.name == "Player2":
            self.ai =True
        else:
            self.ai=False

        players.append(self)


    def draw(self, win):
        if not self.ai:
            self.movement()
        else:
            self.autoplay()

        win.blit(self.sprite, (self.x, self.y))
        self.hitbox = (self.x + 20, self.y + 10, 96, 80)

        if self.shootratelimit > 0:
            self.shootratelimit -= 1
        #if self.supershotratelimit > 0:
        #    self.supershotratelimit -= 1
        #    self.supershotready=False
        #else:
        #    self.supershotready=True
#        pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)
        if self.score >= 100:
            winscreen(self)
            self.score=0

        #self.info=f"Supershot: {self.supershotready}"
        #info=font1.render(self.info,1,(255,255,255))
        #win.blit(info,(self.x,450))

    def movement(self):
        # Goingup
        keys = pygame.key.get_pressed()
        if keys[self.up] and self.y > 50:
            self.y -= self.vel
            # Goingdown
        if keys[self.down] and self.y < 450:
            self.y += self.vel
        if keys[self.shootkey] and self.shootratelimit == 0:
            shot=bullet((self.bulletcolor),10,self.x,self.y+30, self,1)
            self.shootratelimit = 10

        #if keys[self.supershotkey] #and self.supershotratelimit == 0:
        #    shot=bullet((self.bulletcolor),10,self.x,self.y+30, self,20)

        # FIXME: this shit (supershot) sucks and needs to be fixed but im lazy
        #    self.shootratelimit = 10

    def autoplay(self):
        for player in players:
            if player != self:
                enemy=player
        if enemy.y < self.y:
            self.y -= self.vel -3
        elif enemy.y > self.y:
            self.y += self.vel -3
        elif self.y == enemy.y and self.shootratelimit == 0:
            shot=bullet((self.bulletcolor),10,self.x,self.y+30, self,1)
            self.shootratelimit = 10




class bullet(object):
    def __init__(self, color, speed, x, y, shooter, strenght):
        self.color=color
        self.speed=speed
        self.x=x
        self.y=y
        self.strenght = strenght
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
                        self.shooter.score += self.strenght
                        bullets.pop(bullets.index(self))


def displaydraw():
    window.fill((0,0,0))
    for player in players:
        player.draw(window)
        scorecounter=font1.render(f"{player.name}'s score: {player.score}", 1 , player.bulletcolor)
        window.blit(scorecounter, (player.x,50))
    for shoot in bullets:
        shoot.draw(window)
    clock.tick(60)
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







Player('Player1',100,200,96,96,6,pygame.K_w,pygame.K_s,pygame.K_e,pygame.K_r,(255,0,0),(255,255,0),'redplane.png')
Player('Player2',600,200,96,96,6,pygame.K_UP,pygame.K_DOWN,pygame.K_RETURN,pygame.K_RSHIFT,(0,0,255),(0,255,255), 'blueplane.png')


if __name__=='__main__':
    while True:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        displaydraw()
