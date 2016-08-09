import random
import pygame
import time
#import spritesheet ----> We'll use this once we get all our sprites done.

# Set up pygame
pygame.init()
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Weeping Willow 0.6')
done = False
font = pygame.font.Font('prstartk.ttf', 15)# This sets the font for screen text (lives, time left, etc)
textbFont = pygame.font.Font('prstartk.ttf', 8) # This sets the font for text in the textbox
clock = pygame.time.Clock()
FPS = 60
#playtime = 13846 #1 second equals about 923. This is 15 seconds long


# Game variables & images
score = 0
lives = 5
player_sprite1 = pygame.transform.scale(pygame.image.load('Girl_Stand.png'), (25, 75))
good_sprite1 = pygame.image.load('flower.png')
bad_sprite1 = pygame.image.load('goomba.png')
textbox = pygame.image.load('textbox.png')
spotlight = pygame.image.load('spotlight.gif')
turtleimg = pygame.image.load('turtle.png')
mountainback = pygame.image.load('mountain.png')
hillback = pygame.image.load('hill.png')
#intromus = pygame.mixer.music.load('intro.mp3')
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
    def setcoords(self, x, y):
        self.rect.x = x
        self.rect.y = y
    
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
        self.rect.center = (self.sizex / 2, self.sizey/ 2)
        
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
     
    def shoot(self):
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprite.add(bullet)
            bullets.add(bullet)
            #bullets is going to be a group and we going to add bullet to bullets
	
''' -*-*-*- Bullet Sprite Class -*-*-*- '''
class Bullet(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__inti__(self)
		self.image = pygame.Surface((18,20))
		self.image.fill(BLUE)
		self.rect = self.image.get_rect()
		self.rect.bottom = y
		self.rect.centerx = x
		self.speedy = -10
	
	def update(self):
		self.rect.y += self.speedy
		#kill of ot move off screen
		if self.rect.bottom <0:
			self.kill()

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

''' Creating all the sprites! '''
# The coins/good sprites for the character to collect
goodSprites = pygame.sprite.Group()
for k in range(3):
        goodSprites.add(NPCSprite(good_sprite1, SCREEN_WIDTH, random.randint(200, SCREEN_HEIGHT), -2, 0))

# Level 1 enemies
enemySprites1 = pygame.sprite.Group()
for k in range(3): 
        enemySprites1.add(NPCSprite(bad_sprite1, SCREEN_WIDTH, random.randint(200, SCREEN_HEIGHT), -3, 0))
#Image for bullets
bullet_img = pygame.image.load("fireball.png").convert()
#bullet_img = pygame.image.load(path.join(image_dir, "fireball")).convert()

# Creating player
player = playerSprite(player_sprite1, 330, 300)
playerList = pygame.sprite.Group(player)
bullets = pygame.sprite.Group()

# Create bosses. Ignore the fact that They are playerSprites.. I was too lazy to make a boss class because it was like midnight when I coded this
turtle = playerSprite(turtleimg, 600, 170)
turtleBoss = pygame.sprite.Group(turtle)

# Now, putting sprites and backgrounds together to make levels
levelEnemies1 = [enemySprites1, goodSprites] 
level_1 = level(1, levelEnemies1, levelBack1)

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
    time.sleep(1)

    
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
    textList = ["Hello..?   ", "Willow, can you hear me?", "If you can, I need you to... Wait. You  don't remember, do you?", "...       ", "Listen to me, Willow. You may not       remember me or what you're doing here,  but you are in great danger.", "There is an army of monsters controlled by an evil witch, and they're probably  looking for you right now.", "You need to get out of there, wherever  you are. It is not safe.", "I hope you still remember enough magic  to defend yourself..."]
    done = False
    player.setcoords(330, 300)
    pygame.mixer.music.load('intro.mp3')
    pygame.mixer.music.play(-1)
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
            playerList.draw(screen)
            text(textList[k], textCoords)
            pygame.event.wait() # Wait for user to do something

        done = True
    pygame.mixer.music.fadeout(1000)
    
def gameOver():
    screen.fill((0,0,0))
    overText = font.render("GAME OVER", True, WHITE)
    retryText = font.render("Press r to restart!", True, WHITE)
    done = False
    print(done)
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                print(done)
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
    pygame.quit()
    quit()
    
def level1():
    # Level 1 code
    screen.fill(BLACK)
    screen.blit(textbox, textboxCoords)
    text("Level 1, START!", textCoords)
    player.setcoords(0, SCREEN_HEIGHT-player.sizey)
    clock.tick(FPS)
    #level_1 = level(1, levelEnemies1, levelBack1)
    playtime = 27690
    BACKGROUND = (204, 255, 255)
    global lives
    global score
    screen.fill(BACKGROUND)
    level_1.drawBack()
    #screen.blit(textbox, textboxCoords)
    #text("*You think you still remember some magic.. Press SPACE to use it!* ", textCoords) #can't get the projectiles to work
    time.sleep(3)
    def level1():
    # Level 1 code
    screen.fill(BLACK)
    screen.blit(textbox, textboxCoords)
    text("Level 1, START!", textCoords)
    player.setcoords(0, SCREEN_HEIGHT-player.sizey)
    clock.tick(FPS)
    #level_1 = level(1, levelEnemies1, levelBack1)
    playtime = 27690
    BACKGROUND = (204, 255, 255)
    global lives
    global score
    screen.fill(BACKGROUND)
    level_1.drawBack()
    #screen.blit(textbox, textboxCoords)
    #text("*You think you still remember some magic.. Press SPACE to use it!* ", textCoords) #can't get the projectiles to work
    time.sleep(3)

def level3():
    # Level 3 code
    screen.fill(BLACK)
    screen.blit(textbox, textboxCoords)
    text("Level 3, START!", textCoords)
    player.setcoords(0, SCREEN_HEIGHT-player.sizey)
    clock.tick(FPS)
    #level_1 = level(1, levelEnemies1, levelBack1)
    playtime = 27690
    BACKGROUND = (204, 255, 255)
    global lives
    global score
    screen.fill(BACKGROUND)
    level_3.drawBack()
    #screen.blit(textbox, textboxCoords)
    #text("*You think you still remember some magic.. Press SPACE to use it!* ", textCoords) #can't get the projectiles to work
    time.sleep(3)


    #Now for the main while loop
    while playtime >= 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        if lives <= 0:
            return
        
        
        playtime -= (clock.tick(FPS))
        playtime = int(playtime)

        # Backgrounds, sprites, and player
        screen.fill(BACKGROUND)
        level_1.drawBack()
        level_1.updateSprites()
        playerList.draw(screen)
        player.move(pygame.key.get_pressed())
        #Handling sprite interaction
        # For every bad sprite the player runs into:
        for k in range(player.collide(enemySprites1)):
            enemySprites1.add(NPCSprite(bad_sprite1, SCREEN_WIDTH, random.randint(200, SCREEN_HEIGHT), -3, 0)) # Add another bad sprite
            lives -= 1 # Take away a life

        # Same as above, except for good sprites
        for k in range(player.collide(goodSprites)):
            goodSprites.add(NPCSprite(good_sprite1, SCREEN_WIDTH, random.randint(200, SCREEN_HEIGHT), -2, 0))
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
    # Level ended!
    screen.fill(BLACK)
    screen.blit(textbox, textboxCoords)
    text("Level ended!", textCoords)
    time.sleep(3)

def boss1():
    global lives
    if lives <= 0:
        return
    '''Script! '''
    #Turtle is facing player
    textList = ["...       ", "...       ", "...?!       ", "A.. A person?! A visitor?!"]
    #Turtle walks a little closer
    textList2 = ["I-I haven't seen another sane being     since the war of '76!", "Wait, wasn't I supposed to do something?", "...oh!", "Halt, intruder! You are trespassing on  royal territory!", "If you do not leave in 5 seconds, I will be forced to remove you myself!", "...and it won't be pleasant!"]
    #Wait 5 seconds
    textList3 = ["Nothing?", "Well. This is the most stubborn         trespasser I've seen yet!", "and, uh, the only one, BUT DON'T        UNDERESTIMATE ME!", "I can split the very land under our feet through sheer willpower! And I shall do so now!"]
    #Wait 3 seconds
    textList4 = ["HRRNG!!", "gRGRRRRR..!!"] #wait 3 secs between each. Have turtle shaking if possible
    #Stop shaking
    textList5 = ["...Well, I tried.", "I mean, I could still do it if I wanted to, you know!", "I used to be very strong in my prime,   you know!", "I was the strongest soldier in Her army, you know!", "...Well, um, do me a favor and forget   this ever happened.", "She wouldn't be happy if she found out I let a girl get away..", "Haha.. uh, you will forget this, right?"]
    #end
    ''' End of script '''
    
    player.setcoords(100, 350)
    screen.fill(BACKGROUND)
    screen.blit(mountainback, (0,-50))
    screen.blit(hillback, (0,50))
    playerList.draw(screen)
    turtleBoss.draw(screen)
    pygame.display.flip()
    pygame.display.update()
    
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
            
        #Keeping text on screen (hopefully)   
        anysec = textbFont.render("ANY... SECOND... NOW...", True, BLACK)
        screen.blit(anysec, textCoords)
        screen.blit(textbox, textboxCoords)
        #Redraw the player and background to prepare them for madness
        screen.fill(BACKGROUND)
        screen.blit(mountainback, (0,-50))
        screen.blit(hillback, (0,50))
        playerList.draw(screen)
        turtleBoss.draw(screen)
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

#Ok, now that all that nonsense is done, we can actually make the game do stuff.
while True:
    #startScreen()
    #cutscene1()
    level1()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                playerSprite.shoot()
    hits = pygame.sprite.collide(enemySprites1, bullets)
    for hit in hits:
        e = enemySprites()
        all_sprite.add(e)
        enemySprites.add(e)
    boss1()
    #cutscene2() Figure out what is happening in this scene
    gameOver()