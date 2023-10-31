import pygame
from telas.tela_menu import *

class Config:
    def __init__(self):
        self.asset = {
            'tam_tela' : [1280, 720],
            'vsync' : True,
            'vol_musica' : 100,
        }

        self.buttons = [pygame.Rect(5*self.asset['tam_tela'][0]/6 - 30, self.asset['tam_tela'][1]/6, 30, 30)]
    
    def interacoes(self, window, asset, state):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                state['tela_jogo'] = 'main'
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    if button.collidepoint(pygame.mouse.get_pos()):
                        asset['mapa'].desenha(window, asset, state)
                        state['tela_jogo'] = 'menu'

        return True
    
    def desenha(self, window):
        rect = pygame.Rect(self.asset['tam_tela'][0]/6, self.asset['tam_tela'][1]/6, 4*self.asset['tam_tela'][0]/6, 4*self.asset['tam_tela'][1]/6)
        x = self.buttons[0]
        pygame.draw.rect(window, (0,0,0), rect)
        pygame.draw.rect(window, (255,0,0), x)

        palavra = pygame.font.Font(pygame.font.get_default_font(), 15).render('x', True, (255, 255, 255))
        window.blit(palavra, (self.buttons[0].x + self.buttons[0].width/2 - palavra.get_width()/2, self.buttons[0].y + self.buttons[0].height/2 - palavra.get_height()/2))

        return