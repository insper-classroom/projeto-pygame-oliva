import pygame
import webbrowser

class Menu:
    def __init__(self):
        self.rects = {}
        self.keys = ['Continuar', 'Configurações', 'Como Jogar', 'Sobre Nós']
        for i in range(4):
            self.rects[self.keys[i]] = pygame.Rect(430, 100 + 140*i, 420, 100)

    def interacoes(self, state):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                state['tela_jogo'] = 'main'
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for key, val in self.rects.items():
                    if val.collidepoint(pygame.mouse.get_pos()):
                        if key == 'Continuar':
                            state['tela_jogo'] = 'main'
                        elif key == 'Configurações':
                            state['tela_jogo'] = 'config'
                        elif key == 'Como Jogar':
                            pass
                        elif key == 'Sobre Nós':
                            webbrowser.open('https://henriquebrnetto.github.io/personal-website/index.html')
                            return True

        return True

    def desenha(self, window, asset):
        i = 0
        fonte = pygame.font.Font(pygame.font.get_default_font(), 18)
        for rect in self.rects.values():
            pygame.draw.rect(window, (80,80,80), rect)
            palavra = fonte.render(Menu().keys[i], True, (0, 0, 0))
            window.blit(palavra, (asset['tam_tela'][0]/2 - palavra.get_width()/2, 150 + 140*i))

            i+=1
        
        return