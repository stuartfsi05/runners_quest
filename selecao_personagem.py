import pygame
from interface import renderizar_com_contorno  # Reutiliza a função para texto com contorno

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

    fonte_local_selecao = pygame.font.Font("recursos/fontes/title_screen.ttf", 25)

    # Desce a posição do título
    pos_titulo_y += 30

    while selecao_ativa:
        tela.blit(fundo, (0, 0))  # Redesenha o fundo

        # Renderiza o título "Escolha seu personagem"
        texto_titulo = renderizar_com_contorno("Escolha seu personagem", fonte_local_selecao, cor_titulo, (0, 0, 0))
        tela.blit(texto_titulo, (pos_titulo_x - texto_titulo.get_width() // 2, pos_titulo_y))

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

        # Faz a transição suave para o jogo (Fade-Out)
        if terminou_animacao:
            # Aguarda um pequeno tempo antes de começar o fade-out (tela preta reduzida em 1 segundo)
            pygame.time.delay(1000)  # Ajuste reduzindo o tempo da tela preta de 2000 ms para 1000 ms

            for alpha in range(255, -1, -5):  # Passo de opacidade para fade-out
                overlay = pygame.Surface(tela.get_size())
                overlay.set_alpha(alpha)
                overlay.fill((0, 0, 0))
                tela.blit(overlay, (0, 0))
                pygame.display.flip()
                pygame.time.delay(20)

            selecao_ativa = False

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

    # Retorna o nome do personagem escolhido
    return personagens[indice_selecionado]["nome"]
