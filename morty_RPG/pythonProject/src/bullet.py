import pygame
import math


#definir la classe qui va gérer le projectile de notre joueur
class Playerbullet(pygame.sprite.Sprite):

    #définir le constructeur
    def __init__(self, player, mouse_x, mouse_y):

        super().__init__()
        self.velocity = 5
        self.player = player
        self.image = pygame.image.load('./sprite/projectile.png')
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = 300
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y
        self.angle = math.atan2(self.rect.y - self.mouse_y, self.rect.x - self.mouse_x)
        self.x_vel = math.cos(self.angle) * self.velocity
        self.y_vel = math.sin(self.angle) * self.velocity


# fait déplacer les projectiles en partznt du joueur
    def move_player(self):
        self.rect.x -= int(self.x_vel)
        self.rect.y -= int(self.y_vel)

    def move_npc(self):
        # collision projectile et monstre
        self.rect.y += self.velocity
        #collision projectile et monstre
        """for monster in self.player.game.check_collision(self, self.player.game.all_monnsters):
            self.remove()
            # infliger les dégats et le nombre de degat
            monster.damage(self.player.attack)"""

    def remove(self):
        self.player.all_projectiles.remove(self)

    def verify(self):
        # vérifier si le projectile est encore dans l'écran
        if self.rect.x > 800 or self.rect.y > 600:
            # suprrimer le projectile (en dehors de de l'écran)
            self.remove()