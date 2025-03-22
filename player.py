import pygame
from game_utils import GRAVIDADE, PULO


class Player(pygame.sprite.Sprite):
    """Classe para representar o jogador no jogo."""

    def __init__(self, personagem: str):
        """
        Inicializa o jogador com base no personagem selecionado.
        :param personagem: Nome do personagem (Kael, Ryuji, Jinzo).
        """
        super().__init__()

        # Caminho base para os sprites do personagem
        base_path = f"recursos/imagens/{personagem.lower()}"

        # Carregar spritesheets específicos do personagem
        self.frames_corrida = self._carregar_spritesheet(f"{base_path}/spritesheet_run.png", 8)
        self.frames_jump = self._carregar_spritesheet(f"{base_path}/spritesheet_jump.png", 10)
        self.frames_dead = self._carregar_spritesheet(f"{base_path}/spritesheet_dead.png", 3)

        # Configuração inicial do sprite
        self.frame_atual = 0
        self.image = self.frames_corrida[self.frame_atual]

        # Ajustar o rect e hitbox inicial com base no sprite
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

        # Frame da animação "Dead"
        self.frame_dead_atual = 0

    def _carregar_spritesheet(self, caminho, num_frames):
        """Carrega e divide um spritesheet em frames."""
        spritesheet = pygame.image.load(caminho).convert_alpha()
        largura_frame = spritesheet.get_width() // num_frames
        altura_frame = spritesheet.get_height()

        return [
            spritesheet.subsurface(
                (i * largura_frame, 0, largura_frame, altura_frame)
            )
            for i in range(num_frames)
        ]

    def update(self, teclas):
        """Atualiza o movimento e a animação do jogador."""
        if self.estado == "morto":
            self.executar_animacao_dead()
            return

        if teclas[pygame.K_SPACE] and self.no_chao:
            self.velocidade_y = PULO
            self.no_chao = False
            self.estado = "pulando"

        # Aplicar gravidade
        self.velocidade_y += GRAVIDADE
        self.rect.y += self.velocidade_y

        # Limitar o jogador ao chão
        if self.rect.y >= 250:
            self.rect.y = 250
            self.velocidade_y = 0
            self.no_chao = True
            self.estado = "correndo"

        # Atualizar a animação e a posição da hitbox
        self.atualizar_animacao()
        self.hitbox.topleft = (self.rect.x + 35, self.rect.y + 55)

    def atualizar_animacao(self):
        """Troca o frame do spritesheet com base no estado do jogador."""
        tempo_atual = pygame.time.get_ticks()

        if tempo_atual - self.tempo_ultima_atualizacao > self.intervalo_animacao:
            self.tempo_ultima_atualizacao = tempo_atual

            if self.estado == "correndo":
                self.frame_atual = (self.frame_atual + 1) % len(self.frames_corrida)
                self.image = self.frames_corrida[self.frame_atual]
            elif self.estado == "pulando":
                self.frame_atual = (self.frame_atual + 1) % len(self.frames_jump)
                self.image = self.frames_jump[self.frame_atual]

            # Atualizar o rect e a hitbox com base no novo frame
            bounding_rect = self.image.get_bounding_rect()
            self.rect.size = bounding_rect.size
            self.hitbox = self.rect.inflate(0, 0)

    def executar_animacao_dead(self):
        """Executa a animação de 'morto'."""
        tempo_atual = pygame.time.get_ticks()

        if tempo_atual - self.tempo_ultima_atualizacao > self.intervalo_animacao:
            self.tempo_ultima_atualizacao = tempo_atual

            if self.frame_dead_atual < len(self.frames_dead) - 1:
                self.frame_dead_atual += 1
            self.image = self.frames_dead[self.frame_dead_atual]

    def draw_hitbox(self, tela):
        """Desenha a hitbox na tela."""
        cor_hitbox = (0, 255, 0)  # Verde
        espessura_hitbox = 2  # 2px
        pygame.draw.rect(tela, cor_hitbox, self.hitbox, espessura_hitbox)
