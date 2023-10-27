# Importa as bibliotecas necessárias para o jogo
import pygame
import os
import random

# Define a classe Blackjack
class Blackjack():
    def __init__(self, window):
        """Inicializa a classe com a janela do jogo e variáveis de estado"""
        self.window = window
        self.userCards = []
        self.dealerCards = []
        self.deck = []
        self.isInMenu = True
        self.font = pygame.font.Font(pygame.font.get_default_font(), 20)
        self.pedir = pygame.rect.Rect(510, 650, 100, 50)
        self.parar = pygame.rect.Rect(660, 650, 100, 50)
        self.userPoints = 0
        self.dealerPoints = 0
        self.resultMessage = ''
        self.reset = False
        self.resetButton = pygame.rect.Rect(510, 650, 100, 50)
        self.finishButton = pygame.rect.Rect(660, 650, 100, 50)

    def start(self):
        """Inicia o jogo criando o baralho e distribuindo cartas para o jogador e o dealer"""
        self.deck = self.createDeck()
        self.userCards = []
        self.dealerCards = []
        for _ in range(2):
            card = random.randint(0, len(self.deck) - 1)
            self.userCards.append(self.deck[card])
            self.deck.pop(card)
        for _ in range(2):
            card = random.randint(0, len(self.deck) - 1)
            self.dealerCards.append(self.deck[card])
            self.deck.pop(card)

    def createDeck(self):
        """Cria o baralho com cartas de imagem"""
        deck = []
        for folderName in os.listdir('./images/cards'):
            if folderName == 'Backs':
                continue
            for i in range(1, 14):
                deck.append(f'{folderName}/{i}.png')
        return deck

    def desenha(self, status=False):
        """Desenha a tela do jogo"""
        self.window.fill((2, 85, 0))
        userCardsWidth = len(self.userCards) * 150
        dealerCardsWidth = len(self.dealerCards) * 150
        startXUser = (1280 - userCardsWidth) // 2
        startXDealer = (1280 - dealerCardsWidth) // 2
        
        for index, card in enumerate(self.userCards):
            self.window.blit(pygame.transform.scale(pygame.image.load(f'./images/cards/{card}'), (125, 181)), (startXUser + (index * 150), 420))
        
        for index, card in enumerate(self.dealerCards):
            if not status:
                if index == 0:
                    self.window.blit(pygame.transform.scale(pygame.image.load(f'./images/cards/{card}'), (125, 181)), (startXDealer + (index * 150), 100))
                else:
                    self.window.blit(pygame.transform.scale(pygame.image.load('images/cards/Backs/back.png'), (125, 181)), (startXDealer + (index * 150), 100))
            else:
                self.window.blit(pygame.transform.scale(pygame.image.load(f'./images/cards/{card}'), (125, 181)), (startXDealer + (index * 150), 100))
        
        if self.isInMenu:
            self.drawButtons()
        
        if self.reset:
            self.drawText(self.resultMessage, 570, 350, self.font, (255, 255, 255))
            pygame.draw.rect(self.window, (0, 128, 0), self.resetButton)
            pygame.draw.rect(self.window, (255, 0, 0), self.finishButton)
            self.drawText("Reiniciar", 515, 665, self.font, (255, 255, 255))
            self.drawText("Fechar", 675, 665, self.font, (255, 255, 255))

    def drawText(self, text, x, y, font, color):
        """Desenha um texto na tela"""
        text_surface = font.render(text, True, color)
        self.window.blit(text_surface, (x, y))

    def drawButtons(self):
        """Desenha os botões Pedir e Parar"""
        pygame.draw.rect(self.window, (0, 128, 0), self.pedir)  # Botão Pedir
        pygame.draw.rect(self.window, (255, 0, 0), self.parar)  # Botão Parar
        self.drawText("Pedir", 530, 665, self.font, (255, 255, 255))
        self.drawText("Parar", 680, 665, self.font, (255, 255, 255))

    def getCardValue(self, card):
        """Obtém o valor numérico da carta"""
        value = card.split('/')[1].split('.')[0]
        if value.isnumeric():
            if int(value) > 10:
                return 10
            return int(value)

    def addCard(self, user=True):
        """Adiciona uma carta ao jogador ou dealer"""
        if user:
            # self.userCards.append(random.choice(self.deck))
            card1 = random.randint(0, len(self.deck) - 1)
            self.userCards.append(self.deck[card1])
            self.deck.pop(card1)
            self.userPoints = sum(map(self.getCardValue, self.userCards))
            if self.userPoints > 21:
                self.isInMenu = False
        else:
            self.dealerCards.append(random.choice(self.deck))

    def finishGame(self):
        """Finaliza o jogo, calcula a pontuação e determina o resultado"""
        self.dealerPoints = sum(map(self.getCardValue, self.dealerCards))
        self.userPoints = sum(map(self.getCardValue, self.userCards))
        while self.dealerPoints < 17:
            self.addCard(False)
            self.dealerPoints = sum(map(self.getCardValue, self.dealerCards))
        if self.dealerPoints > 21 and self.userPoints <= 21:
            self.resultMessage = 'Você ganhou!'
        elif (self.userPoints <= 21) and (21 - self.userPoints) < (21 - self.dealerPoints):
            self.resultMessage = 'Você ganhou!'
        elif self.userPoints == self.dealerPoints and self.userPoints <= 21:
            self.resultMessage = 'Empate!'
        else:
            self.resultMessage = 'Você perdeu!'
        self.reset = True

    def resetGame(self):
        """Reinicia o jogo"""
        self.userCards = []
        self.dealerCards = []
        self.deck = []
        self.isInMenu = True
        self.userPoints = 0
        self.dealerPoints = 0
        self.resultMessage = ''
        self.reset = False
        self.start()

if __name__ == '__main__':
    pygame.init()
    window = pygame.display.set_mode((1280,720))
    pygame.display.set_caption('Blackjack')
    blackjack = Blackjack(window)
    blackjack.start()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if blackjack.isInMenu:
                    if blackjack.pedir.collidepoint(event.pos):
                        blackjack.addCard()
                    elif blackjack.parar.collidepoint(event.pos):
                        blackjack.isInMenu = False
                elif blackjack.reset:
                    if blackjack.resetButton.collidepoint(event.pos):
                        blackjack.resetGame()
                    elif blackjack.finishButton.collidepoint(event.pos):
                        running = False
        blackjack.desenha()
        if not blackjack.isInMenu:
            blackjack.finishGame()
            blackjack.desenha(True)
        pygame.display.update()
    pygame.quit()