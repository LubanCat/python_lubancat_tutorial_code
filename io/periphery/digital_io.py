"""Digital IO (Input/Output) using periphery"""
from periphery import GPIO

# 根据具体板卡的LED灯和按键连接修改使用的Chip和Line
LED_CHIP = "/dev/gpiochip3"
LED_LINE_OFFSET = 19

BUTTON_CHIP = "/dev/gpiochip4"
BUTTON_LINE_OFFSET = 1

led = GPIO(LED_CHIP, LED_LINE_OFFSET, "out")
button = GPIO(BUTTON_CHIP, BUTTON_LINE_OFFSET, "in")

try:
    while True:
        led.write(button.read())
finally:
    led.write(True)
    led.close()
    button.close()
