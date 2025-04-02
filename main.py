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
        texto = fonte.render(f"Pontuação: {self.pontos}", True, (0, 0, 0))  # Preto
        tela.blit(texto, (10, 10))


def exibir_game_over(tela: pygame.Surface, fonte: pygame.font.Font) -> None:
    """Exibe a mensagem de 'Game Over' no cenário atual."""
    texto_game_over = fonte.render("Game Over", True, (255, 0, 0))
    texto_pos = texto_game_over.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2))
    tela.blit(texto_game_over, texto_pos)
    pygame.display.flip()
    pygame.time.wait(3000)  # Aguarda 3 segundos antes de encerrar


def atualizar_cenario(cenario, cenario_largura, cenario_x1, cenario_x2):
    """Atualiza o movimento do cenário para criar a ilusão de deslocamento."""
    cenario_x1 -= 2
    cenario_x2 -= 2

    if cenario_x1 <= -cenario_largura:
        cenario_x1 = cenario_x2 + cenario_largura
    if cenario_x2 <= -cenario_largura:
        cenario_x2 = cenario_x1 + cenario_largura

    tela.blit(cenario, (cenario_x1, 0))
    tela.blit(cenario, (cenario_x2, 0))

    return cenario_x1, cenario_x2


def main():
    """Loop principal do jogo."""
    pontuacao = Pontuacao()
    fonte_pontuacao = pygame.font.Font(None, 36)
    tempo_ultimo_obstaculo = pygame.time.get_ticks()
    tempo_ultimo_incremento = pygame.time.get_ticks()  # Controle de tempo para pontuação

    exibir_tela_inicial(tela)

    fundo = pygame.image.load("recursos/imagens/background/title_screen.jpg").convert()
    fundo = pygame.transform.scale(fundo, tela.get_size())
    cor_titulo = (255, 255, 255)
    fonte_titulo = pygame.font.Font("recursos/fontes/title_screen.ttf", 48)

    largura_tela, altura_tela = tela.get_size()
    pos_titulo_x = largura_tela // 2
    pos_titulo_y = (altura_tela // 4) - 50

    acao = exibir_menu(tela, fundo, fonte_titulo, cor_titulo, pos_titulo_x, pos_titulo_y)

    if acao == "INICIAR_JOGO":
        personagem_escolhido = exibir_selecao_personagem(
            tela, fundo, fonte_titulo, cor_titulo, pos_titulo_x, pos_titulo_y
        )

        jogador = Player(personagem_escolhido)
        grupo_jogador.add(jogador)

        carregar_fase_1(tela)

        running = True
        jogador_morto = False
        tempo_inicio_dead = 0

        cenario = pygame.image.load(
            "recursos/imagens/background/fase_1/fundo_fase_1.png"
        ).convert()
        cenario = pygame.transform.scale(cenario, (LARGURA_TELA, ALTURA_TELA))
        cenario_largura = cenario.get_width()
        cenario_x1 = 0
        cenario_x2 = cenario_largura

        while running:
            if not jogador_morto:
                tela.fill(BRANCO)
                cenario_x1, cenario_x2 = atualizar_cenario(
                    cenario, cenario_largura, cenario_x1, cenario_x2
                )
            else:
                tela.blit(cenario, (cenario_x1, 0))
                tela.blit(cenario, (cenario_x2, 0))

            teclas = pygame.key.get_pressed()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    running = False

            if not jogador_morto:
                grupo_jogador.update(teclas)

            grupo_jogador.draw(tela)

            if not jogador_morto:
                tempo_atual = pygame.time.get_ticks()

                if len(grupo_obstaculos) < MAX_OBSTACULOS_TELA:
                    if tempo_atual - tempo_ultimo_obstaculo > INTERVALO_OBSTACULOS:
                        gerar_obstaculos_fase_1(grupo_obstaculos, velocidade=5)
                        tempo_ultimo_obstaculo = tempo_atual

                grupo_obstaculos.update()

            grupo_obstaculos.draw(tela)

            for obstaculo in grupo_obstaculos:
                tela.blit(obstaculo.image, obstaculo.rect.topleft)

                if not jogador_morto and jogador.hitbox.colliderect(obstaculo.hitbox):
                    jogador.estado = "morto"
                    jogador_morto = True
                    tempo_inicio_dead = pygame.time.get_ticks()
                    break

            if jogador_morto:
                jogador.executar_animacao_dead()
                grupo_jogador.draw(tela)
                grupo_obstaculos.draw(tela)

                if pygame.time.get_ticks() - tempo_inicio_dead > 1000:
                    exibir_game_over(tela, fonte_titulo)
                    running = False

            if not jogador_morto:
                tempo_atual = pygame.time.get_ticks()
                if tempo_atual - tempo_ultimo_incremento > 500:  # Incrementa a cada 500ms
                    pontuacao.incrementar(1)
                    tempo_ultimo_incremento = tempo_atual

            pontuacao.exibir(tela, fonte_pontuacao)

            pygame.display.flip()
            relogio.tick(60)

        pygame.mixer.music.stop()
        pygame.quit()


if __name__ == "__main__":
    main()