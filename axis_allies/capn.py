#!/usr/bin/env python
"""
This simple example is used for the line-by-line tutorial
that comes with pygame. It is based on a 'popular' web banner.
Note there are comments here, but for the full explanation,
follow along in the tutorial.
"""


#Import Modules
import os, pygame
from pygame.locals import *
from pygame.compat import geterror
import random 
if not pygame.font: print ('Warning, fonts disabled')
if not pygame.mixer: print ('Warning, sound disabled')

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'creatures')
mus_dir = os.path.join(main_dir, 'tunes')

#functions to create our resources
def load_image(name, colorkey=None):
    fullname = os.path.join(data_dir, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error:
        print ('Cannot load image:', fullname)
        raise SystemExit(str(geterror()))
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()
    fullname = os.path.join(mus_dir, name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error:
        print ('Cannot load sound: %s' % fullname)
        raise SystemExit(str(geterror()))
    return sound


#classes for our game objects

class Item(pygame.sprite.Sprite):
    """drops ingredients and bad items"""
    def __init__(self):        
        global image
        global stuff
        global sounds
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        image = ['tomato.bmp','lettuce.bmp','salami.bmp','oil.bmp','bacon.bmp','cheese.bmp','turkey.bmp']
        sounds = ['A_Chord.wav','B_Chord.wav','C_Chord.wav','D_Chord.wav','E_Chord.wav','F_Chord.wav','G_Chord.wav']
        x = random.randint(0,len(image)-1)
        stuff.append(image[x][:-4])
        self.image, self.rect = load_image(image[x],-1)
        self.rect.midbottom = (random.randint(20,480),0)
        
    def update(self, speed):
        "move the item one pixel lower"
        self.rect = self.rect.move(0,speed)
        if self.rect[1] > 480:
            
            try:
                item_sprites.remove(self)
                stuff.pop(0)
            except:
                pass
        collision = pygame.sprite.spritecollide(capn, item_sprites, False)
        #Check for collision and adjust score 
        if collision:
            try:
                item_sprites.remove(collision[0]) 
            except:
                pass
            self.update_scoring()
            stuff.pop(0)
            y = random.randint(0,len(sounds)-1)
            sound = load_sound(sounds[y])
            sound.play()
    def update_scoring(self):
            global score
            global sandwich
            menu = {'italian':['tomato','salami','oil','cheese'],'club':['tomato','lettuce','bacon','cheese','turkey'],'blt':['tomato','lettuce','bacon']}
            #add ingredient to sandwich
            sandwich.append(stuff[0])
            self.writer(stuff[0],(250,250,250),(264,183))
            cnt = 0
            if len(sandwich) == 3:
                for i in sandwich:
                    if i in menu['blt']:
                        cnt += 1
                if cnt == 3:
                    score += 10
                    self.writer('BLT!',(250,250,250),(264,183))
                    sandwich = []
                cnt = 0    
            if len(sandwich) == 4:
                for i in sandwich:
                    if i in menu['italian']:
                        cnt += 1
                if cnt == 4:
                    score += 30
                    self.writer('Italian!',(250,250,250),(264,183))
                    sandwich = []
                cnt = 0    
            if len(sandwich) == 5:
                for i in sandwich:
                    if i in menu['club']:
                        cnt += 1
                if cnt == 5:
                    score += 100
                    self.writer('Club!',(250,250,250),(264,183))
                else:
                    score += -20
                    self.writer('Try again!',(250,250,250),(264,183))
                    sandwich=[]
            self.writer(str(score),(250,250,250),(264,203),True)                    
    def writer(self, word, color, pos,flag = None):
        font = pygame.font.Font(None, 18)
        text = font.render(word, 0, color)
        textpos = text.get_rect(center=(pos))
        if flag is None:
            background.fill(pygame.Color("black"),(220,158,160,80))
        background.blit(text, textpos)
        
                           

class Capn(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.image, self.rect = load_image('capn_new.bmp', -1)
        screen = pygame.display.get_surface()
        self.rect.midbottom = (250, 500)
        global start    
    
    def move(self,dir):
        if dir == 1:
            if self.rect[0] < 412:
                self.rect = self.rect.move(5,0)
        if dir == -1:
            if self.rect[0] > 5:
                self.rect = self.rect.move(-5,0)
  
def main():
    """this function is called when the program starts.
       it initializes everything it needs, then runs in
       a loop until the function returns."""
#Set global variables
    global item_sprites
    global score
    global capn
    global sandwich
    global background
    global stuff
    start = False
    score = 0
    sandwich = []
    stuff = []
#Initialize Everything
    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    pygame.display.set_caption('Captain Sandwich Hands')
    speed = 1
    

#Create The Backgound
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    

#Prepare Game Objects
    clock = pygame.time.Clock()
    #whiff_sound = load_sound('whiff.wav')
    #punch_sound = load_sound('punch.wav')
    #chimp = Chimp()
    item = Item()
    capn= Capn()
    item_sprites = pygame.sprite.Group()
    item_sprites.add(item)
    demon = 100
#Main Loop
    going = True
    cnt = 0
    speed = 1
    sprites = item_sprites.sprites()
    time = 0
    while True:
        if start == True:
            pygame.mouse.set_visible(0)
            restaurant = pygame.image.load('background.bmp')
            background.blit(restaurant, (0,0))
            #Display The Background
            screen.blit(background, (0, 0))
            pygame.display.flip()
            while going:    
                clock.tick(60)
                if time % 1000 == 0:
                    speed += .3                   
                if cnt == demon:
                    item2 = Item()
                    item_sprites.add(item2)
                    cnt = 0
                    item_sprites.update(speed)
                    #Draw Everything
                    screen.blit(background, (0, 0))
                    screen.blit(capn.image,capn.rect)
                    item_sprites.draw(screen) 
                    pygame.display.flip()
                    demon = demon*.99
                    if demon < 1:
                        demon = 1
                    demon = int(demon)
                #Handle Input Events        
                keys_pressed = pygame.key.get_pressed()
                if keys_pressed[K_LEFT]:    
                    capn.move(-1)
                if keys_pressed[K_RIGHT]:
                    capn.move(1)
                for event in pygame.event.get():            
                    if event.type == QUIT:
                        going = False
                    elif event.type == KEYDOWN and event.key == K_RIGHT:
                        capn.move(.1)
                    elif event.type == KEYDOWN and event.key == K_LEFT:
                           capn.move(-.1)
                   
                else:  
                    cnt += 1
                    item_sprites.update(speed)
                    #draw everything
                    screen.blit(background, (0, 0))
                    item_sprites.draw(screen)
                    screen.blit(capn.image,capn.rect)
                    pygame.display.flip()
                time +=1
        else:
            pygame.mouse.set_visible(1)
            start_screen = pygame.image.load('start_screen.bmp')
            background.blit(start_screen, (0,0))
            #Display The Background
            screen.blit(background, (0, 0))
            pygame.display.flip()
            while going:
                clock.tick()
                for event in pygame.event.get():            
                    if event.type == QUIT:
                        going = False
                    elif event.type == MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        if pos[0] > 139 and pos[0] < 202 and pos[1] > 228 and pos[1] < 280:    
                            start = True
                            break
                break
                            
    pygame.quit()

#Game Over


#this calls the 'main' function when this script is executed
if __name__ == '__main__':
    main()
