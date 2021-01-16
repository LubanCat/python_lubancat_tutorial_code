import board
import digitalio

led = digitalio.DigitalInOut(board.GPIO_PC33)  # pin 37
led.direction = digitalio.Direction.OUTPUT

button = digitalio.DigitalInOut(board.GPIO_PD17)  # pin 36
button.direction = digitalio.Direction.INPUT

try:
  while True:
    led.value = button.value
finally:
  led.value = True
  led.deinit()
  button.deinit()