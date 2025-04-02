import pygame
from obstaculo import Obstaculo
from interface import exibir_tela_inicial
from menu import exibir_menu
from selecao_personagem import exibir_selecao_personagem
from player import Player
from fase_1 import carregar_fase_1, gerar_obstaculos_fase_1

# Constantes do jogo
LARGURA_TELA = 800
ALTURA_TELA = 400
BRANCO = (255, 255, 255)
INTERVALO_OBSTACULOS = 3000  # Intervalo entre geração de obstáculos (ms)
MAX_OBSTACULOS_TELA = 5      # Máximo de obstáculos simultâneos

# Inicialização do Pygame
pygame.init()
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Runner's Quest")
relogio = pygame.time.Clock()


class Pontuacao:
    """Gerenciador de pontuação do jogo."""

    def __init__(self):
        self.pontos = 0

    def incrementar(self, valor: int) -> None:
        """Incrementa os pontos."""
        self.pontos += valor

    def resetar(self) -> None:
        """Reseta a pontuação."""
        self.pontos = 0

    def exibir(self, tela: pygame.Surface, fonte: pygame.font.Font) -> None:
        """Exibe os pontos na tela."""
        texto = fonte.render(f"Pontuação: {self.pontos}", True, (0, 0, 0))
        tela.blit(texto, (10, 10))


def atualizar_cenario(
    cenario: pygame.Surface,
    largura_cenario: int,
    x1: int,
    x2: int,
    velocidade: int = 2
):
    """
    Atualiza o movimento do cenário para criar a ilusão de deslocamento.

    Args:
        cenario: Superfície do cenário.
        largura_cenario: Largura total do cenário.
        x1: Posição atual do primeiro cenário.
        x2: Posição atual do segundo cenário.
        velocidade: Velocidade do deslocamento do cenário.

    Returns:
        Tuple contendo as novas posições (x1, x2).
    """
    x1 -= velocidade
    x2 -= velocidade

    if x1 <= -largura_cenario:
        x1 = x2 + largura_cenario
    if x2 <= -largura_cenario:
        x2 = x1 + largura_cenario

    tela.blit(cenario, (x1, 0))
    tela.blit(cenario, (x2, 0))

    return x1, x2


def exibir_game_over(
    tela: pygame.Surface,
    cenario: pygame.Surface,
    cenario_x1: int,
    cenario_x2: int,
    largura_cenario: int
) -> bool:
    """
    Exibe a mensagem de 'Game Over' com cenário rolando e opção de jogar novamente.

    Retorna:
        True se o jogador optar por jogar novamente (S), False se optar por sair (N).
    """
    # Carrega e toca o tema de Game Over em loop
    pygame.mixer.music.load("recursos/sons/ending.wav")
    pygame.mixer.music.play(-1)

    # Fontes para o texto
    fonte_game_over = pygame.font.Font("recursos/fontes/title_screen.ttf", 48)
    fonte_opcao = pygame.font.Font("recursos/fontes/title_screen.ttf", 32)

    clock = pygame.time.Clock()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_s:  # 'S' para sim (jogar novamente)
                    return True
                elif evento.key == pygame.K_n:  # 'N' para não (sair)
                    return False

        # Atualiza e desenha o cenário rolando
        cenario_x1, cenario_x2 = atualizar_cenario(
            cenario, largura_cenario, cenario_x1, cenario_x2
        )

        # Renderiza texto "Game Over"
        texto_game_over = fonte_game_over.render("GAME OVER", True, (255, 0, 0))
        rect_game_over = texto_game_over.get_rect(
            center=(LARGURA_TELA // 2, ALTURA_TELA // 2 - 50)
        )
        tela.blit(texto_game_over, rect_game_over)

        # Renderiza texto "Jogar novamente? (S/N)"
        texto_opcao = fonte_opcao.render("Jogar novamente? (S ou N)", True, (0, 0, 0))
        rect_opcao = texto_opcao.get_rect(
            center=(LARGURA_TELA // 2, ALTURA_TELA // 2 + 20)
        )
        tela.blit(texto_opcao, rect_opcao)

        pygame.display.flip()
        clock.tick(60)


def main():
    """Loop principal do jogo."""
    while True:
        # Inicializa a pontuação e variáveis de controle
        pontuacao = Pontuacao()
        fonte_pontuacao = pygame.font.Font(None, 36)
        tempo_ultimo_obstaculo = pygame.time.get_ticks()
        tempo_ultimo_incremento = pygame.time.get_ticks()

        # Exibe tela inicial
        exibir_tela_inicial(tela)

        # Carregamento do fundo (title screen) e configurações iniciais
        fundo = pygame.image.load("recursos/imagens/background/title_screen.jpg").convert()
        fundo = pygame.transform.scale(fundo, tela.get_size())
        cor_titulo = (255, 255, 255)
        fonte_titulo = pygame.font.Font("recursos/fontes/title_screen.ttf", 48)

        largura_tela, altura_tela = tela.get_size()
        pos_titulo_x = largura_tela // 2
        pos_titulo_y = (altura_tela // 4) - 50

        # Menu inicial
        acao = exibir_menu(tela, fundo, fonte_titulo, cor_titulo, pos_titulo_x, pos_titulo_y)
        if acao != "INICIAR_JOGO":
            break

        # Seleciona personagem
        personagem_escolhido = exibir_selecao_personagem(
            tela, fundo, fonte_titulo, cor_titulo, pos_titulo_x, pos_titulo_y
        )

        # Cria grupos de sprites
        jogador = Player(personagem_escolhido)
        grupo_jogador = pygame.sprite.GroupSingle(jogador)
        grupo_obstaculos = pygame.sprite.Group()

        # Carrega fase 1
        carregar_fase_1(tela)

        running = True
        jogador_morto = False
        tempo_inicio_dead = 0

        # Carrega cenário da fase
        cenario = pygame.image.load(
            "recursos/imagens/background/fase_1/fundo_fase_1.png"
        ).convert()
        cenario = pygame.transform.scale(cenario, (LARGURA_TELA, ALTURA_TELA))
        largura_cenario = cenario.get_width()
        cenario_x1 = 0
        cenario_x2 = largura_cenario

        # Loop principal da fase
        while running:
            if not jogador_morto:
                # Atualiza cenário rolando
                tela.fill(BRANCO)
                cenario_x1, cenario_x2 = atualizar_cenario(
                    cenario, largura_cenario, cenario_x1, cenario_x2
                )
            else:
                # Se o jogador estiver morto, apenas exibe o cenário congelado
                tela.blit(cenario, (cenario_x1, 0))
                tela.blit(cenario, (cenario_x2, 0))

            teclas = pygame.key.get_pressed()
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    return

            # Atualiza jogador
            if not jogador_morto:
                grupo_jogador.update(teclas)

            grupo_jogador.draw(tela)

            # Atualiza e desenha obstáculos
            if not jogador_morto:
                tempo_atual = pygame.time.get_ticks()

                # Gera novos obstáculos se necessário
                if len(grupo_obstaculos) < MAX_OBSTACULOS_TELA:
                    if tempo_atual - tempo_ultimo_obstaculo > INTERVALO_OBSTACULOS:
                        gerar_obstaculos_fase_1(grupo_obstaculos, velocidade=5)
                        tempo_ultimo_obstaculo = tempo_atual

                grupo_obstaculos.update()

            grupo_obstaculos.draw(tela)

            # Verifica colisão
            for obstaculo in grupo_obstaculos:
                tela.blit(obstaculo.image, obstaculo.rect.topleft)
                if not jogador_morto and jogador.hitbox.colliderect(obstaculo.hitbox):
                    jogador.estado = "morto"
                    jogador_morto = True
                    tempo_inicio_dead = pygame.time.get_ticks()
                    break

            # Se o jogador morreu, executa animação de morte
            if jogador_morto:
                jogador.executar_animacao_dead()
                grupo_jogador.draw(tela)
                grupo_obstaculos.draw(tela)

                # Espera um pequeno intervalo antes de encerrar a fase
                if pygame.time.get_ticks() - tempo_inicio_dead > 1000:
                    running = False

            # Incrementa pontuação
            if not jogador_morto:
                tempo_atual = pygame.time.get_ticks()
                if tempo_atual - tempo_ultimo_incremento > 500:
                    pontuacao.incrementar(1)
                    tempo_ultimo_incremento = tempo_atual

            # Exibe pontuação
            pontuacao.exibir(tela, fonte_pontuacao)

            pygame.display.flip()
            relogio.tick(60)

        # Para a música atual
        pygame.mixer.music.stop()

        # Exibe tela de Game Over, mantendo o cenário rolando
        jogar_novamente = exibir_game_over(
            tela, cenario, cenario_x1, cenario_x2, largura_cenario
        )
        # Se o jogador não quiser jogar novamente, encerra o loop principal
        if not jogar_novamente:
            break

    pygame.quit()


if __name__ == "__main__":
    main()
