#!/usr/bin/env python
"""
Pymodbus Asynchronous Client Examples
--------------------------------------------------------------------------

The following is an example of how to use the asynchronous serial modbus
client implementation from pymodbus with ayncio.

The example is only valid on Python3.4 and above
"""
import os
from pymodbus.compat import IS_PYTHON3, PYTHON_VERSION

if IS_PYTHON3 and PYTHON_VERSION >= (3, 4):
    import logging
    import asyncio
    from pymodbus.client.asynchronous.serial import (
        AsyncModbusSerialClient as ModbusClient,
    )
    from pymodbus.client.asynchronous import schedulers
else:
    import sys

    sys.stderr("This example needs to be run only on python 3.4 and above")
    sys.exit(1)

# --------------------------------------------------------------------------- #
# 配置主机客户端log
# --------------------------------------------------------------------------- #
fmt = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler = logging.FileHandler(os.getcwd() + "/master_client.log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(fmt)

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)
log.addHandler(file_handler)

UNIT = 0x01  # 目标从机的地址


async def start_async_test(client):
    """
    测试代码
    """
    try:
        # --------------------------------------------------------------------------- #
        # --------------------------------------------------------------------------- #
        log.debug("\nINFO : 写入单个线圈测试----写入的寄存器地址为0，写入值为True，写入的从机地址为0x01")
        # write_coil 写线圈功能，参数：线圈的地址、写入的数值、从机地址
        rq = await client.write_coil(0, True, unit=UNIT)

        log.debug("\nINFO : 读取单个线圈测试----读取的寄存器地址为0，读取数量为1，读取的从机地址为0x01")
        # read_coils 读线圈功能，参数：线圈的地址、读取线圈的数量、从机地址
        rr = await client.read_coils(0, 1, unit=UNIT)

        assert rq.function_code < 0x80  # 检测写线圈测试响应是否正常
        assert rr.bits[0] == True  # 检测读线圈测试读取的值是否为True
        # --------------------------------------------------------------------------- #
        # --------------------------------------------------------------------------- #
        log.debug("\nINFO : 写入多个线圈测试----写入的寄存器起始地址为1，写入8个值均为True，写入的从机地址为0x01")
        # write_coil 参数：线圈的起始地址、写入的数值（参数为列表则写入对应数量的线圈）、从机地址
        rq = await client.write_coils(1, [True] * 8, unit=UNIT)
        assert rq.function_code < 0x80

        log.debug("\nINFO : 读取多个线圈测试----读取的寄存器起始地址为1，读取数量为8，读取的从机地址为0x01")
        # read_coils 参数：线圈的起始地址、读取线圈的数量、从机地址
        rr = await client.read_coils(1, 8, unit=UNIT)
        assert rr.function_code < 0x80

        resp = [True] * 8  # 构造期望的返回值，8个True
        assert rr.bits == resp  # 将期望值与线圈读回值对比
        # --------------------------------------------------------------------------- #
        # --------------------------------------------------------------------------- #
        log.debug("\nINFO : 写入多个线圈测试----写入的寄存器起始地址为1，写入9个值均为False，写入的从机地址为0x01")
        rq = await client.write_coils(1, [True] * 9, unit=UNIT)
        log.debug("\nINFO : 读取多个线圈测试----读取的寄存器起始地址为1，读取9个值，读取的从机地址为0x01")
        rr = await client.read_coils(1, 9, unit=UNIT)
        assert rq.function_code < 0x80

        # 每次读取线圈，返回值位数会对8向上圆整
        # 且返回值数量不为8的倍数，则剩余位会被置为False
        # 即读取9位数据：1111 1111 1
        # 返回值则为   ：1111 1111 1000 0000
        resp = [True] * 9  # 构造期望的返回值，9个True
        resp.extend([False] * 7)  # 构造期望的返回值，圆整到8的倍数，将无效数据置为False
        assert rr.bits == resp  # 将期望值与线圈读回值对比
        # --------------------------------------------------------------------------- #
        # --------------------------------------------------------------------------- #
        log.debug("\nINFO : 读取离散输入寄存器测试----读取的寄存器起始地址为0，读取8个值，读取的从机地址为0x01")
        # read_discrete_inputs 读离散输入功能，参数：离散输入寄存器的地址、读取离散输入寄存器的数量、从机地址
        rr = await client.read_discrete_inputs(0, 8, unit=UNIT)
        assert rq.function_code < 0x80
        # --------------------------------------------------------------------------- #
        # --------------------------------------------------------------------------- #
        log.debug("\nINFO : 写入单个保持寄存器测试----写入的寄存器起始地址为1，写入1个值为88，写入的从机地址为0x01")
        # write_register 读保持寄存器功能，参数：保持寄存器的地址、写入保持寄存器的值、从机地址
        rq = await client.write_register(1, 88, unit=UNIT)
        log.debug("\nINFO : 读取单个保持寄存器测试----读取的寄存器起始地址为1，读取1个值，读取的从机地址为0x01")
        # read_holding_registers 写保持寄存器功能，参数：保持寄存器的地址、读取保持寄存器的数量、从机地址
        rr = await client.read_holding_registers(1, 1, unit=UNIT)

        assert rq.function_code < 0x80
        assert rr.registers[0] == 88  # 将期望值与保持寄存器读回值对比
        # --------------------------------------------------------------------------- #
        # --------------------------------------------------------------------------- #
        log.debug("\nINFO : 写入多个保持寄存器测试----写入的寄存器起始地址为1，写入8个值均为66，写入的从机地址为0x01")
        rq = await client.write_registers(1, [66] * 8, unit=UNIT)
        log.debug("\nINFO : 读取多个保持寄存器测试----读取的寄存器起始地址为1，读取8个值，读取的从机地址为0x01")
        rr = await client.read_holding_registers(1, 8, unit=UNIT)
        assert rq.function_code < 0x80
        assert rr.registers == [66] * 8  # 将期望值与保持寄存器读回值对比
        # --------------------------------------------------------------------------- #
        # --------------------------------------------------------------------------- #
        arguments = {
            "read_address": 1,
            "read_count": 8,
            "write_address": 1,
            "write_registers": [77] * 8,
        }
        log.debug("\nINFO : 同时读写保持寄存器测试----读写输入寄存器起始地址均为1，读写8个值，写入8个值均为20，读写的从机地址为0x01")
        rq = await client.readwrite_registers(unit=UNIT, **arguments)
        rr = await client.read_holding_registers(1, 8, unit=UNIT)
        assert rq.function_code < 0x80
        assert rq.registers == [77] * 8
        assert rr.registers == [77] * 8  # 将期望值与保持寄存器读回值对比
        # --------------------------------------------------------------------------- #
        # --------------------------------------------------------------------------- #
        log.debug("\nINFO : 读取输入寄存器测试----读取输入寄存器起始地址为1，读取8个值，读取的从机地址为0x01")
        # read_input_registers 读取输入寄存器功能，参数：输入寄存器的起始地址、读取输入寄存器的数量、从机地址
        rr = await client.read_input_registers(1, 8, unit=UNIT)
        assert rq.function_code < 0x80
    except Exception as e:
        log.exception(e)
        client.transport.close()
    await asyncio.sleep(0.5)
    import sys

    sys.exit()


if __name__ == "__main__":
    # 启动主机客户端，监听串行端口'/dev/ttymxc2'，串口波特率115200，modbus传输方式rtu
    loop, serial_client = ModbusClient(
        schedulers.ASYNC_IO, port="/dev/ttymxc2", baudrate=115200, method="rtu"
    )
    loop.run_until_complete(start_async_test(serial_client.protocol))
    loop.close()
