import pygame
import os
from telas.tela_main import Cassino
from telas.tela_menu import Menu
from telas.tela_como_jogar import ComoJogar
from telas.tela_config import Config
from minigames.blackjack import Blackjack
from minigames.roleta import Roleta
from player import Player

def inicializa():
    """
    Inicializa todas as informações e objetos do jogo.
    """

    pygame.init()

    asset = {
        **Config().asset,
        'def_font' : pygame.font.Font(pygame.font.get_default_font(), 15),
        'leg_font' : pygame.font.Font(pygame.font.get_default_font(), 11),
        'money_font' : pygame.font.Font(pygame.font.match_font('Abel'), 30),
        'old_font' : pygame.font.Font(pygame.font.match_font('Old English Five'), 45),
        'objs' : {},
        'personagens' : {},
    }

    asset['como_jogar'] = ComoJogar(asset)

    window = pygame.display.set_mode(tuple(asset['tam_tela']), vsync=asset['vsync'], flags=pygame.SCALED)
    pygame.display.set_caption('Cassino')

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

def atualiza_estado(window, asset, state):
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
    elif state['tela_jogo'] == 'config':
        return Config().interacoes(window, asset, state)
    elif state['tela_jogo'] == 'como_jogar':
        return asset['como_jogar'].interacoes(window, asset, state)
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
    roleta = Roleta(window)
    roleta_started = False
    while game:
        game = atualiza_estado(window, asset, state)
        if game == False:
            return
        if state['tela_jogo'] == 'main':
            asset['mapa'].desenha(window, asset, state)
            blackjack_started = False
            roleta_started = False
        elif state['tela_jogo'] ==  'menu':
            Menu().desenha(window, asset)
        elif state['tela_jogo'] == 'config':
                Config().desenha(window)
        elif state['tela_jogo'] == 'como_jogar':
                asset['como_jogar'].desenha(window)
        elif state['tela_jogo'] == 'blackjack':
            if not blackjack_started:
                blackjack = Blackjack(window)
                state['minigame'] = blackjack
                blackjack.start()
                blackjack_started = True
            blackjack.desenha()
            if not blackjack.isInMenu:
                blackjack.finishGame()
                if blackjack.resultGame == 'win':
                    state['dinheiro'] += 100
                elif blackjack.resultGame == 'lose':
                    state['dinheiro'] -= 100
                blackjack.resultGame = None
                blackjack.desenha(True)
        elif state['tela_jogo'] == 'roleta':
            if not roleta_started:
                roleta = Roleta(window)
                state['minigame'] = roleta
                roleta_started = True
            roleta.desenha()
            if roleta.resultMenu:
                if not roleta.giveMoney:
                    state['dinheiro'] += roleta.money
                    roleta.money = 0
                    roleta.giveMoney = True
        if state['dinheiro'] >= 0:
            window.blit(asset['money_font'].render(f'Balance: ${state["dinheiro"]}', True, (0, 0, 0)), (10,10))
        else:
            window.blit(asset['money_font'].render(f'Balance: ${state["dinheiro"]}', True, (255, 0, 0)), (10,10))
        pygame.display.update()

if __name__ == '__main__':
    game_loop(*inicializa())