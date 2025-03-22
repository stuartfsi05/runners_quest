import pygame
import sys


def renderizar_com_contorno(texto, fonte, cor_texto, cor_borda):
    """
    Renderiza texto com contorno.
    """
    texto_superficie = fonte.render(texto, True, cor_texto)
    borda_superficie = fonte.render(texto, True, cor_borda)
    largura, altura = texto_superficie.get_size()
    superficie = pygame.Surface((largura + 4, altura + 4), pygame.SRCALPHA)
    for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2), (-2, -2), (2, -2), (-2, 2), (2, 2)]:
        superficie.blit(borda_superficie, (2 + dx, 2 + dy))
    superficie.blit(texto_superficie, (2, 2))
    return superficie


def exibir_tela_inicial(tela: pygame.Surface) -> None:
    """
    Exibe a tela inicial com o nome do jogo e a mensagem piscando 'Pressione ENTER para começar'.
    """
    fundo = pygame.image.load("recursos/imagens/title_screen.jpg").convert()
    fundo = pygame.transform.scale(fundo, tela.get_size())

    pygame.mixer.init()
    pygame.mixer.music.load("recursos/sons/title_screen.wav")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    cor_titulo = (255, 255, 255)
    cor_contorno = (0, 0, 0)
    fonte_titulo = pygame.font.Font("recursos/fontes/title_screen.ttf", 48)
    titulo = renderizar_com_contorno("RUNNER'S QUEST", fonte_titulo, cor_titulo, cor_contorno)

    fonte_instrucoes = pygame.font.Font(None, 36)
    instrucoes = renderizar_com_contorno(
        "Pressione ENTER para começar", fonte_instrucoes, cor_titulo, cor_contorno
    )

    largura_tela, altura_tela = tela.get_size()
    pos_titulo_x = (largura_tela - titulo.get_width()) // 2
    pos_titulo_y = altura_tela // 4
    pos_instrucoes_x = (largura_tela - instrucoes.get_width()) // 2
    pos_instrucoes_y = altura_tela // 2 + 100

    tempo_ultimo_piscando = pygame.time.get_ticks()
    instrucoes_visiveis = True

    tela_ativa = True
    while tela_ativa:
        tela.blit(fundo, (0, 0))
        tela.blit(titulo, (pos_titulo_x, pos_titulo_y))

        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - tempo_ultimo_piscando > 500:
            instrucoes_visiveis = not instrucoes_visiveis
            tempo_ultimo_piscando = tempo_atual

        if instrucoes_visiveis:
            tela.blit(instrucoes, (pos_instrucoes_x, pos_instrucoes_y))

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                pygame.event.clear()
                return
