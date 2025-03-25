import pygame
import random
from obstaculo import Obstaculo

def carregar_fase_1(tela):
    """
    Carrega e inicia a fase 1.
    """
    try:
        # Configuração do fundo
        fundo = pygame.image.load("recursos/imagens/background/fase_1/fundo_fase_1.png").convert()
        fundo = pygame.transform.scale(fundo, tela.get_size())
        tela.blit(fundo, (0, 0))
    except pygame.error:
        print("Erro ao carregar a imagem de fundo da fase 1.")
    
    try:
        # Música de fundo
        pygame.mixer.music.load("recursos/sons/fase_1.wav")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
    except pygame.error:
        print("Erro ao carregar a música de fundo da fase 1.")

def gerar_obstaculos_fase_1(grupo_obstaculos, velocidade):
    """
    Gera obstáculos aleatórios para a fase 1.
    """
    tipo = random.choice(["tronco", "galho"])  # Escolhe aleatoriamente entre os tipos de obstáculos
    
    # Configura posição inicial dependendo do tipo de obstáculo
    y_pos = 320 if tipo == "tronco" else random.randint(180, 220)  # Altura ajustada para galhos
    obstaculo = Obstaculo(velocidade=velocidade, tipo=tipo)
    
    # Posição inicial segura (fora da tela, lado direito)
    obstaculo.rect.x = 800
    obstaculo.rect.y = y_pos  # Define a altura segura do obstáculo
    
    grupo_obstaculos.add(obstaculo)
