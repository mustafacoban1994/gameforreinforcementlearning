import pygame
import random
import numpy as np
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam


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


class DQLAgent:
    def __init__(self):
        # parameter / hyperparameter
        self.state_size = 4 # distance [(playerx-m1x),(playery-m1y),(playerx-m2x),(playery-m2y)]
        self.action_size = 5 # sağa, sola, yukarı, aşağı, hareketetme
        
        self.gamma = 0.95
        self.learning_rate = 0.001 
        
        self.epsilon = 1  # explore
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.01
        
        self.memory = deque(maxlen = 1000)
        
        self.model = self.build_model()
        
        
    def build_model(self):
        # neural network for deep q learning
        model = Sequential()
        model.add(Dense(48, input_dim = self.state_size, activation = "relu"))
        model.add(Dense(self.action_size,activation = "linear"))
        model.compile(loss = "mse", optimizer = Adam(lr = self.learning_rate))
        return model
    
    def remember(self, state, action, reward, next_state, done):
        # storage
        self.memory.append((state, action, reward, next_state, done))
    
    def act(self, state):
        state = np.array(state)
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])
    
    def replay(self, batch_size):
        # training
        if len(self.memory) < batch_size:
            return
        minibatch = random.sample(self.memory,batch_size)
        for state, action, reward, next_state, done in minibatch:
            state = np.array(state)
            next_state = np.array(next_state)
            if done:
                target = reward 
            else:
                target = reward + self.gamma*np.amax(self.model.predict(next_state)[0])
            train_target = self.model.predict(state)
            train_target[0][action] = target
            self.model.fit(state,train_target, verbose = 0)
            
    def adaptiveEGreedy(self):
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay



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
    def getKoor (self):
        return (self.rect.x, self.rect.y)


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
        
    def update(self, action):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        
        if keystate[pygame.K_LEFT] or action == 0:
            self.speedx = random.randint(-20,0)
        elif keystate[pygame.K_RIGHT] or action == 1:
            self.speedx = random.randint(0,20)
        elif keystate[pygame.K_UP] or action == 2:
            self.speedy = random.randint(-20,0)
        elif keystate[pygame.K_DOWN] or action == 3:
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
    
    

class Env(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.butun_sprite = pygame.sprite.Group()
        self.butun_dusman = pygame.sprite.Group()
        self.oyuncu = oyuncu()   
        self.dusman1 = dusman()
        self.dusman2 = dusman()
        self.butun_dusman.add(self.dusman1,self.dusman2)
        self.butun_sprite.add(self.oyuncu,self.dusman1,self.dusman2)
        
        self.reward = 0
        self.done = False
        self.total_reward = 0
        self.agent = DQLAgent()
        
    def findDist(self,a,b):
        d = a-b
        return d
        
    def step(self, action):
        statelist = []
        #update
        self.oyuncu.update(action)
        self.butun_dusman.update() 
        
        #get coordinate
        next_oyuncu_state = self.oyuncu.getKoor()
        next_dusman1_state = self.dusman1.getKoor()
        next_dusman2_state = self.dusman2.getKoor()
    
        #find distane
        statelist.append(self.findDist(next_oyuncu_state[0],next_dusman1_state[0]))
        statelist.append(self.findDist(next_oyuncu_state[1],next_dusman1_state[1]))
        statelist.append(self.findDist(next_oyuncu_state[0],next_dusman2_state[0]))
        statelist.append(self.findDist(next_oyuncu_state[1],next_dusman2_state[1]))
        return [statelist]
        
    
    #res
    def initialState(self):
        self.butun_sprite = pygame.sprite.Group()
        self.butun_dusman = pygame.sprite.Group()
        self.oyuncu = oyuncu()   
        self.dusman1 = dusman()
        self.dusman2 = dusman()
        self.butun_dusman.add(self.dusman1,self.dusman2)
        self.butun_sprite.add(self.oyuncu,self.dusman1,self.dusman2)
        
        self.reward = 0
        self.done = False
        self.total_reward = 0
        
        
        statelist = []
        #get coordinate
        oyuncu_state = self.oyuncu.getKoor()
        dusman1_state = self.dusman1.getKoor()
        dusman2_state = self.dusman2.getKoor()
    
        #find distane
        statelist.append(self.findDist(oyuncu_state[0],dusman1_state[0]))
        statelist.append(self.findDist(oyuncu_state[1],dusman1_state[1]))
        statelist.append(self.findDist(oyuncu_state[0],dusman2_state[0]))
        statelist.append(self.findDist(oyuncu_state[1],dusman2_state[1]))
        return [statelist]
        
    def run(self):
        #Oyun döngüsü
        state = self.initialState()
        running = True
        batch_size = 24
        while running:
            self.reward = 2
            #Döngü hızı
            clock.tick(fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
            action = self.agent.act(state)
            next_state=self.step(action)
            self.total_reward += self.reward
            
            hits = pygame.sprite.spritecollide(self.oyuncu,self.butun_dusman,False, pygame.sprite.collide_circle)
            if hits:
                self.reward = -150
                self.total_reward += self.reward
                self.done = True
                running = False
                print ("Toplam Skor: ", self.total_reward)
            #storage
            self.agent.remember(state,action, self.reward,next_state, self.done)
            #update state
            state = next_state
            
            #training
            
            self.agent.replay(batch_size)
            
            #epsilon
            self.agent.adaptiveEGreedy()
            
            ekran.fill(bg)
            self.butun_sprite.draw(ekran)
            pygame.display.flip()
        pygame.quit()           
        
if __name__ == "__main__":
    env = Env()
    liste = []
    t = 0
    while True:
        t += 1
        print("Episode: ",t)
        liste.append(env.total_reward)
                
        # initialize pygame and create window
        pygame.init()
        ekran = pygame.display.set_mode((w,h))
        pygame.display.set_caption("RL Game")
        clock = pygame.time.Clock()
        
        env.run()
  





