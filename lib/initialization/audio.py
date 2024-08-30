import pyttsx3

from pygame import mixer, _sdl2 as devices

def init(use_audio):
    if use_audio:
        mixer.init()
        print("Outputs:", devices.audio.get_audio_device_names(False))
        mixer.quit()

        mixer.init(devicename="Bot (VB-Audio Virtual Cable)")
        return pyttsx3.init()