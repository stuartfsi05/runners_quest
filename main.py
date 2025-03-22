import pygame
from player import Player
from obstaculo import Obstaculo
from interface import exibir_tela_inicial, renderizar_com_contorno
from menu import exibir_menu  # Menu principal agora no menu.py

# Configurações do jogo
LARGURA_TELA = 800
ALTURA_TELA = 400
BRANCO = (255, 255, 255)
INTERVALO_OBSTACULOS = 2000  # Intervalo entre obstáculos (em milissegundos)

# Inicialização do Pygame e tela principal
pygame.init()
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Runner's Quest")
relogio = pygame.time.Clock()

# Grupos de sprites
grupo_jogador = pygame.sprite.GroupSingle()
grupo_jogador.add(Player())

grupo_obstaculos = pygame.sprite.Group()

# Carregamento do cenário
cenario = pygame.image.load("recursos/imagens/fundo_fase_1.png").convert()
cenario = pygame.transform.scale(cenario, (LARGURA_TELA, ALTURA_TELA))
cenario_largura = cenario.get_width()
cenario_x1 = 0
cenario_x2 = cenario_largura

# Temporizador global
tempo_ultimo_obstaculo = pygame.time.get_ticks()


def gerar_obstaculo():
    """
    Gera um novo obstáculo e o adiciona ao grupo.
    """
    velocidade = 5  # Velocidade inicial dos obstáculos
    novo_obstaculo = Obstaculo(velocidade)
    grupo_obstaculos.add(novo_obstaculo)


def exibir_game_over():
    """
    Exibe a mensagem de 'Game Over' na tela.
    """
    font = pygame.font.Font(None, 74)
    texto_game_over = font.render("Game Over", True, (255, 0, 0))
    tela.blit(texto_game_over, (250, 150))
    pygame.display.flip()
    pygame.time.wait(3000)  # Aguarda 3 segundos antes de encerrar


def atualizar_cenario():
    """
    Atualiza o movimento do cenário para criar a ilusão de deslocamento.
    """
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
    """
    Loop principal do jogo.
    """
    global tempo_ultimo_obstaculo

    # Exibe a tela inicial antes de ir para o menu
    exibir_tela_inicial(tela)

    # Configurações visuais do título e fundo
    fundo = pygame.image.load("recursos/imagens/title_screen.jpg").convert()
    fundo = pygame.transform.scale(fundo, tela.get_size())
    cor_titulo = (255, 255, 255)
    cor_contorno = (0, 0, 0)
    fonte_titulo = pygame.font.Font("recursos/fontes/title_screen.ttf", 48)
    titulo = renderizar_com_contorno("RUNNER'S QUEST", fonte_titulo, cor_titulo, cor_contorno)

    largura_tela, altura_tela = tela.get_size()
    pos_titulo_x = (largura_tela - titulo.get_width()) // 2
    pos_titulo_y = (altura_tela // 4) - 50

    # Exibe o menu principal e aguarda a ação do jogador
    acao = exibir_menu(tela, fundo, titulo, pos_titulo_x, pos_titulo_y)

    # Verificar a ação retornada pelo menu
    if acao == "INICIAR_JOGO":
        pygame.mixer.music.load("recursos/sons/level_1.wav")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

        running = True
        jogador_morto = False
        tempo_inicio_dead = 0

        while running:
            if not jogador_morto:
                tela.fill(BRANCO)
                atualizar_cenario()
            else:
                tela.blit(cenario, (cenario_x1, 0))
                tela.blit(cenario, (cenario_x2, 0))

            teclas = pygame.key.get_pressed()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    running = False

            jogador = grupo_jogador.sprite
            if not jogador_morto:
                grupo_jogador.update(teclas)

            grupo_jogador.draw(tela)
            jogador.draw_hitbox(tela)

            if not jogador_morto:
                tempo_atual = pygame.time.get_ticks()
                if tempo_atual - tempo_ultimo_obstaculo > INTERVALO_OBSTACULOS:
                    gerar_obstaculo()
                    tempo_ultimo_obstaculo = tempo_atual

                grupo_obstaculos.update()

            grupo_obstaculos.draw(tela)

            if not jogador_morto:
                for obstaculo in grupo_obstaculos:
                    if jogador.hitbox.colliderect(obstaculo.rect):
                        jogador.estado = "morto"
                        jogador_morto = True
                        tempo_inicio_dead = pygame.time.get_ticks()
                        break

            if jogador_morto:
                jogador.executar_animacao_dead()
                grupo_jogador.draw(tela)
                jogador.draw_hitbox(tela)
                grupo_obstaculos.draw(tela)

                if pygame.time.get_ticks() - tempo_inicio_dead > 1000:
                    exibir_game_over()
                    running = False

            pygame.display.flip()
            relogio.tick(60)

        pygame.mixer.music.stop()
        pygame.quit()


if __name__ == "__main__":
    main()
