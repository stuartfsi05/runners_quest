import pygame
import sys


def exibir_menu(tela: pygame.Surface) -> None:
    """Exibe o menu principal do jogo."""
    cor_texto = (255, 255, 255)  # Branco
    cor_selecionada = (255, 255, 0)  # Amarelo para destacar a opção selecionada
    fonte_menu = pygame.font.Font(None, 50)
    opcoes = ["Iniciar Jogo", "Configurações", "Créditos", "Sair"]

    menu_ativo = True
    selecionado = 0

    while menu_ativo:
        tela.fill((0, 0, 0))

        for i, opcao in enumerate(opcoes):
            cor = cor_texto if i != selecionado else cor_selecionada
            texto = fonte_menu.render(opcao, True, cor)
            pos_x = (tela.get_width() - texto.get_width()) // 2
            pos_y = (tela.get_height() // 2) + i * 60
            tela.blit(texto, (pos_x, pos_y))

        pygame.display.flip()

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
                        menu_ativo = False
                    elif selecionado == 1:  # Configurações
                        exibir_configuracoes(tela)
                    elif selecionado == 2:  # Créditos
                        exibir_creditos(tela)
                    elif selecionado == 3:  # Sair
                        pygame.quit()
                        sys.exit()

    # Limpa os eventos pendentes antes de sair do menu
    pygame.event.clear()


def exibir_configuracoes(tela: pygame.Surface) -> None:
    """Exibe a tela de configurações."""
    tela.fill((0, 0, 0))
    font = pygame.font.Font(None, 50)
    texto = font.render("Configurações em desenvolvimento...", True, (255, 255, 255))
    tela.blit(texto, ((tela.get_width() - texto.get_width()) // 2, tela.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(2000)  # Placeholder para configurações


def exibir_creditos(tela: pygame.Surface) -> None:
    """Exibe a tela de créditos."""
    tela.fill((0, 0, 0))
    font = pygame.font.Font(None, 50)
    texto = font.render("Criado por: Seu Nome", True, (255, 255, 255))
    tela.blit(texto, ((tela.get_width() - texto.get_width()) // 2, tela.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(3000)  # Placeholder para créditos
