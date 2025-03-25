import pygame
from obstaculo import Obstaculo
from interface import exibir_tela_inicial
from menu import exibir_menu
from selecao_personagem import exibir_selecao_personagem
from player import Player
from fase_1 import carregar_fase_1, gerar_obstaculos_fase_1

# Configurações do jogo
LARGURA_TELA = 800
ALTURA_TELA = 400
BRANCO = (255, 255, 255)
INTERVALO_OBSTACULOS = 3000  # Intervalo entre geração de obstáculos em milissegundos
MAX_OBSTACULOS_TELA = 5  # Número máximo de obstáculos simultâneos

# Inicialização do Pygame e da tela principal
pygame.init()
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Runner's Quest")
relogio = pygame.time.Clock()

# Grupos de sprites
grupo_jogador = pygame.sprite.GroupSingle()
grupo_obstaculos = pygame.sprite.Group()

# Carregamento do cenário
cenario = pygame.image.load("recursos/imagens/background/fase_1/fundo_fase_1.png").convert()
cenario = pygame.transform.scale(cenario, (LARGURA_TELA, ALTURA_TELA))
cenario_largura = cenario.get_width()
cenario_x1 = 0
cenario_x2 = cenario_largura

# Temporizador global
tempo_ultimo_obstaculo = pygame.time.get_ticks()


def exibir_game_over():
    """Exibe a mensagem de 'Game Over' na tela."""
    font = pygame.font.Font(None, 74)
    texto_game_over = font.render("Game Over", True, (255, 0, 0))
    tela.blit(texto_game_over, (250, 150))
    pygame.display.flip()
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

    # Exibe a tela inicial antes do menu
    exibir_tela_inicial(tela)

    # Configurações visuais do menu principal
    fundo = pygame.image.load("recursos/imagens/background/title_screen.jpg").convert()
    fundo = pygame.transform.scale(fundo, tela.get_size())
    cor_titulo = (255, 255, 255)
    fonte_titulo = pygame.font.Font("recursos/fontes/title_screen.ttf", 48)

    largura_tela, altura_tela = tela.get_size()
    pos_titulo_x = largura_tela // 2
    pos_titulo_y = (altura_tela // 4) - 50

    # Exibe o menu principal
    acao = exibir_menu(tela, fundo, fonte_titulo, cor_titulo, pos_titulo_x, pos_titulo_y)

    if acao == "INICIAR_JOGO":
        # Exibe a tela de seleção de personagem
        personagem_escolhido = exibir_selecao_personagem(
            tela, fundo, fonte_titulo, cor_titulo, pos_titulo_x, pos_titulo_y
        )

        # Carrega o personagem escolhido
        jogador = Player(personagem_escolhido)
        grupo_jogador.add(jogador)

        # Carrega o cenário e a música da fase 1
        carregar_fase_1(tela)

        running = True
        jogador_morto = False
        tempo_inicio_dead = 0

        # Controle de tempo da fase
        tempo_fase = 0
        DURACAO_FASE_1 = 60000  # Duração de 60 segundos

        while running:
            tela.fill(BRANCO)

            if not jogador_morto:
                atualizar_cenario()

            teclas = pygame.key.get_pressed()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    running = False

            if not jogador_morto:
                grupo_jogador.update(teclas)

            # Desenha o jogador
            grupo_jogador.draw(tela)
            pygame.draw.rect(tela, (0, 255, 0), jogador.hitbox, 2)  # Verde para hitbox

            if not jogador_morto:
                tempo_atual = pygame.time.get_ticks()

                # Geração controlada de obstáculos
                if len(grupo_obstaculos) < MAX_OBSTACULOS_TELA:
                    if tempo_atual - tempo_ultimo_obstaculo > INTERVALO_OBSTACULOS:
                        gerar_obstaculos_fase_1(grupo_obstaculos, velocidade=5)
                        tempo_ultimo_obstaculo = tempo_atual

                grupo_obstaculos.update()

            # Desenha os obstáculos
            grupo_obstaculos.draw(tela)

            # Força o desenho manual caso draw não funcione corretamente
            for obstaculo in grupo_obstaculos:
                tela.blit(obstaculo.image, obstaculo.rect.topleft)  # Desenho manual
                pygame.draw.rect(tela, (255, 0, 0), obstaculo.rect, 2)  # Hitbox

            if not jogador_morto:
                # Verifica colisões
                for obstaculo in grupo_obstaculos:
                    if jogador.hitbox.colliderect(obstaculo.rect):
                        jogador.estado = "morto"
                        jogador_morto = True
                        tempo_inicio_dead = pygame.time.get_ticks()
                        break

            if jogador_morto:
                jogador.executar_animacao_dead()
                grupo_jogador.draw(tela)
                grupo_obstaculos.draw(tela)

                if pygame.time.get_ticks() - tempo_inicio_dead > 1000:
                    exibir_game_over()
                    running = False

            # Controle do tempo da fase
            tempo_fase += relogio.get_time()
            if tempo_fase >= DURACAO_FASE_1:
                print("Fase 1 concluída!")  # Substitua pela transição para a próxima fase
                running = False

            pygame.display.flip()
            relogio.tick(60)

        pygame.mixer.music.stop()
        pygame.quit()


if __name__ == "__main__":
    main()
