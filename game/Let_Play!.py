import random
import pygame
import time
#import spritesheet ----> We'll use this once we get all our sprites done.

# Set up pygame
pygame.mixer.pre_init(44100, -16, 2, 2048) #this code avoids the lag in the sound
pygame.init()
#pygame.mixer.init()
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Weeping Willow 0.7')
done = False
font = pygame.font.Font('prstartk.ttf', 15)# This sets the font for screen text (lives, time left, etc)
textbFont = pygame.font.Font('prstartk.ttf', 8) # This sets the font for text in the textbox
clock = pygame.time.Clock()
FPS = 60

#counter, text = 10, '10'.rjust(3)
#pygame.time.set_timer(pygame.USEREVENT, 1000)
#font = pygame.font.SysFont('Consolas', 30)

#playtime = 13846 #1 second equals about 923. This is 15 seconds long


# Game variables & images
score = 0
lives = 5
player_sprite1 = pygame.transform.scale(pygame.image.load('Girl_Stand.png'), (25, 75))
good_sprite1 = pygame.transform.scale(pygame.image.load('coin.png'), (25, 25))
bad_sprite1 = pygame.transform.scale(pygame.image.load('dragon.png'), (65, 50))
bad_sprite2 = pygame.transform.scale(pygame.image.load('earth.png'), (67, 75))
bad_sprite3 = pygame.transform.scale(pygame.image.load('icedragon.png'), (64, 50))
bad_sprite4 = pygame.transform.scale(pygame.image.load('ice.png'), (67, 75))
bad_sprite5 = pygame.transform.scale(pygame.image.load('dragon_fire.png'), (64, 50))
bad_sprite6 = pygame.transform.scale(pygame.image.load('fire1.png'), (67, 75))
bubble = pygame.transform.scale(pygame.image.load('bubble.png'), (100, 95))
buttonimg = pygame.transform.scale(pygame.image.load('button.png'), (50, 33))
textbox = pygame.image.load('textbox.png')
spotlight = pygame.image.load('spotlight.gif')
turtleimg = pygame.image.load('turtle.png')
winterimg = pygame.image.load('iceprincess.png')
firelordimg = pygame.image.load('fireboss.png')
mountainback = pygame.image.load('mountain.png')
hillback = pygame.image.load('hill.png')
iceback = pygame.image.load('icy.png')
icefloor = pygame.image.load('icefloor.png')
redback = pygame.image.load('redland.png')
fireback = pygame.image.load('fire.png')
textboxCoords = [175, 400]
textCoords = [195, 415]
skipCoords = [600, 50]
skipText = [610, 63]

# Some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREY = (129, 129, 129)
HILL_COLOR = (30,30,100)
HILL_COLOR2 = (0,0,30)
BACKGROUND = (204, 255, 255)
colors = [BLACK, GREEN, BLUE, RED]


''' -*-*-*- Scrolling background -*-*-*- '''
class background():
    def __init__(self, img, speed, y):
        #Yeah, it's a lot of variables. Sorry
        self.layer = pygame.image.load(img)
        self.layerSize = self.layer.get_size()
        self.w,self.h = self.layerSize
        self.x = 0
        self.y = y
        self.x1 = self.w
        self.y1 = y
        self.speed = speed

        # Probably don't need?:
        #self.layerRect = self.layer.get_rect()
        #self.screen = pygame.display.set_mode(self.layerSize)
        
    def move(self):
        # Move the image to the left
        self.x1 -= self.speed
        self.x -= self.speed
        # Checking the image's location. If it's at the edge, it changes the x
        if self.x < 0-self.w:
            self.x = self.w-4
        if self.x1 < 0-self.w:
            self.x1 = self.w-4

    def draw(self):
        # Drawing the images
        screen.blit(self.layer, (self.x,self.y))
        screen.blit(self.layer, (self.x1,self.y1))



''' -*-*-*- Main Sprite Class -*-*-*- '''
class sprite(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.sizex, self.sizey = img.get_rect().size
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def collide(self, checkList):
        hitList = pygame.sprite.spritecollide(self, checkList, True)
        return len(hitList)
    def setcoords(self, x, y):
        self.rect.x = x
        self.rect.y = y
    
''' -*-*-*- Player Sprite Class -*-*-*- '''
class playerSprite(sprite):
    def __init__(self, img, x, y):
        sprite.__init__(self, img, x, y)
        pygame.sprite.Sprite.__init__(self)
        self.isjump = False
        self.isfalling = False
        self.v = 0
        
    def move(self, inp):
        F = 0
        # Making the player move
        if inp[pygame.K_LEFT]:
            self.rect.x -= 6
        if inp[pygame.K_RIGHT]:
            self.rect.x += 6
        if inp[pygame.K_UP]:
            self.isjump = True

        #jumping
        if self.isjump:
            self.rect.y -= self.v
            self.v -= 1
            if self.rect.y >= SCREEN_HEIGHT-self.sizey:
                self.isjump = False
        else:
            self.v = 20
            
        # Making sure the player does not leave the windowed cage
        if self.rect.y > SCREEN_HEIGHT - self.sizey:
            self.rect.y = SCREEN_HEIGHT - self.sizey
        elif self.rect.y < 0:
            self.rect.y = 0
        if self.rect.x > SCREEN_WIDTH - self.sizex:
            self.rect.x = SCREEN_WIDTH - self.sizex
        elif self.rect.x < 0:
            self.rect.x = 0

    #def fire(self, target): We need this to work!
        '''if len(self.fireList) < 10:
            self.fireList.append((len(self.fireList))=NPCSprite(pygame.image.load('flower.png'), self.rect.x, self.rect.y, 2, 0))
            self.fireGroup.add(len(self.fireList))
            print(len(self.fireList))
        for k in range(10):
            self.fireList[k].collide(target)
            #if self.fireList[k].x > SCREEN_WIDTH:
                #self.fireList[k].remove()
        self.fireGroup.update()'''
            

''' -*-*-*- NPC Sprite Class -*-*-*- '''
# Other Sprites
class NPCSprite(sprite):
    def __init__(self, img, x, y, speedx, speedy):
        sprite.__init__(self, img, x, y)
        self.speedx = speedx
        self.speedy = speedy

    def update(self):
        # Move that enemy around
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        # When the enemy hits the edge of the screen
        #if self.rect.x > SCREEN_WIDTH + self.sizex:
            #self.rect.x = 0
        if self.rect.x < 0 - self.sizex:
            self.rect.x = random.randint(SCREEN_WIDTH, SCREEN_WIDTH+500)
        if self.rect.y > SCREEN_HEIGHT + self.sizey:
            self.rect.y = 0 - self.sizey
        elif self.rect.y < 0 - self.sizey:
            self.rect.y = SCREEN_HEIGHT

''' -*-*-*- Flying Sprite Class -*-*-*- '''
class flyingSprite(sprite):
    # This class is for flying enemies
    def __init__(self, img, x, y, speedx, speedy, height):
        sprite.__init__(self, img, x, y)
        self.speedx = speedx
        self.speedy = speedy
        self.highy = height + y
        self.lowy = y - height
    def update(self):
        # Move that enemy around
        self.rect.x += self.speedx
        if self.rect.y >= self.highy or self.rect.y <= self.lowy:
            self.speedy = -self.speedy

        self.rect.y += self.speedy
        
        # When the enemy hits the edge of the screen
        if self.rect.x < 0 - self.sizex:
            self.rect.x = random.randint(SCREEN_WIDTH, SCREEN_WIDTH+500)

''' -*-*-*- Button Sprite Class -*-*-*- '''
class button(sprite):
    def __init__(self, img, x, y):
        sprite.__init__(self, img, x, y)

    def isPressed(self):
        mouseposx, mouseposy = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed() and (((mouseposx >= self.rect.x) and (mouseposx <= self.rect.x + self.sizex)) and ((mouseposy >= self.rect.y) and (mouseposy <= self.rect.y + self.sizey))):
            return True
        else:
            return False
            
            
''' -*-*-*- Making Levels -*-*-*- '''
class level():
    def __init__(self, speed, sprites, backgroundList):
        ''' Speed determines how fast the level moves
            Sprites and backgrounds are meant to be lists. They contain every background and sprite the level uses.
            **Backgrounds should contain the image names and locations, not actual background objects
        '''
        self.speed = speed
        self.sprites = sprites
        self.backgrounds = []
        for i in range(len(backgroundList)):
            self.backgrounds.append(background(backgroundList[i][0], self.speed+i, backgroundList[i][1]))

    def drawBack(self):
        for i in range(len(self.backgrounds)):
            self.backgrounds[i].move()
            self.backgrounds[i].draw()

    def updateSprites(self):
        for i in range(len(self.sprites)):
            self.sprites[i].update()
            self.sprites[i].draw(screen)




'''-----------------------------'''

# Making those pretty pictures in the background
levelBack1 = [['mountain.png', -50], ['hill.png', 50]]
levelBack2 = [['icy.png', 0], ['icefloor.png', 70]]
levelBack3 = [['redland.png', -50], ['fire.png', 50]]

#Creating skip button
skipbutton = button(buttonimg, skipCoords[0], skipCoords[1]) #skipCoords = [600, 50]
buttonList = pygame.sprite.Group(skipbutton)

''' Creating all the sprites! '''
# The coins/good sprites for the character to collect
goodSprites = pygame.sprite.Group()
for k in range(2):
        goodSprites.add(NPCSprite(good_sprite1, random.randint(SCREEN_WIDTH, SCREEN_WIDTH+500), random.randint(200, SCREEN_HEIGHT), -3, 0))

# Level 1 enemies
groundEnemies1 = pygame.sprite.Group()
for k in range(1): 
        groundEnemies1.add(NPCSprite(bad_sprite1, random.randint(SCREEN_WIDTH, SCREEN_WIDTH+500), SCREEN_HEIGHT-50, -1, 0))
flyingEnemies1 = pygame.sprite.Group()
for k in range(2): 
        flyingEnemies1.add(flyingSprite(bad_sprite2, random.randint(SCREEN_WIDTH, SCREEN_WIDTH+500), random.randint(100, SCREEN_HEIGHT-200), -1, 1, 50))

# Level 2 enemies
groundEnemies2 = pygame.sprite.Group()
for k in range(2): 
        groundEnemies2.add(NPCSprite(bad_sprite3, random.randint(SCREEN_WIDTH, SCREEN_WIDTH+500), SCREEN_HEIGHT-50, -2, 0))
flyingEnemies2 = pygame.sprite.Group()
for k in range(2): 
        flyingEnemies2.add(flyingSprite(bad_sprite4, random.randint(SCREEN_WIDTH, SCREEN_WIDTH+500), random.randint(100, SCREEN_HEIGHT-200), -2, 2, 50))

# Level 3 enemies
groundEnemies3= pygame.sprite.Group()
for k in range(1): 
        groundEnemies3.add(NPCSprite(bad_sprite5, random.randint(SCREEN_WIDTH, SCREEN_WIDTH+500), SCREEN_HEIGHT-50, -2, 0))
flyingEnemies3 = pygame.sprite.Group()
for k in range(3): 
        flyingEnemies3.add(flyingSprite(bad_sprite6, random.randint(SCREEN_WIDTH, SCREEN_WIDTH+500), random.randint(100, SCREEN_HEIGHT-200), -2, 2, 50))
        
# Creating player
player = playerSprite(player_sprite1, 330, 300)
playerList = pygame.sprite.Group(player)

# Create bosses. Ignore the fact that They are playerSprites.. I was too lazy to make a boss class because it was like midnight when I coded this
turtle = playerSprite(turtleimg, 600, 170)
turtleBoss = pygame.sprite.Group(turtle)
winter = playerSprite(winterimg, 500, 170)
winterBoss = pygame.sprite.Group(winter)
firelord = playerSprite(firelordimg, 500, 170)
fireBoss = pygame.sprite.Group(firelord)

# Now, putting sprites and backgrounds together to make levels
levelEnemies1 = [groundEnemies1, goodSprites, flyingEnemies1]
level_1 = level(1, levelEnemies1, levelBack1)
levelEnemies2 = [groundEnemies2, goodSprites, flyingEnemies2]
level_2 = level(1, levelEnemies2, levelBack2)
levelEnemies3 = [groundEnemies3, goodSprites, flyingEnemies3]
level_3 = level(1, levelEnemies3, levelBack3)

#Misc thing, so be used later...
bubbleAttack = sprite(bubble, 600, 170)
bubbleList = pygame.sprite.Group(bubbleAttack)

'''-----------------------------'''
# Now we make all the functions for the scenes in the game
def text(text, location):
    ''' This function creates the text in textboxes. '''

    outText = ""
    outText2 = ""
    outText3 = ""
    for k in range(len(text)):
        # Gotta check if the window is closed out of
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.quit()
                pygame.quit()
                quit()
        #if not skipbutton.isPressed():
            
        # Getting the text
        if k < 40:    
            outText += text[k]
        elif k < 80:
            outText2 += text[k]
        else:
            outText3 += text[k]
            
        # Create Font objects with the text we just got
        displayText = textbFont.render(outText, True, BLACK)
        displayText2 = textbFont.render(outText2, True, BLACK)
        displayText3 = textbFont.render(outText3, True, BLACK)
        #Displaying the text
        screen.blit(displayText, location)
        screen.blit(displayText2, [location[0], location[1]+20])
        screen.blit(displayText3, [location[0], location[1]+40])
        # Update the screen and wait
        pygame.display.flip()
        pygame.display.update()
        
        time.sleep(0.05)
    time.sleep(0.5)

    
def startScreen():
    # Going to make buttons for start and character select. Need a title logo
    '''List with 2 buttons: Start and options (maybe instructions too?)
    Have arrow pointing at selected option
    If user presses up or down: Change selected index in list
    Add option to click later maybe, with option being selected when moused over
    Play menu music if we have time to find some
    '''
    global lives
    lives = 5
    mountain = background('mountain.png', 1, -50)
    hill = background('hill.png', 2, 50)
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.quit()
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    done = True
                    
        screen.fill(BACKGROUND)
        mountain.draw()
        hill.draw()
        mountain.move()
        hill.move()
        
        livestext = font.render("Press S to start!", True, BLACK) #Temporary. Will replace with buttons once I get basics working
        screen.blit(livestext, [250, 450])

        pygame.display.flip()
        pygame.display.update()
        clock.tick(60)

def cutscene1():
    # This list contains all the dialogue for the cutscene!
    textList = ["???: Hello..?   ", "Willow, can you hear me?", "If you can, I need you to... Wait. You  don't remember, do you?", "???: ...       ", "Listen to me, Willow. You may not       remember me or what you're doing here,  but you are in great danger.", "There is an army of monsters controlled by an evil witch, and they're probably  looking for you right now.", "You need to get out of there, wherever  you are. It is not safe.", "I hope you still remember enough magic  to defend yourself..."]
    done = False
    player.setcoords(330, 300)
    pygame.mixer.music.load('intro.mp3')
    pygame.mixer.music.play(-1)
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.quit()
                pygame.quit()
                quit()
        
        # A loop going through the text list and displaying it all
        for k in range(len(textList)):
            #Checking if user skipped cutscene
            if skipbutton.isPressed():
                screen.fill(BLACK)
                screen.blit(textbox, textboxCoords)
                text("Skipped!", textCoords)
                pygame.mixer.music.fadeout(1000)
                pygame.event.wait()
                return
            screen.fill(BLACK)
            screen.blit(spotlight, [220, 50])
            screen.blit(textbox, textboxCoords)
            playerList.draw(screen)
            buttonList.draw(screen)
            skipmsg = textbFont.render("Skip", True, BLACK)
            screen.blit(skipmsg, skipText)
            text(textList[k], textCoords)
            pygame.event.wait() # Wait for user to do something

        done = True
    pygame.mixer.music.fadeout(1000)
    
def gameOver():
    global lives
    global score
    screen.fill((0,0,0))
    overText = font.render("GAME OVER", True, WHITE)
    retryText = font.render("Press r to restart!", True, WHITE)
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN: # If the user presses a key
                    if event.key == pygame.K_r: # and the key pressed is r
                            lives = 5 
                            score = 0
                            return
        screen.fill((0,0,0))
        screen.blit(overText, [250, 50])
        screen.blit(retryText, [200, 400])
        
        pygame.display.flip()
        pygame.display.update()
        
    pygame.mixer.quit()
    pygame.quit()
    quit()

# ------- LEVEL 1 ------- #    
def level1():
    # Level 1 code
    screen.fill(BLACK)
    screen.blit(textbox, textboxCoords)
    text("Level 1, START!", textCoords)
    player.setcoords(0, SCREEN_HEIGHT-player.sizey)
    clock.tick(FPS)
    playtime = 27690
    BACKGROUND = (204, 255, 255)
    global lives
    global score
    screen.fill(BACKGROUND)
    level_1.drawBack()
    #screen.blit(textbox, textboxCoords)
    #text("*You think you still remember some magic.. Press SPACE to use it!* ", textCoords) #can't get the projectiles to work
    pygame.mixer.init()
    pygame.mixer.music.load('level_music.mp3')
    pygame.mixer.music.play(-1)
    print(pygame.mixer.music.get_busy())
    
    time.sleep(3)

    #start tick 
    start_ticks = pygame.time.get_ticks()  

    #Now for the main while loop
    while playtime >= 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.quit()
                pygame.quit()
                quit()
        if lives <= 0:
            return
        seconds=(pygame.time.get_ticks()-start_ticks)/1000 #calculate how many seconds
        if seconds>30: # if more than 30 seconds close the game
            break
        print (seconds) #print how many seconds
        
        #playtime -= (clock.tick(FPS))
        #playtime = int(playtime)

        # Backgrounds, sprites, and player
        screen.fill(BACKGROUND)
        level_1.drawBack()
        level_1.updateSprites()
        playerList.draw(screen)
        player.move(pygame.key.get_pressed())
        #Handling sprite interaction
        # For every bad sprite the player runs into:
        for k in range(player.collide(groundEnemies1)):
            groundEnemies1.add(NPCSprite(bad_sprite1, random.randint(SCREEN_WIDTH, SCREEN_WIDTH+500), SCREEN_HEIGHT-50, -1, 0)) # Add another bad sprite
            lives -= 1 # Take away a life
            #Flash lives red on screen
            livestext = font.render("Lives:"+str(lives), True, RED)
            screen.blit(livestext, [10, 30])
            pygame.display.flip()
            pygame.display.update()
            time.sleep(0.05)
            
        # Now for flying enemies
        for k in range(player.collide(flyingEnemies1)):
            flyingEnemies1.add(flyingSprite(bad_sprite2, random.randint(SCREEN_WIDTH, SCREEN_WIDTH+500), random.randint(200, SCREEN_HEIGHT-100), -1, 1, 100))
            lives -= 1
            livestext = font.render("Lives:"+str(lives), True, RED)
            screen.blit(livestext, [10, 30])
            pygame.display.flip()
            pygame.display.update()
            time.sleep(0.05)

        # Same as above, except for good sprites
        for k in range(player.collide(goodSprites)):
            goodSprites.add(NPCSprite(good_sprite1, random.randint(SCREEN_WIDTH, SCREEN_WIDTH+500), random.randint(200, SCREEN_HEIGHT), -2, 0))
            score += 1
            scoretext = font.render("Score:"+str(lives), True, GREEN)
            screen.blit(scoretext, [10, 5])
            pygame.display.flip()
            pygame.display.update()
            time.sleep(0.09)
            if score % 10 == 0 and score != 0:
                lives += 1
                livestext = font.render("Lives:"+str(lives), True, GREEN)
                screen.blit(livestext, [10, 30])
                pygame.display.flip()
                pygame.display.update()
                time.sleep(0.05)
        
        # Displaying score, lives, time
        scoretext = font.render("Score:"+str(score), True, BLACK)
        screen.blit(scoretext, [10, 5])

        livestext = font.render("Lives:"+str(lives), True, BLACK)
        screen.blit(livestext, [10, 30])

        timetext = font.render(str(int(30-seconds)), True, BLACK)
        screen.blit(timetext, [500, 5])

        pygame.display.flip()
        pygame.display.update()
    # Level ended!
    screen.fill(BLACK)
    screen.blit(textbox, textboxCoords)
    text("Level ended!", textCoords)
    pygame.mixer.music.fadeout(1000)
    time.sleep(3)
    
# ------- LEVEL 2 ------- #
def level2():
    # Level 2 code
    pygame.mixer.music.load('level_music.mp3')
    pygame.mixer.music.play(-1)
    screen.fill(BLACK)
    player.setcoords(0, SCREEN_HEIGHT-player.sizey)
    clock.tick(FPS)
    playtime = 32305
    BACKGROUND = (204, 255, 255)
    global lives
    global score
    if lives <= 0:
        return
    screen.blit(textbox, textboxCoords)
    text("Level 2, START!", textCoords)
    screen.fill(BACKGROUND)
    level_2.drawBack()
    time.sleep(3)

    #start tick 
    start_ticks = pygame.time.get_ticks()  

    #Now for the main while loop
    while playtime >= 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.quit()
                pygame.quit()
                quit()
        if lives <= 0:
            return
        seconds=(pygame.time.get_ticks()-start_ticks)/1000 #calculate how many seconds
        if seconds>20: # if more than 20 seconds close the game
            break
        print (seconds) #print how many seconds
            
        playtime -= (clock.tick(FPS))
        playtime = int(playtime)

        # Backgrounds, sprites, and player
        screen.fill(BACKGROUND)
        level_2.drawBack()
        level_2.updateSprites()
        playerList.draw(screen)
        player.move(pygame.key.get_pressed())
        #Handling sprite interaction
        # For every bad sprite the player runs into:
        for k in range(player.collide(groundEnemies2)):
            groundEnemies2.add(NPCSprite(bad_sprite3, random.randint(SCREEN_WIDTH, SCREEN_WIDTH+500), SCREEN_HEIGHT-50, -2, 0)) # Add another bad sprite
            lives -= 1 # Take away a life
            livestext = font.render("Lives:"+str(lives), True, RED)
            screen.blit(livestext, [10, 30])
            pygame.display.flip()
            pygame.display.update()
            time.sleep(0.05)
            
        # Now for flying enemies
        for k in range(player.collide(flyingEnemies2)):
            flyingEnemies2.add(flyingSprite(bad_sprite4, random.randint(SCREEN_WIDTH, SCREEN_WIDTH+500), random.randint(100, SCREEN_HEIGHT-200), -2, 2, 50))
            lives -= 1
            livestext = font.render("Lives:"+str(lives), True, RED)
            screen.blit(livestext, [10, 30])
            pygame.display.flip()
            pygame.display.update()
            time.sleep(0.05)

        # Same as above, except for good sprites
        for k in range(player.collide(goodSprites)):
            goodSprites.add(NPCSprite(good_sprite1, random.randint(SCREEN_WIDTH, SCREEN_WIDTH+500), random.randint(200, SCREEN_HEIGHT), -2, 0))
            score += 1
            scoretext = font.render("Score:"+str(score), True, GREEN)
            screen.blit(scoretext, [10, 5])
            pygame.display.flip()
            pygame.display.update()
            time.sleep(0.05)
            if score % 10 == 0 and score != 0:
                lives += 1
                livestext = font.render("Lives:"+str(lives), True, GREEN)
                screen.blit(livestext, [10, 30])
                pygame.display.flip()
                pygame.display.update()
                time.sleep(0.05)
        
        # Displaying score, lives, time
        scoretext = font.render("Score:"+str(score), True, BLACK)
        screen.blit(scoretext, [10, 5])

        livestext = font.render("Lives:"+str(lives), True, BLACK)
        screen.blit(livestext, [10, 30])

        timetext = font.render(str(int(20-seconds)), True, BLACK)
        screen.blit(timetext, [500, 5])

        pygame.display.flip()
        pygame.display.update()
    # Level ended!
    screen.fill(BLACK)
    screen.blit(textbox, textboxCoords)
    text("Level ended!", textCoords)
    pygame.mixer.music.fadeout(1000)
    time.sleep(3)

# ------- LEVEL 3 ------- #
def level3():
    # Level 3 code
    pygame.mixer.music.load('level_music.mp3')
    pygame.mixer.music.play(-1)
    screen.fill(BLACK)
    global lives
    global score
    if lives <= 0:
            return
    screen.blit(textbox, textboxCoords)
    text("Level 3, START!", textCoords)
    player.setcoords(0, SCREEN_HEIGHT-player.sizey)
    clock.tick(FPS)
    playtime = 36920
    BACKGROUND = (255, 191, 128)
    screen.fill(BACKGROUND)
    level_3.drawBack()
    time.sleep(3)

    start_ticks = pygame.time.get_ticks()  
    
    #Now for the main while loop
    while playtime >= 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.quit()
                pygame.quit()
                quit()
        if lives <= 0:
            return

        seconds=(pygame.time.get_ticks()-start_ticks)/1000 #calculate how many seconds
        if seconds>10: # if more than 10 seconds close the game
            break
        print (seconds) #print how many seconds

        playtime -= (clock.tick(FPS))
        playtime = int(playtime)

        # Backgrounds, sprites, and player
        screen.fill(BACKGROUND)
        level_3.drawBack()
        level_3.updateSprites()
        playerList.draw(screen)
        player.move(pygame.key.get_pressed())
        #Handling sprite interaction
        # For every bad sprite the player runs into:
        for k in range(player.collide(groundEnemies3)):
            groundEnemies3.add(NPCSprite(bad_sprite5, random.randint(SCREEN_WIDTH, SCREEN_WIDTH+500), SCREEN_HEIGHT-50, -2, 0)) # Add another bad sprite
            lives -= 1 # Take away a life
            livestext = font.render("Lives:"+str(lives), True, RED)
            screen.blit(livestext, [10, 30])
            pygame.display.flip()
            pygame.display.update()
            time.sleep(0.05)
            
        # Now for flying enemies
        for k in range(player.collide(flyingEnemies3)):
            flyingEnemies3.add(flyingSprite(bad_sprite6, random.randint(SCREEN_WIDTH, SCREEN_WIDTH+500), random.randint(100, SCREEN_HEIGHT-200), -2, 2, 50))
            lives -= 1
            livestext = font.render("Lives:"+str(lives), True, RED)
            screen.blit(livestext, [10, 30])
            pygame.display.flip()
            pygame.display.update()
            time.sleep(0.05)

        # Same as above, except for good sprites
        for k in range(player.collide(goodSprites)):
            goodSprites.add(NPCSprite(good_sprite1, random.randint(SCREEN_WIDTH, SCREEN_WIDTH+500), random.randint(200, SCREEN_HEIGHT), -2, 0))
            score += 1
            scoretext = font.render("Score:"+str(score), True, GREEN)
            screen.blit(scoretext, [10, 5])
            pygame.display.flip()
            pygame.display.update()
            time.sleep(0.05)
            if score % 10 == 0 and score != 0:
                lives += 1
                livestext = font.render("Lives:"+str(lives), True, GREEN)
                screen.blit(livestext, [10, 30])
                pygame.display.flip()
                pygame.display.update()
                time.sleep(0.05)
        
        # Displaying score, lives, time
        scoretext = font.render("Score:"+str(score), True, BLACK)
        screen.blit(scoretext, [10, 5])

        livestext = font.render("Lives:"+str(lives), True, BLACK)
        screen.blit(livestext, [10, 30])

        timetext = font.render(str(int(10-seconds)), True, BLACK)
        screen.blit(timetext, [500, 5])

        pygame.display.flip()
        pygame.display.update()
    # Level ended!
    screen.fill(BLACK)
    screen.blit(textbox, textboxCoords)
    text("Level ended!", textCoords)
    pygame.mixer.music.fadeout(1000)
    time.sleep(3)
    
def boss1():
    global lives
    if lives <= 0:
        return
    '''Script! '''
    #Turtle is facing player
    textList = ["???: Boss whatnow?", "...       ", "...       ", "...?!       ", "A.. A person?! A visitor?!"]
    #Turtle walks a little closer
    textList2 = ["I-I haven't seen another sane being     since the war of '76!", "Wait, wasn't I supposed to do something?", "...oh!", "Halt, intruder! You are trespassing on  royal territory!", "If you do not leave in 5 seconds, I willbe forced to remove you myself!", "...and it won't be pleasant!"]
    #Wait 5 seconds
    textList3 = ["Turtle thing: Nothing?", "Well. This is the most stubborn         trespasser I've seen yet!", "and, uh, the only one, BUT DON'T        UNDERESTIMATE ME!", "I can split the very land under our feetthrough sheer willpower! And I shall do so now!"]
    #Wait 3 seconds
    textList4 = ["HRRNG!!", "gRGRRRRR..!!"] #wait 3 secs between each. Have turtle shaking if possible
    #Stop shaking
    textList5 = ["Turtle thing: ...Well, I tried.", "I mean, I could still do it if I wanted to, you know!", "I used to be very strong in my prime,   you know!", "I was the strongest soldier in Her army,you know!", "...Well, um, do me a favor and forget   this ever happened.", "She wouldn't be happy if she found out Ilet an enemy get away..", "Haha.. uh, you will forget this, right?"]
    #end
    ''' End of script '''
    
    player.setcoords(100, 350)
    screen.fill(BACKGROUND)
    screen.blit(mountainback, (0,-50))
    screen.blit(hillback, (0,50))
    playerList.draw(screen)
    turtleBoss.draw(screen)
    screen.blit(textbox, textboxCoords)
    text("*Boss, FIGHT!*", textCoords)
    time.sleep(3)
    screen.blit(hillback, (0,50))
    playerList.draw(screen)
    turtleBoss.draw(screen)
    pygame.display.flip()
    pygame.display.update()
    time.sleep(0.5)
    
    #Turtle says his first lines
    for k in range(len(textList)):
        screen.blit(textbox, textboxCoords)
        text(textList[k], textCoords)
        pygame.event.wait()
        
    #Turtle moves a little closer
    for k in range(200):
        turtle.setcoords(turtle.rect.x - 1, turtle.rect.y)
        screen.fill(BACKGROUND)
        screen.blit(mountainback, (0,-50))
        screen.blit(hillback, (0,50))
        playerList.draw(screen)
        turtleBoss.draw(screen)
        pygame.display.flip()
        pygame.display.update()
        
    #Turtle says next lines
    for k in range(len(textList2)):
        screen.blit(textbox, textboxCoords)
        text(textList2[k], textCoords)
        pygame.event.wait()
        
    #Redraw stuff and wait 5 seconds
    screen.blit(mountainback, (0,-50))
    screen.blit(hillback, (0,50))
    playerList.draw(screen)
    turtleBoss.draw(screen)
    pygame.display.flip()
    pygame.display.update()
    time.sleep(4.5)
    
    #Turtle says even more lines! oh boy
    for k in range(len(textList3)):
        screen.blit(textbox, textboxCoords)
        text(textList3[k], textCoords)
        pygame.event.wait()

    #Oh dear he's trying to destroy the world again
    for k in range(len(textList4)):
        screen.fill(BACKGROUND)
        screen.blit(mountainback, (0,-50))
        screen.blit(hillback, (0,50))
        playerList.draw(screen)
        turtleBoss.draw(screen)
        #currentx = turtle.rect.x
        screen.blit(textbox, textboxCoords)
        text(textList4[k], textCoords)
        '''for k in range(100):
            if turtle.rect.x == currentx:
                turtle.setcoords(currentx+5, turtle.rect.y)
            else:
                turtle.setcoords(currentx, turtle.rect.y)'''
        pygame.display.flip()
        pygame.display.update()
        
    screen.blit(textbox, textboxCoords)
    text("ANY... SECOND... NOW...", textCoords)
    #Ok now he's shaking a lot. He needs to chill
    currentx = turtle.rect.x
    for k in range(100):
        if turtle.rect.x == currentx:
            turtle.setcoords(currentx+5, turtle.rect.y)
        else:
            turtle.setcoords(currentx, turtle.rect.y)   

        #Redraw the player and background to prepare them for madness
        screen.fill(BACKGROUND)
        screen.blit(mountainback, (0,-50))
        screen.blit(hillback, (0,50))
        playerList.draw(screen)
        turtleBoss.draw(screen)
        #Keeping text on screen (hopefully)
        anysec = textbFont.render("ANY... SECOND... NOW...", True, BLACK)
        screen.blit(anysec, textCoords)
        screen.blit(textbox, textboxCoords)
        pygame.display.flip()
        pygame.display.update()
        time.sleep(0.03)
        


    #His final lines. He's probably insane from living alone in the mountains
    for k in range(len(textList5)):
        screen.blit(textbox, textboxCoords)
        text(textList5[k], textCoords)
        pygame.event.wait()

    #Boss.. Defeated?
    screen.fill(BLACK)
    screen.blit(textbox, textboxCoords)
    text("Boss... Defeated?", textCoords)
    pygame.event.wait()

def boss2():
    global lives
    if lives <= 0:
        return

    '''Script! '''
    #Screen is black
    textList = ['???: Fight? Ugh, no thanks. ']
    #Screen shows Winter and Willow together
    textList2 = ["Fighting's for people with no chill.", "The name's Winter. And I don't know who you are, but you better freeze where you are. No trespassing!"]
    #Winter walks a little closer
    textList3 = ["Winter: Wait, wasn't turtle dude        supposed to be guarding the border?     How'd you get past him?", "Did you fight him?"]
    #Short pause
    textList4 = ["...", "You didn't fight him?", "How'd you get past him then?!"] #first is for yes, second is for no
    #short pause
    textList5 = ["Winter: Well, nevermind. It was ice to  meet you, but you're going down now!", "..What, you don't want to fight?", "Too bad, you'll just have to let it go!"]
    #Winter walks a little closer
    textList6 = ["Well, on second thought, you seem prettychill. I mean, you haven't flinched at  all from the cold or my monologue..", "You know what, I'll just let the next   guy take care of you. I have some       snowmen to build!", "...Well this is my snowland after all. I can do what I want!"]
    #Winter backs away quickly
    textList7 = ["I have to warn you, though. He's pretty .. hotheaded!"]
    '''End of Script'''
    
    player.setcoords(100, 350)
    screen.blit(textbox, textboxCoords)
    text("*Boss, FIGHT!*", textCoords)
    time.sleep(3)
    #Says first lines
    screen.blit(textbox, textboxCoords)
    text(textList[0], textCoords)
    pygame.event.wait()
    
    screen.fill(BACKGROUND)
    screen.blit(iceback, (0, 0))
    screen.blit(icefloor, (0, 50))
    playerList.draw(screen)
    winterBoss.draw(screen)
    pygame.display.flip()
    pygame.display.update()
    time.sleep(0.5)
    
    #Says next lines
    for k in range(len(textList2)):
        screen.blit(textbox, textboxCoords)
        text(textList2[k], textCoords)
        pygame.event.wait()

    #Walking a little closer..
    for k in range(200):
        winter.setcoords(winter.rect.x - 1, winter.rect.y)
        screen.fill(BACKGROUND)
        screen.blit(iceback, (0, 0))
        screen.blit(icefloor, (0, 50))
        playerList.draw(screen)
        winterBoss.draw(screen)
        pygame.display.flip()
        pygame.display.update()

    #Says next lines
    for k in range(len(textList3)):
        screen.blit(textbox, textboxCoords)
        text(textList3[k], textCoords)
        pygame.event.wait()

    screen.fill(BACKGROUND)
    screen.blit(iceback, (0, 0))
    screen.blit(icefloor, (0,50))
    playerList.draw(screen)
    winterBoss.draw(screen)
    pygame.display.flip()
    pygame.display.update()
    time.sleep(0.5)

    #Say more lines
    for k in range(len(textList4)):
        screen.blit(textbox, textboxCoords)
        text(textList4[k], textCoords)
        pygame.event.wait()

    screen.fill(BACKGROUND)
    screen.blit(iceback, (0, 0))
    screen.blit(icefloor, (0,50))
    playerList.draw(screen)
    winterBoss.draw(screen)
    pygame.display.flip()
    pygame.display.update()
    time.sleep(0.5)

    #Talk, talk, talk
    for k in range(len(textList5)):
        screen.blit(textbox, textboxCoords)
        text(textList5[k], textCoords)
        pygame.event.wait()

    #Ok, she's getting a little too close for comfort
    for k in range(100):
        winter.setcoords(winter.rect.x - 1, winter.rect.y)
        screen.fill(BACKGROUND)
        screen.blit(iceback, (0, 0))
        screen.blit(icefloor, (0, 50))
        playerList.draw(screen)
        winterBoss.draw(screen)
        pygame.display.flip()
        pygame.display.update()

    #She is talking a lot because she has no one to talk to
    for k in range(len(textList6)):
        screen.blit(textbox, textboxCoords)
        text(textList6[k], textCoords)
        pygame.event.wait()

    #Personal space restored
    for k in range(300):
        winter.setcoords(winter.rect.x + 1, winter.rect.y)
        screen.fill(BACKGROUND)
        screen.blit(iceback, (0, 0))
        screen.blit(icefloor, (0, 50))
        playerList.draw(screen)
        winterBoss.draw(screen)
        pygame.display.flip()
        pygame.display.update()
        
    screen.blit(textbox, textboxCoords)
    text(textList7[0], textCoords)
    pygame.event.wait()

    #Boss Defeated... kinda?
    screen.fill(BLACK)
    screen.blit(textbox, textboxCoords)
    text("Was that even a boss fight?", textCoords)
    pygame.event.wait()
def boss3():
    global lives
    if lives <= 0:
        return
    ''' Script! '''
    textList = ["???: Halt! Who goes there?", "How DARE you interrupt my thinking time!", "Do you even know who I am?!"]
    #delay
    textList2 = ["...  ", "..You don't know who I am? Seriously?!", "I am the one! The only! The fire lord!"]
    #delay
    textList3 = ["Fire Lord: ...  ", "No, seriously. That's my name.", "It would have been Zuko, but a certain  SOMEONE already had that name..."]
    #shake a little
    textList4 = ["No matter! I will DESTROY YOU WHERE YOU STAND!", "AHHHHHHHH!"]
    #shake again
    textList5 = ["*?! You feel an intense power in you..!*"]
    #bubble pops up and hits him
    textList6 = ["Fire Lord: ARRGH! I have been defeated!", "..And by a puny girl, no less!", "H-how? How did you do this?", "I..I think this is it for me.. light,   fading...", "Never mind, I going to take a lava bath.Bye!"]
    #takes a few back
    textList7 = ["...Wait! Before I go!", "You should meet our lovely, amazing,    beautiful queen!", "She will teach you a lesson for sure!", "HAHAAHAHA!"]
    #Shakes a bit
    textList8 = ["Fire Lord: You'll have to meet her in   her mighty castle! It's just upstream of this lava river. ", "Take a right at the three burnt trees   and you'll be there!", "Good luck, little mortal!"]
    # Fire Lord leaves.
    textList9 = ["*You don't know how, but you somehow    defeated that fire thing.*", "*Is this the magic that voice was       talking about when you woke up?*"]
    #TO BE CONTINUED
    '''End Script'''
    
    player.setcoords(100, 350)
    '''screen.fill(BACKGROUND)
    screen.blit(redback, (0,-50))
    screen.blit(fireback, (0,50))
    playerList.draw(screen)
    fireBoss.draw(screen)'''
    screen.fill(BLACK)
    screen.blit(textbox, textboxCoords)
    text("*Boss, FIGHT!*", textCoords)
    time.sleep(3)
    screen.fill(BACKGROUND)
    screen.blit(redback, (0,-50))
    screen.blit(fireback, (0,50))
    playerList.draw(screen)
    fireBoss.draw(screen)
    pygame.display.flip()
    pygame.display.update()
    time.sleep(0.5)
    
    #First Lines
    for k in range(len(textList)):
        screen.blit(textbox, textboxCoords)
        text(textList[k], textCoords)
        pygame.event.wait()

    time.sleep(2)

    #He's in denial now
    for k in range(len(textList2)):
        screen.blit(textbox, textboxCoords)
        text(textList2[k], textCoords)
        pygame.event.wait()

    time.sleep(2)

    #How could you not know the one, the only, Fire Lord?!
    for k in range(len(textList3)):
        screen.blit(textbox, textboxCoords)
        text(textList3[k], textCoords)
        pygame.event.wait()

    #He really doesn't like Zuko.
    screen.blit(textbox, textboxCoords)
    text("GRRRRRR... ZUKO...", textCoords)
    currentx = firelord.rect.x
    for k in range(100):
        if firelord.rect.x == currentx:
            firelord.setcoords(currentx+5, firelord.rect.y)
        else:
            firelord.setcoords(currentx, firelord.rect.y)
            
        #Redrawing everything for more madness
        screen.fill(BACKGROUND)
        screen.blit(redback, (0,-50))
        screen.blit(fireback, (0,50))
        playerList.draw(screen)
        fireBoss.draw(screen)
        #Keeping text on screen (hopefully)
        anysec = textbFont.render("GRRRRRR... ZUKO...", True, BLACK)
        screen.blit(textbox, textboxCoords)
        screen.blit(anysec, textCoords)
        pygame.display.flip()
        pygame.display.update()
        time.sleep(0.03)

    #Oh, he's mad now!
    for k in range(len(textList4)):
        screen.blit(textbox, textboxCoords)
        text(textList4[k], textCoords)
        pygame.event.wait()

    #HE'S CHARGING
    for k in range(25):
        firelord.setcoords(firelord.rect.x - 4, firelord.rect.y)
        screen.fill(BACKGROUND)
        screen.blit(redback, (0,-50))
        screen.blit(fireback, (0,50))
        playerList.draw(screen)
        fireBoss.draw(screen)
        pygame.display.flip()
        pygame.display.update()

    #Oh snippity snap, things about to go down
    screen.blit(textbox, textboxCoords)
    text(textList5[0], textCoords)
    time.sleep(1.5)
    bubbleAttack.setcoords(player.rect.x + player.sizex, player.rect.y)
    currentx = player.rect.x
    for k in range(200):
        if player.rect.x == currentx:
            player.setcoords(currentx+5, player.rect.y)
        else:
            player.setcoords(currentx, player.rect.y)
        screen.fill(BACKGROUND)
        screen.blit(redback, (0,-50))
        screen.blit(fireback, (0,50))
        playerList.draw(screen)
        fireBoss.draw(screen)
        #these beautiful conditionals make that bubble thing flash
        if k >= 50 and k < 150 and k % 3 == 0:
            bubbleList.draw(screen)
        elif k >= 150:
            bubbleList.draw(screen)
        pygame.display.flip()
        pygame.display.update()

    #It's like bowling, except the bowling pin is the Fire Lord and the ball is a... blue bubble thing
    time.sleep(1)
    for k in range(100):
        bubbleAttack.setcoords(bubbleAttack.rect.x+1, bubbleAttack.rect.y)
        screen.fill(BACKGROUND)
        screen.blit(redback, (0,-50))
        screen.blit(fireback, (0,50))
        playerList.draw(screen)
        fireBoss.draw(screen)
        bubbleList.draw(screen)
        pygame.display.flip()
        pygame.display.update()

#

    for k in range(int((SCREEN_WIDTH-(bubbleAttack.rect.x + bubbleAttack.sizex)-(firelord.sizex))/2)):
        screen.fill(BACKGROUND)
        screen.blit(redback, (0,-50))
        screen.blit(fireback, (0,50))
        playerList.draw(screen)
        fireBoss.draw(screen)
        
        if bubbleAttack.rect.x >= firelord.rect.x:
            bubbleAttack.setcoords(bubbleAttack.rect.x+5, bubbleAttack.rect.y)
            firelord.setcoords(firelord.rect.x+5, firelord.rect.y)
            if bubbleAttack.rect.x % 3 == 0:
                bubbleList.draw(screen)
        else:
            bubbleAttack.setcoords(bubbleAttack.rect.x+5, bubbleAttack.rect.y)
            bubbleList.draw(screen)
        
        pygame.display.flip()
        pygame.display.update()

    #Ouch.. That look like that hurt
    for k in range(len(textList6)):
        screen.blit(textbox, textboxCoords)
        text(textList6[k], textCoords)
        pygame.event.wait()

    time.sleep(0.1)

    #He's got better things to do than being beat up by a mere mortal
    for k in range(50):
        firelord.setcoords(firelord.rect.x + 1, firelord.rect.y)
        screen.fill(BACKGROUND)
        screen.blit(redback, (0,-50))
        screen.blit(fireback, (0,50))
        playerList.draw(screen)
        fireBoss.draw(screen)
        pygame.display.flip()
        pygame.display.update()

    screen.blit(redback, (0,-50))
    screen.blit(fireback, (0,50))
    playerList.draw(screen)
    fireBoss.draw(screen)
    time.sleep(0.1)

    #Inviting you to fight his queen. How kind
    for k in range(len(textList7)):
        screen.blit(textbox, textboxCoords)
        text(textList7[k], textCoords)
        pygame.event.wait()

    #Wow, he's even giving directions!
    for k in range(len(textList8)):
        screen.blit(textbox, textboxCoords)
        text(textList8[k], textCoords)
        pygame.event.wait()

    #Goodbye, fire-man thing. You shall be remembered
    for k in range(50):
        firelord.setcoords(firelord.rect.x + 5, firelord.rect.y)
        screen.fill(BACKGROUND)
        screen.blit(redback, (0,-50))
        screen.blit(fireback, (0,50))
        playerList.draw(screen)
        fireBoss.draw(screen)
        pygame.display.flip()
        pygame.display.update()

    for k in range(len(textList9)):
        screen.blit(textbox, textboxCoords)
        text(textList9[k], textCoords)
        pygame.event.wait()

    #Boss Defeated!
    screen.fill(BLACK)
    screen.blit(textbox, textboxCoords)
    text("Boss Defeated!", textCoords)
    pygame.event.wait()

def toBeContin():
    if lives <= 0:
        return
    textList = ["Willow just fought off the mighty Fire  Lord!", "But she was only able to do so after a  strange blue orb appeared..", "Is this the magic she was told about by the mysterious voice at the beginning?", "Will Willow encounter the evil witch?", "Stay tuned to find out!"]
    screen.fill(BLACK)
    screen.blit(textbox, textboxCoords)
    for k in range(len(textList)):
        screen.blit(textbox, textboxCoords)
        text(textList[k], textCoords)
        pygame.event.wait()

    screen.fill(BLACK)
    continued = font.render("To be continued", True, WHITE)
    screen.blit(continued, [220, 250])
    #pygame.display.flip()
    pygame.display.update()
    time.sleep(3)
    pygame.event.wait()
#start tick 
#start_ticks = pygame.time.get_ticks()  
#Ok, now that all that nonsense is done, we can actually make the game do stuff.
while True:
    #for e in pygame.event.get():
    #    if e.type == pygame.USEREVENT:
      #      counter -= 1
       #     text = str(counter).rjust(3) if counter > 0 else 'boom!'
       # if e.type == pygame.QUIT:break
    #else:
      #  screen.fill((255, 255, 255))
     #   screen.blit(font.render(text, True, (0, 0, 0)), (32, 48))
      #  pygame.display.flip()
       # clock.tick(60)
        #continue
    #break
    #seconds=(pygame.time.get_ticks()-start_ticks)/1000 #calculate how many seconds
    #if seconds>30: # if more than 30 seconds close the game
        #break
   # print (seconds) #print how many seconds

    startScreen()
    #cutscene1()
    level1()
    #boss1()
    level2()
    #boss2()
    level3()
    #boss3()
    toBeContin()
    gameOver()
