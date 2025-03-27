import pygame
import random
from obstaculo import Obstaculo

def carregar_fase_1(tela: pygame.Surface) -> None:
    """
    Carrega e inicia a fase 1.

    Args:
        tela (pygame.Surface): Superfície onde o fundo será carregado.
    """
    try:
        # Configuração do fundo
        fundo = pygame.image.load("recursos/imagens/background/fase_1/fundo_fase_1.png").convert()
        fundo = pygame.transform.scale(fundo, tela.get_size())
        tela.blit(fundo, (0, 0))
    except pygame.error:
        print("[ERRO] Não foi possível carregar a imagem de fundo da fase 1.")
    
    try:
        # Música de fundo
        pygame.mixer.music.load("recursos/sons/fase_1.wav")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
    except pygame.error:
        print("[ERRO] Não foi possível carregar a música de fundo da fase 1.")

def gerar_obstaculos_fase_1(grupo_obstaculos: pygame.sprite.Group, velocidade: int) -> None:
    """
    Gera obstáculos aleatórios para a fase 1.

    Args:
        grupo_obstaculos (pygame.sprite.Group): Grupo de sprites para adicionar os obstáculos.
        velocidade (int): Velocidade horizontal dos obstáculos.
    """
    tipo = random.choice(["tronco", "galho"])  # Escolhe aleatoriamente entre os tipos de obstáculos
    
    # Configura posição inicial dependendo do tipo de obstáculo
    if tipo == "tronco":
        y_pos = 320  # Posição fixa para tronco
    else:
        y_pos = random.randint(180, 220)  # Posição aleatória ajustada para galhos
    
    # Instancia o obstáculo
    obstaculo = Obstaculo(velocidade=velocidade, tipo=tipo)
    
    # Define posição inicial segura (fora da tela, lado direito)
    obstaculo.rect.x = 800
    obstaculo.rect.y = y_pos  # Define altura inicial segura para o obstáculo
    
    # Atualiza a posição inicial da hitbox após definir o rect
    obstaculo.hitbox.topleft = (obstaculo.rect.x, obstaculo.rect.y + 10)  # Desce a hitbox um pouco
    
    # Adiciona ao grupo de obstáculos
    grupo_obstaculos.add(obstaculo)
