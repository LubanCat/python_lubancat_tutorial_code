"""Digital IO (Output) using periphery, command line"""
import sys
import time
from periphery import GPIO

if len(sys.argv) > 2:
    LED_CHIP = "/dev/gpiochip" + sys.argv[1]
    LED_LINE_OFFSET = int(sys.argv[2])
else:
    print('''Usage:
    python3 blink_cmd.py <chip> <line offset>
    example: python3 blink_cmd.py 3 19'''
    )
    sys.exit()

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
