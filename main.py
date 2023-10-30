import pygame
import os
from tela_main import *
from minigames.blackjack import *
from tela_menu import *
from player import Player

def inicializa():
    """
    Inicializa todas as informações e objetos do jogo.
    """
    pygame.init()
    window = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption('Cassino')

    asset = {
        'def_font' : pygame.font.Font(pygame.font.get_default_font(), 15),
        'leg_font' : pygame.font.Font(pygame.font.get_default_font(), 11),
        'money_font' : pygame.font.Font(pygame.font.match_font('Abel'), 30),
        'old_font' : pygame.font.Font(pygame.font.match_font('Old English Five'), 45),
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
        'dt' : 0,
        'minigame' : None,
    }

    return window, asset, state

def atualiza_estado(asset, state):
    """
    Atualiza estado do jogo, e checa ações e interações.
    """
    t_atual = pygame.time.get_ticks()
    state['dt'] = (t_atual - state['last_updated'])/1000
    state['last_updated'] = t_atual

    if state['tela_jogo'] == 'main':
        return asset['mapa'].interacoes(asset, state)
    elif state['tela_jogo'] == 'menu':
        return Menu().interacoes(state)
    elif state['tela_jogo'] == 'blackjack':
        if not state['minigame'].interacoes():
            state['tela_jogo'] = 'main'
    elif state['tela_jogo'] == 'roleta':
        if not state['minigame'].interacoes():
            state['tela_jogo'] = 'main'
        
        return True

def game_loop(window, asset, state):
    """
    Loop principal do jogo, onde roda todas as outras funções necessárias.
    """
    game = True
    blackjack = Blackjack(window)
    blackjack_started = False
    while game:
        game = atualiza_estado(asset, state)
        if game == False:
            return
        if state['tela_jogo'] == 'main':
            asset['mapa'].desenha(window, asset, state)
        elif state['tela_jogo'] ==  'menu':
            Menu().desenha(window)
        elif state['tela_jogo'] == 'blackjack':
            if not blackjack_started:
                blackjack = Blackjack(window)
                state['minigame'] = blackjack
                blackjack.start()
                blackjack_started = True
            blackjack.desenha()
            if not blackjack.isInMenu:
                blackjack.finishGame()
                blackjack.desenha(True)
        if state['dinheiro'] >= 0:
            window.blit(asset['money_font'].render(f'Balance: ${state["dinheiro"]}', True, (0, 0, 0)), (10,10))
        else:
            window.blit(asset['money_font'].render(f'Balance: ${state["dinheiro"]}', True, (255, 0, 0)), (10,10))
        pygame.display.update()

if __name__ == '__main__':
    game_loop(*inicializa())