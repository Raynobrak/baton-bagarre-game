class VolumeManager:
    generalVolume : float = 1.0
    soundVolume : float = 1.0
    musicVolume : float = 1.0

    def __init__(self):
        pass

    def update_general_volume(self, volume):
        VolumeManager.generalVolume = volume

    def update_sound_volume(self, volume):
        VolumeManager.soundVolume = volume

    def update_music_volume(self, volume):
        VolumeManager.musicVolume = volume