class VolumeManager:
    generalVolume : float = 1.0
    soundVolume : float = 1.0
    musicVolume : float = 1.0

    def __init__(self):
        pass

    def update_general_volume(self, volume):
        self.generalVolume = volume
        self.musicVolume = self.musicVolume / volume
        self.soundVolume = self.soundVolume / volume

    def update_sound_volume(self, volume):
        self.soundVolume = volume / self.generalVolume

    def update_music_volume(self, volume):
        self.musicVolume = volume / self.generalVolume