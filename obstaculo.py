import pygame
import os


class Obstaculo(pygame.sprite.Sprite):
    """Classe para representar os obstáculos no jogo."""

    def __init__(self, velocidade: int, tipo: str = "tronco") -> None:
        """
        Inicializa o obstáculo com velocidade e configurações visuais.

        Args:
            velocidade (int): Velocidade horizontal do obstáculo.
            tipo (str): Tipo de obstáculo ("tronco" ou "galho").
        """
        super().__init__()

        # Armazena o tipo do obstáculo
        self.tipo = tipo

        # Caminho base para recursos de obstáculos
        base_path = "recursos/imagens/obstaculos"

        # Tentativa de carregar a imagem do obstáculo
        try:
            if self.tipo == "tronco":
                image_path = f"{base_path}/tronco.png"
                self.image = pygame.image.load(image_path).convert_alpha()
                print(f"Imagem tronco carregada com sucesso! {image_path}")
            elif self.tipo == "galho":
                image_path = f"{base_path}/galho.png"
                self.image = pygame.image.load(image_path).convert_alpha()
                print(f"Imagem galho carregada com sucesso! {image_path}")
            else:
                raise ValueError(f"Tipo de obstáculo inválido: {self.tipo}")
        except pygame.error as e:
            # Fallback para representação visual temporária
            print(f"Erro ao carregar imagem do obstáculo '{self.tipo}': {e}")
            self.image = pygame.Surface((50, 20) if self.tipo == "tronco" else (60, 15))
            self.image.fill((255, 0, 0) if self.tipo == "tronco" else (0, 255, 0))

        # Verificação adicional se o arquivo existe no sistema
        image_file = f"{base_path}/{self.tipo}.png"
        if not os.path.exists(image_file):
            print(f"Erro: O arquivo '{self.tipo}.png' não foi encontrado no diretório '{base_path}'.")

        # Configuração inicial do hitbox
        self.rect = self.image.get_rect()

        # Configurações específicas para cada tipo de obstáculo
        if self.tipo == "tronco":
            largura_hitbox = 100  # Largura exata da linha azul (ajustar conforme necessário)
            altura_hitbox = 30    # Altura exata da linha azul
            ajuste_vertical = 50  # Deslocamento vertical para alinhar com a linha azul
        elif self.tipo == "galho":
            largura_hitbox = 70   # Largura para galho
            altura_hitbox = 20    # Altura para galho
            ajuste_vertical = 15  # Ajuste para centralizar o hitbox no galho

        # Atualiza o tamanho da hitbox para corresponder às dimensões ideais
        self.rect = pygame.Rect(
            self.rect.x, self.rect.y,
            largura_hitbox, altura_hitbox
        )

        # Centraliza o hitbox horizontalmente e ajusta verticalmente
        self.rect.centerx = self.image.get_rect().centerx
        self.rect.centery = self.image.get_rect().centery + ajuste_vertical

        # Configuração inicial da posição
        self.rect.x = 800  # Começa fora da tela, à direita

        # Velocidade do movimento horizontal
        self.velocidade = velocidade

    def update(self) -> None:
        """Atualiza a posição do obstáculo na tela."""
        self.rect.x -= self.velocidade  # Move o obstáculo para a esquerda

        # Mensagens de depuração para rastrear movimento e remoção
        if self.rect.x == 800:
            print(f"Obstáculo {self.tipo} gerado na posição inicial: {self.rect.x}, {self.rect.y}")
        if self.rect.right <= 0:
            print(f"Obstáculo {self.tipo} removido na posição final: {self.rect.x}, {self.rect.y}")
            self.kill()
