""" 使用pygame进行屏幕测试 """
import os
import time
import pygame


class PyScope:
    """ 定义一个PyScope类，进行屏幕测试 """

    screen = None

    def __init__(self):
        "PyScope类的初始化方法，使用framebuffer构造pygame会使用到的图像缓冲区"
        # Based on "Python GUI in Linux frame buffer"
        # http://www.karoltomala.com/blog/?p=679
        # 尝试获取环境目录下定义的显示设备
        disp_no = os.getenv("DISPLAY")
        if disp_no:
            print("I'm running under X display = {0}".format(disp_no))

        # 检查何种驱动方式可用
        # 从fbcon开始，因为directfb会挂起复合输出
        drivers = ["fbcon", "directfb", "svgalib"]
        # 设置系统环境为无鼠标模式
        os.environ["SDL_NOMOUSE"] = "1"
        found = False
        # 根据枚举的framebuffer设备类型适配驱动
        for driver in drivers:
            # 确保环境变量SDL_VIDEODRIVER被设置
            if not os.getenv("SDL_VIDEODRIVER"):
                os.putenv("SDL_VIDEODRIVER", driver)
            try:
                print("Driver: {0} is checking now...".format(driver))
                # 尝试初始化显示设备功能
                pygame.display.init()
            except pygame.error:
                # 出错，打印提示
                print("Driver: {0} failed.".format(driver))
                continue
            print("Driver: {0} is suitable.".format(driver))
            found = True
            break

        if not found:
            raise Exception("No suitable video driver found!")

        # 获取显示设备的大小
        size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        # 打印显示设备的大小
        print("Framebuffer size: %d x %d" % (size[0], size[1]))
        # 设置pygame使用的窗口显示为全屏幕
        self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
        # 清屏
        self.screen.fill((0, 0, 0))
        # 初始化字体库
        pygame.font.init()
        # 更新屏幕，以显示写入缓冲区的内容
        pygame.display.update()

    def __del__(self):
        "退出pygame库的时候会调用该方法，可以在此添加资源释放操作"

    def test(self):
        "PyScope类的测试方法，使屏幕填充为红色"
        # 填充屏幕为红色，其rgb值为(255, 0, 0)
        red = (255, 0, 0)
        # 填充
        self.screen.fill(red)
        # 更新屏幕，以显示写入缓冲区的内容
        pygame.display.update()


# 创建一个测试实例，开始测试
scope = PyScope()
# 调用scope类的测试方法
scope.test()
time.sleep(3)
exit()
