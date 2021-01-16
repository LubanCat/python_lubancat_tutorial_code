import gpiod

LED_LINE_OFFSET = 19
BUTTON_LINE_OFFSET = 1

chip3 = gpiod.Chip("3", gpiod.Chip.OPEN_BY_NUMBER)
chip4 = gpiod.Chip("4", gpiod.Chip.OPEN_BY_NUMBER)

led = chip3.get_line(LED_LINE_OFFSET)  
led.request(consumer="LED", type=gpiod.LINE_REQ_DIR_OUT, default_vals=[0])

button = chip4.get_line(BUTTON_LINE_OFFSET) 
button.request(consumer="BUTTON", type=gpiod.LINE_REQ_DIR_IN)

print(led.consumer())
print(button.consumer())

try:
  while True:
    led.set_value(button.get_value())
finally:
  led.set_value(1)
  led.release()
  button.release()