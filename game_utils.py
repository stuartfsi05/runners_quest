import pygame

# Constantes de Configuração
CORES = {
    "BRANCO": (255, 255, 255),
    "AZUL": (0, 0, 255),
    "VERMELHO": (255, 0, 0),
    "VERDE": (0, 255, 0),
    "PRETO": (0, 0, 0)
}

GRAVIDADE = 1
PULO = -20  # Intensidade do pulo
LARGURA_TELA = 800
ALTURA_TELA = 400  # Adicionei ALTURA para manter coerência em diferentes arquivos

# Relógio para controle de FPS
RELOGIO = pygame.time.Clock()


def carregar_fonte(caminho: str, tamanho: int) -> pygame.font.Font:
    """Carrega uma fonte personalizada com um tamanho específico.

    Args:
        caminho (str): Caminho para o arquivo da fonte.
        tamanho (int): Tamanho da fonte.

    Returns:
        pygame.font.Font: Objeto de fonte carregada.
    """
    try:
        return pygame.font.Font(caminho, tamanho)
    except FileNotFoundError:
        raise FileNotFoundError(f"Fonte não encontrada no caminho: {caminho}")


def exibir_pontuacao(tela: pygame.Surface, pontuacao: int, fonte: pygame.font.Font) -> None:
    """Exibe a pontuação na tela.

    Args:
        tela (pygame.Surface): Superfície onde a pontuação será exibida.
        pontuacao (int): Valor numérico da pontuação.
        fonte (pygame.font.Font): Fonte usada para renderizar o texto.
    """
    texto = fonte.render(f"Pontuação: {pontuacao}", True, CORES["PRETO"])
    tela.blit(texto, (10, 10))


def exibir_texto_centralizado(tela: pygame.Surface, texto: str, fonte: pygame.font.Font, cor: tuple) -> None:
    """Exibe um texto centralizado na tela.

    Args:
        tela (pygame.Surface): Superfície onde o texto será exibido.
        texto (str): Texto a ser renderizado.
        fonte (pygame.font.Font): Fonte usada para o texto.
        cor (tuple): Cor do texto.
    """
    texto_renderizado = fonte.render(texto, True, cor)
    pos_x = (LARGURA_TELA - texto_renderizado.get_width()) // 2
    pos_y = (ALTURA_TELA - texto_renderizado.get_height()) // 2
    tela.blit(texto_renderizado, (pos_x, pos_y))


def aplicar_gravidade(velocidade: int) -> int:
    """Aplica a gravidade à velocidade do jogador.

    Args:
        velocidade (int): Velocidade vertical atual do jogador.

    Returns:
        int: Velocidade atualizada após aplicar a gravidade.
    """
    return velocidade + GRAVIDADE
