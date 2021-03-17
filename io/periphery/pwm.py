"""periphery库 PWM测试."""
import time
from periphery import PWM

# 打开 PWM 3, channel 0 ,对应开发板上PWM3外设

try:
    pwm = PWM(2, 0)
    # 设置PWM输出频率为 1 kHz
    pwm.frequency = 1e3
    # 设置占空比为 50%
    pwm.duty_cycle = 0.50
    # 开启PWM输出
    pwm.enable()
    while True:
        for i in range(0, 9):
            time.sleep(0.1)
            pwm.duty_cycle += 0.05
        for i in range(0, 9):
            time.sleep(0.1)
            pwm.duty_cycle -= 0.05
        if pwm.duty_cycle == 0.0:
            time.sleep(1)
finally:
    pwm.close()
