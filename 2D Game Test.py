import pygame
from pygame.locals import KEYDOWN, K_ESCAPE, QUIT
import math
import random
import time as sleep
print("Github Commit Test")
pygame.init()
infoObject = pygame.display.Info()
ScreenWidth = infoObject.current_w
ScreenHeight = infoObject.current_h

Distance = 1000
Points = 0
FrameCount = 0
PlayerWidth = 50
PlayerLength = 50
x = 150
y = (ScreenHeight/2)-PlayerLength/2
vel = 15
direction = 0
TargetWidth = 50
TargetLength = 50
obstacle_x, obstacle_y = 0, 0
Targetx= (ScreenWidth/2)-TargetWidth/2 + 200
Targety = (ScreenHeight/2)-TargetLength/2 + 200
time = 6

class Obstacle:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self):
        pygame.draw.rect(screen, (255, 255, 255), self.rect)

obstacles = []

clock = pygame.time.Clock()

screen = pygame.display.set_mode([ScreenWidth, ScreenHeight])
running = True

font = pygame.font.Font('freesansbold.ttf', 32)
GOfont = pygame.font.Font('freesansbold.ttf', 55)
def Xobstacle(obstacle_width, obstacle_height, obstacle_x, obstacle_y):
    obstacles.append(Obstacle(obstacle_x, obstacle_y, obstacle_width, obstacle_height))

# Obstacles (width, length, x, y)
Xobstacle(55,700, 650, 100)
Xobstacle(1000,55, 200, 450)


#`Main Game loop
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False
    
    # Based on distance between player and target
    Distance = int(math.sqrt(((Targetx-x) ** 2 + (Targety - y) ** 2)))

    # Change colour of background based on points
    Rpoints = (1 - (Distance / ScreenHeight)) * 255
    Bpoints = (Distance / ScreenHeight) * 255
    if Rpoints > 255:
        Rpoints = 255
    if Bpoints > 255:
        Bpoints = 255
    Rpoints, Bpoints = abs(Rpoints), abs(Bpoints)
    screen.fill((Rpoints,0,Bpoints))
   
    keys = pygame.key.get_pressed()

    for obstacle in obstacles:
        # renders each obstacle
        obstacle.draw()

    PlayerObject =  pygame.Rect(x, y, PlayerWidth, PlayerLength)
    TargetObject =  pygame.Rect(Targetx, Targety, TargetWidth, TargetLength)
    collide = PlayerObject.colliderect(TargetObject)

    # Movement and Collision checking with obstacles
    if keys[pygame.K_a] and x > vel:
        new_x = x - vel
        if not any(obstacle.rect.colliderect(pygame.Rect(new_x, y, PlayerWidth, PlayerLength)) for obstacle in obstacles):
            x = new_x
    if keys[pygame.K_d] and x < ScreenWidth - vel - PlayerWidth:
        new_x = x + vel
        if not any(obstacle.rect.colliderect(pygame.Rect(new_x, y, PlayerWidth, PlayerLength)) for obstacle in obstacles):
            x = new_x
    if keys[pygame.K_w] and y > vel:
        new_y = y - vel
        if not any(obstacle.rect.colliderect(pygame.Rect(x, new_y, PlayerWidth, PlayerLength)) for obstacle in obstacles):
            y = new_y
    if keys[pygame.K_s] and y < ScreenHeight - PlayerLength - vel:
        new_y = y + vel
        if not any(obstacle.rect.colliderect(pygame.Rect(x, new_y, PlayerWidth, PlayerLength).inflate(0, -8.5)) for obstacle in obstacles):
            y = new_y
    
    text = font.render('Distance: ' + str(Distance), True, (255,255,255))
    textRect = (text.get_rect()[0] +15, 15, 0, 0)
    
    # Timer
    FrameCount += 1
    if FrameCount % 6 == 0:
        time -= 0.1

    point = pygame.mouse.get_pos()
    collide2 = TargetObject.collidepoint(point)

    # Collision checking with target and Spawns new target
    if collide or (collide2 and pygame.mouse.get_pressed()[0]):
        time += 1
        Targetx, Targety = random.randint(0,ScreenWidth-50), random.randint(0,ScreenHeight-50)
        for obstacle in obstacles:
            if (obstacle_x-Targetx < 100 or obstacle_y-Targety < 100):
                Targetx, Targety = random.randint(0,ScreenWidth-50), random.randint(0,ScreenHeight-50)
        Points += 1
            
    text2 = font.render('Points: ' + str(Points), True, (255,255,255))
    textRect2 = ((ScreenWidth/2) - 80,15, 0, 0)

    # Rendering 
    TimeText = font.render('Time: ' + str(round(time, 1)), True, (255,255,255))
    TimeRect = (ScreenWidth - TimeText.get_rect()[2] - 50,15, 0, 0)
    screen.blit(text, textRect)
    screen.blit(text2, textRect2)
    screen.blit(TimeText, TimeRect)
    pygame.draw.rect(screen, (255,255,255), PlayerObject)
    pygame.draw.rect(screen, (0,255,255), TargetObject)

    if time < 0:
        running = False

    pygame.display.update()
    clock.tick(60)

# Game Over Screen
if time < 0:
    screen.fill((Rpoints,40,Bpoints))
    GameOver = GOfont.render("You ran out of time!", True, (255,255,255))
    GameOverRect = (ScreenWidth/2 - (GameOver.get_rect()[2]/2), ScreenHeight/2 - (GameOver.get_rect()[3]/2), 0, 0)
    screen.blit(GameOver, GameOverRect)
    pygame.display.update()
    sleep.sleep(3)

pygame.quit()