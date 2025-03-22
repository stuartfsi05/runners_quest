import pygame
from interface import renderizar_com_contorno  # Reutiliza a função para texto com contorno

def exibir_selecao_personagem(tela: pygame.Surface, fundo: pygame.Surface, titulo, pos_titulo_x, pos_titulo_y) -> str:
    """
    Exibe a tela de seleção de personagem com spritesheets animados e retorna o personagem escolhido.
    """
    # Lista de personagens com spritesheets e seus nomes
    personagens = [
        {"nome": "Kael", "spritesheet": "recursos/imagens/personagem1_spritesheet.png"},
        {"nome": "Ryuji", "spritesheet": "recursos/imagens/personagem2_spritesheet.png"},
        {"nome": "Jinzo", "spritesheet": "recursos/imagens/personagem3_spritesheet.png"},
    ]

    # Dimensões de cada frame no spritesheet
    largura_sprite = 128
    altura_sprite = 128
    total_frames = 6  # Total de frames na animação

    # Controle de animação
    indice_selecionado = 0
    frame_atual = 0
    frame_delay = 100
    ultimo_tempo = pygame.time.get_ticks()

    # Controle do cursor piscante
    cursor_visivel = True
    cursor_delay = 100  # Tempo reduzido para alternar a visibilidade do cursor
    ultimo_tempo_cursor = pygame.time.get_ticks()

    # Carrega os spritesheets
    sprites = []
    for personagem in personagens:
        spritesheet = pygame.image.load(personagem["spritesheet"]).convert_alpha()
        sprites.append(spritesheet)

    selecao_ativa = True
    espacamento_horizontal = 250
    ajuste_vertical = (tela.get_height() // 2) - altura_sprite + 100  # Ajuste vertical dos sprites

    while selecao_ativa:
        tela.blit(fundo, (0, 0))  # Redesenha o fundo
        tela.blit(titulo, (pos_titulo_x, pos_titulo_y))  # Exibe o título fixo no topo

        # Atualiza o frame atual da animação com base no tempo decorrido
        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - ultimo_tempo > frame_delay:
            frame_atual = (frame_atual + 1) % total_frames  # Avança para o próximo frame
            ultimo_tempo = tempo_atual

        # Alterna a visibilidade do cursor piscante
        if tempo_atual - ultimo_tempo_cursor > cursor_delay:
            cursor_visivel = not cursor_visivel
            ultimo_tempo_cursor = tempo_atual

        # Renderiza os personagens na tela
        for i, personagem in enumerate(personagens):
            pos_x = (tela.get_width() // 2) + (i - indice_selecionado) * espacamento_horizontal
            pos_y = ajuste_vertical

            if i == indice_selecionado:
                # Desenha o retângulo piscante sobre o personagem
                if cursor_visivel:
                    rect_x = pos_x - largura_sprite // 2 - 10  # Leve margem ao redor do sprite
                    rect_y = pos_y - 10
                    rect_width = largura_sprite + 20
                    rect_height = altura_sprite + 20
                    pygame.draw.rect(tela, (255, 255, 0), (rect_x, rect_y, rect_width, rect_height), 3)

                # Calcula o frame atual da animação
                frame_x = frame_atual * largura_sprite
                frame_rect = pygame.Rect(frame_x, 0, largura_sprite, altura_sprite)
                sprite_idle = sprites[i].subsurface(frame_rect)
                tela.blit(sprite_idle, (pos_x - largura_sprite // 2, pos_y))
            else:
                # Exibe apenas o sprite do personagem não selecionado
                frame_x = 0  # Sempre mostra o primeiro frame de idle para personagens não selecionados
                frame_rect = pygame.Rect(frame_x, 0, largura_sprite, altura_sprite)
                sprite_idle = sprites[i].subsurface(frame_rect)
                tela.blit(sprite_idle, (pos_x - largura_sprite // 2, pos_y))

            # Exibe o nome do personagem fixo abaixo do sprite
            fonte = pygame.font.Font(None, 35)
            texto = renderizar_com_contorno(personagem["nome"], fonte, (255, 255, 255), (0, 0, 0))
            tela.blit(texto, (pos_x - texto.get_width() // 2, pos_y + altura_sprite + 20))

        pygame.display.flip()

        # Captura eventos de teclado para navegação e seleção
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

    # Retorna o nome do personagem selecionado
    return personagens[indice_selecionado]["nome"]
