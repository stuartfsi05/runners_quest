import pygame


class Obstaculo(pygame.sprite.Sprite):
    """Classe para representar os obstáculos no jogo."""

    def __init__(self, velocidade: int, tipo: str = "padrao") -> None:
        """
        Inicializa o obstáculo com velocidade e configurações visuais.
        
        Args:
            velocidade (int): Velocidade horizontal do obstáculo.
            tipo (str): Tipo de obstáculo (padrão: "padrao"). Pode ser usado para variações visuais.
        """
        super().__init__()

        # Caminho base para recursos de obstáculos
        base_path = "recursos/imagens/obstaculos"

        # Configuração visual do obstáculo com base no tipo
        if tipo == "padrao":
            self.image = pygame.Surface((40, 40))
            self.image.fill((255, 0, 0))  # Cor vermelha para o obstáculo padrão
        elif tipo == "spike":
            self.image = pygame.image.load(f"{base_path}/spike.png").convert_alpha()
        elif tipo == "block":
            self.image = pygame.image.load(f"{base_path}/block.png").convert_alpha()
        else:
            raise ValueError(f"Tipo de obstáculo inválido: {tipo}")

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
