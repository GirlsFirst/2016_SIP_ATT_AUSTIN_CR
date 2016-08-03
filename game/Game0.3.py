''' Game0.3
by Emma, Nathalie, Nisa
Updated 8/2/16

TODO:
Name game!
Make sprites
    - Powerups (if there's time)
    - Bosses (if there's time)
    - Spritesheet
    - Make jumping mechanic for player
Make better backgrounds (I (Emma) made these in 5 minutes in Paint. They're bad)
    - It's preferrable that we make them since we don't want to steal
Levels (just need to get backgrounds & enemy sprites)
Backgrounds
Timer
Story?

If you have any more ideas, please let everyone know!

'''
import random
import pygame
#import spritesheet ----> We'll use this once we get all our sprites done.

# Set up pygame
pygame.init()
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Game 0.3')
done = False
font = pygame.font.SysFont('Calibri', 25, True, False)# This sets the font for screen text
clock = pygame.time.Clock()
FPS = 60
playtime = 120 #How many seconds a level will last

# Game variables & images
currentLevel = 1
score = 0
lives = 3
player_sprite1 = pygame.image.load('mario.png')
good_sprite1 = pygame.image.load('flower.png')
bad_sprite1 = pygame.image.load('goomba.png')

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
        
    def move(self, inp):
        # Making the player move
        if inp[pygame.K_LEFT]:
            self.rect.x -=5
        if inp[pygame.K_RIGHT]:
            self.rect.x += 5
        if inp[pygame.K_UP]:
            self.rect.y -=5
        if inp[pygame.K_DOWN]:
            self.rect.y +=5

        # Making sure the player does not leave the windowed cage
        if self.rect.y > SCREEN_HEIGHT - self.sizey:
            self.rect.y = SCREEN_HEIGHT - self.sizey
        elif self.rect.y < 0:
            self.rect.y = 0
        if self.rect.x > SCREEN_WIDTH - self.sizex:
            self.rect.x = SCREEN_WIDTH - self.sizex
        elif self.rect.x < 0:
            self.rect.x = 0

''' -*-*-*- NPC Sprite Class -*-*-*- '''
# This is mostly for powerups
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
            Length is how long the level is. Emma is looking into adding a timer for the game to make this work better
        '''
        self.speed = speed
        self.sprites = sprites # We need sprites to be coded before this works
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


# Making those pretty pictures in the background
levelBack1 = [['mountain.png', -50], ['hill.png', 50]]

# Making those sprites be who they be
# We will simplify all this code later
testSprite = playerSprite(player_sprite1, 50, 50)
testSprite2 = NPCSprite(bad_sprite1, random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT), random.randint(-2, 2), random.randint(-2, 2))
testSprite3 = NPCSprite(bad_sprite1, random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT), random.randint(-2, 2), random.randint(-2, 2))
testSprite4 = NPCSprite(bad_sprite1, random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT), random.randint(-2, 2), random.randint(-2, 2))

testSprite5 = NPCSprite(good_sprite1, random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT), random.randint(-2, 2), random.randint(-2, 2))
testSprite6 = NPCSprite(good_sprite1, random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT), random.randint(-2, 2), random.randint(-2, 2))
testSprite7 = NPCSprite(good_sprite1, random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT), random.randint(-2, 2), random.randint(-2, 2))

playerSprite = pygame.sprite.Group(testSprite)
enemySprites = pygame.sprite.Group(testSprite2, testSprite3, testSprite4)
goodSprites = pygame.sprite.Group(testSprite5, testSprite6, testSprite7)

levelEnemies1 = [enemySprites, goodSprites]
level_1 = level(1, levelEnemies1, levelBack1)


while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    '''# Timer
    #print(clock.tick(FPS))
    playtime -= clock.tick(FPS)//1000
    #print(playtime)'''
    
    if playtime <= 0:
        currentLevel += 1
        playtime = 120
    '''
    '''
    # Creating levels
    screen.fill(BACKGROUND)
    
    if currentLevel == 1:
        level_1.drawBack()
        level_1.updateSprites()
        

        # For every bad sprite the player runs into:
        for k in range(testSprite.collide(enemySprites)):
            enemySprites.add(NPCSprite(bad_sprite1, random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT), random.randint(-2, 2), random.randint(-2, 2))) # Add another bad sprite
            lives -= 1 # Take away a life

        # Same as above, except for good sprites
        for k in range(testSprite.collide(goodSprites)):
            goodSprites.add(NPCSprite(good_sprite1, random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT), random.randint(-2, 2), random.randint(-2, 2)))
            score += 1
            
    '''^ ^Next up: more levels^ ^'''
    

    
    '''testing things here'''
    playerSprite.draw(screen)
    #enemySprites.draw(screen)
    #goodSprites.draw(screen)

    testSprite.move(pygame.key.get_pressed())
    #enemySprites.update()
    #goodSprites.update()
    ''' End of tests '''

    # Displaying score, lives, time
    scoretext = font.render("Score: "+str(score), True, BLACK)
    screen.blit(scoretext, [10, 5])

    livestext = font.render("Lives: "+str(lives), True, BLACK)
    screen.blit(livestext, [10, 30])

    timetext = font.render(str(playtime), True, BLACK)
    screen.blit(timetext, [500, 5])

    # Flip, update, clock
    pygame.display.flip()
    pygame.display.update()
    clock.tick(60)
pygame.quit()
quit()
