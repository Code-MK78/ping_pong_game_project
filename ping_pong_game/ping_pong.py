from pygame import *
import time as timer
window_height = 500
window_width = 700
window = display.set_mode( (window_width, window_height) )
display.set_caption("Ping Pong Game")

game = True
finish = False
rate = time.Clock()
fps = 60
bg = transform.scale(image.load("kitchen.jpg") ,(window_width, window_height) )

font.init()
style = font.SysFont("Comic Sans", 30)

class skills():
    def __init__(self):
        self.cooldown = 0
        self.activate_time = 0
        self.activate_status = False
    def loadImage(self, filename, x, y):
        self.filename = filename
        self.image = transform.scale(image.load(self.filename) ,(100, 100) )
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class speedup_skill(skills):
    def __init__(self, x, y, player):
        super().__init__()
        self.loadImage("speeds_up.png", x, y)
        self.cooldown = 2
        self.player = player
    def activate(self):
        if self.activate_status == False:
            # print("activate speedup")
            self.activate_status = True
            self.image = transform.grayscale(self.image)
            self.activate_time = timer.time()
            self.player.speed += 2
    def draw(self):
        if (timer.time() - self.activate_time > self.cooldown) and self.activate_status == True:
            self.image = transform.scale(image.load(self.filename) ,(100, 100) )
            self.activate_status = False
            self.player.speed -= 2
        window.blit(self.image, (self.rect.x, self.rect.y))

class invertcontrol_skill(skills):
    def __init__(self, x, y, target):
        super().__init__()
        self.loadImage("mirrors.png", x, y)
        self.cooldown = 3
        self.target = target
    def activate(self):
        if self.activate_status == False:
            self.activate_status = True
            self.image = transform.grayscale(self.image)
            self.activate_time = timer.time()
            self.target.speed *= -1

    def draw(self):
        if (timer.time() - self.activate_time > self.cooldown) and self.activate_status == True:
            self.image = transform.scale(image.load(self.filename) ,(100, 100) )
            self.activate_status = False
            self.target.speed *= -1
        window.blit(self.image, (self.rect.x, self.rect.y))


class character(sprite.Sprite):
    def __init__(self, x, y, size_x, size_y, speed, filename):
        super().__init__()
        self.speed_skill = None
        self.invert_skill = None
        self.filename = filename
        self.x = x
        self.y = y
        self.size_x = size_x
        self.size_y = size_y
        self.speed = speed
        self.image = transform.scale(image.load(filename) ,(size_x, size_y) )
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_x = speed
        self.speed_y = speed
    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
        # draw.rect(window, (255, 0, 0), self.rect, width=2)

class ball(character):
    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.y >= 430:
            self.speed_y *= -1
        elif self.rect.y <= 0:
            self.speed_y *= -1
        elif self.rect.x >= 630:
            self.speed_x *= -1
        elif self.rect.x <- 0:
            self.speed_x *= -1

class goal(character):
    def update(self):
        pass
p1 = character(110, 200, 35, 175, 4, "baguette.png")
p2 = character(550, 200, 35, 175, 4, "baguette.png")

p1.speed_skill = speedup_skill(10, 50, p1)
p1.invert_skill = invertcontrol_skill(110, 50, p2)
p2.speed_skill = speedup_skill(400, 50, p2)
p2.invert_skill = invertcontrol_skill(510, 50, p1)
ball = ball(300, 200, 100, 100, 3, "meatball.png")
goal1 = goal(0, 200, 100, 150, 0, "plate1.png")
goal2 = goal(600, 200, 100, 150, 0, "plate2.png")

score_goal1 = 0
score_goal2 = 0
speedball_change_interval = 1
speedball_change_time  = timer.time()
while game:
    # print(p1.speed)
    for e in event.get():
        if e.type == QUIT:
            game = False
    if finish == False:
        keys = key.get_pressed()
        if keys[K_w] and p1.rect.y > 0:
            p1.rect.y -= p1.speed

        if keys[K_s] and p1.rect.y < window_height-p1.size_y:
            p1.rect.y += p1.speed

        if keys[K_a]:
            p1.speed_skill.activate()

        if keys[K_d]:
            p1.invert_skill.activate()

        if keys[K_UP] and p2.rect.y > 0:
            p2.rect.y -= p2.speed

        if keys[K_DOWN] and p2.rect.y < window_height-p2.size_y:
            p2.rect.y += p2.speed

        if keys[K_RIGHT]:
            p2.speed_skill.activate()

        if keys[K_LEFT]:
            p2.invert_skill.activate()

    IsCollide = sprite.collide_rect(p2, ball)
    if IsCollide and timer.time()-speedball_change_time > speedball_change_interval:
        ball.speed_x = -1 * abs(ball.speed_x)
        ball.speed_x -= 0.1
        ball.speed_y += 0.1
        speedball_change_time  = timer.time()
    IsCollide = sprite.collide_rect(p1, ball)
    if IsCollide and timer.time()-speedball_change_time > speedball_change_interval:
        ball.speed_x = 1 * abs(ball.speed_x)
        ball.speed_x += 0.1
        ball.speed_y += 0.1
        speedball_change_time  = timer.time()
    collide_goal1 = sprite.collide_rect(goal1, ball)
    collide_goal2 = sprite.collide_rect(goal2, ball)
    if collide_goal1:
        score_goal2 += 1
        ball.rect.x = 300
        ball.rect.y = 200
        ball.speed_x = 3
        ball.speed_y = 3
    elif collide_goal2:
        score_goal1 += 1
        ball.rect.x = 300
        ball.rect.y = 200
        ball.speed_x = 3
        ball.speed_y = 3


    window.blit(bg, (0, 0))
    p1.draw()
    p1.speed_skill.draw()
    p1.invert_skill.draw()
    p2.draw()
    p2.speed_skill.draw()
    p2.invert_skill.draw()
    ball.draw()
    ball.update()
    goal1.draw()
    goal2.draw()
    goal1.update()
    goal2.update()
    score_count_text = style.render(":", True, (0, 0, 0))
    window.blit(score_count_text, (330, 50))
    score1_count_text = style.render(str(score_goal1), True, (0, 0, 0))
    window.blit(score1_count_text, (310, 50))
    score2_count_text = style.render(str(score_goal2), True, (0, 0, 0))
    window.blit(score2_count_text, (340, 50))
    if score_goal1 == 12:
        ENDSCREEN1 = style.render("You win P1!", True, (0, 0, 0))
        window.blit(ENDSCREEN1, (270, 180))
        ball.speed_x = 0
        ball.speed_y = 0
        finish = True
    elif score_goal2 == 12:
        ENDSCREEN2 = style.render("You win P2!", True, (0, 0, 0))
        window.blit(ENDSCREEN2, (270, 180))
        ball.speed_x = 0
        ball.speed_y = 0
        finish = True

    display.update()
    rate.tick(60)