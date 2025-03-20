import pygame
import sys


def exibir_menu(tela: pygame.Surface) -> None:
    """Exibe o menu principal do jogo.

    Args:
        tela (pygame.Surface): A superfície da tela onde o menu será exibido.
    """
    # Configuração de cores e fontes
    cor_texto = (255, 255, 255)  # Branco
    cor_selecionada = (255, 255, 0)  # Amarelo para destacar a opção selecionada
    fonte_menu = pygame.font.Font(None, 50)  # Fonte padrão com tamanho 50
    opcoes = ["Iniciar Jogo", "Configurações", "Créditos", "Sair"]  # Opções do menu

    # Variável de controle do menu
    menu_ativo = True
    selecionado = 0  # Índice da opção selecionada

    while menu_ativo:
        tela.fill((0, 0, 0))  # Fundo preto

        # Renderizar as opções do menu
        for i, opcao in enumerate(opcoes):
            cor = cor_texto if i != selecionado else cor_selecionada
            texto = fonte_menu.render(opcao, True, cor)
            pos_x = (tela.get_width() - texto.get_width()) // 2
            pos_y = (tela.get_height() // 2) + i * 60  # Distância entre as opções
            tela.blit(texto, (pos_x, pos_y))

        # Atualizar a tela
        pygame.display.flip()

        # Capturar eventos do teclado
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:  # Fechar o jogo
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:  # Navegar para cima
                    selecionado = (selecionado - 1) % len(opcoes)
                if evento.key == pygame.K_DOWN:  # Navegar para baixo
                    selecionado = (selecionado + 1) % len(opcoes)
                if evento.key == pygame.K_RETURN:  # Selecionar uma opção
                    if selecionado == 0:  # Iniciar Jogo
                        print("Iniciando o jogo...")
                        menu_ativo = False  # Fechar o menu e iniciar o jogo
                    elif selecionado == 1:  # Configurações
                        print("Abrindo Configurações...")
                    elif selecionado == 2:  # Créditos
                        print("Exibindo Créditos...")
                    elif selecionado == 3:  # Sair
                        pygame.quit()
                        sys.exit()
