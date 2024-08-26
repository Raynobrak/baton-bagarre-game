import pygame

class ImageManager():
    images = dict() # static attribute

    def __init__(self):
        pass
    
    def load_image(self, path, key):
        image = pygame.image.load(path).convert_alpha()
        ImageManager.images.update({key : image})

    def get_image(self, key):
        return ImageManager.images[key]