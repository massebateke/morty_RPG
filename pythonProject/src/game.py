import pygame, pyscroll, math, sys


from player import Player
from src.dialog import DialogBox
from src.map import MapManager
from src.sounds import SoundManager


class Game:

    def __init__(self, map_layer=None):
        # créer la fenêtre
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Rick et Morty")

        #créer le menu avec background et bouton play
        self.background = pygame.image.load('./sprite/rickm.png')
        self.play_button = pygame.image.load('./sprite/button.png')
        self.play_button = pygame.transform.scale(self.play_button, (400, 150))
        self.play_button_rect = self.play_button.get_rect()
        self.play_button_rect.x = math.ceil(self.screen.get_width() / 4)
        self.play_button_rect.y = math.ceil(self.screen.get_height() / 1.5)

        self.game_over = pygame.image.load('./sprite/gameov.jpg')
        self.game_over_rect = self.game_over.get_rect()

        self.win = pygame.image.load('./sprite/win.jpg')
        self.win_rect = self.win.get_rect()

        self.player = Player()
        self.dialog_box = DialogBox()
        self.map_manager = MapManager(self.screen, self.player)

        #group de monstre
        #self.all_monsters =pygame.sprite.Group()

        #gérer le son
        self.soud_manager = SoundManager()

        # dessiner  le groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=3)
        self.group.add(self.player)

    def handle_input(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_UP]:
            self.player.move_up()
        elif pressed[pygame.K_DOWN]:
            self.player.move_down()
        elif pressed[pygame.K_LEFT]:
            self.player.move_left()
        elif pressed[pygame.K_RIGHT]:
            self.player.move_right()

    def update(self):

        self.map_manager.update()
        #Mettre a jour la bar de vie sur le screen
        self.player.update_health_bar(self.screen)

    def run(self):
        running = True
        is_playing = False
        clock = pygame.time.Clock()

        while running:
            if is_playing == False:
                self.background = pygame.transform.scale(self.background, (800, 600))
                self.screen.blit(self.background, (0, 0))
                self.screen.blit(self.play_button, self.play_button_rect)
                self.soud_manager.play('generique', 1)

            if self.player.check_live() == False:
                self.screen.blit(self.game_over, self.game_over_rect)
                self.soud_manager.stop('fond')
                self.soud_manager.play('morty_mort', 1)

            if self.map_manager.check_collisions() == True:
                self.screen.blit(self.win, self.win_rect)
                self.soud_manager.play('fin', 1)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    #detecter si le joueur veut jouer
                #verifie si la souris est en collision avec le bouton play et lance le jeu si c'est le cas
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.play_button_rect.collidepoint(event.pos):
                        # mettre le jeu en mode lancé
                        is_playing = True
                        running = True
                        self.soud_manager.stop('generique')
                        self.soud_manager.play('fond', 44)
                    elif event.button == 1:
                        self.player.launch_projectile_player(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                #lorsque barre d'espace enclenchée, on passe au texte suivant de la boîte de dialogue
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.dialog_box.next_text()
            clock.tick(60)

            self.player.save_location()
            self.handle_input()
            self.update()
            self.map_manager.draw()
            self.dialog_box.render(self.screen) #rendre l'image et l'afficher sur la surface screen
            self.map_manager.recup()

            #récupérer les projectiles du joueur
            for projectile in self.player.all_projectiles_player:
                projectile.move_player()
            #appliquer l'ensemble des images de mon groupe de projectile
            self.player.all_projectiles_player.draw(self.screen)


            #appliquer la bar de vie sur l'ennemie
            for npc in self.map_manager.all_ennemies:
                npc.update_health_bar(self.screen)


        pygame.quit()
