import random
import json
import os

import game_framework
import random
import title_state
import Background
from pico2d import*
from Background import*
from Enemy import*
import time


name='MainState'
image=None
jump_sound=None
jump_time=0.0
jump_check=1.0
speed=5.0
jump_p=0
start_time = 0
check_time=0
check_des=0
enemyspeed =10.0
enemyspeed2 =8.0
arrowcheck=2
checkrank=1
class Main_Char:
    def __init__(self):
        self.x,self.y=90,40
        self.run_frame=0
        self.jump_frame=0
        self.run_image=load_image('new_char_sheet.png')
        self.jump_image=load_image('jump_sheet.png')
        self.jump_sound=load_wav('pickup.wav')
        self.shoot_sound=load_wav('shoot.wav')
        self.jump_sound.set_volume(32)
        self.shoot_sound.set_volume(35)

    def update(self):
        global jump_p,jump,jump_time,jump_check,background ,running,check_time
        self.run_frame=(self.run_frame+1)%6
        self.jump_frame=(self.jump_frame+1)%6
        
        if(jump==False):
            jump_check=2
            if boy.y<135:
                for i in range(1,13):
                    boy.y+=i*0.3
            if boy.y>=135:
                jump=True
        if(jump==True  and  boy.y>40):
            for i in range(1,13):
                boy.y-=i*0.5
        if(jump==True and boy.y<=40):
            jump_check=1
            
    def draw(self):
        global jump
        if(jump==True):
            self.run_image.clip_draw(self.run_frame*100,0,100,55,self.x,self.y)
        elif(jump==False):
            self.jump_image.clip_draw(self.jump_frame*100,0,100,55,self.x,self.y)

    def get_bb(self):
        return self.x-8,self.y-3,self.x+8,self.y+13
    
    def draw_bb(self):
        draw_rectangle(*self.get_bb())
      
class Arrow:
     def __init__(self):
        self.x,self.y=-300,40
        self.run_frame=0
        self.run_image=load_image('Arrow.png')
        self.checktime=0
        self.speed=5
        
     def update(self):
         global arrowcheck
         arrow.x+=self.speed
         if self.speed < 10:
             for i in range(1,10):
                 self.speed+=i*0.3
         if(self.x>800):
             self.x=-300
             arrowcheck=2            
     def draw(self):
         self.run_image.draw(self.x,self.y)
     def get_bb(self):
          return self.x-14,self.y-5,self.x+14,self.y+2
     def draw_bb(self):
          draw_rectangle(*self.get_bb())
          
def enter():
    global game_over,main_sound,enemyspeed,enemyspeed2,checkrank,arrow,green,moun,font,image,background,running,boy,jump,flying,sun,moon
    font=load_font('ENCR10B.TTF',30)
    boy=Main_Char()
    checkrank=1
    main_sound=load_music('main.mp3')
    game_over=load_wav('gameover.wav')
    main_sound.set_volume(35)
    game_over.set_volume(35)
    enemyspeed =6.0
    enemyspeed2 =3.0
    moun=Mountain(800,400)
    moon=Moon()
    background = Background(800,400)
    flying=enemy()
    arrow=Arrow()
    green=G_enemy()
    sun=Sun()
    jump=True
    running=True
    image=None
    main_sound.repeat_play()


    
def exit():
    global game_over,main_sound,arrow,green,background,boy,flying,moun,sun,moon,font,image
    del(boy)
    del(background)
    del(moun)
    del(flying)
    del(sun)
    del(moon)
    del(green)
    del(arrow)
    del(main_sound)
    del(game_over)


    
def handle_events():
    global arrowcheck,arrow,running,jump,jump_time,jump_check
    events=get_events()
    for event in events:
        if event.type==SDL_QUIT:
            game_framework.quit()  
        elif(event.type,event.key)==(SDL_KEYDOWN,SDLK_SPACE) and jump_check==1:
             jump=False
             boy.jump_sound.play()
        elif(event.type,event.key)==(SDL_KEYDOWN,SDLK_a) and jump_check==1:
            if arrowcheck<3:
                arrow.x=90
                boy.shoot_sound.play()
            arrowcheck+=1
        else:  
            if(event.type,event.key)==(SDL_KEYDOWN,SDLK_ESCAPE):
                running=False
                if(event.type,event.key)==(SDL_KEYDOWN,SDLK_ESCAPE):
                    running=False
                    #game_framework.quit()
                    game_framework.change_state(title_state)

def loadscore():
    f = open('Ranking_file', 'r')
    score_data = json.load(f)
    f.close()
    score_data.append({"Score": round(check_time,2)})
    f = open('Ranking_file', 'w')
    json.dump(score_data, f)
    f.close()
    
def collide(a,b):
    left_a,bottom_a,right_a,top_a=a.get_bb()
    left_b,bottom_b, right_b,top_b=b.get_bb()
    
    if left_a>right_b: return False
    if right_a<left_b: return False
    if top_a<bottom_b: return False
    if bottom_a>top_b: return False

    return True
    

def bubble_sort(data):
    for i in range(0, len(data)):
         for j in range(0,len(data)):
            if(data[i]['Score']>data[j]['Score']):
                data[i], data[j] = data[j], data[i]
                
def draw_ranking():
    f = open('Ranking_file', 'r')
    score_data = json.load(f)
    f.close()

    bubble_sort(score_data)
    score_data = score_data[:5]
    L=0
    i = 0
    for score in score_data:
        font.draw(40,350-L,'%d. Score:%.1f'% (i+1,score['Score']),(255,94,0))
        i+=1
        L+=50
        
def update():
    global game_over,main_sound,flying,enemyspeed,enemyspeed2,checkrank,arrowcheck,arrow,check_des,green,running,moun,jump,jump_time,jump_check,background,flying,sun,moon,boy,enemy
    boy.update()
    enemyspeed +=int(check_time)/5000
    enemyspeed2 +=int(check_time)/5000
    sun.update()
    moon.update()
    moun.update()
    background.update()
    if arrowcheck>2:
        arrow.update()
    green.update(enemyspeed2)
    flying.update(enemyspeed)
    font.draw(680,330,"%0.1f"%check_time)
    font.draw(550,330,"Score:")
    if running == False:
        main_sound.stop()

    if collide(flying,arrow):
        flying.x+=50
        arrow.x=-300
        arrowcheck=2
        
        flying.hit_sound.play()
    if collide(green,arrow):
        green.x+=50
        arrow.x=-300
        arrowcheck=2
        flying.hit_sound.play()
        
    if collide(flying,boy):
        running=False
        font.draw(330,200,"Game Over")
        font.draw(280,150,"Score : ")
        font.draw(420,150,"%0.1f"%check_time)
        font.draw(500,150,"Second ")
        font.draw(520,100,"Press ESC ")
        if checkrank>0:
            loadscore()
            checkrank=-1
            game_over.play()
        draw_ranking()

    if collide(green,boy):
        running=False
        font.draw(330,200,"Game Over")
        font.draw(280,150,"Score : ")
        font.draw(420,150,"%0.1f"%check_time)
        font.draw(500,150,"Second ")
        font.draw(520,100,"Press ESC ")
        if checkrank>0:
            loadscore()
            checkrank=-1
            game_over.play()
        draw_ranking()
        
def draw():
    start_time = time.time()
    global check_time,moun
    while running:
        end_time = time.time()
        clear_canvas()
        moun.draw()
        sun.draw()
        moon.draw()
        background.draw()
        update()
        check_time=(end_time - start_time)
        boy.draw()
        flying.draw()
        green.draw()
        #green.draw_bb()
        arrow.draw()
        #arrow.draw_bb()
        #flying.draw_bb()        
        update_canvas()
        handle_events()
        delay(0.05)

    
