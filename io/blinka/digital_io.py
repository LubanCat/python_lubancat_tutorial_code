"""Digital IO (Input/Output) using Blinka"""
import board
import digitalio

# 根据具体板卡的LED灯和按键连接修改使用的GPIO
# LubanCat i.MX6ULL board, GPIO_PC32 = Pin 115
led = digitalio.DigitalInOut(board.GPIO_PC32)
led.direction = digitalio.Direction.OUTPUT

# LubanCat i.MX6ULL board, GPIO_PD17 = Pin 129
button = digitalio.DigitalInOut(board.GPIO_PD17)
button.direction = digitalio.Direction.INPUT

try:
    while True:
        led.value = button.value
finally:
    led.value = True
    led.deinit()
    button.deinit()
