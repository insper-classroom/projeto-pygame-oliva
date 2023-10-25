import pygame
import os

def inicializa():
    """
    Inicializa todas as informações e objetos do jogo.
    """
    pygame.init()
    window = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption('Cassino')


    asset = {
        'def_font' : pygame.font.match_font('old english five'),
    }

    for img in os.listdir('./Cassino'):
        if img.endswith('.png'):
            asset[img[:-4]] = pygame.transform.scale(pygame.image.load(f'Cassino/{img}'), (60,60))
        elif img.endswith('.jpg'):
            asset[img[:-4]] = pygame.image.load(f'Cassino/{img}')
    
    asset['mapa'] = pygame.transform.scale(pygame.transform.rotate(asset['mapa'], 90), (1280,720))

    state = {
        'jogador' : [5,300],
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

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:
            state['vel'][0] += 120
        elif event.type == pygame.KEYUP and event.key == pygame.K_d:
            state['vel'][0] += -120
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_a:
            state['vel'][0] += -120
        elif event.type == pygame.KEYUP and event.key == pygame.K_a:
            state['vel'][0] += 120
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_w:
            state['vel'][1] += -120
        elif event.type == pygame.KEYUP and event.key == pygame.K_w:
            state['vel'][1] += 120
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            state['vel'][1] += 120
        elif event.type == pygame.KEYUP and event.key == pygame.K_s:
            state['vel'][1] += -120
    
    state['jogador'][0] = state['jogador'][0] + state['vel'][0] * dt
    state['jogador'][1] = state['jogador'][1] + state['vel'][1] * dt

    if state['jogador'][0] < 0 or state['jogador'][0] + asset['jogador'].get_size()[0] >= 1280:
        state['jogador'][0] = state['jogador'][0] - state['vel'][0] * dt

    if state['jogador'][1] < 0 or state['jogador'][1] + asset['jogador'].get_size()[0] >= 720:
        state['jogador'][1] = state['jogador'][1] - state['vel'][1] * dt

    return True

def desenha(window, asset, state):
    """
    Desenha todos os objetos e strings na tela.
    """
    window.fill((0,0,0))
    window.blit(asset['mapa'], (0,0))

    for i in range(3):
        window.blit(pygame.transform.scale(asset['blackjack_table'], (100,84)), (50 + 160*i, 570))
        window.blit(pygame.transform.scale(asset['slot_machine'], (80,80)), (1010, 140 + 80*i))
        window.blit(pygame.transform.scale(asset['slot_machine'], (80,80)), (1160, 140 + 80*i))
        window.blit(pygame.transform.scale(asset['roulette'], (100,100)), (815 + 160*i, 475 + 65*i))

    window.blit(pygame.transform.scale(asset['placa'], (250,85)), (970, 0))
    window.blit(pygame.transform.scale(asset['poker_table'], (290,150)), (370, 210))

    window.blit(asset['jogador'], (state['jogador']))

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