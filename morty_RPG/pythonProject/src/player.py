import pygame

from src.bullet import Playerbullet
from src.animation import AnimateSprite


class Entity(AnimateSprite):

    def __init__(self, name, x, y):
        super().__init__(name)
        self.all_projectiles_player = pygame.sprite.Group()
        self.image = self.get_image(0, 0)
        self.image.set_colorkey([0, 0, 0])
        self.position = [x, y]
        self.speed = 3
        self.health = 100
        self.health_max = 100
        self.attack = 5
        self.velocity = 2



        self.rect = pygame.Rect(self.position[0], self.position[1], 32, 32) #rectangle de l'entité
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)
        self.old_position = self.position.copy()

    def save_location(self):
        self.old_position = self.position.copy()

    def move_right(self):
        self.position[0] += self.speed
        self.change_animation('right')

    def move_left(self):
        self.position[0] -= self.speed
        self.change_animation('left')

    def move_up(self):
        self.position[1] -= self.speed
        self.change_animation('up')

    def move_down(self):
        self.position[1] += self.speed
        self.change_animation('down')

    def move_back(self):
        self.position = self.old_position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def update(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def damage(self, amount):
        # infliger les dégat
        self.health -= amount


    def update_health_bar(self, surface):
        # le déssin , la position et la couleur de la bar de vie
        #En premier temps la l'arriére plan de la bar de vie (gris)
        pygame.draw.rect(surface, (255, 0, 0), [600, 0, self.health_max, 5])
        #En deuxiéme temps la bar de vie (vert)
        pygame.draw.rect(surface, (255, 0, 0), [600, 0, self.health, 5])

class Player(Entity):

    def __init__(self):
        super().__init__("morty", 0, 0)

    def launch_projectile_player(self, mouse_x, mouse_y):
        #creer une nouvelle instance de la classe projectile
        self.all_projectiles_player.add(Playerbullet(self, mouse_x, mouse_y))

    #vérifie si le joueur est encore en vie
    def check_live(self):
        if self.health > 0:
            is_playing = True
        else:
            is_playing = False
        return is_playing


class NPC(Entity):

    def __init__(self, name, nb_points):
        super().__init__(name, 0, 0) #49:00 chemin du PNJ
        self.nb_points = nb_points
        self.points = []
        self.name = name
        self.speed = 3
        self.current_point = 0
        self.all_projectiles_npc = pygame.sprite.Group()


    #le joueur bouge en fonction du chemin tracé sur tiled
    def move(self):

        current_point = self.current_point
        target_point = self.current_point + 1

        if target_point >= self.nb_points:
            target_point = 0

        current_rect = self.points[current_point]
        target_rect = self.points[target_point]

        if current_rect.y < target_rect.y and abs(current_rect.x - target_rect.x) < 3:
            self.move_down()
        elif current_rect.y > target_rect.y and abs(current_rect.x - target_rect.x) < 3:
            self.move_up()
        elif current_rect.x > target_rect.x and abs(current_rect.y - target_rect.y) < 3:
            self.move_left()
        elif current_rect.x < target_rect.x and abs(current_rect.y - target_rect.y) < 3:
            self.move_right()

        if self.rect.colliderect(target_rect):
            self.current_point = target_point

    #téléporte le NPC à son premier point de spawn
    def teleport_spawn(self):
        location = self.points[self.current_point]
        self.position[0] = location.x
        self.position[1] = location.y
        self.save_location()

    #récupère tous les points de chemin du NPC
    def load_points(self, map):
        for num in range(1, self.nb_points+1):
            point = map.get_object_by_name(f"{self.name}_path{num}")
            rect = pygame.Rect(point.x, point.y, point.width, point.height)
            self.points.append(rect)


    def verify_npc_alive(self):
        # vérifier si le npc est oujours en vie
        if self.health <= 0:
            # suprrimer le npc
            self.remove()

    """def launch_projectile_npc(self, x, y):
        #creer une nouvelle instance de la classe projectile*
        self.all_projectiles_npc.add(Playerbullet(self, x, y))"""