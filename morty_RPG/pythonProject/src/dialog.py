import pygame


class DialogBox:
    #position defini comme constante de la class
    X_POSITION = 60
    Y_POSITION = 470

    def __init__(self):
        self.box = pygame.image.load('./dialogs/dialog_box.png')
        self.box = pygame.transform.scale(self.box, (700, 100)) #redimensionner l'image
        self.texts = ["(Appuyez sur la barre d'espace pour lire la suite.)",
                      "Rick: MORTY, MORTY!!!",
                      "Rick: Réveille-toi! Nous sommes dans la merde.", "Rick: La fédération m'a capturé.", "Rick: Je te parle grâce à une puce dans ta tête.", "Morty: HEIN? QUOI??! Mais je suis tout seul Rick!",
                      "Rick: *ROT* Calme toi Morty.", "Rick: On est dans un vaisseau et il y a des armes.", "Rick: Récupère-les sans te faire prendre.", "Rick: Cherche dans chaque pièce pour trouver...", "Rick: ...les objets qui vont nous permettre de...", "Rick: ...dégager d’ici.", "(Utilise les flèches pour te déplacer)",
                      "Morty: Et si je tombe sur des gardes, qu’est-ce...", "Morty: ...que je fais ?",
                      "Rick: Tant que tu n’as pas d’armes, évites-les.", "(En t'approchant d'une arme...", "...elle entrera directement dans ton inventaire.)", "Rick: Lorsque tu en trouveras une, élimine-les.","Rick: S'ils t'attrapent tu meurs.", "(Utilise ta souris pour viser et tirer).", "Rick: J'ai confiance en toi Morty *ROT*"]
        self.text_index = 0
        self.letter_index = 0
        #charge la police d'écriture à utiliser pour le texte avec la taille
        self.font = pygame.font.Font("./dialogs/dialog_font.ttf", 18)
        self.reading = True

    # rendre l'image boîte de dialogue, les textes et les lettres une à une pour qu'elle défilent à l'écran avec police et couleur aux coordonnées x et y
    def render(self, screen):
        if self.reading:
            self.letter_index += 1
            if self.letter_index >= len(self.texts[self.text_index]):
                self.letter_index = self.letter_index
            screen.blit(self.box, (self.X_POSITION, self.Y_POSITION))
            text = self.font.render(self.texts[self.text_index][0:self.letter_index], False, (0, 0, 0))
            screen.blit(text, (self.X_POSITION + 60, self.Y_POSITION + 30))

    #permet de passer au prochain texte
    def next_text(self):
        self.text_index += 1
        self.letter_index = 0

        if self.text_index >= len(self.texts):
            #close le dialog
            self.reading = False