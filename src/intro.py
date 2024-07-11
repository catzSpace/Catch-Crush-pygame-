import pygame
from pyvidplayer2 import Video


# animacion de introduccion con historia

class Intro:
    def __init__(self, surface, ancho, alto):

        self.ancho = ancho
        self.alto = alto
        self.surface = surface 
        self.vid = Video('assets/lore/intro.mp4')
        self.vid_run = 1


    def render(self):
        # esperar hasta que termine el video
        while self.vid.active:
            self.vid.draw(self.surface, (self.ancho / 10, 0), force_draw=False)
            pygame.display.update()
        self.vid_run = 0
                
    # opcion para que el juego empiece una vez que termina la cinemática
    def retorno(self):
        return self.vid_run


# pantalla de muerte
class Dead:
    def __init__(self, surface, alto, ancho):
        self.surface = surface
        self.alto = alto
        self.ancho = ancho
        self.image = []

    def load(self):
        self.load = pygame.image.load('assets/lore/rip.png')
        self.deadimg = pygame.transform.scale(self.load, (self.ancho, self.alto))
        self.image.append(self.deadimg)

    def render(self):
        self.surface.blit(self.image[0], (0,0))

    def run(self):
        self.render()



# pantalla de victoria
class Win:
    def __init__(self, surface, alto, ancho):
        self.ancho = ancho
        self.alto = alto
        self.surface = surface
        self.images = []

    def load(self):
        self.load = pygame.image.load('assets/lore/win.png')
        self.sprite = pygame.transform.scale(self.load, (self.ancho, self.alto))
        self.images.append(self.sprite)

    def render(self):
        self.surface.blit(self.images[0], (0,0))

    def run(self):
        self.render()

