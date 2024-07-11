import pygame
from src.player import *
from src.obj import *
from src.entity import *

class Level:
    def __init__(self, surface, alto, ancho):
        # objetos del entorno
        self.obj = Obj(alto, ancho, surface)
        self.obj.load_mesas()
        self.obj.load_obj_cuad()

        # coliciones crush
        self.rect_crush = None


        #parciales y empanadas
        self.tiempo = 0
        self.parcial = Parcial(alto, ancho, surface)
        self.parcial.random_pos()
        self.parcial.load()


        self.empanadas = Food(alto, ancho, surface)
        self.empanadas.load()
        self.empanadas.random_pos()


        # coliciones objetos
        self.obj.col()
        mesas_col = self.obj.return_col()

        # ventana
        self.surface = surface

        #jugador
        self.life = 4
        self.player = Player(alto, ancho, surface, mesas_col, self.life)
        self.parcial_st = 0
        self.empanadas_st = None


        # Npcs
        self.crush = Npcs(alto, ancho, 'crush', 8, surface, 0, 0.1)
        self.crush.load_sprites()

        self.boss = Npcs(alto, ancho, 'boss', 2, surface, 1, 0.05)
        self.boss.load_sprites()

        # barra de vida y contador de parciales recogidos
        self.sprites = []
        self.sprites_pa = []

        # medidas
        self.alto = alto
        self.ancho = ancho

        # cargando sprites jugador
        self.player.load_sprites()

        #musica
        pygame.mixer.music.load('assets/music/game_ost.mp3')
        pygame.mixer.music.play(-1)

    def load(self):
        #for i in range(0,1):
        #   pass


        # cargar medidores de vida y parciales
        for i in range(0,5):
            self.load = pygame.image.load(f'assets/character/player/bar_life_{i}.png')
            self.sprite = pygame.transform.scale(self.load, ( (self.ancho / 6), (self.ancho / 12) ))
            self.sprites.append(self.sprite)


        for i in range(1, 6):
            self.load = pygame.image.load(f'assets/character/player/parcial_{i}.png')
            self.sprite = pygame.transform.scale(self.load, ( (self.ancho / 4), (self.alto / 12) ))
            self.sprites_pa.append(self.sprite)



    def setup(self, tiempo, tiempo2):

        parcial_col, op = self.parcial.retorno()
        empanada_col, op_emp = self.empanadas.retorno()

        # jugador
        self.parcial_st, self.life, self.pos_x, self.pos_y, self.contact, self.col_emp = self.player.run(parcial_col, op, empanada_col, op_emp)

        # empanadas y parciales
        self.parcial.run(self.pos_x, self.pos_y, tiempo, tiempo2, self.contact)
        self.empanadas.run(self.col_emp, tiempo)

        # Npcs
        self.rect_crush = self.crush.run()
        self.boss.run()



    def entorno(self):
        
        # renderizar objetos del entorno
        self.surface.blit(self.sprites[int(self.life)], (0,0))
        if self.parcial_st >= 1:
            self.surface.blit(self.sprites_pa[int(self.parcial_st) - 1], ( (self.ancho / 6), (self.alto // -100)))
        self.obj.render()

   
    def run(self, tiempo, tiempo2, life):
        self.entorno()
        self.setup(tiempo, tiempo2)
        return self.life, self.parcial_st, self.rect_crush
        self.life = life

