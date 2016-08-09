import random
import pygame
import time
file = 'intro.mp3'
level_music = 'level_music.mp3'
#<<<<<< HEAD

#=======
#>>>>>>> bf07322e37038967621cec0d10131fdc8dcaa5ae
#import spritesheet ----> We'll use this once we get all our sprites done.

# Set up pygame
pygame.init()
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Game 0.5')
done = False
font = pygame.font.Font('prstartk.ttf', 15)# This sets the font for screen text (lives, time left, etc)
textbFont = pygame.font.Font('prstartk.ttf', 9) # This sets the font for text in the textbox
clock = pygame.time.Clock()
FPS = 60
#<<<<<<< HEAD
playtime = 13846 #1 second equals about 923. This is 15 seconds long
#set up intro music

pygame.mixer.init()
pygame.mixer.music.load(file)

pygame.mixer.music.play(-1)
#=======
#playtime = 13846 #1 second equals about 923. This is 15 seconds long
#>>>>>>> bf07322e37038967621cec0d10131fdc8dcaa5ae


# Game variables & images
score = 0
lives = 3
player_sprite1 = pygame.transform.scale(pygame.image.load('Girl_Stand.png'), (25, 75))
good_sprite1 = pygame.image.load('flower.png')
bad_sprite1 = pygame.image.load('goomba.png')
textbox = pygame.image.load('textbox.png')
spotlight = pygame.image.load('spotlight.gif')
textboxCoords = [175, 400]
textCoords = [195, 415]

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
    
''' -*-*-*- Player Sprite Class -*-*-*- '''
class playerSprite(sprite):
    def __init__(self, img, x, y):
        sprite.__init__(self, img, x, y)
        pygame.sprite.Sprite.__init__(self)
        #self.velocy = 0
        #self.ground = y
        #self.fireList = []
        #self.fireGroup = pygame.sprite.Group()
        self.isjump = False
        self.isfalling = False
        self.v = 0
        
    def move(self, inp):
        F = 0
        # Making the player move
        if inp[pygame.K_LEFT]:
            self.rect.x -= 4
        if inp[pygame.K_RIGHT]:
            self.rect.x += 4
        '''if inp[pygame.K_UP]:
            self.rect.y -= 4
        if inp[pygame.K_DOWN]:
            self.rect.y += 4'''
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

        '''if self.isfalling:
            self.rect.y += self.v
            self.v += 0.5
            if self.rect.y => SCREEN_HEIGHT:
                self.isfalling = False'''
            
        '''self.rect.y = self.rect.y - F
        self.v = self.v - 1

        if self.rect.y >= 500:
            self.rect.y = 500
            self.isjump = 0
            self.v = 8
            self.isjump = False

        
        self.rect.y += self.velocy
        if self.velocy < 0:
            self.velocy += 0.1
        #if self.rect.y > self.ground:
            #self.velocy = 0
            #self.rect.y = self.ground'''
            
        # Making sure the player does not leave the windowed cage
        if self.rect.y > SCREEN_HEIGHT - self.sizey:
            self.rect.y = SCREEN_HEIGHT - self.sizey
        elif self.rect.y < 0:
            self.rect.y = 0
        if self.rect.x > SCREEN_WIDTH - self.sizex:
            self.rect.x = SCREEN_WIDTH - self.sizex
        elif self.rect.x < 0:
            self.rect.x = 0

    #def fire(self, target):
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
        if self.rect.x > SCREEN_WIDTH + self.sizex:
            self.rect.x = 0
        elif self.rect.x < 0 - self.sizex:
            self.rect.x = SCREEN_WIDTH
        if self.rect.y > SCREEN_HEIGHT + self.sizey:
            self.rect.y = 0 - self.sizey
        elif self.rect.y < 0 - self.sizey:
            self.rect.y = SCREEN_HEIGHT

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
#<<<<<<< HEAD
levelBack2 = [['nglac.png', -50], ['icefloor.png', 50]]
levelBack3 = [['back_fire.png', -50], ['fire.png', 50]]
stop3 = [['back_fire.png', -50], ['castle.png', 50]]
#=======
#>>>>>>> bf07322e37038967621cec0d10131fdc8dcaa5ae

''' Creating all the sprites! '''
# The coins/good sprites for the character to collect
goodSprites = pygame.sprite.Group()
for k in range(3):
        goodSprites.add(NPCSprite(good_sprite1, random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT), random.randint(-2, 2), random.randint(-2, 2)))

# Level 1 enemies
enemySprites1 = pygame.sprite.Group()
for k in range(3): 
        enemySprites1.add(NPCSprite(bad_sprite1, random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT), random.randint(-2, 2), random.randint(-2, 2)))

# Creating player
player = playerSprite(player_sprite1, 340, 350)
playerSprite = pygame.sprite.Group(player)


# Now, putting sprites and backgrounds together to make levels
levelEnemies1 = [enemySprites1, goodSprites]
level_1 = level(1, levelEnemies1, levelBack1)
#<<<<<<< HEAD
levelEnemies2 = [enemySprites1, goodSprites]
level_2 = level (2, levelEnemies1, levelBack2)
levelEnemies3 = [enemySprites1, levelBack3]
level_3 = level (3, levelEnemies1, levelBack3)
levelEnemies6 = [enemySprites1, stop3]
stop_3 = level (4, levelEnemies1, stop3)
#=======
#>>>>>>> bf07322e37038967621cec0d10131fdc8dcaa5ae

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
                pygame.quit()
                quit()
                
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

    
def startScreen():
    # Going to make buttons for start and character select. Need a title logo
    '''List with 2 buttons: Start and options (maybe instructions too?)
    Have arrow pointing at selected option
    If user presses up or down: Change selected index in list
    Add option to click later maybe, with option being selected when moused over
    Play menu music if we have time to find some
    '''
    mountain = background('starter_screen.png', 1, -50)
    #hill = background('hill.png', 2, 50)
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    done = True
                    
        screen.fill(BACKGROUND)
        mountain.draw()
        #hill.draw()
        #mountain.move()
        #hill.move()
        
        livestext = font.render("Press S to start!", True, BLACK) #Temporary. Will replace with buttons once I get basics working
        screen.blit(livestext, [250, 450])

        pygame.display.flip()
        pygame.display.update()
        clock.tick(60)

def cutscene1():
    # This list contains all the dialogue for the cutscene!
    textList = ["Hello..?   ", "Willow, can you hear me?", "If you can, I need you to... Wait. You  don't remember, do you?", "...       ", "Listen to me, Willow. You may not       remember me or what you're doing here,  but you are in great danger.", "There is an army of monsters controlled by an evil witch, and they're probably  looking for you right now.", "You need to get out of there, wherever  you are. It is not safe.", "I hope you still remember enough magic  to defend yourself...", "Good Luck Willow", "and remember...", "use the arrow keys to move"]
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
        # A loop going through the text list and displaying it all
        for k in range(len(textList)):
            screen.fill(BLACK)
            screen.blit(spotlight, [220, 50])
            screen.blit(textbox, textboxCoords)
            playerSprite.draw(screen)
            text(textList[k], textCoords)
            pygame.event.wait() # Wait for user to do something

        done = True

def gameOver():
    #not working correctly
    screen.fill((0,0,0))
    overText = font.render("GAME OVER", True, WHITE)
    screen.blit(overText, [300, 50])
    done = False
    print(done)
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                print(done)
        #print("hi")
        screen.fill((0,0,0))
        #overText = font.render("GAME OVER", True, WHITE)
        screen.blit(overText, [300, 50])
#<<<<<<< HEAD

        pygame.display.flip()
        pygame.display.update()
#=======
#>>>>>>> bf07322e37038967621cec0d10131fdc8dcaa5ae
    pygame.quit()
    quit()
    
def level1():
    # Level 1 code
    cutscene1()
    score = 0
    lives = 3
    clock.tick(FPS)
    #level_1 = level(1, levelEnemies1, levelBack1)
    playtime = 27690
    BACKGROUND = (204, 255, 255)
    screen.fill(BACKGROUND)
    level_1.drawBack()
    #screen.blit(textbox, textboxCoords)
    #text("*You think you still remember some magic.. Press SPACE to use it!* ", textCoords) #can't get the projectiles to work
    #pygame.event.wait()

    #Now for the main while loop
    while playtime >= 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

    
    
#<<<<<<< HEAD
        if lives <= 0:
            '''screen.fill((0,0,0))
            overText = font.render("GAME OVER", True, WHITE)
            screen.blit(overText, [300, 50]) #not working correctly'''
            return
#=======
        '''if lives <= 0:
            screen.fill((0,0,0))
            overText = font.render("GAME OVER", True, WHITE)
            screen.blit(overText, [300, 50])''' #not working correctly
#>>>>>>> bf07322e37038967621cec0d10131fdc8dcaa5ae
        
        
        playtime -= (clock.tick(FPS))
        playtime = int(playtime)

        # Backgrounds, sprites, and player
        screen.fill(BACKGROUND)
        level_1.drawBack()
        level_1.updateSprites()
        playerSprite.draw(screen)
        player.move(pygame.key.get_pressed())
        #Handling sprite interaction
        # For every bad sprite the player runs into:
        for k in range(player.collide(enemySprites1)):
            enemySprites1.add(NPCSprite(bad_sprite1, random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT), random.randint(-2, 2), random.randint(-2, 2))) # Add another bad sprite
            lives -= 1 # Take away a life

        # Same as above, except for good sprites
        for k in range(player.collide(goodSprites)):
            goodSprites.add(NPCSprite(good_sprite1, SCREEN_WIDTH, random.randint(50, SCREEN_HEIGHT), -4, 0))
            score += 1
        
        # Displaying score, lives, time
        scoretext = font.render("Score:"+str(score), True, BLACK)
        screen.blit(scoretext, [10, 5])

        livestext = font.render("Lives:"+str(lives), True, BLACK)
        screen.blit(livestext, [10, 30])

        timetext = font.render(str(playtime), True, BLACK)
        screen.blit(timetext, [500, 5])

        pygame.display.flip()
        pygame.display.update()



startScreen()
#cutscene1()
level1()
#cutscene2() Figure out what is happening in this scene
gameOver()

'''# This while loop will be replaced eventually
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # Timer
    playtime -= (clock.tick(FPS))
    playtime = int(playtime)
    
    if playtime <= 0:
        currentLevel += 1
        playtime = 13846

    
    # Creating levels
    screen.fill(BACKGROUND)
    print(currentLevel)
    if currentLevel == 1:
        level_1.drawBack()
        level_1.updateSprites()
        

        # For every bad sprite the player runs into:
        for k in range(player.collide(enemySprites1)):
            enemySprites1.add(NPCSprite(bad_sprite1, random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT), random.randint(-2, 2), random.randint(-2, 2))) # Add another bad sprite
            lives -= 1 # Take away a life

        # Same as above, except for good sprites
        for k in range(player.collide(goodSprites)):
            goodSprites.add(NPCSprite(good_sprite1, random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT), random.randint(-2, 2), random.randint(-2, 2)))
            score += 1
            
    ^ ^Next up: more levels^ ^

    # Now drawing and moving the player
    playerSprite.draw(screen)
    player.move(pygame.key.get_pressed())

    
    testing code goes here
    # No tests atm
     End of tests 

    # Displaying score, lives, time
    scoretext = font.render("Score:"+str(score), True, BLACK)
    screen.blit(scoretext, [10, 5])

    livestext = font.render("Lives:"+str(lives), True, BLACK)
    screen.blit(livestext, [10, 30])

    timetext = font.render(str(playtime), True, BLACK)
    screen.blit(timetext, [500, 5])

    # Flip, update, clock
    pygame.display.flip()
    pygame.display.update()
    #clock.tick(60)
pygame.quit()
quit()
'''
