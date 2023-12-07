import pygame
import os
import random
def resize_image(image):
    width = image.get_width() * 2
    height = image.get_height() * 2
    resized_image = pygame.transform.scale(image, (width, height))
    return resized_image

def unpack_assprite_files(path):
    images = []
    for filename in os.listdir(path):
        if filename.endswith(".png"):
            image = resize_image(pygame.image.load(os.path.join(path, filename)))
            images.append(image)
    return images

run_frames = unpack_assprite_files(path="ASSEST\Run")
# for i in range(5):
#     run_frames=run_frames+run_frames

walk_frames =  unpack_assprite_files(path="ASSEST\Run") 
shoot_frames = unpack_assprite_files(path="ASSEST\ATTACK") 
idle_frame =  resize_image(pygame.image.load(r"ASSEST\PNGExports\PNGExports\Idle.png"))


import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, run_frames, walk_frames, shoot_frames, idle_frame):
        super(Player, self).__init__()
        self.image = idle_frame
        self.rect = self.image.get_rect(topleft=pos)

        self.run_frames = run_frames
        self.walk_frames = walk_frames
        self.shoot_frames = shoot_frames
        self.idle_frame = idle_frame

        self.current_frame = 0
        self.animation_speed = 10
        self.animation_delay = 0

        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 5

        self.is_shooting = False
        self.flipped = False

    def update(self):
        self.handle_input()
        self.animate()
        self.move()

    def handle_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_a]:
            self.direction.x = -1
            self.flipped = True
        elif keys[pygame.K_d]:
            self.direction.x = 1
            self.flipped = False
        else:
            self.direction.x = 0

        self.is_shooting = pygame.mouse.get_pressed()[0]
        if self.is_shooting == False:
            self.handle_mouse_release()
            self.speed=5
        else:
            self.speed=0
        
        

    def flip_image(self, image):
        return pygame.transform.flip(image, True, False)

    def animate(self):
        self.animation_delay += 1
        #print(self.direction.magnitude())

        if self.is_shooting:
            # Handle shooting animation
            if self.current_frame < len(self.shoot_frames):
                self.image = self.flip_image(self.shoot_frames[self.current_frame]) if self.flipped else self.shoot_frames[self.current_frame]
                self.current_frame += 1
            else:
                self.is_shooting = False
                self.current_frame = 0

        else:
            # Handle movement animation
            if self.direction.magnitude() > 0.1:
                if self.current_frame < len(self.shoot_frames):
                    self.image = self.flip_image(self.shoot_frames[self.current_frame]) if self.flipped else self.shoot_frames[self.current_frame]
                    self.current_frame += 1
                else:
                    self.is_shooting = False
                    self.current_frame = 0
                
                # Update frame and reset delay when threshold reached
                # if self.animation_delay >= self.animation_speed:
                #     self.current_frame = (self.current_frame + 1) % len(self.run_frames)
                #     self.image = self.flip_image(self.run_frames[self.current_frame]) if self.flipped else self.run_frames[self.current_frame]
                #     self.animation_delay = 0  # Reset the delay
            else:
                # Set idle frame and reset delay for smooth transition
                self.image = self.idle_frame
                self.animation_delay = 0  # Reset the delay

    def move(self):
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed

    def handle_mouse_release(self):
        self.is_shooting = False
        self.current_frame = 0
        

                



        


# ...

# Sample usage
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Load player animation frames


player = Player((100, 100), run_frames, walk_frames, shoot_frames, idle_frame)





class Zombie(pygame.sprite.Sprite):
    def __init__(self, pos, run_frames, dead_frame):
        super(Zombie, self).__init__()
        self.image = run_frames[0]
        self.rect = self.image.get_rect(center=pos)

        self.run_frames = run_frames
        self.dead_frames = dead_frame

        self.current_frame = 0
        self.animation_speed = 5
        self.animation_delay = 0

        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 1

        self.is_dead = False
        self.flipped = False  # Added: Initial flipped state

    def flip_image(self, image):
        return pygame.transform.flip(image, True, False)

    def update(self, player_pos):
        self.move_towards_player(player_pos)
        self.animate()

    def move_towards_player(self, player_pos):
        # Convert player position to a vector
        player_vector = pygame.math.Vector2(*player_pos)
        # Calculate direction vector
        try:
            self.direction = (player_vector - self.rect.center).normalize()
        except:
            pass
        # Update position based on direction and speed
        self.rect.center += self.direction * self.speed
        distance = (player_vector - self.rect.center).magnitude()

        if distance > 0.1:
            self.direction = (player_vector - self.rect.center).normalize()
            self.flipped = self.direction.x < 0


    # def animate(self):
    #     self.animation_delay += 1

    #     if self.is_dead:
    #         # Play dead animation sequence
    #         if self.current_frame < len(self.dead_frames):
    #             self.image = self.dead_frames[self.current_frame]
    #             self.current_frame += 1
    #         else:
    #             # Show last frame of dead animation indefinitely
    #             self.image = self.dead_frames[-1]
    #     else:
    #         # Play run animation as usual
    #         if self.animation_delay >= self.animation_speed:
    #             self.current_frame = (self.current_frame + 1) % len(self.run_frames)
    #             self.image = self.run_frames[self.current_frame]
    #             self.animation_delay = 0
    def animate(self):
        self.animation_delay += 1

        if self.is_dead:
            # Play dead animation sequence
            if self.current_frame < len(self.dead_frames):
                self.image = self.flip_image(self.dead_frames[self.current_frame]) if self.flipped else self.dead_frames[self.current_frame]
                self.current_frame += 1
            else:
                # Show last frame of dead animation indefinitely
                self.image = self.flip_image(self.dead_frames[-1]) if self.flipped else self.dead_frames[-1]
        else:
            # Play run animation with flipping
            if self.animation_delay >= self.animation_speed:
                self.current_frame = (self.current_frame + 1) % len(self.run_frames)
                self.image = self.flip_image(self.run_frames[self.current_frame]) if self.flipped else self.run_frames[self.current_frame]
                self.animation_delay = 0


    def check_death(self, player_pos,is_shooting):
        # Convert player position to a vector
        player_vector = pygame.math.Vector2(*player_pos)
        # Calculate distance
        distance = (player_vector - self.rect.center).magnitude()
        if not self.is_dead and distance < 30 and is_shooting:
            self.is_dead = True



screen_width, screen_height = screen.get_size()
dead_frame=unpack_assprite_files(path=r"ASSEST\64x64 Pixel Art Character and zombie by RgsDev\Zombie\Dead")
run_frames_zombie=unpack_assprite_files(path=r"ASSEST\64x64 Pixel Art Character and zombie by RgsDev\Zombie\Walk")
zombies = []

for i in range(10):
    dead_frame=dead_frame+dead_frame

for _ in range(10):
    pos = random.randint(0, screen_width), random.randint(0, screen_height)
    zombie = Zombie(pos, run_frames_zombie, dead_frame)
    zombies.append(zombie)


dead_zombies=[]
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    for pos in dead_zombies:
        screen.blit(dead_frame[-1], pos)
    
    
    

    
    
    
    
    
    
    for zombie in zombies:
        zombie.update(player.rect.center)
        zombie.check_death(player.rect.center,player.is_shooting)
        screen.blit(zombie.image, zombie.rect)

    # ...
    
    # Check for dead zombies and spawn new ones
    for i, zombie in enumerate(zombies):
        if zombie.is_dead:
            dead_zombies.append(zombie.rect.center)

            del zombies[i]
            pos = random.randint(0, screen_width), random.randint(0, screen_height)
            zombie = Zombie(pos, run_frames_zombie, dead_frame)
            zombies.append(zombie)
            break
    
    # Draw dead zombies

    player.update()
    screen.blit(player.image, player.rect)
    
    
    pygame.display.flip()
    clock.tick(30)
