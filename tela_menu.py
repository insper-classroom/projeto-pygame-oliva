import pygame

class Menu:
    def __init__(self):
        self.rects = [pygame.Rect(415, 100 + 140*i, 450, 100) for i in range(4)]

    def interacoes(self, state):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                state['tela_jogo'] = 'main'
        
        return True

    def desenha(self, window):
        for rect in self.rects:
            pygame.draw.rect(window, (60,60,60), rect)
        
        return