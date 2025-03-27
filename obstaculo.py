import os
import pygame


class Obstaculo(pygame.sprite.Sprite):
    """Classe para representar os obstáculos no jogo."""

    BASE_PATH = "recursos/imagens/obstaculos"
    CONFIGS = {
        "tronco": {"size": (100, 50)},  # Dimensões ajustadas da hitbox
        "galho": {"size": (70, 30)},   # Dimensões ajustadas para o galho
    }

    def __init__(self, velocidade: int, tipo: str = "tronco") -> None:
        """
        Inicializa o obstáculo com velocidade e configurações visuais.

        Args:
            velocidade (int): Velocidade horizontal do obstáculo.
            tipo (str): Tipo de obstáculo ("tronco" ou "galho").
        """
        super().__init__()
        self.tipo = tipo
        self.velocidade = velocidade

        self.image = self._carregar_imagem()
        self._configurar_rect()
        self._configurar_hitbox()

    def _carregar_imagem(self) -> pygame.Surface:
        """Carrega a imagem do obstáculo ou cria um fallback visual."""
        image_path = os.path.join(self.BASE_PATH, f"{self.tipo}.png")
        if os.path.exists(image_path):
            return pygame.image.load(image_path).convert_alpha()

        print(f"[ERRO] Imagem '{self.tipo}.png' não encontrada. Usando fallback.")
        size = self.CONFIGS.get(self.tipo, {"size": (50, 20)})["size"]
        surface = pygame.Surface(size)
        surface.fill((255, 0, 0) if self.tipo == "tronco" else (0, 255, 0))
        return surface

    def _configurar_rect(self) -> None:
        """Configura o retângulo principal baseado na imagem."""
        bounding_rect = self.image.get_bounding_rect()
        self.rect = pygame.Rect(800, 250, bounding_rect.width, bounding_rect.height)

    def _configurar_hitbox(self) -> None:
        """Configura a hitbox baseada no tipo de obstáculo."""
        bounding_rect = self.image.get_bounding_rect()
        hitbox_width = bounding_rect.width - 5  # Ajuste fino na largura
        hitbox_height = bounding_rect.height - 5  # Ajuste fino na altura

        if self.tipo == "tronco":
            # Ajuste específico para tronco
            self.hitbox = pygame.Rect(
                self.rect.x + 7,  # Movendo a hitbox 7px mais para a direita
                self.rect.y + 44,  # Movendo a hitbox 44px mais para baixo
                hitbox_width,
                hitbox_height
            )
        elif self.tipo == "galho":
            # Ajuste específico para galho
            self.hitbox = pygame.Rect(
                self.rect.x + 5,  # Movendo a hitbox 5px mais para a direita
                self.rect.y + 50,  # Movendo a hitbox 50px mais para baixo
                hitbox_width,
                hitbox_height
            )

        self.hitbox.centerx = self.rect.centerx  # Centraliza horizontalmente

    def update(self) -> None:
        """Atualiza a posição do obstáculo na tela."""
        self.rect.x -= self.velocidade

        # Atualiza a posição da hitbox com base no tipo
        if self.tipo == "tronco":
            self.hitbox.x = self.rect.x + 7  # Ajuste horizontal para tronco
            self.hitbox.y = self.rect.y + 44  # Ajuste vertical para tronco
        elif self.tipo == "galho":
            self.hitbox.x = self.rect.x + 5  # Ajuste horizontal para galho
            self.hitbox.y = self.rect.y + 20  # Ajuste vertical para galho

        if self.rect.right <= 0:
            print(f"[INFO] Obstáculo {self.tipo} removido: {self.rect.x}, {self.rect.y}")
            self.kill()

    def draw_hitbox(self, tela: pygame.Surface) -> None:
        """Desenha a hitbox para depuração."""
        pygame.draw.rect(tela, (255, 0, 0), self.hitbox, 2)  # Vermelho, espessura 2px
