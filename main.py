from pygame import *

class GameSprite(sprite.Sprite):
    def __init__(self,player_image,x,y,speed,w,h):
        super().__init__()
        self.h = h
        self.w = w
        self.image = transform.scale(image.load(player_image), (self.w,self.h))
        self.rect = self.image.get_rect()
        self.speed = speed
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        app.blit(self.image, (self.rect.x,self.rect.y))

class Player(GameSprite):
    def __init__(self,player_image,x,y,speed,w,h,u,d):
        super().__init__(player_image,x,y,speed,w,h)
        self.u = u
        self.d = d
    def p_update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[self.u] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys_pressed[self.d] and self.rect.y < 400:
            self.rect.y += self.speed

class Ball(GameSprite):
    def __init__(self,player_image,x,y,w,h,speed_x,speed_y,speed):
        super().__init__(player_image,x,y,speed,w,h)
        self.speed_x = speed_x
        self.speed_y = speed_y

    def b_update(self,player_r,player_l):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        global count_l
        global count_r
        if self.rect.y >= 450:
            self.speed_y *= -1
        if self.rect.y <= 0:
            self.speed_y *= -1  
        if sprite.collide_rect(ball,player_l):
            self.speed_x *= -1   
        if sprite.collide_rect(ball,player_r):
            self.speed_x *= -1  

font.init()
font = font.Font(None,50)
count_l = 0
count_r = 0
app = display.set_mode((700,500))
display.set_caption('Ping-Pong')
# background = transform.scale(image.load('backgroundwn.png'),(700,500))
app.fill((153,217,234))
player_l = Player('platform.png',0,250,5,20,100,K_w,K_s)
player_r = Player('platform.png',680,250,5,20,100,K_UP,K_DOWN)
ball = Ball('ball.png',350,250,50,50,3,3,3)
game = True
finish = False
restart_count = 0
clock = time.Clock()
text_wait = font.render('Wait 5 seconds',1,(255,0,0))
while game:

    for e in event.get():
        if e.type == QUIT:
            game = False

    if finish != True:

        app.fill((153,217,234))

        text_count = font.render(str(count_l) + ':' + str(count_r),1,(255,255,255))
        app.blit(text_count,(355,0))

        player_r.reset()
        player_l.reset()

        player_l.p_update()
        player_r.p_update()

        ball.reset()

        ball.b_update(player_l,player_r)

        if ball.rect.x > 700:
            count_l += 1
            finish = True
            ball.rect.x = 350
            ball.rect.y = 250
            player_l.rect.y = 250
            player_r.rect.y = 250
        if ball.rect.x < 0:
            count_r += 1
            finish = True
            ball.rect.x = 350
            ball.rect.y = 250
            player_l.rect.y = 250
            player_r.rect.y = 250
    else:
        if restart_count >= 100:
            finish = False
            restart_count = 0
        else:
            restart_count += 1
        if count_l == 5:
            text_lose = font.render('Right Player lose',1,(255,0,0))
            app.blit(text_lose,(250,200))
        elif count_r == 5:
            text_lose = font.render('Left Player lose',1,(255,0,0))
            app.blit(text_lose,(250,200))
        else:
            app.blit(text_wait,(250,200))

    display.update() 
    clock.tick(60)