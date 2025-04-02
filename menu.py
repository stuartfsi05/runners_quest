import pygame
import sys
from interface import renderizar_com_contorno
from selecao_personagem import exibir_selecao_personagem  # Tela de seleção de personagens


def exibir_menu(
    tela: pygame.Surface,
    fundo: pygame.Surface,
    fonte_titulo: pygame.font.Font,
    cor_titulo: tuple,
    pos_titulo_x: int,
    pos_titulo_y: int
) -> str:
    """
    Exibe o menu principal do jogo e retorna a ação escolhida.

    Args:
        tela (pygame.Surface): Superfície onde o menu será exibido.
        fundo (pygame.Surface): Superfície do fundo da tela.
        fonte_titulo (pygame.font.Font): Fonte utilizada para o título.
        cor_titulo (tuple): Cor do título.
        pos_titulo_x (int): Posição X do título centralizado.
        pos_titulo_y (int): Posição Y do título centralizado.

    Returns:
        str: Ação escolhida pelo jogador.
    """
    cor_texto = (255, 255, 255)  # Branco
    cor_selecionada = (255, 255, 0)  # Amarelo para destacar a opção selecionada

    # Configuração do menu
    fonte_menu = pygame.font.Font(None, 35)  # Fonte para o texto do menu
    opcoes = ["Iniciar Jogo", "Configurações", "Créditos", "Sair"]

    menu_ativo = True
    selecionado = 0
    espacamento = 45
    deslocamento_vertical = 170

    # Calcula as posições das opções do menu
    posicoes_opcoes = []
    for i, opcao in enumerate(opcoes):
        texto = fonte_menu.render(opcao, True, cor_texto)
        largura_texto = texto.get_width()
        altura_texto = texto.get_height()
        pos_x = (tela.get_width() - largura_texto) // 2
        pos_y = pos_titulo_y + deslocamento_vertical + i * espacamento
        posicoes_opcoes.append(pygame.Rect(pos_x, pos_y, largura_texto, altura_texto))

    while menu_ativo:
        tela.blit(fundo, (0, 0))  # Redesenha o fundo

        # Renderiza o título do menu
        texto_titulo = renderizar_com_contorno(
            "Runner's Quest", fonte_titulo, cor_titulo, (0, 0, 0)
        )
        tela.blit(
            texto_titulo,
            (pos_titulo_x - texto_titulo.get_width() // 2, pos_titulo_y)
        )

        # Renderiza as opções do menu
        for i, opcao in enumerate(opcoes):
            cor = cor_texto if i != selecionado else cor_selecionada
            texto = renderizar_com_contorno(opcao, fonte_menu, cor, (0, 0, 0))
            pos_x = (tela.get_width() - texto.get_width()) // 2
            pos_y = pos_titulo_y + deslocamento_vertical + i * espacamento
            tela.blit(texto, (pos_x, pos_y))

        pygame.display.flip()

        # Processa eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Controle do teclado
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    selecionado = (selecionado - 1) % len(opcoes)
                if evento.key == pygame.K_DOWN:
                    selecionado = (selecionado + 1) % len(opcoes)
                if evento.key == pygame.K_RETURN:
                    if selecionado == 0:  # Iniciar Jogo
                        return "INICIAR_JOGO"
                    if selecionado == 1:  # Configurações
                        exibir_configuracoes(
                            tela, fundo, fonte_titulo, cor_titulo,
                            pos_titulo_x, pos_titulo_y
                        )
                    if selecionado == 2:  # Créditos
                        exibir_creditos(
                            tela, fundo, fonte_titulo, cor_titulo,
                            pos_titulo_x, pos_titulo_y
                        )
                    if selecionado == 3:  # Sair
                        pygame.quit()
                        sys.exit()

            # Controle do mouse
            if evento.type == pygame.MOUSEMOTION:
                for i, pos in enumerate(posicoes_opcoes):
                    if pos.collidepoint(evento.pos):
                        selecionado = i

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                for i, pos in enumerate(posicoes_opcoes):
                    if pos.collidepoint(evento.pos):
                        if i == 0:  # Iniciar Jogo
                            return "INICIAR_JOGO"
                        if i == 1:  # Configurações
                            exibir_configuracoes(
                                tela, fundo, fonte_titulo, cor_titulo,
                                pos_titulo_x, pos_titulo_y
                            )
                        if i == 2:  # Créditos
                            exibir_creditos(
                                tela, fundo, fonte_titulo, cor_titulo,
                                pos_titulo_x, pos_titulo_y
                            )
                        if i == 3:  # Sair
                            pygame.quit()
                            sys.exit()


def exibir_configuracoes(
    tela: pygame.Surface,
    fundo: pygame.Surface,
    fonte_titulo: pygame.font.Font,
    cor_titulo: tuple,
    pos_titulo_x: int,
    pos_titulo_y: int
) -> None:
    """
    Exibe a tela de configurações.

    Args:
        tela (pygame.Surface): Superfície onde as configurações serão exibidas.
        fundo (pygame.Surface): Fundo do menu.
        fonte_titulo (pygame.font.Font): Fonte utilizada no título.
        cor_titulo (tuple): Cor do título.
        pos_titulo_x (int): Posição X do título centralizado.
        pos_titulo_y (int): Posição Y do título centralizado.
    """
    tela.blit(fundo, (0, 0))  # Redesenha o fundo

    fonte_titulo_config = pygame.font.Font("recursos/fontes/title_screen.ttf", 50)
    texto_titulo = renderizar_com_contorno(
        "Configurações", fonte_titulo_config, cor_titulo, (0, 0, 0)
    )
    tela.blit(
        texto_titulo,
        (pos_titulo_x - texto_titulo.get_width() // 2, pos_titulo_y)
    )

    fonte_informativo = pygame.font.Font(None, 35)
    texto = renderizar_com_contorno(
        "Configurações em desenvolvimento...",
        fonte_informativo, (255, 255, 255), (0, 0, 0)
    )
    pos_x = (tela.get_width() - texto.get_width()) // 2
    pos_y = tela.get_height() // 2
    tela.blit(texto, (pos_x, pos_y))

    pygame.display.flip()
    pygame.time.wait(2000)


def exibir_creditos(
    tela: pygame.Surface,
    fundo: pygame.Surface,
    fonte_titulo: pygame.font.Font,
    cor_titulo: tuple,
    pos_titulo_x: int,
    pos_titulo_y: int
) -> None:
    """
    Exibe a tela de créditos.

    Args:
        tela (pygame.Surface): Superfície onde os créditos serão exibidos.
        fundo (pygame.Surface): Fundo do menu.
        fonte_titulo (pygame.font.Font): Fonte utilizada no título.
        cor_titulo (tuple): Cor do título.
        pos_titulo_x (int): Posição X do título centralizado.
        pos_titulo_y (int): Posição Y do título centralizado.
    """
    tela.blit(fundo, (0, 0))  # Redesenha o fundo

    fonte_titulo_creditos = pygame.font.Font("recursos/fontes/title_screen.ttf", 50)
    texto_titulo = renderizar_com_contorno(
        "Créditos", fonte_titulo_creditos, cor_titulo, (0, 0, 0)
    )
    tela.blit(
        texto_titulo,
        (pos_titulo_x - texto_titulo.get_width() // 2, pos_titulo_y)
    )

    fonte_informativo = pygame.font.Font(None, 35)
    texto = renderizar_com_contorno(
        "Criado por: Thiago Dias Precivalli",
        fonte_informativo, (255, 255, 255), (0, 0, 0)
    )
    pos_x = (tela.get_width() - texto.get_width()) // 2
    pos_y = tela.get_height() // 2
    tela.blit(texto, (pos_x, pos_y))

    pygame.display.flip()
    pygame.time.wait(3000)
