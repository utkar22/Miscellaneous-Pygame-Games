import pygame
import time
import random

pygame.init()

display_width=800
display_height=600

gameDisplay=pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('A Bit Racey')

black=(0,0,0)
white=(255,255,255)
red=(255,0,0)
green=(0,255,0)
blue=(0,0,255)

red2=(200,0,0)
green2=(0,200,0)

car_width=73

clock=pygame.time.Clock()

pause=True

carImg=pygame.image.load('racecar.png')

pygame.display.set_icon(carImg)

intro_music=pygame.mixer.Sound("Astronomia.wav")
game_music=pygame.mixer.Sound("Mortals.wav")
crash_sound=pygame.mixer.Sound("Bruh.wav")

def things_dodged(count):
    font=pygame.font.SysFont(None, 25)
    text=font.render("Dodged: "+str(count), True, black)
    gameDisplay.blit(text,(0,0))

def things(thingx, thingy, thingw, thingh, color):
    pygame.draw.rect(gameDisplay, color, [thingx, thingy, thingw, thingh])

def car(x,y):
    gameDisplay.blit(carImg,(x,y))

def text_objects(text,font):
    textSurface=font.render(text, True,  black)
    return (textSurface, textSurface.get_rect())

def message_display(text,font,size,x,y):
    largeText=pygame.font.Font(font,size)
    TextSurf,TextRect=text_objects(text, largeText)
    TextRect.center=(x,y)
    gameDisplay.blit(TextSurf,TextRect)
    pygame.display.update()

def button(msg,x,y,w,h,ic,ac,action=None):
    mouse=pygame.mouse.get_pos()
    click=pygame.mouse.get_pressed()

    if x+w>mouse[0]>x and y+h>mouse[1]>y:
        pygame.draw.rect(gameDisplay,ac,(x,y,w,h))

        if click[0]==1 and action!=None:
            action()
    else:
        pygame.draw.rect(gameDisplay,ic,(x,y,w,h))

    smallText=pygame.font.Font('freesansbold.ttf',20)
    textSurf,textRect=text_objects(msg,smallText)
    textRect.center=(x+w/2,y+h/2)
    gameDisplay.blit(textSurf, textRect)


def quitgame():
    pygame.quit()

def unpause():
    global pause
    pause=False

def paused():
    pygame.mixer.music.pause()
    
    pause=True

    gameDisplay.fill(white)
    
    largeText=pygame.font.SysFont('comicsansms',115)
    TextSurf,TextRect=text_objects("Paused",largeText)
    TextRect.center=(display_width/2,display_height/2)
    gameDisplay.blit(TextSurf,TextRect)

    while pause:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_p:
                    return ()

        button("Press P to Continue",150,450,300,50,green,green2,)
        button("Quit",550,450,100,50,red,red2,quitgame)

        pygame.display.update()
        clock.tick(15)

def crashed(score):
    message_display('You Crashed','freesansbold.ttf',115,display_width/2,display_height/2)
    pygame.mixer.music.load("bruh.wav")
    pygame.mixer.music.play(0)
    time.sleep(1)

    score_str="Score: "+str(score)
    message_display(score_str,'freesansbold.ttf',75,display_width/2,(display_height/4)-30)

    f=open("highscore.txt","r+")
    highscore=int(f.read())
    if score>highscore:
        highscore=score
        f.seek(0)
        f.write(str(score))
    f.close()

    highscore_str="Highscore: "+str(highscore)
    message_display(highscore_str,'freesansbold.ttf',45,display_width/2,(display_height/4)+30)

    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()

        button("Play Again",150,450,120,50,green,green2,gameloop)
        button("Quit",550,450,120,50,red,red2,quitgame)

        pygame.display.update()
        clock.tick(15)
        

def gameintro():
    pygame.mixer.music.load("Astronomia.wav")
    pygame.mixer.music.play(-1)
    
    intro=True

    while intro:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()

        gameDisplay.fill(white)
        largeText=pygame.font.Font('freesansbold.ttf',115)
        TextSurf,TextRect=text_objects("A bit Racey", largeText)
        TextRect.center=(display_width/2,display_height/2)
        gameDisplay.blit(TextSurf,TextRect)

        mouse=pygame.mouse.get_pos()

        button("GO!",150,450,100,50,green,green2,gameloop)
        button("No.",550,450,100,50,red,red2,quitgame)

        pygame.display.update()
        clock.tick(15)

def gameloop():
    pygame.mixer.music.load("Mortals.wav")
    pygame.mixer.music.play(-1)
    
    x=display_width*0.45
    y=display_height*0.8
    x_change=0
    car_speed=5

    thing_startx=random.randrange(0, display_width)
    thing_starty=-600
    thing_speed=7
    thing_width=100
    thing_height=100

    thingCount=1
    dodged=0
    

    gameExit=False

    while not gameExit:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                gameExit=True

            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_LEFT or event.key==pygame.K_a:
                    x_change=-car_speed
                elif event.key==pygame.K_RIGHT or event.key==pygame.K_d:
                    x_change=car_speed
                elif event.key==pygame.K_p:
                    paused()
                    pygame.mixer.music.unpause()
                    
            if event.type==pygame.KEYUP:
                if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT or event.key==pygame.K_a or event.key==pygame.K_d:
                    x_change=0

        x+=x_change

        gameDisplay.fill(white)
        
        things(thing_startx, thing_starty, thing_width, thing_height, black)
        thing_starty+=thing_speed
        car(x,y)
        things_dodged(dodged)

        if x>display_width-car_width or x<0:
            crashed(dodged)

        if thing_starty>display_height:
            thing_starty=0-thing_height
            thing_startx=random.randrange(0,display_width)
            dodged+=1
            thing_speed+=0.5
            thing_width+=1.05
            car_speed+=0.15
            

        if y<thing_starty+thing_height:
            if x>thing_startx and x<thing_startx+thing_width or x+car_width>thing_startx and x+car_width<thing_startx+thing_width:
                crashed(dodged)
    
        pygame.display.update()
        clock.tick(60)


gameintro()
pygame.quit()

