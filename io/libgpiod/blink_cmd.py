"""Digital IO (Output) using libgpiod, command line"""
import sys
import time
import gpiod

# 根据具体板卡的LED灯连接修改使用的Chip和Line
if len(sys.argv) > 2:
    LED_CHIP = sys.argv[1]
    LED_LINE_OFFSET = int(sys.argv[2])
else:
    print('''Usage:
    python3 blink_cmd.py <chip> <line offset>
    example: python3 blink_cmd.py 3 19''')
    sys.exit()

led = gpiod.Chip(LED_CHIP).get_line(LED_LINE_OFFSET)
led.request(consumer="LED", type=gpiod.LINE_REQ_DIR_OUT, default_vals=[0])

print(led.consumer())

try:
    while True:
        led.set_value(0)
        time.sleep(0.1)
        led.set_value(1)
        time.sleep(0.1)
finally:
    led.set_value(1)
    led.release()
