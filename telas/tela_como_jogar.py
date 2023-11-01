import pygame
import os
from const import explicacoes, traducao

class ComoJogar:
    def __init__(self, asset):
        self.textos = explicacoes
        self.tela = pygame.Rect(asset['tam_tela'][0]/6, asset['tam_tela'][1]/6, 4*asset['tam_tela'][0]/6, 4*asset['tam_tela'][1]/6)
        self.fechar = pygame.Rect(self.tela.x + self.tela.width - 40, self.tela.y, 40, 40)

        tam = self.fechar.x - self.tela.x
        self.buttons = {}
        i = 0
        for k in self.textos.keys():
            self.buttons[k] = pygame.Rect(self.tela.x + tam/len(self.textos.keys())*i, self.tela.y, tam/len(self.textos.keys()) - 1, 40)
            i += 1

        self.page = 'blackjack'

    def interacoes(self, window, asset, state):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.fechar.collidepoint(pygame.mouse.get_pos()):
                    asset['mapa'].desenha(window, asset, state)
                    state['tela_jogo'] = 'menu'
                for k, button in self.buttons.items():
                    if button.collidepoint(pygame.mouse.get_pos()):
                        self.page = k
            
        return True
    
    def divide_texto(self, key, fonte):
        words = self.textos[key].split(' ')
        space = fonte.size(' ')[0]
        max_width = self.tela.width
        linhas = []
        linha = []
        tam_linha = 0

        for i in range(len(words)):
            if tam_linha > max_width or i == len(words)-1:
                if i == len(words)-1:
                    tam_linha += fonte.render(words[i], True, (255, 255, 255)).get_width() + space
                    linha += [words[i]]
                linhas += [' '.join(linha)]
                linha = []
                tam_linha = 0
                continue
            tam_linha += fonte.render(words[i], True, (255, 255, 255)).get_width() + space
            linha += [words[i]]

        return linhas

    def desenha(self, window):
        fonte_tit = pygame.font.Font(pygame.font.get_default_font(), 20)
        fonte_txt = pygame.font.Font(pygame.font.get_default_font(), 12)

        pygame.draw.rect(window, (0,0,0), self.tela)

        i = 0
        for b in self.buttons.values():
            pygame.draw.rect(window, (100,0,0), b)
            i += 1
        
        pygame.draw.rect(window, (255,255,255), self.fechar)

        palavra = fonte_tit.render(traducao[self.page], True, (255, 255, 255))
        window.blit(palavra, (self.tela.x + 20, self.tela.y + 50))

        j = 0
        for linha in self.divide_texto(self.page, fonte_txt):
            window.blit(fonte_txt.render(linha, True, (255, 255, 255)), (self.tela.x + 20, self.tela.y + 90 + 18*j))
            j += 1
        return
    