from periphery import GPIO
import sys
import time

if len(sys.argv) > 2:
    LED_CHIP = "/dev/gpiochip" + sys.argv[1]
    LED_LINE_OFFSET = int(sys.argv[2])
else:
    print('''Usage:
    python3 blink.py <chip> <line offset>''')
    sys.exit()

led = GPIO(LED_CHIP, LED_LINE_OFFSET, "out")

while True:
    led.write(False)
    time.sleep(0.1)
    led.write(True)
    time.sleep(0.1)

