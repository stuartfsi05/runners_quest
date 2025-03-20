import pygame
import time


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

    # Função para renderizar texto com contorno
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

    # Elementos de texto com contorno
    titulo = renderizar_com_contorno("RUNNER'S QUEST", fonte_titulo, cor_titulo, cor_contorno)
    instrucoes = renderizar_com_contorno("Pressione ENTER para começar", fonte_instrucoes, cor_titulo, cor_contorno)

    # Cálculo para centralizar os textos na tela
    largura_tela, altura_tela = tela.get_size()

    # Posição do título (um pouco acima do centro)
    pos_titulo_x = (largura_tela - titulo.get_width()) // 2
    pos_titulo_y = (altura_tela // 2) - 120  # Ajustado para ficar mais acima

    # Posição das instruções (um pouco abaixo do centro)
    pos_instrucoes_x = (largura_tela - instrucoes.get_width()) // 2
    pos_instrucoes_y = (altura_tela // 2) + 100  # Mais abaixo da tela

    # Controle de tempo para o efeito de "piscando"
    tempo_ultimo_piscando = pygame.time.get_ticks()
    instrucoes_visiveis = True  # Indica se as instruções estão visíveis

    # Loop da tela inicial
    tela_ativa = True
    while tela_ativa:
        # Desenhar a imagem de fundo
        tela.blit(fundo, (0, 0))

        # Exibir o título com contorno
        tela.blit(titulo, (pos_titulo_x, pos_titulo_y))

        # Alternar a visibilidade das instruções a cada 500ms
        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - tempo_ultimo_piscando > 500:  # 500ms (meio segundo)
            instrucoes_visiveis = not instrucoes_visiveis
            tempo_ultimo_piscando = tempo_atual

        # Exibir as instruções apenas se estiverem "visíveis" (com contorno)
        if instrucoes_visiveis:
            tela.blit(instrucoes, (pos_instrucoes_x, pos_instrucoes_y))

        # Atualizar o display
        pygame.display.flip()

        # Captura eventos de entrada do jogador
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:  # Fechar o jogo
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:  # Pressionar ENTER
                pygame.mixer.music.fadeout(1000)  # Suaviza a música em 1 segundo
                tela_ativa = False
