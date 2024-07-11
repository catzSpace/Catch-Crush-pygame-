import pygame


# TODO
class Obj:
    def __init__(self, alto, ancho, surface):
        self.ancho = ancho
        self.alto = alto
        self.surface = surface

        # otros
        self.other = []
        self.other_col = []
        self.other_pos = [
            (ancho / 5.2, alto / 3), # botella y copa
            (ancho / 20, alto / 1.16), # planta
            (ancho / 2, alto / 10), # reloj
            (ancho / 7, alto / 3), # cofre
            (ancho / 7, alto / 2) # botella roja
        ]

        # mesas
        self.mesas_col = []
        self.pos = [
            # primera fila
            (ancho / 20, alto / 3), 
            (ancho / 20, alto / 1.5),
            (ancho / 20, alto / 1.3),

            # segunda fila
            (ancho / 2.4, alto / 2), (ancho / 2, alto / 2), 
            (ancho / 2.4, alto / 1.5), (ancho / 2, alto / 1.5),
            (ancho / 2.4, alto / 1.2), (ancho / 2, alto / 1.2),

            # tercera fila
            (ancho / 1.5, alto / 2), (ancho / 1.33, alto / 2),
            (ancho / 1.5, alto / 1.5), (ancho / 1.33, alto / 1.5),
            (ancho / 1.5, alto / 1.2), (ancho / 1.33, alto / 1.2),
            (ancho / 2.3, alto / 4)
        ]

    def load_mesas(self):
        self.load = pygame.image.load(f'assets/character/map/mesa.png')
        self.sprite = pygame.transform.scale(self.load, ((self.ancho / 12), (self.ancho / 24)))
        self.other.append(self.sprite)

        self.m_p = pygame.image.load(f'assets/character/map/mesa_1.png')
        self.spm = pygame.transform.scale(self.m_p, ((self.ancho / 12), (self.ancho / 24)))
        self.other.append(self.spm)
        


    def load_obj_cuad(self):
        for i in range(0,5):
            self.load = pygame.image.load(f'assets/character/map/{i}.png')
            self.sprite = pygame.transform.scale(self.load, ((self.alto / 14), (self.alto / 14)))
            self.other.append(self.sprite)


    def col(self):
        c = 2
        c2 = 0
        for pos in self.pos:
            if not c2 >= 15:
                rect = self.other[0].get_rect(topleft = pos)
                self.mesas_col.append(rect)
                c2 += 1

            rect = self.other[1].get_rect(topleft = self.pos[15])
            self.mesas_col.append(rect)

        for pos in self.other_pos:
            rect_o = self.other[c].get_rect(topleft = pos)
            c += 1


    def return_col(self):
        return self.mesas_col


    def render(self):
        c = 2
        c2 = 0
        

        for pos in self.pos:
            if not c2 >= 15:
                self.surface.blit(self.other[0], (pos))
                c2 += 1

        self.surface.blit(self.other[1], self.pos[15])
            

        for pos in self.other_pos:
            self.surface.blit(self.other[c], (pos))
            c += 1


