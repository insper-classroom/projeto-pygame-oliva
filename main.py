import pygame
import os
from tela_main import *
from player import Player

def inicializa():
    """
    Inicializa todas as informações e objetos do jogo.
    """
    pygame.init()
    window = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption('Cassino')


    asset = {
        'objs' : {},
        'personagens' : {},
    }

    for img in os.listdir('images/objs'):
        asset['objs'][img[:-4]] = pygame.image.load(f'images/objs/{img}')
    
    asset['mapa'] = Cassino(asset)

    for img in os.listdir('images/personagens'):
        if img.startswith('jogador'):
            asset[img[:-4]] = Player(pygame.image.load(f'images/personagens/{img}'), [5, 300], (60,60))
        else:
            asset['personagens'][img[:-4]] = pygame.transform.scale(pygame.image.load(f'images/personagens/{img}'), (60,60))

    state = {
        'tela_jogo' : 'main',
        'aviso' : None,
        'jogador' : asset['jogador'].pos,
        'vel' : [0,0],
        'last_updated' : 0,
        'dinheiro' : 2000, 
    }

    return window, asset, state

def atualiza_estado(asset, state):
    """
    Atualiza estado do jogo, e checa ações e interações.
    """

    t_atual = pygame.time.get_ticks()
    dt = (t_atual - state['last_updated'])/1000
    state['last_updated'] = t_atual

    if state['tela_jogo'] == 'main':
        for event in pygame.event.get():
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
        
        asset['jogador'].pos[0] = asset['jogador'].pos[0] + state['vel'][0] * dt
        asset['jogador'].pos[1] = asset['jogador'].pos[1] + state['vel'][1] * dt

        #Check if player is outside bounds in x-axis
        if asset['jogador'].pos[0] < 0 or asset['jogador'].pos[0] + asset['jogador'].size[0] >= 1280:
            asset['jogador'].pos[0] = asset['jogador'].pos[0] - state['vel'][0] * dt
        
        #Check if player is outside bounds in y-axis
        if asset['jogador'].pos[1] < 0 or asset['jogador'].pos[1] + asset['jogador'].size[1] >= 720:
            asset['jogador'].pos[1] = asset['jogador'].pos[1] - state['vel'][1] * dt

        for key, objs in asset['mapa'].rects().items():
            for obj in objs:
                if obj.colliderect(asset['jogador'].transform()):
                    state['aviso'] = key
                    return True
                else:
                    state['aviso'] = None
    else:
        print('entrou')

    return True

def desenha(window, asset, state):
    """
    Desenha todos os objetos e strings na tela.
    """
    window.fill((0,0,0))
    if state['tela_jogo'] == 'main':
        asset['mapa'].desenha(window)

    window.blit(asset['jogador'].img, (state['jogador']))

    if state['aviso'] != None:
        pygame.draw.rect(window, (255,255,255), pygame.Rect(10, 10, 100, 60))

    pygame.display.update()
    return

def game_loop(window, asset, state):
    """
    Loop principal do jogo, onde roda todas as outras funções necessárias.
    """
    game = True
    while game:
        game = atualiza_estado(asset, state)
        if game == False:
            return
        desenha(window, asset, state)


if __name__ == '__main__':
    game_loop(*inicializa())