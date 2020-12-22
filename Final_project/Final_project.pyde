add_library('minim')
import os, random,time
path = os.getcwd()
player = Minim(this)
BOARD_WIDTH = 1290
BOARD_HEIGHT = 780
COLOR_R = [255, 255, 255, 255, 204, 153, 153, 255]
COLOR_G = [102, 204, 255, 204, 204, 204, 102, 153]
COLOR_B = [102, 204, 204, 153, 255, 255, 153, 153]

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.d = 75
        self.vx = 0
        self.vy = 0
        self.img = loadImage(path + "/images/player1.png")
        self.img.resize(self.d, self.d)        
        self.key_handler = {LEFT:False, RIGHT:False, UP:False, DOWN:False}
        self.alive = True
        self.grade = 10
    
    def update(self):
        if self.key_handler[LEFT] == True:
            self.vx = -5
        elif self.key_handler[RIGHT] == True:
            self.vx = 5
        else:
            self.vx = 0
        
        if self.key_handler[UP] == True:
            self.vy = -5
        elif self.key_handler[DOWN] == True:
            self.vy = 5
        else:
            self.vy = 0
        
        self.y += self.vy
        self.x += self.vx
    
    def display(self):
        self.update()
        fill(255, 255, 255)
        textSize(20)
        text(self.grade, self.x+20, self.y)
        image(self.img, self.x, self.y)
        self.img.resize(int(self.d), int(self.d)) 
               
    def grow(self):
        self.d += self.grade * 0.01
        
class Circle():
    def __init__(self, clr_index, x, y):
        self.clr_index = clr_index
        self.r = 10
        self.x = x
        self.y = y
    
    def display(self):        
        fill(COLOR_R[self.clr_index], COLOR_G[self.clr_index], COLOR_B[self.clr_index])
        ellipse(self.x, self.y , self.r*2, self.r*2)
    
class Food(list):    
    def __init__(self):
        self.num_food = 100
        for i in range (self.num_food):
            self.append(Circle(random.randint(0, 7), random.randint(0,BOARD_WIDTH), random.randint(0,BOARD_HEIGHT)))
        
    def display(self):
        for food in self:
            food.display()
        self.update()
        
    def update(self):
        self.regenerate_food()
        self.add_food()
        
    def regenerate_food(self):
        if len(self)< int(self.num_food):
            self.append(Circle(random.randint(0, 7), random.randint(0,BOARD_WIDTH), random.randint(0,BOARD_HEIGHT)))
            self.regenerate_food()
    
    def add_food(self):
        self.num_food = self.num_food + 0.001
                
class Virus:
    def __init__(self, x, y, r,vx,vy):
        self.x = x
        self.y = y
        self.r = r
        self.img = loadImage(path + "/images/enemy.png")
        self.img.resize(self.r, self.r)
        self.vx = vx
        self.vy = vy
        self.dir_x = random.choice([LEFT, RIGHT])
        self.dir_y = random.choice([UP, DOWN])
        self.num_frames = 5
        self.frame = 0
        self.grade = 0
        
        if self.dir_x == LEFT:
            self.vx *= -1
        if self.dir_y == UP:
            self.vy *= -1
            
        self.xl = 0
        self.xr = BOARD_WIDTH -self.r  
        self.yl = 0
        self.yr = BOARD_HEIGHT -self.r 
    
    def display(self):        
        self.x += self.vx
        self.y += self.vy
        fill(255, 255, 255)
        textSize(20)
        text(self.grade, self.x+20, self.y)
        image(self.img, self.x, self.y)
        self.img.resize(int(self.r), int(self.r))        
        if frameCount % (10 - self.vx) == 0:
            self.frame = (self.frame + 1) % self.num_frames
        
        if self.x < self.xl:
            self.vx *= -1
            self.dir = RIGHT
        elif self.x > self.xr:
            self.vx *= -1
            self.dir = LEFT
        
        if self.y < self.yl:
            self.vy *= -1
            self.dir = RIGHT
        elif self.y > self.yr:
            self.vy *= -1
            self.dir = LEFT

    # def grow(self):
    #     self.r += self.grade * 0.002
        
class Enemy(list):
    def __init__(self):
        self.v = 5
        self.num_virus = 2
    
    def add_enemy(self):
        for i in range(self.num_virus):
            x = random.randint(0,BOARD_WIDTH-25)
            y = random.randint(0,BOARD_HEIGHT-25)
            r = 50
            self.append(Virus(x,y,r,self.v,self.v))
    
    def display(self):
        for enemy in self:
            enemy.display()

class Obstacle():
    def __init__(self, img, w, h, x, y):
        self.img = loadImage(path + "/images/" + img)
        self.img_w = w
        self.img_h = h
        self.x = x
        self.y = y
    
    def display(self):
        self.img.resize(self.img_w, self.img_h)
        image(self.img, self.x, self.y)
        
        
class Mask(Obstacle):
    def __init__(self, img, w, h, x, y):
        Obstacle.__init__(self, img, w, h, x, y)

class Party(Obstacle):
    def __init__(self, img, w, h, x, y):
        Obstacle.__init__(self, img, w, h, x, y)
           
class Game:
    def __init__(self):
        self.num_mask = 3
        self.num_party = 1
        self.start = False
        self.player = Player(600, 330)
        self.food = Food()
        self.enemy = Enemy()
        self.facemask = []
        self.party = []
        self.mask_on = False
        self.eat_sound = player.loadFile(path + "/sounds/eat.mp3")
        self.background_sound = player.loadFile(path + "/sounds/bg.mp3")
        self.background_sound.rewind()
        self.background_sound.loop()
    def add_mask(self):
        for m in range(self.num_mask):
            self.facemask.append(Mask("mask.png", 100, 60, random.randint(0, BOARD_WIDTH-140), random.randint(0, BOARD_HEIGHT-80)))
                                      
    def add_party(self):
        for p in range(self.num_party):
            self.party.append(Party("party.png", 100, 100, random.randint(0, BOARD_WIDTH-150), random.randint(0, BOARD_HEIGHT-150)))
            
        
    def display(self):
        self.food.display()
        self.player.display()
        self.enemy.display()
        self.update()
        self.printout()
        for m in self.facemask:
            m.display()
        for p in self.party:
            p.display()
    
    def printout(self):
        textSize(30)
        fill(255, 51, 52)
        text("Player Score :" + str(self.player.grade), 10, 30)
        # text("enemies left", 10, 60)
        
    def update(self):
        self.eat_enemy()
        self.eat_food()
        self.collision()
    
    def collision(self):
        for m in self.facemask:
            if (m.x - m.img_w/2 < self.player.x < (m.x+m.img_w/2) and m.y - m.img_h/2 < self.player.y < (m.y+m.img_h/2)):
                self.eat_sound.rewind()
                self.eat_sound.play()
                self.facemask.remove(m)
                self.player.grade += 10
                self.player.img = loadImage(path + "/images/player2.png")
                self.player.img.resize(75, 75)
                self.mask_on = True
                
#                self.player.grow()
            
            for e in self.enemy:
                if (e.x < m.x < (e.x+e.r) and e.y < m.y < (e.y+e.r)):
                    self.facemask.remove(m)
        
        for p in self.party:
            if (p.x - p.img_w/2 < self.player.x < (p.x+p.img_w/2) and p.y - p.img_h/2 < self.player.y < (p.y+p.img_h/2)):
                if self.mask_on == False:
                    self.player.alive = False
                    self.eat_sound.rewind()
                    self.eat_sound.play()
                else:
                    self.party.remove(p)
                    self.player.img = loadImage(path + "/images/player1.png")
                    self.player.img.resize(75, 75)
                    self.mask_on = False
                    self.eat_sound.rewind()
                    self.eat_sound.play()
                                            
            for e in self.enemy:
                if (e.x < p.x < (e.x+e.r) and e.y < p.y < (e.y+e.r)):
                    self.party.remove(p)
                    e.grade += 10
#                    e.grow()
            
    def eat_food(self):
        for f in self.food:
            if (self.player.x < f.x < (self.player.x+self.player.d) and self.player.y < f.y < (self.player.y+self.player.d)):
                self.food.remove(f)
                self.player.grade += 1
#                self.player.grow()
            for e in self.enemy:
                if (e.x < f.x < (e.x+e.r) and e.y < f.y < (e.y+e.r)):
                    self.food.remove(f)
                    e.grade += 1
#                    e.grow()
                    
    def eat_enemy(self):
        for e in self.enemy:
            if self.player.x<e.x<(self.player.x+self.player.d) and self.player.y<e.y<(self.player.y+self.player.d):
                if self.player.grade >= e.grade:
                    self.enemy.remove(e)
                    self.player.grade += e.grade
                    self.eat_sound.rewind()
                    self.eat_sound.play()
                else:
                    self.player.alive = False
          
    def endgame_display(self):
        textSize(80)
        fill(255, 255, 255)
        text("GAME OVER", 420, 300)
        textSize(60)
        fill(255, 51, 52)
        text("Score: " + str(self.player.grade), 500, 400)
    
    def wingame_display(self):
        textSize(80)
        fill(255, 255, 255)
        text("CONGRATULATIONS!!!", 250, 300)
        text("YOU WIN!", 460, 400)
        textSize(60)
        fill(255, 51, 52)
        text("Score: " + str(self.player.grade), 500, 500)
    
    def level_display(self):
        textSize(80)
        fill(255, 255, 255)
        text("SURVIVAL OF EMOJI", 270, 330)
        fill(255, 255, 255)
        rect(280, 500, 150, 70, 10)
        rect(530, 500, 230, 70, 10)
        rect(860, 500, 150, 70, 10)
        textSize(45)
        fill(0, 0, 0)
        text("Easy", 308, 550)
        text("Medium", 558, 550)
        text("Hard", 885, 550)
                        
game = Game()

def setup():
    size(BOARD_WIDTH,BOARD_HEIGHT)
    background(0, 0, 0)

def draw():
    global game
    background(0, 0, 0)
    if game.start == False:
        game.level_display()
    else:
        if len(game.enemy) == 0:
            game.wingame_display()
            game.background_sound.pause()
        elif game.player.alive == True:
            game.display()
        elif game.player.alive == False:
            game.endgame_display()
            game.background_sound.pause()
     
def mouseClicked():
    X = mouseX
    Y = mouseY
    if 500 <= Y <= 570:
        if 280 <= X <= 430:
            game.food.num_food = 200
            game.enemy.v = 3
            game.enemy.num_virus = 2
            game.enemy.add_enemy()
            game.num_mask = 3
            game.add_mask()
            game.add_party()
        if 530 <= X <= 760:
            game.enemy.num_virus = 3
            game.enemy.add_enemy()
            game.num_mask = 2
            game.add_mask()
            game.num_party = 2
            game.add_party()
        if 860 <= X <= 1110:
            game.enemy.v = 8
            game.enemy.num_virus = 5
            game.enemy.add_enemy()
            game.num_mask = 1
            game.add_mask()
            game.num_party = 3
            game.add_party()
        game.start = True
        game.display()
            
def keyPressed():
    if keyCode == LEFT:
        game.player.key_handler[LEFT] = True
    elif keyCode == RIGHT:
        game.player.key_handler[RIGHT] = True
    elif keyCode == UP:
        game.player.key_handler[UP] = True
    elif keyCode == DOWN:
        game.player.key_handler[DOWN] = True

def keyReleased():
    if keyCode == LEFT:
        game.player.key_handler[LEFT] = False
    elif keyCode == RIGHT:
        game.player.key_handler[RIGHT] = False
    elif keyCode == UP:
        game.player.key_handler[UP] = False
    elif keyCode == DOWN:
        game.player.key_handler[DOWN] = False
