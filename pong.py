# Pong remake
# Original Game Copyright (c)1972 Atari Inc, Remake Copyright (c)2021 cjplays Development

#-- SETUP --#

# Library imports and initial setup
import pygame, random
import pygame.freetype
pygame.init()

# Sets up font for scoring
font = pygame.freetype.Font("CourierPrime-Regular.ttf",100)
font.fgcolor = ([255,255,255])

# Window Setup
w = pygame.display.set_mode([1920,1080])
w.fill([0,0,0])

# Draw Middle Line
mid = pygame.Rect(960,0,5,1080)
pygame.draw.rect(w,[255,255,255],mid)

# Variable Setup

# Will randomly determine a direction for the ball to go in
ballDirX = random.choice([30,-30])
ballDirY = random.choice([5,-5])
ogbx = 960
ogby = 540
bx = ogbx
by = ogby
p1x = 25
p1y = 440
p2x = 1920 - 75
p2y = 440
pSpeed = 30
score1 = 0
score2 = 0
poweruptimer = 0 # -- Work in progress
p1up = False
p1down = False
p2up = False
p2down = False
point = False
begin = True
spawnpowerup = False # -- Also work in progress
powerups = ["fBall","fPaddles","kFace"] # -- Additionally, this is a work in progress
egg = pygame.mixer.Sound("sonar_ping.mp3") # -- Score Sound
crackedEgg = pygame.mixer.Sound("electric_guitar_G.mp3") # -- Win sound
bounce = pygame.mixer.Sound("button_select.mp3") # -- Paddle Sound

# Paddle Setup
p1 = pygame.Rect(p1x,p1y,50,200)
p2 = pygame.Rect(p2x,p2y,50,200)
pygame.draw.rect(w,[255,255,255],p1)
pygame.draw.rect(w,[255,255,255],p2)

# Score Setup

font.render_to(w,(850,10),str(score1))
font.render_to(w,(1020,10),str(score2))

# Main loop

running = True
while running:

#-- BALL --#
    # Erases old ball
    erase = pygame.Rect(bx,by,30,30)
    
    pygame.draw.rect(w,[0,0,0],erase,30)
    pygame.display.flip()
    # Adds current direction to ball coordinates. For example, if the ball is moving right, then ballDirX will equal 1, which adds 1 to the x of the ball. I know myself, and this is definitely something I will forget how to do and find this confusing
    bx += ballDirX
    by += ballDirY

#-- PADDLES --#
    # Moves paddles (same principle as above)
    if p1up: # -- p1up,down,etc. represent players pressing different keys
        erase2 = pygame.Rect(p1x,p1y,50,200)
        pygame.draw.rect(w,[0,0,0],erase2)
        p1y -= pSpeed
        p1 = pygame.Rect(p1x,p1y,50,200)
        pygame.draw.rect(w,[255,255,255],p1)
    if p1down:
        erase2 = pygame.Rect(p1x,p1y,50,200)
        pygame.draw.rect(w,[0,0,0],erase2)
        p1y += pSpeed
        p1 = pygame.Rect(p1x,p1y,50,200)
        pygame.draw.rect(w,[255,255,255],p1)
    if p2up:
        erase3 = pygame.Rect(p2x,p2y,50,200)
        pygame.draw.rect(w,[0,0,0],erase3)
        p2y -= pSpeed
        p2 = pygame.Rect(p2x,p2y,50,200)
        pygame.draw.rect(w,[255,255,255],p2)
    if p2down:
        erase3 = pygame.Rect(p2x,p2y,50,200)
        pygame.draw.rect(w,[0,0,0],erase3)
        p2y += pSpeed
        p2 = pygame.Rect(p2x,p2y,50,200)
        pygame.draw.rect(w,[255,255,255],p2)
    
    # Changes the x and y for the ball and checks for collisions
    ball = pygame.Rect(bx,by,30,30)
    
    # Makes the ball X negative to make it move in the opposite direction
    
    if ball.colliderect(p1):
        ballDirX = -ballDirX
        bounce.play()
        pygame.time.wait(10)
        bounce.stop()
    if ball.colliderect(p2):
        ballDirX = -ballDirX
        bounce.play()
        pygame.time.wait(10)
        bounce.stop()

    # Makes sure paddles don't go off screen
    if p1.bottom >= 1080:
        p1.bottom = 1080
        p1down = False
    if p1.top <= 0:
        p1.top = 0
        p1up = False
    if 0 <= p2.bottom >= 1080:
        p2.bottom = 1080
        p2down = False
    if p2.top <= 0:
        p2.top = 0
        p2up = False
        
    # If the ball goes off screen to the right, player 1 gets a point
    if ball.right >= 1920:
        
        # Erases old paddles
        erase2 = pygame.Rect(p1x-10,p1y-10,100,310)
        pygame.draw.rect(w,[0,0,0],erase2)
        erase3 = pygame.Rect(p2x-10,p2y-10,100,310)
        pygame.draw.rect(w,[0,0,0],erase3)
        pygame.display.flip()
        # Resets paddles to original position
        p1x = 25
        p1y = 440
        p2x = 1920 - 75
        p2y = 440
        
        # Redraws paddles in original position
        erase2 = pygame.Rect(p1x+10,p1y+10,60,210) # -- Draws a slightly bigger box to erase the previous frame (I had some issuer with trailing white pixels)
        erase3 = pygame.Rect(p2x+10,p2y+10,60,210)
        p2 = pygame.Rect(p2x,p2y,50,200)
        pygame.draw.rect(w,[255,255,255],p2)
        p1 = pygame.Rect(p1x,p1y,50,200)
        pygame.draw.rect(w,[255,255,255],p1)
        
        point = True # -- Used later to make sure ball isn't drawn partially off screen
        
        # Erases old ball frame
        erase = pygame.Rect(bx,by,30,30)
        pygame.draw.rect(w,[0,0,0],erase,30)
        
        # Increases player 1 score
        score1 += 1
        
        # Redraws Scores
        score1erase = font.get_rect("0")
        score1erase.x = 850
        score1erase.y = 10
        score1erase.height += 1
        pygame.draw.rect(w,[0,0,0],score1erase)
        font.render_to(w,(850,10),str(score1))
        
        score2erase = font.get_rect("0")
        score2erase.x = 1020
        score2erase.y = 10
        score2erase.height += 1
        pygame.draw.rect(w,[0,0,0],score2erase)
        font.render_to(w,(1020,10),str(score2))
        

        pygame.display.flip()
        
        # Plays Score sound (egg stands for Electric Guitar G)
        egg.play()
        pygame.time.wait(1500)
        egg.stop()
        
        # Chooses new ball direction
        ballDirX = random.choice([30,-30])
        ballDirY = random.choice([5,-5])
        
        # Resets ball position
        bx = ogbx
        by = ogby
        pSpeed = 30 # -- Used for powerups (WIP)
        
        
    # If the ball goes off screen to the left, player 2 gets a point
    if ball.left <= 0:
        
        # Erases old paddles
        erase2 = pygame.Rect(p1x,p1y,50,200)
        pygame.draw.rect(w,[0,0,0],erase2)
        erase3 = pygame.Rect(p2x,p2y,50,200)
        pygame.draw.rect(w,[0,0,0],erase3)
        
        # Resets paddles to original position
        p1x = 25
        p1y = 440
        p2x = 1920 - 75
        p2y = 440
        
        # Redraws paddles in original position
        erase2 = pygame.Rect(p1x+10,p1y+10,60,210) # -- Draws a slightly bigger box to erase the previous frame (I had some issuer with trailing white pixels)
        erase3 = pygame.Rect(p2x+10,p2y+10,50,210)
        p2 = pygame.Rect(p2x,p2y,50,200)
        pygame.draw.rect(w,[255,255,255],p2)
        p1 = pygame.Rect(p1x,p1y,50,200)
        pygame.draw.rect(w,[255,255,255],p1)
        
        
        point = True # -- Used later to make sure ball isn't drawn partially off screen
        
        # Increases player 2 score by 1
        score2 += 1
        
        # Erases old ball frame
        erase = pygame.Rect(bx,by,30,30)
        pygame.draw.rect(w,[0,0,0],erase,30)
        
        # Redraws Scores
        score1erase = font.get_rect("0")
        score1erase.x = 850
        score1erase.y = 10
        score1erase.height += 1
        pygame.draw.rect(w,[0,0,0],score1erase)
        score2erase = font.get_rect("0")
        score2erase.x = 1020
        score2erase.y = 10
        score2erase.height += 1
        pygame.draw.rect(w,[0,0,0],score2erase)
        font.render_to(w,(850,10),str(score1))
        font.render_to(w,(1020,10),str(score2))
        
        
        pygame.display.flip()
        
        # Plays Score sound (egg stands for Electric Guitar G)
        egg.play()
        pygame.time.wait(1500)
        egg.stop()
        
        # Chooses new ball direction
        ballDirX = random.choice([30,-30])
        ballDirY = random.choice([5,-5])
        
        # Resets ball position
        bx = ogbx
        by = ogby
        pSpeed = 30 # -- Used for powerups (WIP)

    if ball.bottom >= 1060 or ball.top <= 20:
        ballDirY = -ballDirY
    # Redraws objects
    if not point:
        pygame.draw.ellipse(w,[255,255,255],ball,30)
    elif point:
        point = False

    pygame.display.flip()
    
    # If movement keys are being held down, move the paddles
    # Event Detection:
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN:
            
            # Makes sure players are not moving both directions at once
            if event.key == pygame.K_DOWN:
                if not p2up:
                    p2down = True
            if event.key == pygame.K_UP:
                if not p2down:
                    p2up = True
            if event.key == pygame.K_w:
                if not p1down:
                    p1up = True
            if event.key == pygame.K_s:
                if not p1up:
                    p1down = True
                    
            # Cheat codes
            if event.key == pygame.K_SPACE:
                cheat = True
                while cheat:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                            cheat = False
                            break
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                cheat = False
                                break
                            if event.key == pygame.K_2: # -- sneak 100
                                score1 = 7
                                cheat = False
                                break
                            if event.key == pygame.K_1:
                                score2 = 7
                                cheat = False
                                break
        # Resets paddle movement
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                p2down = False
            if event.key == pygame.K_UP:
                p2up = False
            if event.key == pygame.K_w:
                p1up = False
            if event.key == pygame.K_s:
                p1down = False
    # Redraws mid line
    if bx <= 1075 and bx >= 850:
        pygame.draw.rect(w,[255,255,255],mid)
        if by >= 7 or by <= 87:
            font.render_to(w,(850,10),str(score1))
            font.render_to(w,(1020,10),str(score2)) 
    # Redraws Paddles
    pygame.draw.rect(w,[255,255,255],p1)
    pygame.draw.rect(w,[255,255,255],p2)
    # Checks if ball has collided with powerup
    if spawnpowerup and ball.colliderect(powerupr):
        pup = random.choice(["fastBall","fastPaddles","keagenFace"])
        if pup == "fastBall":
            ballDirX *= 2
            ballDirY *= 2
           
        elif pup == "fastPaddles":
            pSpeed *= 2

    # Waits so that the ball doesn't go FLYING
    if not begin:
        pygame.time.wait(10)
        #poweruptimer += 1
        if poweruptimer >= 20:
            spawnpowerup = True
            powerupr = pygame.Rect(900,420,120,120)
            pygame.draw.rect(w,[255,0,0],powerupr)
    if begin:
        pygame.time.wait(1500)
        begin = not begin
    if score1 >= 7:
        print("Player 1 WINS!")
        crackedEgg.play()
        pygame.time.wait(1000)
        running = False
    elif score2 >= 7:
        print("Player 2 WINS!")
        crackedEgg.play()
        pygame.time.wait(1000)
        running = False
    
