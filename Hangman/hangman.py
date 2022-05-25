import pygame
import time
import random
import sys
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

pygame.init()

display_width=600
display_height=600

icon_image=pygame.image.load(resource_path("data/images/icon.png"))
icon_image=pygame.transform.scale(icon_image,(32,32))

gameDisplay=pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Hangman')
pygame.display.set_icon(icon_image)


#Colors

white=(255,255,255)
black=(0,0,0)

red=(255, 0, 0)
green=(0, 255, 0)

text_color=(0, 128, 128)

gold=(212, 175, 55)
alpha_dark=(118,150,86)
alpha_light=(238,238,210)

gray=(169, 169, 169)

game_end_color=(0,139,139)


font1=resource_path("data/freesansbold.ttf")
font2=resource_path("data/arial.ttf")

hangman_images=[]
for a in range(7):
    hangman_images.append(pygame.image.load(resource_path("data/images/hangman_"+str(a)+".png")))
    hangman_images[a]=pygame.transform.scale(hangman_images[a], (600, 400))

game_lose_image=pygame.image.load(resource_path("data/images/game_lose.png"))
game_win_image=pygame.image.load(resource_path("data/images/game_win.png"))

game_lose_image=pygame.transform.scale(game_lose_image, (900,900))
game_win_image=pygame.transform.scale(game_win_image, (600,600))


f=open(resource_path("data/words.txt"),"r")
list_of_words=f.readlines()
f.close()



class text_on_top():

    def __init__(self, text):
        self.text=text

        self.used_letters=["A","E","I","O","U"]

        self.required_letters=list()
        for a in self.text:
            if a not in self.required_letters and a not in self.used_letters and a!=" ":
                self.required_letters.append(a)

    def feed(self, letter):
        if letter in self.required_letters:
            self.used_letters.append(letter)
            self.required_letters.pop(self.required_letters.index(letter))
            return (True)
        else:
            return (False)

    def display(self):
        self.display_text=""

        for a in self.text:
            if a in self.used_letters:
                self.display_text+=a
            elif a==" ":
                self.display_text+="/"
            else:
                self.display_text+="_"

        message_display(self.display_text, font2, 50, display_width/2, 25)


class alphabet():

    def __init__(self,letter):
        self.letter=letter

        if self.letter in ("A","E","I","O","U"):
            self.available=False
        else:
            self.available=True

    def display(self, position):
        x,y=position

        pygame.draw.rect(gameDisplay, gold, (x, y, 76, 76))

        if self.available==True:
            mouse=pygame.mouse.get_pos()
            click=pygame.mouse.get_pressed()

            if x+6<mouse[0]<x+70 and y+6<mouse[1]<y+70:
                pygame.draw.rect(gameDisplay, alpha_light, (x+6, y+6, 76-12, 76-12))

                if click[0]==1:
                    self.available=False
                    return(self.letter)
                
            else:
                pygame.draw.rect(gameDisplay, alpha_dark, (x+6, y+6, 76-12, 76-12))

        else:
            pygame.draw.rect(gameDisplay, gray, (x+6, y+6, 76-12, 76-12))

        message_display(self.letter, font1, 45, x+38, y+38)



def text_objects(text,font,color):
    textSurface=font.render(text, True, color)
    return (textSurface, textSurface.get_rect())

def message_display(text,font,size,x,y,color=text_color):
    largeText=pygame.font.Font(font,size)
    TextSurf,TextRect=text_objects(text, largeText, color)
    TextRect.center=(x,y)
    gameDisplay.blit(TextSurf,TextRect)



def game_lose(text):
    game_lose_run=True
    while game_lose_run:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                game_lose_run=False

        gameDisplay.blit(game_lose_image, (0,0))
        message_display(text, font2, 50, display_width/2, 25)        
        message_display("You Lose", font2, 140, display_width/2, display_height/2, red)
        pygame.display.update()

def game_win(text):
    game_win_run=True
    while game_win_run:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                game_win_run=False

        gameDisplay.blit(game_win_image, (0,0))
        message_display(text, font2, 50, display_width/2, 25)  
        message_display("You Win!", font2, 140, display_width/2, 175, green)
        pygame.display.update()



def mainloop():


    text=random.choice(list_of_words)
    text=text.upper().rstrip()

    top_text=text_on_top(text)

    incorrect_answers=0
    
    mainloop_run=True

    alphabet_list=[]
    for a in range(26):
        alphabet_list.append(alphabet(chr(65+a)))

    game_end_extra_loop=10 #arbritary

    while mainloop_run:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                mainloop_run=False

        if incorrect_answers==6:
            if game_end_extra_loop==0:
                game_lose(text)
                mainloop_run=False
            else:
                game_end_extra_loop=1

        if top_text.required_letters==list():
            if game_end_extra_loop==0:
                game_win(text)
                mainloop_run=False
            else:
                game_end_extra_loop=1



        #Display

        gameDisplay.fill(white)

        gameDisplay.blit(hangman_images[incorrect_answers], (135,-10))

        top_text.display()

        alphabet_click=[]
        for b in range(0,7):
            alphabet_click.append(alphabet_list[b].display((34+(76*b),295)))
        for b in range(7,13):
            alphabet_click.append(alphabet_list[b].display((72+76*(b-7),295+72)))
        for b in range(13,20):
            alphabet_click.append(alphabet_list[b].display((34+76*(b-13),295+72*2)))
        for b in range(20,26):
            alphabet_click.append(alphabet_list[b].display((72+76*(b-20),295+72*3)))

        for c in alphabet_click:
            if c!=None:
                check=top_text.feed(c)

                if not check:
                    incorrect_answers+=1

        

                          
        pygame.display.update()

        if game_end_extra_loop==1:
            game_end_extra_loop=0
            time.sleep(2)

    pygame.quit()


mainloop()
