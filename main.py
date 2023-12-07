import pygame
import os

# Initialize Pygame
pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("D1CK")
# Game loop
running = True
clock = pygame.time.Clock()


def resize_image(image):
    width = image.get_width() * 1.5
    height = image.get_height() * 1.5
    resized_image = pygame.transform.scale(image, (width, height))
    return resized_image



def unpack_assprite_files(path):
    images = []
    for filename in os.listdir(path):
        if filename.endswith(".png"):
            image = resize_image(pygame.image.load(os.path.join(path, filename)))
            images.append(image)
    return images


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.images_idle = [resize_image(pygame.image.load(r"ASSEST\PNGExports\PNGExports\Idle.png"))]
        
        # Add idle image(s) here
        self.images_running = unpack_assprite_files(path="ASSEST\Run")  # Add running animation images here
        self.images_shooting = unpack_assprite_files(path="ASSEST\ATTACK")  # Add shooting animation images here
        #self.images_shooting_running = unpack_assprite_files(path="ASSEST\AespriteFiles\Aesprite Files\Run.aseprite")  # Add shooting while running animation images here
        self.current_frame = 0
        self.animation_timer = pygame.time.get_ticks()  # Track time since last update
        self.animation_delay = 60  # Adjust animation delay as needed
        self.image = self.images_idle[self.current_frame]
        self.rect = self.image.get_rect()
        
        self.player_pos_x=screen_width / 2
        self.player_pos_y=screen_height / 2       
        
        self.rect.center = (self.player_pos_x, self.player_pos_y)
        self.running=False
        self.shooting=False
        self.idlle=True
        self.flip = False
        
        self.angle = 90
        
        self.speed_x=0
        self.speed_y=0

        self.speed=5
    # def rotate_check(self, angle):
    #     for i in range(len(self.images_idle)):
    #         self.images_idle[i] = pygame.transform.rotate(self.images_idle[i], angle)
    #     #self.image = pygame.transform.rotate(self.image, angle)
    #     #self.rect = self.image.get_rect(center=self.rect.center)
    #     #self.angle = (self.angle + 1) % 360
        
       
       
    def fliper(self):
        if self.flip:
            for i in range(len(self.images_idle)):
                self.images_idle[i] = pygame.transform.flip(self.images_idle[i], True, False)
            for i in range(len(self.images_running)):
                self.images_running[i] = pygame.transform.flip(self.images_running[i], True, False)
            for i in range(len(self.images_shooting)):
                self.images_shooting[i] = pygame.transform.flip(self.images_shooting[i], True, False)
            #for i in range(len(self.images_shooting_running)):
            #    self.images_shooting_running[i] = pygame.transform.flip(self.images_shooting_running[i], True, False)
            self.image = pygame.transform.flip(self.image, True, False)
            self.rect = self.image.get_rect()
            self.rect.center = (screen_width / 2, screen_height / 2)
        self.flip = False #not self.flip
        
    def run(self):
        self.running=True
        self.idlle=False
        self.shooting=False
    def shoot(self):
        self.running=False
        self.idlle=False
        self.shooting=True
    def idle(self):
        self.running=False
        self.idlle=True
        self.shooting=False
           
        
    def update(self):
        self.fliper()
        # self.rotate_check(self.angle)
        # Update animation frame based on animation delay
        if pygame.time.get_ticks() - self.animation_timer > self.animation_delay:
            self.animation_timer = pygame.time.get_ticks()
            self.current_frame = (self.current_frame + 1) % len(self.images_idle)

        # Update player logic here

        # Update player image based on player state
        if self.idlle==True:
            self.image = self.images_idle[self.current_frame]
        elif self.running==True:
            if self.shooting==True:
                pass
                self.image = self.images_shooting_running[self.current_frame]
            else:
                self.image = self.images_running[self.current_frame]
        else:
            if self.shooting==True:
                self.image = self.images_shooting[self.current_frame]
            else:
                self.image = self.images_idle[self.current_frame]
    

mr_player=Player()


keys_pressed = {}
while running:
    # Handle events
    screen.fill((0, 0, 0))  

    # for event in pygame.event.get():
    #     if event.type == pygame.QUIT:
    #         running = False

    # Update game logic
    
    #player.fliper()

    """ the following code is copied from the previous game i made called dungenouns and zombies"""
    
    mr_player.idle()
    for event in pygame.event.get():
        #print(event)
        
        #if len(pygame.event.get())==0:
        #    mr_player.idle()
        #print(event)
        if event.type == pygame.QUIT:
            running = False
            pygame.quit ()
        #if event.type==pygame.KEYDOWN:
        
        if event.type==pygame.KEYDOWN:
                keys_pressed[event.key]=True
        if event.type==pygame.KEYUP:
                keys_pressed[event.key]=False
        if event.type==pygame.MOUSEBUTTONDOWN:
            mr_player.shoot()

    #print(event.type==None)
        #print(event==pygame.NOEVENT)


    #print(keys_pressed)
    speed_x=-(keys_pressed.get(pygame.K_a,False)-keys_pressed.get(pygame.K_d,False))*mr_player.speed
    print(speed_x,mr_player.player_pos_x)
    mr_player.player_pos_x+=speed_x
    speed_y=-(keys_pressed.get(pygame.K_w,False)-keys_pressed.get(pygame.K_s,False))*5
    
    mr_player.player_pos_y+=speed_y
    mr_player.speed_x=speed_x
    mr_player.speed_y=speed_y
    
    # if mr_player.speed_x>0:
    #      mr_player.flip=False
        
    # if mr_player.speed_x<0:
    #      mr_player.flip=True
    
    if mr_player.speed_x>0:
        mr_player.run()
    
    if mr_player.player_pos_x<-220:
        mr_player.player_pos_x=800
    if mr_player.player_pos_x>800:
        mr_player.player_pos_x=-220     
         

    
    
    
    
    
    mr_player.update()

    screen.blit(mr_player.image, (mr_player.player_pos_x,mr_player.player_pos_y) ) #mr_player.rect)

    pygame.display.flip()  # Update the display
    clock.tick(6)  # Limit FPS to 60


# Clean up
pygame.quit()
