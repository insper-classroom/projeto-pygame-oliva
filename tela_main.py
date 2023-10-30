import pygame
from const import *

class Cassino():
    """Inicializa classe do mapa do Cassino"""
    def __init__(self, asset):
        self.mapa = pygame.transform.scale(pygame.image.load('images/mapa.jpg'), (1280,720))
        self.objs = {}

        #(top, bottom, left, right)
        self.paredes = [pygame.Rect(377, 215, 277, 1), pygame.Rect(377, 348, 277, 1), pygame.Rect(377, 215, 1, 133), pygame.Rect(654, 215, 1, 133), #poker
                        pygame.Rect(975, 80, 240, 1), pygame.Rect(975, 0, 1, 80), pygame.Rect(1215, 0, 1, 80)] #horse_race

        for key, img in asset['objs'].items():
            self.objs[key] = pygame.transform.scale(img, img_sizes[key])

        for i in range(3):
            self.paredes += [pygame.Rect(34 + 177*i, 589, 90, 1), #blackjack top
                             pygame.Rect(34 + 177*i, 636, 90, 1), #blackjack bottom
                             pygame.Rect(34 + 177*i, 589, 1, 47), #blackjack left
                             pygame.Rect(124 + 177*i, 589, 1, 47), #blackjack right
                             pygame.Rect(1021, 148 + 81*i, 59, 1), #slot_machine top
                             pygame.Rect(1021, 214 + 81*i, 59, 1), #slot_machine bottom
                             pygame.Rect(1021, 148 + 81*i, 1, 66), #slot_machine left
                             pygame.Rect(1080, 148 + 81*i, 1, 66), #slot_machine right
                             pygame.Rect(1171, 148 + 81*i, 59, 1), #slot_machine top
                             pygame.Rect(1171, 214 + 81*i, 59, 1), #slot_machine bottom
                             pygame.Rect(1171, 148 + 81*i, 1, 66), #slot_machine left
                             pygame.Rect(1230, 148 + 81*i, 1, 66), #slot_machine right
                             pygame.Rect(820 + 160*i, 480 + 65*i, 90, 1), #roleta top
                             pygame.Rect(820 + 160*i, 570 + 65*i, 90, 1), #roleta bottom
                             pygame.Rect(820 + 160*i, 480 + 65*i, 1, 90), #roleta left
                             pygame.Rect(910 + 160*i, 480 + 65*i, 1, 90) #roleta right
                             ]
    
    def rects(self):
        """Cria e pega Rect de todos os objetos no mapa"""
        pos = {}
        for i in range(3):
            try:
                pos['blackjack'] += [pygame.Rect(*(30 + 177*i, 570), *(100,84))]
                pos['slot_machine'] += [pygame.Rect(*(1010, 140 + 80*i), *(80,80))]
                pos['slot_machine'] += [pygame.Rect(*(1160, 140 + 80*i), *(80,80))]
                pos['roleta'] += [pygame.Rect(*(815 + 160*i, 475 + 65*i), *(100,100))]
            except KeyError:
                pos['blackjack'] = [pygame.Rect(*(30, 570), *(100,84))]
                pos['slot_machine'] = [pygame.Rect(*(1010, 140), *(80,80)), pygame.Rect(*(1160, 140), *(80,80))]
                pos['roleta'] = [pygame.Rect(*(815, 475), *(100,100))]
        
        pos['horse_race'] = [pygame.Rect(*(970, 0), *(250,85))]
        pos['poker'] = [pygame.Rect(*(370, 210), *(290,150))]

        return pos
    
    def interacoes(self, asset, state):
        """Checa interações entre o jogador e objetos enquanto estiver no mapa do cassino"""
        
        #Check interactions
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                state['tela_jogo'] = 'menu'
            elif state['aviso'] != None and event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                state['tela_jogo'] = state['aviso']
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
        
        #Move player
        asset['jogador'].pos[0] = asset['jogador'].pos[0] + state['vel'][0] * state['dt']
        asset['jogador'].pos[1] = asset['jogador'].pos[1] + state['vel'][1] * state['dt']

        #Check if player is outside bounds in x-axis
        if asset['jogador'].pos[0] < 0 or asset['jogador'].pos[0] + asset['jogador'].size[0] >= 1280:
            asset['jogador'].pos[0] = asset['jogador'].pos[0] - state['vel'][0] * state['dt']
        
        #Check if player is outside bounds in y-axis
        if asset['jogador'].pos[1] < 0 or asset['jogador'].pos[1] + asset['jogador'].size[1] >= 720:
            asset['jogador'].pos[1] = asset['jogador'].pos[1] - state['vel'][1] * state['dt']
        
        #Check collisions with walls around objects
        if asset['jogador'].transform().collidelist(self.paredes) != -1:
            asset['jogador'].pos[0] = asset['jogador'].pos[0] - state['vel'][0] * state['dt']
            asset['jogador'].pos[1] = asset['jogador'].pos[1] - state['vel'][1] * state['dt']

        #Check collisions with objects
        for key, objs in self.rects().items():
            for obj in objs:
                if asset['jogador'].transform().colliderect(obj):
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
                if key == 'horse_race':
                    pos = self.rects()['horse_race'][0]
                    window.blit(asset['old_font'].render('Horse Race', True, (0, 0, 0)), (pos.x + 45, pos.y + 27))
        
        for parede in self.paredes:
            pygame.draw.rect(window, (0,0,0), parede)
        window.blit(asset['jogador'].img, (state['jogador']))

        if state['aviso'] != None:
            pygame.draw.rect(window, (255,255,255), pygame.Rect(450, 630, 380, 90))
            window.blit(asset['def_font'].render(f'Você deseja jogar {state["aviso"]}?', True, (0, 0, 0)), (460,640))
            window.blit(asset['leg_font'].render(f'Pressione \"e\" para iniciar o jogo.', True, (0, 0, 0)), (460,700))
            
        return