#Imports all of the modules that I need
import pygame, time, sys, random
from pygame.locals import *
from timeit import default_timer

#Initialises pygame so it can be used.
pygame.init()

#Sets up a clock so the loops can be limited
Clock = pygame.time.Clock()

#Declares all of the colours
WHITE = [255,255,255]
BLACK = [0,0,0]

#NOTES===================
#Cuts the sprites All at the start of the program and stores them
#Animator always loops animation
#Music Routine needs to be worked on

class Screen:
    #Defines the width and height of the window.
    Width = 800
    Height = 600
    
    def Setup(self):
        #Sets up the window so items can be drawn to it
        #The window
        self.Window = pygame.display.set_mode((self.Width, self.Height),0, 32)
        #The caption
        pygame.display.set_caption("NEW GAME")
        #Makes the mouse invisible
        pygame.mouse.set_visible(False)

    def Refresh(self):
        #Updates the display at 60 times per second.
        pygame.display.update()
        Clock.tick(60)
    
def Write_Text(Text, Font,Colour, X, Y, Distance_Apart, Area):
    #Adds another item to the start so if only one string is entered it is still checked as one string.
    Text.insert(0, "")
    
    #Lower cases the area variable to ensure its easier to program.
    Area = Area.lower()
    
    #for the lines in the given text
    for line in Text[1:]:
        #Defines the text ready for it to be drawn
        Render = Font.render(line, True, Colour)

        #Makes a positining rectangle
        Position = Render.get_rect()
        
        #Positions the texts y coordinate
        Position.centery = (Text.index(line) * Distance_Apart) + Y

        #Positions the texts x coordinate in the text box
        if Area == "center":
            Position.centerx = X
        else:
            Position.x = X

        #Draws the text to the screen
        Screen.Window.blit(Render, Position)
        
class Background:
    #Sets up the variables for the background
    ImgFileName = "Map1.png"
    X = 0
    Y = 0
    
    def Setup(self):
        #Loads the background image
        self.Image = pygame.image.load(self.ImgFileName).convert_alpha()
        
class Map:
    #Sets up the variables used to position every item in the map
    X = 0
    Y = 0
    MoveX = 0
    MoveY = 0
    Xedge = False
    Yedge = False

    def Draw(ToBeDrawn):
        #Draws everything to the screen in the position relative to the map coordinate
        for items in ToBeDrawn:
            Screen.Window.blit(items.Image, (items.X + Map.X ,items.Y + Map.Y))

class Player:
    def Setup(self):
        #Sets up all of the player variables and images
        self.X = 400
        self.Y = 300
        self.MoveX = 0
        self.MoveY = 0
        self.Status = "IDLE" 

        self.Sprites.Load()

        self.Draw = Player.Sprites.Idle[0]
        self.Hitbox = self.Draw[Player.Sprites.AnimationStage].get_rect()

    def Controls(self):
        #Allows the player to input commands
        for event in pygame.event.get():
            
            if event.type == KEYDOWN:
                #If down arrow pushed then player moves in the down direction.
                if event.key == K_DOWN:
                    self.MoveY = 2
                    if self.Status == "IDLE":
                        self.Status_Change("R_WALK")
                        
                #If up arrow pushed then player moves in the up direction.
                elif event.key == K_UP:
                    self.MoveY = -2
                    if self.Status == "IDLE":
                        self.Status_Change("R_WALK")
                        
                #If left arrow pushed then player moves in the left direction.
                elif event.key == K_LEFT:
                    self.MoveX = -2
                    self.Status_Change("L_WALK")

                #If right arrow pushed then player moves in the right direction.
                elif event.key == K_RIGHT:
                    self.MoveX = 2
                    self.Status_Change("R_WALK")
                    
            if event.type == KEYUP:
                #If the down or up arrow is let go then the player stops moving on y axis
                if event.key == K_DOWN or event.key == K_UP:
                    self.MoveY = 0

                #If the left or right arrow is let go then the player stops moving on x axis
                elif event.key == K_LEFT or event.key == K_RIGHT:
                    self.MoveX = 0
                    
            if event.type == QUIT:
                #If the X in the top corner is pressed the game is closed.
                pygame.quit()
                sys.exit()
                
        #Changes the player's x or y coordinates according to the Move variables.            
        self.X += self.MoveX
        self.Y += self.MoveY

        #If there is no movement then the player status is idle.
        if self.MoveX == 0 and self.MoveY == 0:
            self.Status_Change("IDLE")

    def Collision(self):
        #Gathers the area for the players hitbox. and positions it around the player.
        self.Hitbox = self.Draw[Player.AnimationStage].get_rect()
        self.Hitbox.x = self.X
        self.Hitbox.y = self.Y

        #Window Collision so the player doesnt leave the screen.
        #Left
        if self.X < 0:
            self. X = 0
            
        #Top
        if self.Y < 0:
            self.Y = 0
            
        #Right
        if self.X > Screen.Width - self.Hitbox.width:
            self. X = Screen.Width - self.Hitbox.width
            
        #Bottom
        if self.Y > Screen.Height - self.Hitbox.height:
            self.Y = Screen.Height - self.Hitbox.height
            
        #pygame.draw.rect(Screen.Window, WHITE, self.Hitbox, 1)
            
    def Status_Change(self,StatusType):
        #Sets the animationstage to zero and changes the players status ready for animation.
        Player.AnimationStage = 0
        self.Status = StatusType

    def Check_Status(self):
        #Checks the player status and determines which list of sprites to use.
        #After it has been determined the animator animates the sprites.
        if self.Status == "L_WALK":
            self.Draw = Player.Sprites.Walking[0]
            
        elif self.Status == "R_WALK":
            self.Draw = Player.Sprites.Walking[1]
            
        elif self.Status == "IDLE":
            self.Draw = Player.Sprites.Idle[0]

        else:
            self.Draw = Player.Sprites.Idle[0]
            
        Animator.Animate(Player, self.Draw)
            
    class Sprites:
        #Sets the variables used for the player sprites
        AnimationStage = 0
        Walking = []
        Idle = []
        
        def Load():
            #Loads the spritesheet and cuts the sheet and stores the spritelists.
            SpriteSheet = pygame.image.load("pr2.png").convert_alpha()
            
            Player.Sprites.Walking.append(Cut_SpriteList(SpriteSheet, 0, 34,39,34, 10))
            Player.Sprites.Walking.append(Cut_SpriteList(SpriteSheet, 0, 0,39,34, 10))
            
            Player.Sprites.Idle.append(Cut_SpriteList(SpriteSheet, 0, 0,39,34, 1))
        

class Animator:
    class Timer:
        #Used to time the duration of the animations in the game.
        #Stores the starting time of each timer.
        Start_Times=[]
        #Stores how long the timer has been running for.
        Time = []
        #Stores the type of timer being run.
        Type =[]
        
        def Start(Time, item):
            #Starts the timer between each sprite in an animation.
            Animator.Timer.Start_Times.append(default_timer())
            Animator.Timer.Time.append(Time)
            Animator.Timer.Type.append(item)
            
        def Check(item):
            #Checks whether the duration of any of the timers running have ended and the timer is removed from each list ready for the next timer.
            A = Animator.Timer.Type.index(item)
            duration = default_timer() - Animator.Timer.Start_Times[A]
            if Animator.Timer.Time[A] < duration:
                del Animator.Timer.Start_Times[A]
                del Animator.Timer.Time[A]
                del Animator.Timer.Type[A]
                return True
            else:
                return False
        
    def Animate(item, Spritelist):
        #If the timer hasnt been started then one is started
        if (item in Animator.Timer.Type) == False:
            Animator.Timer.Start(0.05,item)
        #Else if the timer has started then the timer is checked , If it has ended the next sprite is used.    
        elif (item in Animator.Timer.Type) == True:
            if Animator.Timer.Check(item) == True:
                item.AnimationStage += 1
                if item.AnimationStage >= len(Spritelist):
                    item.AnimationStage = 0
            
        

def Cut_SpriteList(Sheet, SpriteX, SpriteY, SpriteWidth, SpriteHeight, HowManySprites):
    #Resets how many sprites have been cut to 0
    HowMany = 0
              
    #Gets the area of the sheet
    SpriteSheetArea = Sheet.get_rect()

    #Holds the list of sprites that have been cut.
    ListOfSprites = []
    
    #For each row on the sheet.
    for SpriteRows in range(SpriteSheetArea.height // SpriteHeight):

        #For each column on the sheet.
        for SpriteColumns in range(SpriteSheetArea.width // SpriteWidth):
            if HowMany == HowManySprites:
                return ListOfSprites
            #Increments the counter for sprites which have been cut.
            HowMany += 1
            
            #Locates the sprite wanted
            Sheet.set_clip(pygame.Rect((SpriteX , SpriteY), (SpriteWidth , SpriteHeight)))

            #Gathers the sprite which is wanted
            Sprite = Sheet.subsurface(Sheet.get_clip())

            #Adds the sprite to a list of sprites                
            ListOfSprites.append(Sprite)
            
            #Increments to next column on sheet
            SpriteX += SpriteWidth

        #Resets the X position to 0 for the next row.
        SpriteX = 0
        
        #Increments to next row
        SpriteY += SpriteHeight
        
class Music:
    Track_1 = "BombermanMusic.wav"
    
    def Setup(self):
        pygame.mixer.init()
        
    def play(self,sound):
        Music = pygame.mixer.Sound(sound)
        channel = pygame.mixer.find_channel(True)
        channel.set_volume(0.5)
        channel.play(Music)

class Game:
    def InGame():
        while True:
            Screen.Window.fill(BLACK)
            Player.Controls()
    
            BG_Area = Background.Image.get_rect()
    
            if (Map.X >= 0 and Player.X < (Screen.Width / 2) - (Player.Hitbox.width/2)) or \
               (Map.X <= -(BG_Area.width-Screen.Width) and Player.X > (Screen.Width / 2) - (Player.Hitbox.width/2)):
        
                Map.MoveX = 0
                Map.Xedge = True
            else:
                Map.Xedge = False

        
            if (Map.Y >= 0 and Player.Y < (Screen.Height / 2) - (Player.Hitbox.height/2) ) or \
               (Map.Y <= -(BG_Area.height - Screen.Height) and Player.Y > (Screen.Height / 2) - (Player.Hitbox.height/2)):
        
                Map.MoveY = 0
                Map.Yedge = True
            else:
                Map.Yedge = False
            
            if Map.Xedge == False:
                Player.X = (Screen.Width / 2) - (Player.Hitbox.width/2)
                Map.MoveX = -Player.MoveX
                Map.X += Map.MoveX
            
            if Map.Yedge == False:
                Player.Y = (Screen.Height / 2) - (Player.Hitbox.height/2)
                Map.MoveY = -Player.MoveY
                Map.Y += Map.MoveY

            Map.Draw([Background])
            Player.Collision()
            Player.Check_Status()
            Screen.Window.blit(Player.Draw[Player.AnimationStage], (Player.X,Player.Y))
            Screen.Refresh()
        
Screen = Screen()
Background = Background()
Player = Player()
Music = Music()

Screen.Setup()
Background.Setup()
Player.Setup()
Music.Setup()

Music.play(Music.Track_1)

while True:
    Game.InGame()
