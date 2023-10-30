import pygame
import os
import random
import math

class Zero():
    def __init__(self, x, y, value, window):
        self.x = x
        self.y = y
        self.value = value
        self.rect = pygame.rect.Rect(x, y, 36, 116)
        self.window = window
        
        self.font = pygame.font.Font(pygame.font.get_default_font(), 16)
    
    def desenha(self, isBlack):
        pygame.draw.rect(window, (0, 255, 0), self.rect)
        self.drawText(str(self.value), self.x + (18 - 6), self.y + (58 - 6), self.font, (0, 0, 0))

    def drawText(self, text, x, y, font, color):
        text_surface = font.render(text, True, color)
        self.window.blit(text_surface, (x, y))

class Column():
    def __init__(self, x, y, text, value, window):
        self.x = x
        self.y = y
        self.value = value
        self.rect = pygame.rect.Rect(x, y, 72, 36)
        self.window = window
        self.text = text
        self.font = pygame.font.Font(pygame.font.get_default_font(), 12)
    
    def desenha(self, isBlack):
        pygame.draw.rect(window, (0, 0, 0), self.rect)
        self.drawText(str(self.text), self.x + (36 - 12), self.y + (18 - 6), self.font, (255, 255, 255))

    def drawText(self, text, x, y, font, color):
        text_surface = font.render(text, True, color)
        self.window.blit(text_surface, (x, y))

class Dozens():
    def __init__(self, x, y, text, value, window):
        self.x = x
        self.y = y
        self.value = value
        self.rect = pygame.rect.Rect(x, y, 147, 36)
        self.window = window
        self.text = text
        self.font = pygame.font.Font(pygame.font.get_default_font(), 14)
    
    def desenha(self, isBlack):
        pygame.draw.rect(window, (0, 0, 0), self.rect)
        self.drawText(str(self.text), self.x + ((147 // 2) - 12 - (len(self.text))), self.y + (18 - 6), self.font, (255, 255, 255))

    def drawText(self, text, x, y, font, color):
        text_surface = font.render(text, True, color)
        self.window.blit(text_surface, (x, y))
class Buttons():
    def __init__(self, x, y, value, window):
        self.x = x
        self.y = y
        self.value = value
        self.rect = pygame.rect.Rect(x, y, 36, 36)
        self.window = window
        self.font = pygame.font.Font(pygame.font.get_default_font(), 12)
    
    def desenha(self, isBlack):
        if isBlack:
            pygame.draw.rect(window, (0, 0, 0), self.rect)
        else:
            pygame.draw.rect(window, (255, 0, 0), self.rect)
        self.drawText(str(self.value), self.x + (18 - 6), self.y + (18 - 6), self.font, (255, 255, 255))

    def drawText(self, text, x, y, font, color):
        text_surface = font.render(text, True, color)
        self.window.blit(text_surface, (x, y))

class Roleta:
    def __init__(self, window):
        self.window = window
        self.originalImage = pygame.transform.scale(pygame.image.load(os.path.join('images', 'objs', 'roleta.png')), (400, 400))
        self.roleta = pygame.transform.scale(pygame.image.load(os.path.join('images', 'objs', 'roleta.png')), (400, 400))
        self.roletaAngle = 0
        self.ballPos = [640, 250]
        self.columns = [[1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34], [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35], [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36]]
        self.dozens = [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], [13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24], [25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36]]
        self.roulleteOrder = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26]
        self.blackNumbers = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
        self.redNumbers = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
        self.isPlaying = True
        self.bets = []
        self.lastUptaded = 0
        self.actualAngle = 0
        self.expectedAngle = 1440
        self.sortedNumber = 0
        self.sorted = False
        self.radio = 150
        self.betsButtons = [
            [Zero(387, 510, 0, self.window)],
            [Buttons(425 + (i * 37), 510, self.columns[2][i], self.window) for i in range(12)],
            [Buttons(425 + (i * 37), 550, self.columns[1][i], self.window) for i in range(12)],
            [Buttons(425 + (i * 37), 590, self.columns[0][i], self.window) for i in range(12)],
            [Column(869, 510, '2 to 1', 'coluna3', self.window), Column(869, 550, '2 to 1', 'coluna2', self.window), Column(869, 590, '2 to 1', 'coluna1', self.window)],
            [Dozens(425, 630, '1 to 12', 'duzia1', self.window), Dozens(573, 630, '13 to 24', 'duizia2', self.window), Dozens(721, 630, '25 to 36', 'duzia3', self.window)],
        ]

    def desenha(self):
        self.window.fill((2, 85, 0))

        roleta_rect = self.roleta.get_rect(center=(640, 250))
        self.window.blit(self.roleta, roleta_rect)
        time = pygame.time.get_ticks()
        if not self.isPlaying:
            if (time - self.lastUptaded) / 1000 >= 0.01:
                self.lastUptaded = time
                self.roletaAngle += 1
                if self.roletaAngle >= 360:
                    self.roletaAngle = 0
                self.roleta = pygame.transform.rotate(self.originalImage, self.roletaAngle)
            self.drawButtons()
            for number in self.bets:
                for col in self.betsButtons:
                    for button in col:
                        if button.value == number:
                            pygame.draw.circle(self.window, (255, 255, 255), (button.x + (button.rect[2] // 2), button.y + (button.rect[3] // 2)), 7)
        else:
            if not self.sorted:
                self.sorted = True
                index = random.randint(0, len(self.roulleteOrder) - 1)
                self.sortedNumber = self.roulleteOrder[index]
                print(self.sortedNumber)
                if index != 0:
                    self.expectedAngle += (index / 37) * 360
            self.roleta = self.originalImage
            if (time - self.lastUptaded) / 1000 >= 0.001:
                self.lastUptaded = time
                self.actualAngle += 5
                if self.actualAngle >= self.expectedAngle:
                    self.actualAngle = self.expectedAngle
                    if self.radio > 105:
                        self.radio -= 1
                self.ballPos[0] = 640 + math.sin(math.radians(self.actualAngle)) * self.radio
                self.ballPos[1] = 250 - math.cos(math.radians(self.actualAngle)) * self.radio
                
        pygame.draw.circle(self.window, (255, 255, 255), self.ballPos, 7)
    def drawButtons(self):
        for col in self.betsButtons:
            for button in col:
                button.desenha(True if button.value in self.blackNumbers else False)

    def interacoes(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not self.isPlaying:
                    for col in self.betsButtons:
                        for button in col:
                            if button.rect.collidepoint(event.pos):
                                if button.value not in self.bets:
                                    self.bets.append(button.value)
                                else:
                                    self.bets.remove(button.value)
                                return True
        return True


if __name__ == '__main__':
    playing = True
    pygame.init()
    window = pygame.display.set_mode((1280, 720), vsync=True, flags=pygame.SCALED)
    roleta = Roleta(window)

    while playing:
        if not roleta.interacoes():
            playing = False
            break

        roleta.desenha()

        pygame.display.update()
        
    pygame.quit()