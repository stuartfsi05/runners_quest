import pygame
import sys
import time


def renderizar_com_contorno(texto, fonte, cor_texto, cor_borda):
    """Renderiza texto com contorno preto."""
    texto_superficie = fonte.render(texto, True, cor_texto)
    borda_superficie = fonte.render(texto, True, cor_borda)
    largura, altura = texto_superficie.get_size()
    superficie = pygame.Surface((largura + 4, altura + 4), pygame.SRCALPHA)  # Buffer com espaço para o contorno
    for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2), (-2, -2), (2, -2), (-2, 2), (2, 2)]:
        superficie.blit(borda_superficie, (2 + dx, 2 + dy))  # Camadas do contorno
    superficie.blit(texto_superficie, (2, 2))  # Texto principal no centro
    return superficie


def exibir_tela_inicial(tela: pygame.Surface) -> None:
    """Exibe a tela inicial do jogo com imagem de fundo, texto contornado e piscante.

    Args:
        tela (pygame.Surface): A superfície da tela onde a tela inicial será exibida.
    """
    # Carregar a imagem de fundo
    fundo = pygame.image.load("recursos/imagens/title_screen.jpg").convert()
    fundo = pygame.transform.scale(fundo, tela.get_size())  # Escalar para o tamanho da tela

    # Iniciar o mixer de áudio
    pygame.mixer.init()
    pygame.mixer.music.load("recursos/sons/title_screen.wav")  # Caminho do arquivo de música
    pygame.mixer.music.set_volume(0.5)  # Ajusta o volume da música
    pygame.mixer.music.play(-1)  # Reproduz a música em loop

    # Configuração de cores para o texto
    cor_titulo = (255, 255, 255)  # Branco
    cor_contorno = (0, 0, 0)  # Preto para o contorno
    fonte_titulo = pygame.font.Font("recursos/fontes/title_screen.ttf", 48)  # Fonte personalizada
    fonte_instrucoes = pygame.font.Font(None, 36)  # Fonte menor para as instruções

    # Elementos de texto com contorno
    titulo = renderizar_com_contorno("RUNNER'S QUEST", fonte_titulo, cor_titulo, cor_contorno)
    instrucoes = renderizar_com_contorno("Pressione ENTER para começar", fonte_instrucoes, cor_titulo, cor_contorno)

    # Cálculo para centralizar os textos na tela
    largura_tela, altura_tela = tela.get_size()
    pos_titulo_x = (largura_tela - titulo.get_width()) // 2
    pos_titulo_y = (altura_tela // 2) - 120  # Ajustado para ficar mais acima
    pos_instrucoes_x = (largura_tela - instrucoes.get_width()) // 2
    pos_instrucoes_y = (altura_tela // 2) + 100  # Mais abaixo da tela

    # Controle de tempo para o efeito de "piscando"
    tempo_ultimo_piscando = pygame.time.get_ticks()
    instrucoes_visiveis = True  # Indica se as instruções estão visíveis

    # Loop da tela inicial
    tela_ativa = True
    while tela_ativa:
        tela.blit(fundo, (0, 0))  # Desenhar a imagem de fundo
        tela.blit(titulo, (pos_titulo_x, pos_titulo_y))  # Exibir o título com contorno

        # Alternar a visibilidade das instruções a cada 500ms
        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - tempo_ultimo_piscando > 500:  # 500ms (meio segundo)
            instrucoes_visiveis = not instrucoes_visiveis
            tempo_ultimo_piscando = tempo_atual

        if instrucoes_visiveis:
            tela.blit(instrucoes, (pos_instrucoes_x, pos_instrucoes_y))  # Exibir as instruções visíveis

        pygame.display.flip()  # Atualizar o display

        # Captura eventos de entrada do jogador
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:  # Fechar o jogo
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:  # Pressionar ENTER
                pygame.mixer.music.fadeout(1000)  # Suaviza a música em 1 segundo
                exibir_menu(tela)  # Chamar o menu principal
                tela_ativa = False


def exibir_menu(tela: pygame.Surface) -> None:
    """Exibe o menu principal do jogo.

    Args:
        tela (pygame.Surface): A superfície da tela onde o menu será exibido.
    """
    # Configuração de cores e fontes
    cor_texto = (255, 255, 255)  # Branco
    cor_selecionada = (255, 255, 0)  # Amarelo para destacar a opção selecionada
    fonte_menu = pygame.font.Font(None, 50)  # Fonte padrão
    opcoes = ["Iniciar Jogo", "Configurações", "Créditos", "Sair"]

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

        pygame.display.flip()  # Atualizar o display

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
                        menu_ativo = False  # Fechar o menu
                    elif selecionado == 1:  # Configurações
                        print("Abrindo Configurações...")
                    elif selecionado == 2:  # Créditos
                        print("Exibindo Créditos...")
                    elif selecionado == 3:  # Sair
                        pygame.quit()
                        sys.exit()
