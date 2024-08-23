from src.VolumeManager import VolumeManager


class TestVolumeManager():

    def test_base_volume(self):
        assert VolumeManager().generalVolume == 1.0
        assert VolumeManager().soundVolume == 1.0
        assert VolumeManager().musicVolume == 1.0

    def test_base_half_volume(self):
        VolumeManager().update_general_volume(0.5)
        assert VolumeManager().generalVolume == 0.5
        assert VolumeManager().soundVolume == 0.5
        assert VolumeManager().musicVolume == 0.5

    def test_half_base_half_music(self):
        VolumeManager().update_general_volume(0.5)
        VolumeManager().update_sound_volume(0.5)
        VolumeManager().update_music_volume(0.5)
        assert VolumeManager().generalVolume == 0.5
        assert VolumeManager().soundVolume == 0.25
        assert VolumeManager().musicVolume == 0.25
