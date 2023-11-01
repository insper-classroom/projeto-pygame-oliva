import pygame
from telas.tela_menu import *
from const import nomes_config

class Config:
    def __init__(self):
        self.asset = {
            'tam_tela' : [1280, 720],
            'vsync' : True,
            'vol_musica' : 100,
        }

        self.buttons = [pygame.Rect(5*self.asset['tam_tela'][0]/6 - 30, self.asset['tam_tela'][1]/6, 30, 30), 
                        *[pygame.Rect(2*self.asset['tam_tela'][0]/3 - 120, i*self.asset['tam_tela'][1]/12 + 60 + self.asset['tam_tela'][1]/6, 240, 30) for i in range(len(self.asset.keys()))]]
    
    def interacoes(self, window, asset, state):
        buttons = dict(zip(self.asset.keys(), self.buttons[1:]))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                state['tela_jogo'] = 'main'
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.buttons[0].collidepoint(pygame.mouse.get_pos()):
                        asset['mapa'].desenha(window, asset, state)
                        state['tela_jogo'] = 'menu'
                for key, button in buttons.items():
                    if button.collidepoint(pygame.mouse.get_pos()):
                        print(key)
                        if key == 'tam_tela':
                            pass
                        if key == 'vsync':
                            asset[key] = False
                        if key == 'vol_musica':
                            if asset[key] >= 5:
                                asset[key] -= 5
                            else:
                                asset[key] = 100

        return True
    
    def desenha(self, window):
        rect = pygame.Rect(self.asset['tam_tela'][0]/6, self.asset['tam_tela'][1]/6, 4*self.asset['tam_tela'][0]/6, 4*self.asset['tam_tela'][1]/6)
        but = self.buttons[0]
        pygame.draw.rect(window, (0,0,0), rect)
        pygame.draw.rect(window, (255,0,0), but)

        palavra = pygame.font.Font(pygame.font.get_default_font(), 15).render('x', True, (255, 255, 255))
        window.blit(palavra, (but.x + but.width/2 - palavra.get_width()/2, but.y + but.height/2 - palavra.get_height()/2))

        buttons = self.buttons[1:]
        fonte = pygame.font.Font(pygame.font.get_default_font(), 14)
        for i in range(len(buttons)):
            pygame.draw.rect(window, (60,60,60), buttons[i]) #botões

            key = fonte.render(nomes_config[list(self.asset.keys())[i]], True, (255, 255, 255)) #nome da config
            window.blit(key, (self.asset['tam_tela'][0]/3 - 120, buttons[i].y + buttons[i].height/2 - key.get_height()/2)) #desenha nome da config

            val = fonte.render(str(list(self.asset.values())[i]), True, (255, 255, 255)) #valor da config
            window.blit(val, (buttons[i].x + buttons[i].width/2 - val.get_width()/2, buttons[i].y + buttons[i].height/2 - val.get_height()/2)) #desenha valor da config

            
            window.blit(fonte.render('>', True, (255, 255, 255)), (buttons[i].x + buttons[i].width - 20, buttons[i].y + buttons[i].height/2 - 7))
            window.blit(fonte.render('<', True, (255, 255, 255)), (buttons[i].x + 15, buttons[i].y + buttons[i].height/2 - 7))
        return