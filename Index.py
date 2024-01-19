
from pygame import *
import random
from sys import exit
class Player(sprite.Sprite):
    def __init__(self):
        super().__init__()
        #animation
        player_walk1=image.load(r"Platformer Art Deluxe (Pixel)\player_walk_1.png").convert_alpha()
        player_walk2=image.load(r"Platformer Art Deluxe (Pixel)\player_walk_2.png").convert_alpha()
        self.player_walk=[player_walk1,player_walk2]
        self.player_index=0
        self.player_jump=image.load(r"Platformer Art Deluxe (Pixel)\jump.png").convert_alpha()
        
        self.image=self.player_walk[self.player_index]
        self.rect=self.image.get_rect(midbottom=(80,300))
        self.gravity=0
        
        self.jump_sound=mixer.Sound(r"Platformer Art Deluxe (Pixel)\jump.mp3")
        self.jump_sound.set_volume(0.5)
    def player_input(self):
        keys=key.get_pressed()
        if keys[K_SPACE] and self.rect.bottom>=300:
            self.gravity=-20
            self.jump_sound.play()
    
    def apply_gravity(self):
        self.gravity+=1
        self.rect.y+=self.gravity
        if self.rect.bottom>=300:
            self.rect.bottom=300
    
    def animation(self):
        if self.rect.bottom<300:
            self.image=self.player_jump
        else:
            self.player_index+=0.1
            if self.player_index>=len(self.player_walk):self.player_index=0
            self.image=self.player_walk[int(self.player_index)]
    
    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation()
class Obstacle(sprite.Sprite):
        def __init__(self,type):
            super().__init__()
            if type=='fly':
                fly1= image.load(r"Platformer Art Deluxe (Pixel)\Fly1.png").convert_alpha()
                fly2= image.load(r"Platformer Art Deluxe (Pixel)\Fly2.png").convert_alpha()
                self.frames=[fly1,fly2]
                y_pos=210
            else:
                snail1 = image.load(r"Platformer Art Deluxe (Pixel)\snail1.png").convert_alpha()
                snail2 = image.load(r"Platformer Art Deluxe (Pixel)\snail2.png").convert_alpha()
                self.frames=[snail1,snail2]
                y_pos=300
            self.animation_index=0
            self.image=self.frames[self.animation_index]
            self.rect=self.image.get_rect(midbottom=(random.randint(900,1100),y_pos))
        def animation(self):
            self.animation_index+=0.1
            if self.animation_index>=len(self.frames) :self.animation_index=0
            self.image=self.frames[int(self.animation_index)]
        def update(self):
            self.animation()
            self.rect.x-=6
            self.destroy()
        def destroy(self):
            if self.rect.x<=-100:
                self.kill()         
def display_score():
    current_time =time.get_ticks()-start_time
    score_surface=test_font.render(f'Score: {current_time//100}',False,(64,64,64))
    score_rect = score_surface.get_rect(center =(400,50))
    screen.blit(score_surface,score_rect)
    return current_time//100

def collision_sprite():
    if sprite.spritecollide(player.sprite,obstacle_group,False):
        obstacle_group.empty()
        return False
    else:
        return True

init()
screen=display.set_mode((800,400))
display.set_caption('Kuki Runner')
clock=time.Clock()
test_font=font.Font(r"Platformer Art Deluxe (Pixel)\Pixeltype.ttf",50)
game_active=False
start_time=0
score=0
h_score=0
bgm=mixer.Sound(r"Platformer Art Deluxe (Pixel)\music.wav")

#Groups
player=sprite.GroupSingle()
player.add(Player())

obstacle_group=sprite.Group()

sky_surface=image.load(r"Platformer Art Deluxe (Pixel)\backgrounds.png").convert()
ground_surface=image.load(r"Platformer Art Deluxe (Pixel)\ground.png").convert()

#Intro screen
player_stand=image.load(r"Platformer Art Deluxe (Pixel)\player_stand.png").convert_alpha()
player_stand=transform.rotozoom(player_stand,0,2)
player_stand_rect =player_stand.get_rect(center=(400,200))

game_name=test_font.render('Kuki Runner',False,(111,196,169))
game_name_rect =game_name.get_rect(center =(400,80))

game_message=test_font.render('Press space to run',False,(111,196,169))
game_message_rect =game_message.get_rect(center=(400,350))


#Timer
i=0
obstacle_timer = USEREVENT +1
time.set_timer(obstacle_timer,1300)



while True:
    for eve in event.get():
        if eve.type==QUIT:
            quit()
            exit()
        if game_active:
            if eve.type==obstacle_timer:
                obstacle_group.add(Obstacle(random.choice(['fly','snail','snail'])))
        else:
            if eve.type== KEYDOWN and eve.key == K_SPACE:
                game_active=True
                start_time=time.get_ticks()
        

    if game_active:
        screen.blit(transform.scale(sky_surface, (1000,1000 )), (0, 0))
        screen.blit(ground_surface,(0,300))
        score=display_score()
        
        player.draw(screen)
        player.update()
        
        obstacle_group.draw(screen)
        obstacle_group.update()
        game_active=collision_sprite()
        
        i+=0.01
        bgm.play()
        bgm.set_volume(0.1)
    else:
        screen.fill((94,126,162))
        screen.blit(ground_surface,(0,300))
        
        score_message=test_font.render(f"Your Score: {score}",False,(111,196,169))
        score_message_rect=score_message.get_rect(center=(400,200))
        screen.blit(game_name,game_name_rect)
        
        h_score=max([score,h_score])
        h_score_message=test_font.render(f"High Score: {h_score}",False,(111,196,169))
        h_score_message_rect=score_message.get_rect(center=(400,250))
        screen.blit(game_name,game_name_rect)
        player_gravity=300
        if score ==0:screen.blit(game_message,game_message_rect)
        else:
            screen.blit(score_message,score_message_rect)
            screen.blit(h_score_message,h_score_message_rect)
            i=0
    display.update()
    clock.tick(60+i)