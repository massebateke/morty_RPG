from dataclasses import dataclass
import pygame, pytmx, pyscroll
from player import NPC
from src.sounds import SoundManager


@dataclass #représente des données
class Portal:
    from_world: str
    origin_point: str
    target_world: str
    teleport_point: str


@dataclass
class Map:
    name: str
    walls: list[pygame.Rect] #les murs: liste de rectangles de collision
    group: pyscroll.PyscrollGroup
    tmx_data: pytmx.TiledMap
    portals: list[Portal]
    npcs: list[NPC]
    objets: list[pygame.Rect]


class MapManager:

    def __init__(self, screen, player):
        self.soud_manager = SoundManager()
        self.all_ennemies = pygame.sprite.Group()
        self.maps = dict()
        self.screen = screen
        self.player = player
        self.current_map = "map01" #carte par défaut

        #Enregistrement de toutes les cartes avec leurs portails, leurs NPCS
        self.register_map("map01", portals=[
            Portal(from_world="map01", origin_point="exit_house01", target_world="map02", teleport_point="spawn_house02")])
        self.register_map("map02", portals=[
            Portal(from_world="map02", origin_point="exit_house02", target_world="map03", teleport_point="spawn_house03" )],
            npcs=[
            NPC("mechant", nb_points=2)
            ])
        self.register_map("map03", portals=[
            Portal(from_world="map03", origin_point="exit_house03", target_world="map04", teleport_point="spawn_house04")],
            npcs=[
            NPC("mechant", nb_points=2),
            NPC("mechant2", nb_points=2),
            NPC("mechant3", nb_points=1)
        ])
        self.register_map("map04")

        #téléportation du joeur à son premier point de spawn
        self.teleport_player("player")

        #téléportation de tous les NPCS dans toutes les maps
        self.teleport_npcs()



    #vérification de toutes les collisions
    def check_collisions(self):
        clock = pygame.time.Clock()
        #collisions avec les portails et téléportation
        for portal in self.get_map().portals:
            if portal.from_world == self.current_map:
                point = self.get_object(portal.origin_point)
                rect = pygame.Rect(point.x, point.y, point.width, point.height)

                if self.player.feet.colliderect(rect):
                    copy_portal = portal
                    self.current_map = portal.target_world
                    self.teleport_player(copy_portal.teleport_point)



        #collision avec les murs et les NPCS
        for sprite in self.get_group().sprites():
            win = False
            if type(sprite) is NPC:
                if sprite.rect.colliderect(self.player.rect):
                    #si le joueur rencontre un NPC, les deux s'arrêtent
                    sprite.speed = 0
                    #si le joueur touche un NPC il perd 50 points de vie
                    self.player.damage(10)


                else:
                    sprite.speed = 1
            #Nous avons essayé de faire perdre des points de vie au NPC s'il
            #rentre en collision avec un projectile
            #Nous n'avons pas pu aboutir
            """for projectile in self.player.all_projectiles_player:
                if type(sprite) is NPC:
                    if sprite.rect.colliderect(projectile.rect) > - 1:
                        print("yep")
                        sprite.damage(self.player.attack)
                        clock.tick(5)"""

            #si le joueur rencontre un mur, il retourne en arrière
            if sprite.rect.collidelist(self.get_walls()) > - 1:
                sprite.move_back()

            #si le joueur rencontre un objet, il récupère des points d'attaque ou de vie
            if sprite.rect.collidelist(self.get_objets()) > -1:
                for i in range(0, len(self.get_objets())):
                    if self.get_objets() == "blaster":
                        self.player.attack += 30
                    elif self.get_objets() == "minipistolet":
                        self.player.attack += 20
                    elif self.get_objets() == "potion":
                        self.player.health = 100
                    if self.get_objets() == "rick":
                        print("win")
                        win = True
                        return win

    #fonction qui permet de téléporter le joueur à chaque point de spawn
    def teleport_player(self, name):
        point = self.get_object(name)
        self.player.position[0] = point.x
        self.player.position[1] = point.y
        self.player.save_location()

    def register_map(self, name, portals=[], npcs=[], objets= []):
        # charger la carte (tmx)
        tmx_data = pytmx.util_pygame.load_pygame(f".\maps\{name}.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        # définir une liste qui va stocker les rectangles de collision
        walls = []
        objets = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            elif obj.type == "pistoportail":
                objets.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            elif obj.type == "blaster":
                objets.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            elif obj.type == "minipistolet":
                objets.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            elif obj.type == "potion":
                objets.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            elif obj.type == "rick":
                objets.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))


        # dessiner le groupe de calques
        group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=4)
        group.add(self.player)

        #récupérer tous les NPC pour les ajouter au groupe
        for npc in npcs:
            group.add(npc)

        # enregistrer la nouvelle carte chargée
        self.maps[name] = Map(name, walls, group, tmx_data, portals, npcs, objets)

    #récupère la map
    def get_map(self):
        return self.maps[self.current_map]

    # récupère le groupe de calques de la map
    def get_group(self):
        return self.get_map().group

    # récupère les murs de la map
    def get_walls(self):
        return self.get_map().walls

    # récupère les objets de la map
    def get_objets(self):
        return self.get_map().objets

    # récupère les objets de spawn de la map
    def get_object(self, name):
        return self.get_map().tmx_data.get_object_by_name(name)

    def recup(self):
        for npc in self.get_map().npcs:
            self.all_ennemies.add(npc)

    def teleport_npcs(self):
        for map in self.maps:
            map_data = self.maps[map]
            npcs = map_data.npcs

            for npc in npcs:
                npc.load_points(map_data.tmx_data)
                npc.teleport_spawn()

    def draw(self):
        self.get_group().draw(self.screen)
        self.get_group().center(self.player.rect.center) #placer le zoom de la caméra sur le joueur


    def update(self):
        self.get_group().update()
        self.check_collisions()

        for npc in self.get_map().npcs:
            npc.verify_npc_alive()
            npc.move()