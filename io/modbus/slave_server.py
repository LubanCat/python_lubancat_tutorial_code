#!/usr/bin/env python
"""
a simple device simulator.
"""
import os
import logging

from pymodbus.framer.rtu_framer import ModbusRtuFramer
from pymodbus.server.sync import StartSerialServer  # ,StartTcpServer
from pymodbus.datastore import (
    ModbusSequentialDataBlock,
    ModbusSlaveContext,
    ModbusServerContext,
)

# 创建log对象，log对象为pymodbus
pymodbus_logger = logging.getLogger("pymodbus")
# 设置log记录等级，log等级可以参考
# logging.CRITICAL
# logging.ERROR
# logging.WARNING
# logging.INFO
# logging.DEBUG
pymodbus_logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    # 设置log记录格式：log时间-log发生对象-log等级-log打印信息
    fmt = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    # 创建log文件对象，文件创建在当前目录，文件名为slave.log
    file_handler = logging.FileHandler(os.getcwd() + "/slave_server.log")
    # 设置文件对象记录log的等级
    file_handler.setLevel(logging.DEBUG)
    # 设置文件对象log的格式
    file_handler.setFormatter(fmt)
    # 添加log文件对象到当前log系统中，这样产生log后，log会被同步写入到文件中
    pymodbus_logger.addHandler(file_handler)

    # 定义co线圈寄存器，存储起始地址为0，长度为20，内容为15个True及5个False
    co_block = ModbusSequentialDataBlock(0, [True] * 15 + [False] * 5)
    # 定义di离散输入寄存器，存储起始地址为0，长度为20，内容为15个True及5个False
    di_block = ModbusSequentialDataBlock(0, [True] * 15 + [False] * 5)
    # 定义ir输入寄存器，存储起始地址为0，长度为10，内容为0~10递增数值列表
    ir_block = ModbusSequentialDataBlock(0, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    # 定义hr保持寄存器，存储起始地址为0，长度为10，内容为0~10递增数值列表
    hr_block = ModbusSequentialDataBlock(0, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

    # 创建从机，从机的di离散量、co线圈、hr保持寄存器、ir输入寄存器等由上面定义并传入
    slaves = ModbusSlaveContext(di=di_block, co=co_block, hr=hr_block, ir=ir_block)
    # 创建单从机上下文，交由服务器调度
    context = ModbusServerContext(slaves=slaves, single=True)

    # 如果需要创建多个从机，参考如下：从机地址 + 从机配置
    # slaves = {
    # 1:ModbusSlaveContext(di=di_block, co=co_block, hr=hr_block, ir=ir_block),
    # 2:ModbusSlaveContext(di=di_block, co=co_block, hr=hr_block, ir=ir_block),
    # 3:ModbusSlaveContext(di=di_block, co=co_block, hr=hr_block, ir=ir_block)
    # }
    # context = ModbusServerContext(slaves=slaves, single=False)

    # 开启tcp服务器方法
    # StartTcpServer(context, address=('127.0.0.1', 5020))
    # 开启串行设备服务器方法
    # 参数：从机上下文、从机通行帧格式、监听设备'/dev/ttymxc1'、串口波特率、从机监听超时时间0为不阻塞立刻响应
    StartSerialServer(
        context, framer=ModbusRtuFramer, port="/dev/ttymxc1", baudrate=115200, timeout=0
    )
