import pygame
import random


class Parcial:
    def __init__(self, alto, ancho, surface):
        self.sprites = []
        self.pos = []
        self.col_parcial = []
        self.surface = surface

        self.alto = alto
        self.ancho = ancho
        self.med = alto / 14

        self.st_change = False

        self.cont = 0
        self.current_f = 1

        self.n = [1,1,1] # numero inicial de parciales (se iran añadiendo más)
        self.var = None
        

    def load(self):
        for i in range(0,3):
            self.load = pygame.image.load(f'assets/character/map/parcial_{i}.png')
            self.sprite = pygame.transform.scale(self.load, (self.med,self.med))
            self.sprites.append(self.sprite)
        for i in range(0, len(self.n)):
            self.col_parcial.append(self.sprites[0].get_rect(topleft=(self.pos[i])))


    def random_pos(self):
        for i in range(0,3):
            x = random.randint(1, int(self.ancho / 1.04))
            y = random.randint(int(self.alto / 3), int(self.alto / 1.04))
            self.pos.append([x,y])


    # posicion random de los nuevos parciales generados
    def pos_r(self):
        
        x = random.randint(1, int(self.ancho / 1.04))
        y = random.randint(int(self.alto / 3), int(self.alto / 1.02))
        self.pos.append([x,y])


    # hitbox de los nuevos parciales generados
    def new_load(self):
        
        self.col_parcial.append(self.sprites[0].get_rect(topleft=(self.pos[len(self.n) - 1])))


    # detectar coliciones y quitar parciales
    def kill(self, col):
                
        if col is not self.var:
            index = self.col_parcial.index(col)
            self.var = col
            self.col_parcial.pop(index)
            self.pos.pop(index)
            self.n.pop(index)

            

    # los parciales te sigue ('o')
    def move(self, pos_x, pos_y):
        

        for i in range(0, len(self.n)):
           

            if self.pos[i][0] < pos_x:
                self.pos[i][0] += random.uniform(3,6)

                
            if self.pos[i][1] < pos_y:
                self.pos[i][1] += random.uniform(3,6)

                
    
            if self.pos[i][0] > pos_x:
                self.pos[i][0] -= random.uniform(3,6)
                

            if self.pos[i][1] > pos_y:
                self.pos[i][1] -= random.uniform(3,6)
                

            self.col_parcial.pop(i)
            self.col_parcial.insert(i, self.sprites[0].get_rect(topleft=(self.pos[i])))

            

    # cambio de estado entre pasable y hostil
    def change(self, pos_x, pos_y, tiempo, tiempo2):
        
        if tiempo >= 3:
            self.move(pos_x, pos_y)
            

        if tiempo2 == 10:
            for i in range(0,3): # coloca tres parciales nuevos cada 5 segundos (se puede modificar)
                self.n.append(1)
                self.pos_r()
                self.new_load()
            # print(f'{self.n} {tiempo2}')
                            

    # animaciones parciales hostiles
    def animate(self, n):
        self.current_f += 0.1
        if self.current_f >= len(self.sprites):
            self.current_f = 1
        self.surface.blit(self.sprites[int(self.current_f)], (self.pos[n - 1]))


    def render(self, tiempo):
        for i in range(0, len(self.n)):
            if tiempo <= 3:
                self.surface.blit(self.sprites[0], (self.pos[i]))
                self.st_change = False
            else:
                self.animate(i)
                self.st_change = True




    def retorno(self):
        if self.st_change == True:
            return self.col_parcial, 1
        if self.st_change == False:
            return self.col_parcial, 0


    def run(self, pos_x, pos_y, tiempo, tiempo2, contact):
        self.kill(contact)
        self.render(tiempo)
        self.change(pos_x, pos_y, tiempo, tiempo2)
        






# Empanadas

class Food:
    def __init__(self, alto, ancho, surface):
        self.sprites = []
        self.pos = []
        self.rect = []
        self.st_change = False
        self.med = alto / 16
        self.surface = surface
        
        self.var = None

        self.alto = alto
        self.ancho = ancho

    def load(self):
        for i in range(0,2):
            self.load = pygame.image.load(f'assets/character/map/empanada_{i}.png')
            self.sprite = pygame.transform.scale(self.load, (self.med, self.med))
            self.sprites.append(self.sprite)
        

    def random_pos(self):
        for i in range(0, 3):
            x = random.randint(1, int(self.ancho / 1.04))
            y = random.randint(int(self.alto / 3), int(self.alto / 1.04))
            self.pos.append([x,y])
        for i in range(0, len(self.pos)):
            self.rect.append(self.sprites[0].get_rect(topleft=(self.pos[i])))


    def kill(self, col):
       if col is not self.var:
            index = self.rect.index(col)
            self.rect.pop(index)
            self.pos.pop(index)
            self.var = col
            
        #self.col_parcial = self.sprites[0].get_rect(topleft=(self.pos[0], self.pos[1]))

    def render(self, tiempo):
        for i in range(0, len(self.rect)):
            if tiempo <= 3:
                self.surface.blit(self.sprites[0], (self.pos[i]))
                self.st_change = False
            else:
                self.surface.blit(self.sprites[1], (self.pos[i]))
                self.st_change = True

            

    def retorno(self):
        if self.st_change == True:
            return self.rect, 1 
        if self.st_change == False:
            return self.rect, 0



    def run(self, col, tiempo):
        self.kill(col)
        self.render(tiempo)
