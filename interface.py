import pygame
import sys


def renderizar_com_contorno(
    texto: str,
    fonte: pygame.font.Font,
    cor_texto: tuple,
    cor_borda: tuple
) -> pygame.Surface:
    """
    Renderiza texto com contorno.

    Args:
        texto (str): Texto a ser renderizado.
        fonte (pygame.font.Font): Fonte utilizada para renderizar o texto.
        cor_texto (tuple): Cor do texto.
        cor_borda (tuple): Cor do contorno.

    Returns:
        pygame.Surface: Superfície contendo o texto com contorno.
    """
    texto_superficie = fonte.render(texto, True, cor_texto)
    borda_superficie = fonte.render(texto, True, cor_borda)
    largura, altura = texto_superficie.get_size()
    superficie = pygame.Surface((largura + 4, altura + 4), pygame.SRCALPHA)

    offsets = [(-2, 0), (2, 0), (0, -2), (0, 2),
               (-2, -2), (2, -2), (-2, 2), (2, 2)]
    for dx, dy in offsets:
        superficie.blit(borda_superficie, (2 + dx, 2 + dy))

    superficie.blit(texto_superficie, (2, 2))
    return superficie


def exibir_tela_inicial(tela: pygame.Surface) -> None:
    """
    Exibe a tela inicial com o nome do jogo e a mensagem piscando 'Pressione ENTER para começar'.

    Args:
        tela (pygame.Surface): Superfície onde a tela inicial será renderizada.
    """
    # Carrega o fundo e ajusta o tamanho
    fundo = pygame.image.load("recursos/imagens/background/title_screen.jpg").convert()
    fundo = pygame.transform.scale(fundo, tela.get_size())

    # Configura música de fundo
    pygame.mixer.init()
    pygame.mixer.music.load("recursos/sons/title_screen.wav")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    # Cores utilizadas
    cor_titulo = (255, 255, 255)
    cor_contorno = (0, 0, 0)

    # Configura fonte e renderiza o título do jogo
    fonte_titulo = pygame.font.Font("recursos/fontes/title_screen.ttf", 48)
    titulo = renderizar_com_contorno("RUNNER'S QUEST", fonte_titulo, cor_titulo, cor_contorno)

    # Configura fonte e renderiza instruções
    fonte_instrucoes = pygame.font.Font(None, 36)
    instrucoes = renderizar_com_contorno(
        "Pressione ENTER para começar", fonte_instrucoes, cor_titulo, cor_contorno
    )

    # Centraliza elementos na tela
    largura_tela, altura_tela = tela.get_size()
    pos_titulo_x = (largura_tela - titulo.get_width()) // 2
    pos_titulo_y = altura_tela // 4
    pos_instrucoes_x = (largura_tela - instrucoes.get_width()) // 2
    pos_instrucoes_y = altura_tela // 2 + 100

    # Controla instruções piscando
    tempo_ultimo_piscando = pygame.time.get_ticks()
    instrucoes_visiveis = True

    tela_ativa = True
    while tela_ativa:
        # Renderiza fundo e título
        tela.blit(fundo, (0, 0))
        tela.blit(titulo, (pos_titulo_x, pos_titulo_y))

        # Alterna visibilidade das instruções
        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - tempo_ultimo_piscando > 500:
            instrucoes_visiveis = not instrucoes_visiveis
            tempo_ultimo_piscando = tempo_atual

        # Exibe instruções se visíveis
        if instrucoes_visiveis:
            tela.blit(instrucoes, (pos_instrucoes_x, pos_instrucoes_y))

        pygame.display.flip()

        # Processa eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                pygame.event.clear()
                return
