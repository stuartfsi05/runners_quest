import pygame

# Constantes de configuração
CORES = {
    "BRANCO": (255, 255, 255),
    "AZUL": (0, 0, 255),
    "VERMELHO": (255, 0, 0)
}

GRAVIDADE = 1
PULO = -20  # Intensidade do pulo

LARGURA_TELA = 800

# Relógio para controle de FPS
RELOGIO = pygame.time.Clock()


def exibir_pontuacao(tela: pygame.Surface, pontuacao: int, fonte: pygame.font.Font) -> None:
    """Exibe a pontuação na tela.

    Args:
        tela (pygame.Surface): Superfície onde a pontuação será exibida.
        pontuacao (int): Valor numérico da pontuação.
        fonte (pygame.font.Font): Fonte usada para renderizar o texto.
    """
    texto = fonte.render(f"Pontuação: {pontuacao}", True, (0, 0, 0))
    tela.blit(texto, (10, 10))
