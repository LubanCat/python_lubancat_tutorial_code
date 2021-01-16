"""Digital IO (Output) using Blinka"""
import time
import board
import digitalio

# 根据具体板卡的LED灯连接修改使用的Chip和Line
led = digitalio.DigitalInOut(board.GPIO_PC32)
led.direction = digitalio.Direction.OUTPUT

try:
    while True:
        led.value = True
        time.sleep(0.5)
        led.value = False
        time.sleep(0.5)
finally:
    led.value = True
    led.deinit()
