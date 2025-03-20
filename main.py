import pygame
from player import Player  # Certifique-se de que o player.py está configurado corretamente
from obstaculo import Obstaculo  # Certifique-se de que o obstaculo.py está configurado corretamente
from interface import exibir_tela_inicial, exibir_menu  # Importa a tela inicial e o menu do arquivo interface.py

# Configurações do jogo
LARGURA_TELA = 800
ALTURA_TELA = 400
BRANCO = (255, 255, 255)
INTERVALO_OBSTACULOS = 2000  # Intervalo entre obstáculos (em milissegundos)

# Inicialização do Pygame e tela principal
pygame.init()
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
relogio = pygame.time.Clock()

# Grupos de sprites
grupo_jogador = pygame.sprite.GroupSingle()
grupo_jogador.add(Player())

grupo_obstaculos = pygame.sprite.Group()

# Carregamento do cenário
cenario = pygame.image.load("recursos/imagens/fundo_fase_1.png").convert()
cenario = pygame.transform.scale(cenario, (LARGURA_TELA, ALTURA_TELA))  # Redimensiona para caber na tela
cenario_largura = cenario.get_width()
cenario_x1 = 0
cenario_x2 = cenario_largura

# Temporizador global
tempo_ultimo_obstaculo = pygame.time.get_ticks()


def gerar_obstaculo():
    """Gera um novo obstáculo e o adiciona ao grupo."""
    velocidade = 5  # Velocidade inicial dos obstáculos
    novo_obstaculo = Obstaculo(velocidade)
    grupo_obstaculos.add(novo_obstaculo)


def exibir_game_over():
    """Exibe a mensagem de 'Game Over' na tela."""
    font = pygame.font.Font(None, 74)
    texto_game_over = font.render("Game Over", True, (255, 0, 0))
    tela.blit(texto_game_over, (250, 150))
    pygame.display.flip()  # Atualiza a tela para exibir a mensagem
    pygame.time.wait(3000)  # Aguarda 3 segundos antes de encerrar


def atualizar_cenario():
    """Atualiza o movimento do cenário para criar a ilusão de deslocamento."""
    global cenario_x1, cenario_x2
    cenario_x1 -= 2
    cenario_x2 -= 2

    if cenario_x1 <= -cenario_largura:
        cenario_x1 = cenario_x2 + cenario_largura
    if cenario_x2 <= -cenario_largura:
        cenario_x2 = cenario_x1 + cenario_largura

    tela.blit(cenario, (cenario_x1, 0))
    tela.blit(cenario, (cenario_x2, 0))


def main():
    """Loop principal do jogo."""
    global tempo_ultimo_obstaculo

    # Exibir a tela inicial antes de iniciar o jogo
    exibir_tela_inicial(tela)

    # Exibir o menu após a tela inicial
    exibir_menu(tela)

    # Carregar e iniciar a música da fase 1 com transição suave
    pygame.mixer.music.load("recursos/sons/level_1.wav")  # Caminho para a música da fase 1
    pygame.mixer.music.set_volume(0.5)  # Ajusta o volume
    pygame.mixer.music.play(-1)  # Reproduz a música em loop

    running = True
    jogador_morto = False
    tempo_inicio_dead = 0

    while running:
        # Atualizar tela com base no estado do jogador
        if not jogador_morto:
            tela.fill(BRANCO)  # Limpa a tela apenas enquanto o jogador não está morto
            atualizar_cenario()
        else:
            # Redesenha o cenário no estado "morto", mantendo o fundo visível
            tela.blit(cenario, (cenario_x1, 0))
            tela.blit(cenario, (cenario_x2, 0))

        teclas = pygame.key.get_pressed()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                running = False

        # Atualizar o jogador e o cenário enquanto não está morto
        jogador = grupo_jogador.sprite
        if not jogador_morto:
            grupo_jogador.update(teclas)

        grupo_jogador.draw(tela)
        jogador.draw_hitbox(tela)  # Exibe a hitbox do jogador

        # Gerar e atualizar obstáculos
        if not jogador_morto:
            tempo_atual = pygame.time.get_ticks()
            if tempo_atual - tempo_ultimo_obstaculo > INTERVALO_OBSTACULOS:
                gerar_obstaculo()
                tempo_ultimo_obstaculo = tempo_atual

            grupo_obstaculos.update()

        grupo_obstaculos.draw(tela)

        # Verificar colisões com obstáculos
        if not jogador_morto:
            for obstaculo in grupo_obstaculos:
                if jogador.hitbox.colliderect(obstaculo.rect):  # Verifica colisão
                    jogador.estado = "morto"
                    jogador_morto = True
                    tempo_inicio_dead = pygame.time.get_ticks()
                    break

        # Processar lógica quando o jogador está morto
        if jogador_morto:
            jogador.executar_animacao_dead()
            grupo_jogador.draw(tela)  # Redesenha o jogador no estado "morto"
            jogador.draw_hitbox(tela)
            grupo_obstaculos.draw(tela)

            # Exibir mensagem "Game Over" após 1 segundo
            if pygame.time.get_ticks() - tempo_inicio_dead > 1000:
                exibir_game_over()
                running = False

        pygame.display.flip()
        relogio.tick(60)

    pygame.mixer.music.stop()
    pygame.quit()


if __name__ == "__main__":
    main()
