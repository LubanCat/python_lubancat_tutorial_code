""" python can 测试 """
import sys
import time
import threading
import can


def msg_recv(device_x):
    "接收消息功能"
    print("success: msg_recv Thread is running!")
    # 将can_mask转换为二进制形式，can_mask中为1的位，用于过滤接收到的帧
    # 举例                     id: 0 0
    #                        mask: 1 0 则接收到消息的ID中，mask为1对应id中的位，必须与id一致，为0
    # 如接收到了四个id的消息  id1: 0 0 此条消息被放行
    #                         id2: 0 1 此条消息被放行
    #                         id3: 1 0 此条消息被过滤
    #                         id4: 1 1 此条消息被过滤
    # 过滤器配置示例如下。第一条规则，接收所有标准帧，第二条规则，接收拓展帧中id为0x300的消息。
    can_filters = [
        {"can_id": 1, "can_mask": 0x0, "extended": False},
        {"can_id": 0x300, "can_mask": 0x1FFFFFFF, "extended": True},
    ]
    # 应用过滤器配置
    device_x.set_filters(can_filters)
    # 查询退出线程是否退出，如果为真，则说明用户期望程序退出，退出本线程循环，线程结束
    while tasks_quitThread.is_alive():
        try:
            # 接收can消息
            msg = device_x.recv(1)
            if msg is not None:
                print("success: ", msg)
        except can.CanError:
            print("error: 接收消息时出错，请检查设备是否启用及状态正常")


def msg_send(device_x):
    "发送消息功能"
    print("success: msg_send Thread is running!")
    # 构造发送的CAN消息结构，ID为0xC0FFEE，数据内容包含在data中，is_extended_id为拓展ID标识
    msg = can.Message(
        arbitration_id=0xC0FFEE, data=[0, 25, 0, 1, 3, 1, 4, 1], is_extended_id=True
    )
    # 查询退出线程是否退出，如果为真，则说明用户期望程序退出，退出本线程循环，线程结束
    while tasks_quitThread.is_alive():
        try:
            # 发送构造的CAN消息
            device_x.send(msg)
            # 打印发送提示
            print(f"success: 消息已发送至 {device_x.channel_info}")
        except can.CanError:
            print("error: 消息发送出错，请检查设备是否启用及状态正常!")
        # 两秒后再次发送
        time.sleep(2)


def tasks_quit():
    "程序退出功能"
    print("success: tasks_quit Thread is running!")
    exitright = "e"
    while exitright not in ["q", "Q"]:
        # 获取用户输入，如果为q则退出程序
        exitright = input(
            """
***********************************
**输入字母q后，按下回车以退出程序**
***********************************
"""
        )
        # 线程退出


# 打印运行程序前提示信息
print(
    "information: 执行本程序前，请先启用can设备。命令如下：\
    \nsudo ip link set can0 type can bitrate 1000000\nsudo ip link set can0 up"
)
# 打开CAN设备，CAN设备类型为socketcan，channel为can0，可使用ifconfig -a命令查看。
with can.interface.Bus(
    bustype="socketcan", channel="can0", bitrate=1000000
) as device_can0:
    # 创建线程：监听程序退出线程、发送can消息线程、接收can消息线程
    try:
        print("information: 开始创建 tasks_quitThread 线程!")
        tasks_quitThread = threading.Thread(target=tasks_quit, daemon=True)
        print("information: 开始创建 msg_sendThread 线程!")
        msg_sendThread = threading.Thread(
            target=msg_send, daemon=True, args=(device_can0,)
        )
        print("information: 开始创建 msg_recvThread 线程!")
        msg_recvThread = threading.Thread(
            target=msg_recv, daemon=True, args=(device_can0,)
        )
        # 开启线程
        print("information: 开始启动 tasks_quitThread 线程!")
        tasks_quitThread.start()
        print("information: 开始启动 msg_sendThread 线程!")
        msg_sendThread.start()
        print("information: 开始启动 msg_recvThread 线程!")
        msg_recvThread.start()
    # pylint: disable=W0702
    except:
        print("error: 创建或启动线程中出错!")
        sys.exit()

    # 等待线程结束
    tasks_quitThread.join()
    print("information: tasks_quitThread结束")
    msg_sendThread.join()
    print("information: msg_sendThread结束")
    msg_recvThread.join()
    print("information: msg_recvThread结束")
    # 所有正常线程结束，退出程序
    sys.exit()
