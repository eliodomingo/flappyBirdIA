import pygame
import os

# Importer les images de l'oiseau
BIRD_IMAGES = [pygame.transform.scale2x(pygame.image.load(
    os.path.join("images", "bird1.png")
)), pygame.transform.scale2x(pygame.image.load(
    os.path.join("images", "bird2.png")
)), pygame.transform.scale2x(pygame.image.load(
    os.path.join("images", "bird3.png")
))]

# Classe de l'oiseau
class Bird:
    IMAGES = BIRD_IMAGES
    MAX_ROTATION = 25
    ROTATION_VELOCITY = 20
    ANIMATION_TIME = 5

    # Constructeur
    def __init__(self, x, y):
        self.x = x
        self.y = y
        # Orientation de l'oiseau
        self.tilt = 0
        self.tick_count = 0
        self.velocity = 0
        self.height = self.y
        self.image_count = 0
        self.image = self.IMAGES[0]

    # Pour sauter
    def jump(self):
        self.velocity = -10.5
        self.tick_count = 0
        self.height = self.y

    # Pour se déplacer
    def move(self):
        self.tick_count += 1
        
        # Equation physique pour faire la parabole du saut
        displacement = self.velocity * self.tick_count + 1.5 * self.tick_count**2
        
        # Vitesse de chute max 
        if displacement >= 16:
            displacement = 16

        if displacement < 0:
            displacement -= 2
        # On déplace
        self.y = self.y + displacement

        # Orientation de l'oiseau
        # Ici vers le haut
        if displacement < 0 or self.y < self.height + 50:
             if self.tilt < self.MAX_ROTATION:
                 self.tilt = self.MAX_ROTATION
        # Ici vers le bas
        else:
            if self.tilt > -90:
                self.tilt -= self.ROTATION_VELOCITY

    # Dessiner l'oiseau et son animation
    def draw(self, window):
        self.image_count += 1

        if self.image_count < self.ANIMATION_TIME:
            self.image = self.IMAGES[0]
        elif self.image_count < self.ANIMATION_TIME * 2:
            self.image = self.IMAGES[1]
        elif self.image_count < self.ANIMATION_TIME * 3:
            self.image = self.IMAGES[2]
        elif self.image_count < self.ANIMATION_TIME * 4:
            self.image = self.IMAGES[1]
        elif self.image_count == self.ANIMATION_TIME * 4 + 1:
            self.image = self.IMAGES[0]
            self.image_count = 0
        
        if self.tilt <= -90:
            self.img = self.IMAGES[1]
            self.image_count = self.ANIMATION_TIME * 2

        # Gérer la rotation de l'image
        rotated_image = pygame.transform.rotate(self.image, self.tilt)
        new_rectangle = rotated_image.get_rect(center=self.image.get_rect(topleft = (self.x, self.y)).center)
        window.blit(rotated_image, new_rectangle.topleft)

    # Gérer les collisions
    def get_mask(self):
        return pygame.mask.from_surface(self.image)