import gpiod
import time

LED_LINE_OFFSET = 19

chip3 = gpiod.Chip("3", gpiod.Chip.OPEN_BY_NUMBER)

led = chip3.get_line(LED_LINE_OFFSET)  
led.request(consumer="LED", type=gpiod.LINE_REQ_DIR_OUT, default_vals=[0])

print(led.consumer())

try:
  while True:
    led.set_value(1)
    time.sleep(0.5)
    led.set_value(0)
    time.sleep(0.5)
finally:
  led.set_value(1)
