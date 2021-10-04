from pygame import mixer
import time

class Sound_Manager:
    def __init__(self,is_playing_bgm_cut=True):
        mixer.init()
        self.sounds = {}
        self.is_playing_bgm_cut = is_playing_bgm_cut
        self.add_sounds()

    def add_sounds(self):
        self.sounds["bgm"] = {}
        if self.is_playing_bgm_cut:
            self.sounds["bgm"]["music"] = {"sound":mixer.Sound('assets/bgm_cut.mp3'), "is_playing":False}
        else:
            self.sounds["bgm"]["music_cut"] = {"sound":mixer.Sound('assets/bgm.mp3'), "is_playing":False}
        self.sounds["bgm"]["wind_sound"] = {"sound":mixer.Sound('assets/wind.mp3'), "is_playing":False}
        self.sounds["effect"] = {}
        self.sounds["effect"]["smash"] = {"sound":mixer.Sound('assets/smash.mp3'), "is_playing":False}
        self.sounds["effect"]["freeze"] = {"sound":mixer.Sound('assets/freeze.mp3'), "is_playing":False}
        self.sounds["effect"]["weak_break"] = {"sound":mixer.Sound('assets/weak_break.mp3'), "is_playing":False}

    def play_bgm(self):
        for i,j in self.sounds["bgm"].items():
            if not j["is_playing"]:
                j["sound"].play()
                j["is_playing"] = True

    def play_freeze_sound(self):
        sound = self.sounds["effect"]["freeze"]
        if sound["is_playing"]:
            sound["sound"].stop()
        sound["sound"].play()
        sound["is_playing"] = True

    def stop_freeze_sound(self):
        sound = self.sounds["effect"]["freeze"]
        if sound["is_playing"]:
            sound["sound"].stop()
        sound["is_playing"] = False

    def play_smash_sound(self):
        sound = self.sounds["effect"]["smash"]
        if sound["is_playing"]:
            sound["sound"].stop()
        sound["sound"].play()
        sound["is_playing"] = True

    def play_weak_break_sound(self):
        sound = self.sounds["effect"]["weak_break"]
        if sound["is_playing"]:
            sound["sound"].stop()
        sound["sound"].play()
        sound["is_playing"] = True

if __name__ == '__main__':
    sm = Sound_Manager()
    sm.play_freeze_sound()
    time.sleep(5)
    sm.play_freeze_sound()
    time.sleep(100)