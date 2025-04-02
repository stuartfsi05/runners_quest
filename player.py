import pygame
from game_utils import GRAVIDADE, PULO


class Player(pygame.sprite.Sprite):
    """
    Classe para representar o jogador no jogo.
    """

    def __init__(self, personagem: str) -> None:
        """
        Inicializa o jogador com base no personagem selecionado.

        Args:
            personagem (str): Nome do personagem (Kael, Ryuji, Jinzo).
        """
        super().__init__()

        # Caminho base para os sprites do personagem
        base_path = f"recursos/imagens/{personagem.lower()}"

        # Configuração dos frames por personagem
        frames_config = {
            "kael": {"jump": 10, "dead": 3},
            "ryuji": {"jump": 12, "dead": 3},
            "jinzo": {"jump": 12, "dead": 4},
        }

        # Carregar spritesheets específicos do personagem
        self.frames_corrida = self._carregar_spritesheet(
            f"{base_path}/spritesheet_run.png", 8
        )
        self.frames_jump = self._carregar_spritesheet(
            f"{base_path}/spritesheet_jump.png", frames_config[personagem.lower()]["jump"]
        )
        self.frames_dead = self._carregar_spritesheet(
            f"{base_path}/spritesheet_dead.png", frames_config[personagem.lower()]["dead"]
        )

        # Configuração inicial do sprite
        self.frame_atual = 0
        self.image = self.frames_corrida[self.frame_atual]

        # Ajustar rect e hitbox inicial com base no sprite
        bounding_rect = self.image.get_bounding_rect()
        self.rect = pygame.Rect(50, 250, bounding_rect.width, bounding_rect.height)
        self.hitbox = self.rect.inflate(0, 0)

        # Física do jogador
        self.velocidade_y = 0
        self.no_chao = True
        self.estado = "correndo"  # Estados possíveis: "correndo", "pulando", "morto"

        # Controle de tempo para animação
        self.tempo_ultima_atualizacao = pygame.time.get_ticks()
        self.intervalo_animacao = 100

        # Frame da animação "morto"
        self.frame_dead_atual = 0

        # Sons do jogador
        self.som_pulo = pygame.mixer.Sound("recursos/sons/jump.wav")
        self.som_aterrissagem = pygame.mixer.Sound("recursos/sons/landing.wav")

        # Configuração dos volumes dos sons
        self.som_pulo.set_volume(1.0)
        self.som_aterrissagem.set_volume(1.0)

    def _carregar_spritesheet(self, caminho: str, num_frames: int) -> list:
        """
        Carrega e divide um spritesheet em frames.

        Args:
            caminho (str): Caminho do arquivo do spritesheet.
            num_frames (int): Número de frames no spritesheet.

        Returns:
            list: Lista de frames extraídos do spritesheet.
        """
        spritesheet = pygame.image.load(caminho).convert_alpha()
        largura_frame = spritesheet.get_width() // num_frames
        altura_frame = spritesheet.get_height()

        return [
            spritesheet.subsurface((i * largura_frame, 0, largura_frame, altura_frame))
            for i in range(num_frames)
        ]

    def update(self, teclas: pygame.key.ScancodeWrapper) -> None:
        """
        Atualiza o movimento e a animação do jogador.

        Args:
            teclas (pygame.key.ScancodeWrapper): Estado atual das teclas pressionadas.
        """
        if self.estado == "morto":
            self.executar_animacao_dead()
            return

        if teclas[pygame.K_SPACE] and self.no_chao:
            self.velocidade_y = PULO
            self.no_chao = False
            self.estado = "pulando"

            # Tocar som de pulo
            self.som_pulo.play()

        # Aplicar gravidade
        self.velocidade_y += GRAVIDADE
        self.rect.y += self.velocidade_y

        # Limitar o jogador ao chão
        if self.rect.y >= 250:
            if not self.no_chao:
                # Tocar som de aterrissagem somente se estava no ar
                self.som_aterrissagem.play()

            self.rect.y = 250
            self.velocidade_y = 0
            self.no_chao = True
            self.estado = "correndo"

        # Atualizar animação e posição da hitbox
        self.atualizar_animacao()
        self.hitbox.topleft = (self.rect.x + 35, self.rect.y + 55)

    def atualizar_animacao(self) -> None:
        """
        Troca o frame do spritesheet com base no estado do jogador.
        """
        tempo_atual = pygame.time.get_ticks()

        if tempo_atual - self.tempo_ultima_atualizacao > self.intervalo_animacao:
            self.tempo_ultima_atualizacao = tempo_atual

            if self.estado == "correndo":
                self.frame_atual = (self.frame_atual + 1) % len(self.frames_corrida)
                self.image = self.frames_corrida[self.frame_atual]
            elif self.estado == "pulando":
                self.frame_atual = (self.frame_atual + 1) % len(self.frames_jump)
                self.image = self.frames_jump[self.frame_atual]

            # Atualizar rect e hitbox com base no novo frame
            bounding_rect = self.image.get_bounding_rect()
            self.rect.size = bounding_rect.size
            self.hitbox = self.rect.inflate(0, 0)

    def executar_animacao_dead(self) -> None:
        """
        Executa a animação de 'morto'.
        """
        tempo_atual = pygame.time.get_ticks()

        if tempo_atual - self.tempo_ultima_atualizacao > self.intervalo_animacao:
            self.tempo_ultima_atualizacao = tempo_atual

            if self.frame_dead_atual < len(self.frames_dead) - 1:
                self.frame_dead_atual += 1
            self.image = self.frames_dead[self.frame_dead_atual]
