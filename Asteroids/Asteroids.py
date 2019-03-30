import simplegui
import math
import random

#note to play this game on the browser, copy the code go to http://www.codeskulptor.org/ paste and play



# globals for user interface
WIDTH = 750
HEIGHT = 650
score = 0
MAX_LIVES = 5
lives = 0
time = 0.5
started = False

#globals for rocks
ROCK_MIN_VEL = -2
ROCK_MAX_VEL = 2
ROCK_MIN_ANG_VEL = -0.1
ROCK_MAX_ANG_VEL = 0.1

TOTAL_NUMBER_ROCKS = 12

class ImageInfo:
    """
    Image information
    """
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False, specialFeatures = None):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated
        self.specialFeatures = specialFeatures

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated
    
    def get_special_features(self):
        return self.specialFeatures

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2013.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

EXPLOSION_CENTER = [50, 50]
EXPLOSION_SIZE = [100, 100]
EXPLOSION_DIM = [9, 9]
ship_explosion_info = ImageInfo(EXPLOSION_CENTER, EXPLOSION_SIZE, 25, 60, True, True)
ship_explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/explosion.hasgraphics.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

class Ship:
    """
    Ship class
    """
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.is_thrusting = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        
        image_center = self.image_center
        
        if(self.is_thrusting):
            image_center = [self.image_center[0] * 3, self.image_center[1]]

        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        
        canvas.draw_image(self.image, 
                          image_center, 
                          self.image_size, 
                          self.pos, 
                          self.image_size,
                          self.angle)
    def thrust(self, on):
        if(on):
            self.is_thrusting = True
            ship_thrust_sound.play()
        else:
            self.is_thrusting = False
            ship_thrust_sound.pause()
            ship_thrust_sound.rewind()
            
    def updateAngle(self, dir):
        self.angle_vel = dir
    
    def update(self):
        self.angle += self.angle_vel
        #Position update
        self.pos[0] +=  self.vel[0]      
        self.pos[1] +=  self.vel[1] 
        #Friction update
        a = 0.1
        c = 0.02
        self.vel[0] *= (1 - c)
        self.vel[1] *= (1 - c)
        #Thrust udpate
        forward = angle_to_vector(self.angle)
        if(self.is_thrusting):
            self.vel[0] += forward[0] * a
            self.vel[1] += forward[1] * a
            
    def shoot(self):
        global missile_group
        
        forward = angle_to_vector(self.angle)
        a_missile = Sprite([forward[0] * self.image_center[0] + self.pos[0], forward[1] * self.image_center[1] + self.pos[1]], 
                           [self.vel[0] + forward[0] * 5, self.vel[1] + forward[1] * 5], 
                           0, 
                           0.4, 
                           missile_image, 
                           missile_info, 
                           missile_sound)
    
        missile_group.add(a_missile)
    
    def get_pos(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
    def get_angle(self):
        return self.angle
        
        
class Sprite:
    """
    Sprite class
    """
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.specialFeatures = info.get_special_features()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        
        if(self.animated):
            if(self.specialFeatures):
                explosion_index = [self.age % EXPLOSION_DIM[0], (self.age // EXPLOSION_DIM[0]) % EXPLOSION_DIM[1]]
                canvas.draw_image(ship_explosion_image, 
                                [EXPLOSION_CENTER[0] + explosion_index[0] * EXPLOSION_SIZE[0], 
                                 EXPLOSION_CENTER[1] + explosion_index[1] * EXPLOSION_SIZE[1]], 
                                 EXPLOSION_SIZE, self.pos, EXPLOSION_SIZE)
            else:
                canvas.draw_image(self.image, 
                                  [self.image_center[0] + self.age * self.image_size[0], self.image_center[1]], 
                                  self.image_size, 
                                  self.pos, 
                                  self.image_size,
                                  self.angle)
        else:
            canvas.draw_image(self.image, 
                              self.image_center, 
                              self.image_size, 
                              self.pos, 
                              self.image_size,
                              self.angle)
    
    def update(self):
        self.angle += self.angle_vel
        self.pos[0] +=  self.vel[0]      
        self.pos[1] +=  self.vel[1]
        self.age += 1
        if(self.age >= self.lifespan):
            return True
        else:
            return False

    def get_pos(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
        
    def collide(self, other_sprite):
        d = dist(self.pos,other_sprite.get_pos())
        if(d < self.radius + other_sprite.get_radius()):
            return True
        else:
            False

def group_collide(group, sprite):
   
    global explosion_group
    
    collisions = False
    for s in set(group):
        if(s.collide(sprite)):
            group.remove(s)
            collisions = True
            explosion = Sprite(s.get_pos(), [0,0], 0, 0, explosion_image, explosion_info, explosion_sound)
            explosion_group.add(explosion)
    
    return collisions

def group_group_collide(rocks_group, missils_group):
    numberHits = 0
    for rock in set(rocks_group):
        if(group_collide(missils_group, rock)):
            rocks_group.remove(rock)
            numberHits += 1

    return numberHits
            
def keyup_handler(key):
    if(started):
        if key == simplegui.KEY_MAP['up']:
            my_ship.thrust(False)
        elif key == simplegui.KEY_MAP['right']:
            my_ship.updateAngle(0)
        elif key == simplegui.KEY_MAP['left']:
            my_ship.updateAngle(0)
        
def keydown_handler(key):
    """
    Event handler for key down
    """
    if(started):
        if key == simplegui.KEY_MAP['up']:
            my_ship.thrust(True)
        elif key == simplegui.KEY_MAP['right']:
            my_ship.updateAngle(0.1)
        elif key == simplegui.KEY_MAP['left']:
            my_ship.updateAngle(-0.1)
        elif key == simplegui.KEY_MAP['space']:
            my_ship.shoot()

def mouse_handler(position):
    if(not started):
        new_game()
    
def draw(canvas):
    global time, lives, score, started, explosion_group
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    if(lives <= 0):
        started = False
    
    if(started == False):
        timer.stop()
        ship_thrust_sound.pause()
        ship_thrust_sound.rewind()
        canvas.draw_image(splash_image, 
                          splash_info.get_center(), 
                          splash_info.get_size(), 
                          (WIDTH / 2, HEIGHT / 2), 
                          (WIDTH / 2, HEIGHT / 2))
    else:
        
        if(group_collide(rock_group, my_ship)):
            lives -= 1
            #explosion = Sprite(my_ship.get_pos(), [0,0], 0, 0, explosion_image, explosion_info, explosion_sound)
            ship_explosion = Sprite(my_ship.get_pos(), [0,0], 0, 0, ship_explosion_image, ship_explosion_info, explosion_sound)
            explosion_group.add(ship_explosion)
            recreate_spaceship(my_ship)
        
        score += group_group_collide(rock_group, missile_group)
        
        my_ship.draw(canvas)
        my_ship.update()
    
        process_sprite_group(rock_group, canvas)
        process_sprite_group(missile_group, canvas)
        process_sprite_group(explosion_group, canvas)
    canvas.draw_text('Lives:', (50, 30), 25, 'White')
    canvas.draw_text(str(lives), (50, 60), 25, 'Yellow')
    canvas.draw_text('Score:', (WIDTH - 100, 30), 25, 'White')
    canvas.draw_text(str(score), (WIDTH - 100, 60), 25, 'Yellow')


def process_sprite_group(group, canvas):
 
    for s in set(group):
        s.draw(canvas)
        if(s.update()):
            group.remove(s)
    
def rock_spawner():
    """
    Rock generator
    """
    global rock_group
 
    if(len(rock_group) < TOTAL_NUMBER_ROCKS):

        vel_range = ROCK_MAX_VEL - ROCK_MIN_VEL
        ang_vel_range = ROCK_MAX_ANG_VEL - ROCK_MIN_ANG_VEL
    
        pos = [random.random() * WIDTH,
               random.random() * HEIGHT]
        
        vel = [random.random() * vel_range + ROCK_MIN_VEL,
               random.random() * vel_range + ROCK_MIN_VEL]
            
        ang = random.random()
        
        ang_vel = random.random() * ang_vel_range + ROCK_MIN_ANG_VEL
        
        a_rock = Sprite(pos, vel, ang, ang_vel, asteroid_image, asteroid_info)
        
        if(not a_rock.collide(my_ship)):
            rock_group.add(a_rock)

def recreate_spaceship(ship = None):
    global my_ship
    
    if(ship):
        my_ship = Ship(ship.get_pos(), [0, 0], ship.get_angle(), ship_image, ship_info)
    else:
        my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
            
def new_game():
    global started, lives, score, rock_group, missile_group, my_ship, explosion_group
    
    started = True
    lives = MAX_LIVES
    score = 0
    
    recreate_spaceship()
    rock_group = set([])
    missile_group = set([])
    explosion_group = set([])
    
    timer.start()
    soundtrack.rewind()
    soundtrack.play()
    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
rock_group = set([])
missile_group = set([])
explosion_group = set([])

# register handlers
frame.set_draw_handler(draw)

timer = simplegui.create_timer(1000.0, rock_spawner)
frame.set_keydown_handler(keydown_handler)
frame.set_keyup_handler(keyup_handler)
frame.set_mouseclick_handler(mouse_handler)

# get things rolling
frame.start()
