import time
from pygame import mixer


user_input=input('Please write the name of the song that you would like to listen to')


mixer.init()
mixer.music.load(user_input +'.mp3')
mixer.music.set_volume(0.8)
mixer.music.play()
while mixer.music.get_busy():
    time.sleep(1)


