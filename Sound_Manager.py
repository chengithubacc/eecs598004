from pygame import mixer
import time

class Sound_Manager:
    def __init__(self):
        mixer.init()
        self.sounds = {}
        self.add_sounds()

    def add_sounds(self):
        self.sounds["bgm"] = {}
        self.sounds["bgm"]["music"] = {"sound":mixer.Sound('assets/bgm.mp3'), "is_playing":False}
        self.sounds["bgm"]["wind_sound"] = {"sound":mixer.Sound('assets/wind.mp3'), "is_playing":False}
        self.sounds["effect"] = {}
        self.sounds["effect"]["smash"] = {"sound":mixer.Sound('assets/smash.mp3'), "is_playing":False}
        self.sounds["effect"]["freeze"] = {"sound":mixer.Sound('assets/freezing.mp3'), "is_playing":False}

    def play_bgm(self):
        for i,j in self.sounds["bgm"].items():
            if not j["is_playing"]:
                j["sound"].play()
                j["is_playing"] = True

    def play_freeze_sound(self):
        pass

    def play_smash_sound(self):
        pass

if __name__ == '__main__':
    sm = Sound_Manager()
    sm.play_bgm()
    time.sleep(100)