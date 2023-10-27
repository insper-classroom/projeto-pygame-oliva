import pygame
from const import *

class Cassino():
    """Inicializa classe do mapa do Cassino"""
    def __init__(self, asset):
        self.mapa = pygame.transform.scale(pygame.image.load('images/mapa.jpg'), (1280,720))
        self.objs = {}

        for key, img in asset['objs'].items():
            self.objs[key] = pygame.transform.scale(img, img_sizes[key])
    
    def rects(self):
        """Cria e pega Rect de todos os objetos no mapa"""
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
    
    def interacoes(self, asset, state):
        for event in pygame.event.get():
            if state['aviso'] != None and event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                state['tela_jogo'] = state['aviso']
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                state['vel'][0] += 150
            elif event.type == pygame.KEYUP and event.key == pygame.K_d:
                state['vel'][0] += -150
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                state['vel'][0] += -150
            elif event.type == pygame.KEYUP and event.key == pygame.K_a:
                state['vel'][0] += 150
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                state['vel'][1] += -150
            elif event.type == pygame.KEYUP and event.key == pygame.K_w:
                state['vel'][1] += 150
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                state['vel'][1] += 150
            elif event.type == pygame.KEYUP and event.key == pygame.K_s:
                state['vel'][1] += -150
        
        asset['jogador'].pos[0] = asset['jogador'].pos[0] + state['vel'][0] * state['dt']
        asset['jogador'].pos[1] = asset['jogador'].pos[1] + state['vel'][1] * state['dt']

        #Check if player is outside bounds in x-axis
        if asset['jogador'].pos[0] < 0 or asset['jogador'].pos[0] + asset['jogador'].size[0] >= 1280:
            asset['jogador'].pos[0] = asset['jogador'].pos[0] - state['vel'][0] * state['dt']
        
        #Check if player is outside bounds in y-axis
        if asset['jogador'].pos[1] < 0 or asset['jogador'].pos[1] + asset['jogador'].size[1] >= 720:
            asset['jogador'].pos[1] = asset['jogador'].pos[1] - state['vel'][1] * state['dt']

        for key, objs in asset['mapa'].rects().items():
            for obj in objs:
                if obj.colliderect(asset['jogador'].transform()):
                    state['aviso'] = key
                    return True
                else:
                    state['aviso'] = None
        return True
    
    def desenha(self, window, asset, state):
        """Desenha mapa e objetos"""
        window.blit(self.mapa, (0,0))
        for key, pos in self.rects().items():
            for p in pos:
                window.blit(self.objs[key], p.topleft)
        window.blit(asset['jogador'].img, (state['jogador']))

        if state['aviso'] != None:
            pygame.draw.rect(window, (255,255,255), pygame.Rect(520, 600, 240, 120))
            
        return