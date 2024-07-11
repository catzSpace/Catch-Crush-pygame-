import pygame


"""
    0 = izquierda
    1 = derecha
    2 = abajo
    3 = arriba
"""


class Player:
    def __init__(self, alto, ancho, surface, mesas_col, life):

        # sprites del jugador
        self.sprites = [[],[],[],[]]

        # info pantalla
        self.ancho = ancho
        self.alto = alto

        self.rect = None

        # pantalla
        self.surface = surface

        # posicon anterior (coliciones)
        self.pos_an = None

        # coliciones obj 
        self.mesas_col = mesas_col
        self.parcial_col = None
        self.empandas_col = None

        # direccion inicial
        self.direct = 'derecha'

        # posicion
        self.pos_x = ancho / 6
        self.pos_y = alto / 1.08
        self.med = alto / 16

        # velocidad
        self.speed = self.med // 8


        # frame actual
        self.current_f = 0

        # vida
        self.life = life

        # parcial con el que se hizo contacto
        self.contact = None
        self.cont_emp = None



        # parciales para ganar
        self.parcials = 0
        self.st = 0
        self.stp = 0 

        #sonidos
        self.perdervida = pygame.mixer.Sound('assets/music/soundEffects/lose_life.wav')
        self.ganarvida = pygame.mixer.Sound('assets/music/soundEffects/new_life.wav')
        self.ganarparcial = pygame.mixer.Sound('assets/music/soundEffects/new_life.wav')

    def load_sprites(self):
        for i in range(0,4):
            for j in range(1,4):
                self.load = pygame.image.load(f'assets/character/player/player_{i}_{j}.png')
                self.sprite = pygame.transform.scale(self.load, (self.med,self.med))
                self.sprites[i].append(self.sprite)
                


    def animate(self, op):
        self.current_f += 0.1
        if self.current_f >= len(self.sprites[op]):
            self.current_f = 0

        self.pos_an = (self.pos_x, self.pos_y)
        
        self.surface.blit(self.sprites[op][int(self.current_f)], (self.pos_x, self.pos_y))
        #self.rect = self.sprites[op][int(self.current_f)].get_rect()
            #print(int(self.current_f))
            #pygame.display.update()


    def colicion(self, op, op2):
        self.rect = self.sprites[op][0].get_rect(topleft=(self.pos_x, self.pos_y))

        # mesas
        for mesa_rec in self.mesas_col:
            if self.rect.colliderect(mesa_rec):
                self.pos_x, self.pos_y = self.pos_an


        # parciales 
        for parcial in self.parcial_col:
            if self.rect.colliderect(parcial) and self.st == 0:
                self.contact = parcial
                self.parcials += 1

                if self.parcials > 5:
                    self.parcials = 5

                if self.parcials < 0:
                    self.parcials = 0
                

            if self.rect.colliderect(parcial) and self.st == 1:
                if not self.life == 0 and not self.parcials > 5:
                    self.life -= 1
                    self.parcials -= 1

                    
                    if self.life < 0:
                        self.life = 0
                    if self.parcials < 0:
                        self.parcials = 0

                    self.contact = parcial
                    self.perdervida.play()

                

        # empanadas
        for empanada in self.empandas_col:
            if self.rect.colliderect(empanada) and self.stp == 0:
                if self.life < 4:
                    self.life += 1
                    self.cont_emp = empanada
                    self.ganarvida.play()


        

        # bordes de la pantalla
        if op2 == 1:
            if self.pos_x >= self.ancho / 1.04 or self.pos_x <= 1:
                self.pos_x = self.pos_an[0]
            if self.pos_y >= self.alto / 1.08 or self.pos_y <= self.alto / 5:
                self.pos_y = self.pos_an[1]





    def move(self):
        self.keys = pygame.key.get_pressed()
        if self.keys[pygame.K_a]:
            self.animate(0)
            self.pos_x -= self.speed
            self.colicion(0, 1)
            self.direct = 'izquierda'


        elif self.keys[pygame.K_d]:
            self.speed = self.med // 8
            self.animate(1)
            self.pos_x += self.speed
            self.colicion(1, 1)
            self.direct = 'derecha'




        elif self.keys[pygame.K_s]:
            self.speed = self.med // 8
            self.animate(2)
            self.pos_y  += self.speed
            self.colicion(2, 1)
            self.direct = 'abajo'
            


        elif self.keys[pygame.K_w]:
            self.speed = self.med // 8
            self.animate(3)
            self.pos_y -= self.speed
            self.colicion(3, 1)
            self.direct = 'arriba'


        # que hacer cuando se queda quieto

        if not any([self.keys[pygame.K_a], self.keys[pygame.K_d], self.keys[pygame.K_w], self.keys[pygame.K_s]]):
            if self.direct == 'derecha':
                self.surface.blit(self.sprites[1][0], (self.pos_x, self.pos_y))
                self.colicion(0, 0)

            if self.direct == 'izquierda':
                self.surface.blit(self.sprites[0][0], (self.pos_x, self.pos_y))
                self.colicion(1, 0)
                
            if self.direct == 'arriba':
                self.surface.blit(self.sprites[3][0], (self.pos_x, self.pos_y)) 
                self.colicion(3, 0)
                
            if self.direct == 'abajo':
                self.surface.blit(self.sprites[2][0], (self.pos_x, self.pos_y))
                self.colicion(2, 0)
                


    def run(self, parcial_col, st, empanadas_col, stp):
        
        self.parcial_col = parcial_col
        self.st = st

        self.empandas_col = empanadas_col
        self.stp = stp

        self.move()

        return self.parcials, self.life, self.pos_x, self.pos_y, self.contact, self.cont_emp





# npcs 
# habran 3 npcs
# cruch, boss, unicornio


class Npcs:
    def __init__(self, alto, ancho, name, rango, surface, op, vel):
        self.sprites = []


        self.state_e = 0

        # rango de sprites que hay
        self.rango = rango

        # nombre de la imagen
        self.name = name
        self.surface = surface

        # frame en actual
        self.current_f = 0

        self.alto = alto
        self.ancho = ancho

        # opcion (decide que personaje mostrar)
        self.op = op
        self.velocity = vel

        # colicion crush
        self.rect = None

        # posicion
        self.pos = [
            (ancho / 1.6, alto / 5),
            (ancho / 10, alto / 2.05)
        ]

        # tamaño
        self.tam = [
            (alto / 10, ancho / 12),
            (alto / 16, ancho / 20)
        ]


        # fuente (no se utilizó :c)
        self.font = pygame.font.Font("assets/fonts/slkscr.ttf", 50)


    def load_sprites(self):
        for i in range(0, self.rango):
            self.load = pygame.image.load(f'assets/character/npcs/{self.name}_{i}.png')
            self.sprite = pygame.transform.scale(self.load, (self.tam[self.op]))
            self.sprites.append(self.sprite)
            if self.rango == 8:
                self.rect = self.sprite.get_rect(topleft=(self.pos[self.op]))
                

    def animate(self):
        if self.current_f >= self.rango:
            self.current_f = 0
        self.surface.blit(self.sprites[int(self.current_f)], (self.pos[self.op]))
        self.current_f += self.velocity



    def render(self):
        self.animate()


    def emotion(self):
        pass

    def action(self):
        click = False # TODO
        if click:
            pass
            #self.text = self.font.render('test',0, (0,0,0))
            #self.surface.blit(self.text, (100, 100))


    def run(self):
        self.render()
        return self.rect
