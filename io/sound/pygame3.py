""" pygame 音频播放测试 """
import pygame

try:
    # 初始化音频设备
    pygame.mixer.init()
    # 加载音频文件，此处未播放mp3文件，因为pygam对MP3格式的播放支持是有限的，在Debian Linux中播放mp3可能会导致程序崩溃
    pygame.mixer.music.load("test.ogg")
    # 设置音量为50%
    pygame.mixer.music.set_volume(0.5)
    # 播放音频文件1次
    pygame.mixer.music.play(0)
    # 获取音频播放状态，如果正在播放，等待播放完毕
    while pygame.mixer.music.get_busy():
        # 空闲延时，释放cpu
        pygame.time.Clock().tick(10)
finally:
    exit()
