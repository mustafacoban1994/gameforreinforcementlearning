import pygame
import random

w = 300
h = 300
fps = 30

#renk
white = (255, 255, 255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
bg = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
bg_oyuncu = (random.randint(0,255), random.randint(0,255), random.randint(0,255))



class dusman (pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10,30))
        self.image.fill(bg_oyuncu)
        self.rect = self.image.get_rect()
        self.rect.centerx = 0
        self.rect.bottom = h
        self.y_speed = 5
        self.x_speed = 5
    def update(self):
        self.rect.y += self.y_speed
        self.rect.x += self.x_speed
        if self.rect.bottom > h:
            self.y_speed = random.randint(-15,0)
            self.x_speed = random.randint(-15,0)   
        if self.rect.top < 0 :
            self.y_speed = random.randint(0,15)
            self.x_speed = random.randint(0,15)
        if self.rect.left < 0 :
            self.y_speed = random.randint(0,15)
            self.x_speed = random.randint(0,15)
        if self.rect.right > w :
            self.y_speed = random.randint(-15,0)
            self.x_speed = random.randint(-15,0)  



class oyuncu (pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((40,20))
        self.image.fill(bg_oyuncu)
        self.radius = 4
        self.rect = self.image.get_rect()
        self.rect.centerx = w/2
        self.rect.bottom = h-1
        self.y_speed = 5
        self.x_speed = 5
        
    def update(self):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        
        if keystate[pygame.K_LEFT]:
            self.speedx = random.randint(-20,0)
        elif keystate[pygame.K_RIGHT]:
            self.speedx = random.randint(0,20)
        elif keystate[pygame.K_UP]:
            self.speedy = random.randint(-20,0)
        elif keystate[pygame.K_DOWN]:
            self.speedy = random.randint(0,20)  
        else:
            self.speedx=0
            self.speedy=0
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        
        if self.rect.right > w:
            self.rect.right = w
            
        if self.rect.left < 0:
            self.rect.left = 0
             
        if self.rect.top < 0 :
            self.rect.top = 0
            
        if self.rect.bottom > h :
            self.rect.bottom = w  
            
    def getKoor (self):
        return (self.rect.x, self.rect.y)
    
#ekran oluşturulması
pygame.init()
ekran = pygame.display.set_mode((w,h))
pygame.display.set_caption("Oyun")
clock = pygame.time.Clock()

butun_sprite = pygame.sprite.Group()
butun_dusman = pygame.sprite.Group()
oyuncu = oyuncu()
dusman1 = dusman()
dusman2 = dusman()
dusman3 = dusman()
butun_dusman.add(dusman1,dusman2,dusman3)
butun_sprite.add(oyuncu,dusman1,dusman2,dusman3)

#Oyun döngüsü
running = True
while running:
    #Döngü hızı
    clock.tick(fps)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    #Guncelleme
    butun_sprite.update()
            
    hits = pygame.sprite.spritecollide(oyuncu,butun_dusman,False, pygame.sprite.collide_circle)
    if hits:
        running = False
        print ("oyun bitti")
    
    
    #Gorsel        
    ekran.fill(bg)
    butun_sprite.draw(ekran)
    pygame.display.flip()
    
pygame.quit()   







