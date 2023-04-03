import pygame


class SoundManager:
    def __init__(self):
        self.sounds = {
            'fond': pygame.mixer.Sound("./sound/fond.ogg"),
            'fin' : pygame.mixer.Sound("./sound/generique_fin.ogg"),
            'generique': pygame.mixer.Sound(".\sound\générique.ogg"),
            'morty_mort': pygame.mixer.Sound(".\sound\mort_morty.ogg")
        }

    def play(self, name, loop):
        self.sounds[name].play(loop)

    def stop(self, name):
        self.sounds[name].stop()