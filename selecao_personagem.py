import pygame
from interface import renderizar_com_contorno  # Reutiliza a função para texto com contorno
import time  # Para adicionar a pausa de 1 segundo

def exibir_selecao_personagem(tela: pygame.Surface, fundo: pygame.Surface, fonte_global, cor_titulo, pos_titulo_x, pos_titulo_y) -> str:
    """
    Exibe a tela de seleção de personagem com spritesheets animados e retorna o nome do personagem escolhido.
    """
    # Lista de personagens com spritesheets de idle e selected
    personagens = [
        {"nome": "Kael", "spritesheet_idle": "recursos/imagens/kael/spritesheet_idle.png",
         "spritesheet_selected": "recursos/imagens/kael/spritesheet_selected.png"},
        {"nome": "Ryuji", "spritesheet_idle": "recursos/imagens/ryuji/spritesheet_idle.png",
         "spritesheet_selected": "recursos/imagens/ryuji/spritesheet_selected.png"},
        {"nome": "Jinzo", "spritesheet_idle": "recursos/imagens/jinzo/spritesheet_idle.png",
         "spritesheet_selected": "recursos/imagens/jinzo/spritesheet_selected.png"},
    ]

    # Dimensões de cada frame no spritesheet
    largura_sprite = 128
    altura_sprite = 128
    total_frames_idle = 6  # Total de frames para animação de idle
    total_frames_selected = 4  # Total de frames para animação de seleção

    # Controle de animação e cursor
    indice_selecionado = 1  # Inicia no meio (Ryuji)
    frame_atual = 0
    frame_delay = 100  # Intervalo entre os frames da animação (em milissegundos)
    ultimo_tempo = pygame.time.get_ticks()

    # Controle do cursor piscante
    cursor_visivel = True  # Inicia com o cursor visível
    cursor_delay = 500  # Tempo em milissegundos para alternar o cursor
    ultimo_tempo_cursor = pygame.time.get_ticks()

    # Controle de seleção
    personagem_confirmado = False
    terminou_animacao = False  # Indica se a animação de seleção terminou

    # Carrega os spritesheets de idle e de seleção para os personagens
    sprites_idle = []
    sprites_selected = []
    for personagem in personagens:
        spritesheet_idle = pygame.image.load(personagem["spritesheet_idle"]).convert_alpha()
        spritesheet_selected = pygame.image.load(personagem["spritesheet_selected"]).convert_alpha()
        sprites_idle.append([
            spritesheet_idle.subsurface((i * largura_sprite, 0, largura_sprite, altura_sprite))
            for i in range(total_frames_idle)
        ])
        sprites_selected.append([
            spritesheet_selected.subsurface((i * largura_sprite, 0, largura_sprite, altura_sprite))
            for i in range(total_frames_selected)
        ])

    selecao_ativa = True
    espacamento_horizontal = 250
    ajuste_vertical = (tela.get_height() // 2) - altura_sprite + 100

    # Fonte ajustada para o título e instruções
    fonte_titulo = pygame.font.Font(None, 40)  # Reduzindo o tamanho para caber na tela
    fonte_instrucoes = pygame.font.Font(None, 27)  # Fonte para instruções

    # Ajustando o título mais para cima
    pos_titulo_y_atualizado = pos_titulo_y - 50

    while selecao_ativa:
        tela.blit(fundo, (0, 0))  # Redesenha o fundo

        # Renderiza o título "Escolha seu personagem"
        texto_titulo = renderizar_com_contorno("ESCOLHA SEU PERSONAGEM", pygame.font.Font("recursos/fontes/title_screen.ttf", 35), cor_titulo, (0, 0, 0))
        tela.blit(texto_titulo, (pos_titulo_x - texto_titulo.get_width() // 2, pos_titulo_y_atualizado))

        # Renderiza as instruções abaixo do título com quebra de linha
        texto_instrucoes_parte1 = renderizar_com_contorno(
            "Use as setas do teclado para alterar entre os personagens",
            fonte_instrucoes,
            (255, 255, 255),  # Branco
            (0, 0, 0)  # Contorno preto
        )
        texto_instrucoes_parte2 = renderizar_com_contorno(
            "e aperte ENTER para selecioná-lo.",
            fonte_instrucoes,
            (255, 255, 255),  # Branco
            (0, 0, 0)  # Contorno preto
        )
        pos_instrucoes_y = pos_titulo_y_atualizado + texto_titulo.get_height() + 20
        tela.blit(texto_instrucoes_parte1, (pos_titulo_x - texto_instrucoes_parte1.get_width() // 2, pos_instrucoes_y))
        tela.blit(texto_instrucoes_parte2, (pos_titulo_x - texto_instrucoes_parte2.get_width() // 2, pos_instrucoes_y + texto_instrucoes_parte1.get_height() + 5))

        # Atualiza o frame da animação baseado no tempo
        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - ultimo_tempo > frame_delay:
            if personagem_confirmado and not terminou_animacao:
                frame_atual += 1
                if frame_atual >= total_frames_selected:
                    terminou_animacao = True  # Marca que a animação de seleção foi concluída
                else:
                    frame_atual %= total_frames_selected  # Garante que a animação seja fluída
            elif not personagem_confirmado:
                frame_atual = (frame_atual + 1) % total_frames_idle
            ultimo_tempo = tempo_atual

        # Alterna a visibilidade do cursor piscante
        if tempo_atual - ultimo_tempo_cursor > cursor_delay:
            cursor_visivel = not cursor_visivel
            ultimo_tempo_cursor = tempo_atual

        # Renderiza os sprites dos personagens
        for i, personagem in enumerate(personagens):
            pos_x = (tela.get_width() // 2) + (i - indice_selecionado) * espacamento_horizontal
            pos_y = ajuste_vertical

            if i == indice_selecionado:
                # Altere para o spritesheet de seleção se o personagem foi confirmado
                if personagem_confirmado:
                    if frame_atual < total_frames_selected:
                        frame = sprites_selected[i][frame_atual]
                    else:
                        frame = sprites_selected[i][-1]  # Mostra o último frame após a conclusão
                else:
                    frame = sprites_idle[i][frame_atual]

                tela.blit(frame, (pos_x - largura_sprite // 2, pos_y))

                # Desenha o cursor piscante ao redor do personagem selecionado
                if not personagem_confirmado and cursor_visivel:
                    rect_x = pos_x - largura_sprite // 2 - 10
                    rect_y = pos_y - 10
                    rect_width = largura_sprite + 20
                    rect_height = altura_sprite + 20
                    pygame.draw.rect(tela, (100, 255, 100), (rect_x, rect_y, rect_width, rect_height), 3)
            else:
                # Mostra apenas o primeiro frame para personagens não selecionados
                frame = sprites_idle[i][0]
                tela.blit(frame, (pos_x - largura_sprite // 2, pos_y))

            # Renderiza o nome do personagem abaixo do sprite
            fonte_nome = pygame.font.Font(None, 35)
            texto_nome = renderizar_com_contorno(personagem["nome"], fonte_nome, (255, 255, 255), (0, 0, 0))
            tela.blit(texto_nome, (pos_x - texto_nome.get_width() // 2, pos_y + altura_sprite + 20))

        pygame.display.flip()

        # Captura eventos de teclado para navegação e seleção
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if not personagem_confirmado:
                    if evento.key == pygame.K_LEFT:
                        indice_selecionado = (indice_selecionado - 1) % len(personagens)
                    if evento.key == pygame.K_RIGHT:
                        indice_selecionado = (indice_selecionado + 1) % len(personagens)
                    if evento.key == pygame.K_RETURN:
                        personagem_confirmado = True  # Confirma a seleção

        # Finaliza a seleção e encerra o loop quando a animação de seleção terminar
        if personagem_confirmado and terminou_animacao:
            pygame.display.flip()
            time.sleep(1)  # Pausa de 1 segundo antes de prosseguir
            selecao_ativa = False

    # Retorna o nome do personagem escolhido
    return personagens[indice_selecionado]["nome"]
