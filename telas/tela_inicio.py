import pygame
from itertools import cycle

class Inicio:
    def __init__(self, window, asset):
        self.circles = [pygame.draw.circle(window, (0,0,0), (asset['tam_tela'][0]/2 + 15, asset['tam_tela'][1]/2 - 150), 15)]
        self.musica = 'musica/jazz_fundo.mp3'
        self.mus_win = pygame.mixer.Sound('musica/prize_win.wav')
        self.img = pygame.transform.scale(pygame.image.load('images/logo.png'), asset['tam_tela'])
        self.prize_win = False
    
    def interacoes(self, asset, state):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                state['tela_jogo'] = 'main'
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for circ in self.circles:
                    if circ.collidepoint(pygame.mouse.get_pos()):
                        pygame.mixer.music.fadeout(2)
                        self.mus_win.play()
                        asset['mapa'].time = pygame.time.get_ticks()
                        self.prize_win = True
                        state['dinheiro'] *= 2
                        state['tela_jogo'] = 'main'
        
        return True

    def desenha(self, window, asset):
        for circ in self.circles:
            circ
        window.blit(self.img, [0,0])
  
        txt = asset['def_font'].render('Aperte qualquer tecla para iniciar o jogo.', True, (255,255,255))
        window.blit(txt, (asset['tam_tela'][0]/2 - txt.get_width()/2, 690))
        return