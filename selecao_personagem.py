import pygame
from interface import renderizar_com_contorno  # Reutiliza a função para texto com contorno

def exibir_selecao_personagem(tela: pygame.Surface, fundo: pygame.Surface, fonte_global, cor_titulo, pos_titulo_x, pos_titulo_y) -> str:
    """
    Exibe a tela de seleção de personagem com spritesheets animados e retorna o nome do personagem escolhido.
    """
    # Lista de personagens com seus spritesheets e nomes
    personagens = [
        {"nome": "Kael", "spritesheet": "recursos/imagens/personagem_1/spritesheet_run.png"},
        {"nome": "Ryuji", "spritesheet": "recursos/imagens/personagem_2/spritesheet_run.png"},
        {"nome": "Jinzo", "spritesheet": "recursos/imagens/personagem_3/spritesheet_run.png"},
    ]

    # Dimensões do frame do spritesheet
    largura_sprite = 128
    altura_sprite = 128
    total_frames = 6  # Total de frames na animação

    # Controle de animação
    indice_selecionado = 0
    frame_atual = 0
    frame_delay = 100  # Intervalo entre os frames da animação
    ultimo_tempo = pygame.time.get_ticks()

    # Controle do cursor piscante
    cursor_visivel = True
    cursor_delay = 100  # Tempo para alternar a visibilidade do cursor
    ultimo_tempo_cursor = pygame.time.get_ticks()

    # Carrega os spritesheets dos personagens
    sprites = []
    for personagem in personagens:
        spritesheet = pygame.image.load(personagem["spritesheet"]).convert_alpha()
        sprites.append(spritesheet)

    selecao_ativa = True
    espacamento_horizontal = 250
    ajuste_vertical = (tela.get_height() // 2) - altura_sprite + 100

    # Ajusta a fonte e posição do título
    fonte_local_selecao = pygame.font.Font("recursos/fontes/title_screen.ttf", 25)
    pos_titulo_y -= 50  # Move o texto para cima 50px

    while selecao_ativa:
        tela.blit(fundo, (0, 0))  # Redesenha o fundo

        # Renderiza o texto "Escolha seu personagem"
        texto_titulo = renderizar_com_contorno("Escolha seu personagem", fonte_local_selecao, cor_titulo, (0, 0, 0))
        tela.blit(texto_titulo, (pos_titulo_x - texto_titulo.get_width() // 2, pos_titulo_y))

        # Atualiza o frame da animação baseado no tempo
        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - ultimo_tempo > frame_delay:
            frame_atual = (frame_atual + 1) % total_frames
            ultimo_tempo = tempo_atual

        # Alterna a visibilidade do cursor
        if tempo_atual - ultimo_tempo_cursor > cursor_delay:
            cursor_visivel = not cursor_visivel
            ultimo_tempo_cursor = tempo_atual

        # Renderiza os sprites dos personagens
        for i, personagem in enumerate(personagens):
            pos_x = (tela.get_width() // 2) + (i - indice_selecionado) * espacamento_horizontal
            pos_y = ajuste_vertical

            if i == indice_selecionado:
                # Desenha o cursor piscante
                if cursor_visivel:
                    rect_x = pos_x - largura_sprite // 2 - 10
                    rect_y = pos_y - 10
                    rect_width = largura_sprite + 20
                    rect_height = altura_sprite + 20
                    pygame.draw.rect(tela, (100, 255, 100), (rect_x, rect_y, rect_width, rect_height), 3)

                # Calcula o frame atual da animação
                frame_x = frame_atual * largura_sprite
                frame_rect = pygame.Rect(frame_x, 0, largura_sprite, altura_sprite)
                sprite_idle = sprites[i].subsurface(frame_rect)
                tela.blit(sprite_idle, (pos_x - largura_sprite // 2, pos_y))
            else:
                # Exibe apenas o primeiro frame para personagens não selecionados
                frame_x = 0
                frame_rect = pygame.Rect(frame_x, 0, largura_sprite, altura_sprite)
                sprite_idle = sprites[i].subsurface(frame_rect)
                tela.blit(sprite_idle, (pos_x - largura_sprite // 2, pos_y))

            # Exibe o nome do personagem abaixo do sprite
            fonte = pygame.font.Font(None, 35)
            texto = renderizar_com_contorno(personagem["nome"], fonte, (255, 255, 255), (0, 0, 0))
            tela.blit(texto, (pos_x - texto.get_width() // 2, pos_y + altura_sprite + 20))

        pygame.display.flip()

        # Captura os eventos de teclado
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    indice_selecionado = (indice_selecionado - 1) % len(personagens)
                if evento.key == pygame.K_RIGHT:
                    indice_selecionado = (indice_selecionado + 1) % len(personagens)
                if evento.key == pygame.K_RETURN:
                    selecao_ativa = False  # Confirma seleção

    # Retorna o nome do personagem escolhido
    return personagens[indice_selecionado]["nome"]
