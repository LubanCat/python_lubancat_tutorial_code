"""CircuitPython Essentials Analog In example"""
import time
import board
from analogio import AnalogIn

analog_in = AnalogIn(board.A2)


def get_voltage(pin):
    """ 获取引脚电压值 """
    return (pin.value * 3.3) / 4096


while True:
    print(get_voltage(analog_in))
    time.sleep(0.1)
