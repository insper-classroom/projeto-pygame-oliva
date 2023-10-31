import pygame

class ComoJogar:
    def __init__(self, asset):
        self.tela = pygame.Rect(self.asset['tam_tela'][0]/6, self.asset['tam_tela'][1]/6, 4*self.asset['tam_tela'][0]/6, 4*self.asset['tam_tela'][1]/6)
        self.buttons = [pygame.Rect(self.tela.x + self.tela.width/5*i, self.tela.y, self.tela.width/5, self.tela.height/12) for i in range(5)]
    
    def interacoes(self):
        return
    
    def desenha(self, window):
        pygame.draw.rect(window, (0,0,0), self.tela)

        i = 0
        for b in self.buttons:
            pygame.draw.rect(window, (5 + 100*i,0,0), b)
            i += 1
        return