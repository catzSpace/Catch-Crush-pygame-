import pygame, sys
from src.level import *
from src.intro import *
#from moviepy.editor import *


pygame.init()



class Game:
    def __init__(self):
        
        # opciones de ventana
        flags = pygame.FULLSCREEN

        # estado 
        self.st = 0

        # tiempo cambio 5 segundos
        self.contador = 0
        self.contador2 = 0
        self.c = 1


        self.life = 4

        # estado para ganar
        self.crush_return = 'wait'
        self.vid_run = 0

        self.parcials = 0
        self.rect = None

        
        # ventana
        self.screen = pygame.display.set_mode((0,0), flags)
        pygame.display.set_caption('parciales')

        self.surface_aux = pygame.Surface(self.screen.get_size())
        
        # informacion de la ventana para medidas relativas
        self.info = pygame.display.Info()
        self.alto, self.ancho = self.info.current_h, self.info.current_w

        #lado
        self.lado = (self.alto / 100) * 3

        # cursor personalizado
        self.load = pygame.image.load('assets/character/ent/cursor.png')
        self.cursor = pygame.transform.scale(self.load, (self.lado, self.lado))
        pygame.mouse.set_visible(False)

        # contador
        self.clock = pygame.time.Clock()

        # instancia de las animaciones (intro)
        self.intro = Intro(self.screen, self.ancho, self.alto)

        self.vid_run = self.intro.retorno()
        if self.vid_run == 1:
            self.intro.render()

        # pantalla de muerte
        self.dead = Dead(self.screen, self.alto, self.ancho)
        self.dead.load()

        # pantalla de victoria
        self.win = Win(self.screen, self.alto, self.ancho)
        self.win.load()

        # instancia del nivel
        self.level = Level(self.surface_aux, self.alto, self.ancho)
        self.level.load()

    # contador de segundos        
    def sum(self):
        self.contador += 0.01
        self.contador2 -= 0.01
        if self.contador >= 10:
            self.contador2 = 10
            self.contador = 0

    def run(self):

        while True:
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # deteccion del mouse para ganar
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.rect.collidepoint(event.pos) and self.parcials == 5:
                        self.crush_return = 'win'
                        

            # teclado
            self.keys = pygame.key.get_pressed()
            


            #if self.c == 1 and self.crush_return == 'wait':
            self.screen.fill((34,32,52))           
            

            # pantalla de muerte
            if self.life == 0 and self.c == 1:
                self.dead.run()
            
            # juego
            if self.life > 0 and self.crush_return != 'win':

                # fondo de pantalla
                self.surface_aux.fill((34,32,52))            

                # nivel
                self.life, self.parcials, self.rect = self.level.run(self.contador, self.contador2, self.life)

                #cursor
                cursor_x, cursor_y = pygame.mouse.get_pos()
                self.surface_aux.blit(self.cursor, (cursor_x, cursor_y))


                # superponiendo pantalla aux
                self.screen.blit(self.surface_aux, (0,0))

                self.sum()

            # pantalla de victoria
            if self.crush_return == 'win':
                self.win.render()
                self.c = 0

            # actualizar
            pygame.display.flip()

            # delta time
            self.clock.tick(60)

 

if __name__ == "__main__":
    game = Game()
    game.run()
       

