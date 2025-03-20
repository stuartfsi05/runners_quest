import pygame


class Obstaculo(pygame.sprite.Sprite):
    """Classe para representar os obstáculos no jogo."""

    def __init__(self, velocidade: int) -> None:
        """Inicializa o obstáculo com velocidade e configurações visuais."""
        super().__init__()

        # Configuração visual do obstáculo (exemplo: quadrado vermelho)
        self.image = pygame.Surface((40, 40))
        self.image.fill((255, 0, 0))  # Cor vermelha para o obstáculo
        self.rect = self.image.get_rect()

        # Posicionamento inicial fora da tela (lado direito)
        self.rect.x = 800
        self.rect.y = 320

        # Velocidade do movimento horizontal
        self.velocidade = velocidade

    def update(self) -> None:
        """Atualiza a posição do obstáculo na tela."""
        self.rect.x -= self.velocidade  # Move o obstáculo para a esquerda

        # Remove o obstáculo se sair completamente da tela
        if self.rect.right < 0:
            self.kill()
