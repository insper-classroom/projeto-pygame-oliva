import pygame
from const import *

class Cassino():
    def __init__(self, asset):
        self.mapa = pygame.transform.scale(pygame.image.load('images/mapa.jpg'), (1280,720))
        self.objs = {}

        for key, img in asset['objs'].items():
            self.objs[key] = pygame.transform.scale(img, img_sizes[key])
    
    def rects(self):
        pos = {}
        for i in range(3):
            try:
                pos['blackjack'] += [pygame.Rect(*(50 + 160*i, 570), *(100,84))]
                pos['slot_machine'] += [pygame.Rect(*(1010, 140 + 80*i), *(80,80))]
                pos['slot_machine'] += [pygame.Rect(*(1160, 140 + 80*i), *(80,80))]
                pos['roulette'] += [pygame.Rect(*(815 + 160*i, 475 + 65*i), *(100,100))]
            except KeyError:
                pos['blackjack'] = [pygame.Rect(*(50 + 160*i, 570), *(100,84))]
                pos['slot_machine'] = [pygame.Rect(*(1010, 140 + 80*i), *(80,80))]
                pos['slot_machine'] += [pygame.Rect(*(1160, 140 + 80*i), *(80,80))]
                pos['roulette'] = [pygame.Rect(*(815 + 160*i, 475 + 65*i), *(100,100))]
        
        pos['horse_race'] = [pygame.Rect(*(970, 0), *(250,85))]
        pos['poker'] = [pygame.Rect(*(370, 210), *(290,150))]

        return pos
    
    def desenha(self, window):
        window.blit(self.mapa, (0,0))
        for key, pos in self.rects().items():
            for p in pos:
                window.blit(self.objs[key], p.topleft)
                #if key == 'horse_race':
                    #window.blit(pygame.font.Font(pygame.font.match_font('old english five'), 60).render('Horse Race', True, (0, 0, 0)), (p.left + 40, p.top + 30))

    
