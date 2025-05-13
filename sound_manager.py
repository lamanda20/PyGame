import pygame

class SoundManager:
    def __init__(self, sound_folder='sounds'):  # Changé 'sound' en 'sounds' pour correspondre à votre dossier
        """
        Initialise le gestionnaire de sons avec les fichiers du dossier spécifié
        
        :param sound_folder: Chemin vers le dossier contenant les fichiers audio
        """
        pygame.mixer.init()
        
        # Chargement des fichiers audio
        try:
            print(f"Chargement des sons depuis le dossier {sound_folder}...")
            self.ugh_sound = pygame.mixer.Sound(f'{sound_folder}/ugh.wav')
            self.coin_sound = pygame.mixer.Sound(f'{sound_folder}/coin.wav')
            self.laser_shot_sound = pygame.mixer.Sound(f'{sound_folder}/laser_shot.wav')
            print("Sons chargés avec succès!")
        except Exception as e:
            print(f"Erreur lors du chargement des fichiers audio: {e}")
            self.ugh_sound = None
            self.coin_sound = None
            self.laser_shot_sound = None
    
    def play_enemy_hit_sound(self):
        """Joue le son quand le joueur touche un ennemi"""
        if self.ugh_sound:
            print("Lecture du son de collision avec ennemi")
            self.ugh_sound.play()
    
    def play_coin_collect_sound(self):
        """Joue le son quand une pièce/diamant est collecté"""
        if self.coin_sound:
            print("Lecture du son de collection de pièce")
            self.coin_sound.play()
    
    def play_laser_shot_sound(self):
        """Joue le son quand un laser/bullet est tiré"""
        if self.laser_shot_sound:
            print("Lecture du son de tir laser")
            self.laser_shot_sound.play()