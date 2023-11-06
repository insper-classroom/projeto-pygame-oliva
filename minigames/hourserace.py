import pygame
from random import randint

class Horse():
    def __init__(self, window, x, y, speed, index):
        self.window = window
        self.hourse = pygame.transform.scale(pygame.image.load('images/horse.png'), (60,60))
        self.x = x
        self.y = y
        self.speed = speed
        self.index = index

    def desenha(self):
        self.window.blit(self.hourse, (self.x, self.y))

    def movimenta(self, delta):
        self.x += self.speed * delta

class HorseRace():
    def __init__(self, window):
        self.isInBetMenu = False
        self.window = window
        self.horses = [Horse(self.window, 100, i * 100, randint(100, 120), i) for i in range(1, 5)]
        self.horseWinner = None
        self.lastTick = 0
        self.messageWinner = ''
        self.bet = 1 
        self.font = pygame.font.Font(pygame.font.get_default_font(), 20)

    def desenha(self):
        window.fill((0,0,0))
        tick = pygame.time.get_ticks()
        delta = (tick - self.lastTick) / 1000
        self.lastTick = tick
        if not self.isInBetMenu:
            text_surface = self.font.render(self.messageWinner, True, (255, 255, 255))
            x =  (1280 // 2) - (text_surface.get_width() // 2)
            y = (720 // 2) - (text_surface.get_height() // 2)
            self.window.blit(text_surface, (x, y))
            for horse in self.horses:
                horse.desenha()
                horse.movimenta(delta)
                if horse.x >= 1280 - 60:
                    if self.messageWinner == '':
                        self.messageWinner = f'O cavalo {horse.index} ganhou! Você ganhou R$ 100,00' if horse.index == self.bet else f'O cavalo {horse.index} ganhou! Você perdeu R$ 100,00'
                    horse.x = 1280 - 60
            if self.horses[0].x >= 600 and self.horseWinner == None:
                self.horseWinner = randint(0, 4)
                self.horses[self.horseWinner - 1].speed += (120 - self.horses[self.horseWinner - 1].speed) + 30

    def interacoes(self):
        """
        Faz todas as interações do jogo
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True

if __name__ == '__main__':
    playing = True
    pygame.init()
    window = pygame.display.set_mode((1280, 720), vsync=True, flags=pygame.SCALED)
    horseRace = HorseRace(window)

    while playing:
        if not horseRace.interacoes():
            playing = False
            break

        horseRace.desenha()

        pygame.display.update()
        
    pygame.quit()