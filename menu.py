import pygame
import sys
from interface import renderizar_com_contorno
from selecao_personagem import exibir_selecao_personagem  # Tela de seleção de personagens


def exibir_menu(tela: pygame.Surface, fundo: pygame.Surface, fonte_titulo, cor_titulo, pos_titulo_x, pos_titulo_y) -> str:
    """
    Exibe o menu principal do jogo e retorna a ação escolhida.
    """
    cor_texto = (255, 255, 255)  # Branco
    cor_selecionada = (255, 255, 0)  # Amarelo para destacar a opção selecionada

    # Ajustando a fonte para o menu
    fonte_menu = pygame.font.Font(None, 35)  # Fonte simples para o texto do menu
    opcoes = ["Iniciar Jogo", "Configurações", "Créditos", "Sair"]

    menu_ativo = True
    selecionado = 0
    espacamento = 45
    deslocamento_vertical = 170

    while menu_ativo:
        tela.blit(fundo, (0, 0))  # Redesenha o fundo

        # Renderiza o título do menu
        texto_titulo = renderizar_com_contorno("Runner's Quest", fonte_titulo, cor_titulo, (0, 0, 0))
        tela.blit(texto_titulo, (pos_titulo_x - texto_titulo.get_width() // 2, pos_titulo_y))

        # Renderiza as opções do menu
        for i, opcao in enumerate(opcoes):
            cor = cor_texto if i != selecionado else cor_selecionada
            texto = renderizar_com_contorno(opcao, fonte_menu, cor, (0, 0, 0))
            pos_x = (tela.get_width() - texto.get_width()) // 2
            pos_y = pos_titulo_y + deslocamento_vertical + i * espacamento
            tela.blit(texto, (pos_x, pos_y))

        pygame.display.flip()

        # Captura eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    selecionado = (selecionado - 1) % len(opcoes)
                if evento.key == pygame.K_DOWN:
                    selecionado = (selecionado + 1) % len(opcoes)
                if evento.key == pygame.K_RETURN:
                    if selecionado == 0:  # Iniciar Jogo
                        return "INICIAR_JOGO"
                    elif selecionado == 1:  # Configurações
                        exibir_configuracoes(tela, fundo, fonte_titulo, cor_titulo, pos_titulo_x, pos_titulo_y)
                    elif selecionado == 2:  # Créditos
                        exibir_creditos(tela, fundo, fonte_titulo, cor_titulo, pos_titulo_x, pos_titulo_y)
                    elif selecionado == 3:  # Sair
                        pygame.quit()
                        sys.exit()


def exibir_configuracoes(tela: pygame.Surface, fundo: pygame.Surface, fonte_titulo, cor_titulo, pos_titulo_x, pos_titulo_y) -> None:
    """
    Exibe a tela de configurações.
    """
    tela.blit(fundo, (0, 0))  # Redesenha o fundo

    # Ajusta o tamanho da fonte para configurações
    fonte_titulo_config = pygame.font.Font("recursos/fontes/title_screen.ttf", 50)
    texto_titulo = renderizar_com_contorno("Configurações", fonte_titulo_config, cor_titulo, (0, 0, 0))
    tela.blit(texto_titulo, (pos_titulo_x - texto_titulo.get_width() // 2, pos_titulo_y))

    # Fonte menor para o texto de informações
    fonte_informativo = pygame.font.Font(None, 35)  # Usando fonte padrão para texto simples
    texto = renderizar_com_contorno(
        "Configurações em desenvolvimento...", fonte_informativo, (255, 255, 255), (0, 0, 0)
    )
    pos_x = (tela.get_width() - texto.get_width()) // 2
    pos_y = tela.get_height() // 2
    tela.blit(texto, (pos_x, pos_y))

    pygame.display.flip()
    pygame.time.wait(2000)


def exibir_creditos(tela: pygame.Surface, fundo: pygame.Surface, fonte_titulo, cor_titulo, pos_titulo_x, pos_titulo_y) -> None:
    """
    Exibe a tela de créditos.
    """
    tela.blit(fundo, (0, 0))  # Redesenha o fundo

    # Ajusta a fonte para a seção de créditos
    fonte_titulo_creditos = pygame.font.Font("recursos/fontes/title_screen.ttf", 50)
    texto_titulo = renderizar_com_contorno("Créditos", fonte_titulo_creditos, cor_titulo, (0, 0, 0))
    tela.blit(texto_titulo, (pos_titulo_x - texto_titulo.get_width() // 2, pos_titulo_y))

    # Fonte simples para informações dos créditos
    fonte_informativo = pygame.font.Font(None, 35)  # Usando fonte padrão para texto simples
    texto = renderizar_com_contorno(
        "Criado por: Thiago Dias Precivalli", fonte_informativo, (255, 255, 255), (0, 0, 0)
    )
    pos_x = (tela.get_width() - texto.get_width()) // 2
    pos_y = tela.get_height() // 2
    tela.blit(texto, (pos_x, pos_y))

    pygame.display.flip()
    pygame.time.wait(3000)
