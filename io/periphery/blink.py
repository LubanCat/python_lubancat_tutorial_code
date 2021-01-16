"""Digital IO (Output) using periphery"""
import time
from periphery import GPIO

# 根据具体板卡的LED灯连接修改使用的Chip和Line
LED_CHIP = "/dev/gpiochip3"
LED_LINE_OFFSET = 19

led = GPIO(LED_CHIP, LED_LINE_OFFSET, "out")

try:
    while True:
        led.write(False)
        time.sleep(0.1)
        led.write(True)
        time.sleep(0.1)
finally:
    led.write(True)
    led.close()
