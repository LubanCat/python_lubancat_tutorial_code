""" 使用pygame进行屏幕测试 """
import os
import sys
import time
import pygame

# 设置系统环境，无鼠标
os.environ["SDL_NOMOUSE"] = "1"

# 初始化显示设备
pygame.display.init()

# 获取显示设备信息，并打印其中的宽度和高度
size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
# 构造rgb色彩中的黑色
black = 0, 0, 0
# 设置显示窗口的范围为屏幕大小，并返回一个屏幕对象
screen = pygame.display.set_mode(size)
# 使用pygame image模块加载图片
ball = pygame.image.load("test.png")
# 获取图片大小矩形信息
ballrect = ball.get_rect()
# 对屏幕对象进行填充，填充色彩为黑色
screen.fill(black)
# 将图片按位拷贝到屏幕上
screen.blit(ball, ballrect)
# 更新屏幕以显示内容
pygame.display.flip()

time.sleep(5)
sys.exit()
