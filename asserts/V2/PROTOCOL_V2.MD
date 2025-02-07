# PIPER SDK Protocol V2 说明文档

[EN](PROTOCOL_V2(EN).MD)

## protocol V2解析

整个协议解析分为两层，一层是基类，一层是实际的数据解析类

### C_PiperParserBase 基类

本代码定义了C_PiperParserBase类，这是一个用于机械臂协议解析的基类。它提供了多种功能用于处理机械臂数据协议的解析和转换。以下是该类的主要结构和功能说明：

#### 1. C_PiperParserBase 类

这是一个抽象基类，用于机械臂协议数据的解析。
包含多个抽象方法，派生类需要实现这些方法以完成协议的具体解析和编码操作。

1.1 内部类 ProtocolVersion

定义了机械臂协议的版本枚举。
枚举值包括 ARM_PROTOCOL_UNKNOWN 和 ARM_PROROCOL_V2，可以在派生类中扩展和指定具体协议版本。

1.2 抽象方法

DecodeMessage(): 解码消息，将CAN数据帧转为指定类型。派生类必须实现此方法。
EncodeMessage(): 编码消息，将输入数据转换为CAN数据帧。派生类必须实现此方法。
GetParserProtocolVersion(): 获取当前使用的协议版本。派生类必须实现此方法。

#### 2. 数据转换方法

该类包含多种用于整数类型转换的方法，这些方法用于将输入的数值转换为指定格式的整数或字节列表：
2.1 转换为不同位数的整数

ConvertToNegative_8bit, ConvertToNegative_16bit, ConvertToNegative_32bit: 将输入的整数转换为8、16、32位的有符号或无符号整数。

ConvertToNegative_int8_t, ConvertToNegative_uint8_t: 特定转换为8位有符号或无符号整数。

ConvertToNegative_int16_t, ConvertToNegative_uint16_t: 特定转换为16位有符号或无符号整数。

ConvertToNegative_int32_t, ConvertToNegative_uint32_t: 特定转换为32位有符号或无符号整数。

2.2 转换为字节列表

ConvertToList_8bit, ConvertToList_16bit, ConvertToList_32bit: 将输入的整数转换为8、16、32位的整数列表。

ConvertToList_int8_t, ConvertToList_uint8_t: 特定转换为8位有符号或无符号整数的字节列表。

ConvertToList_int16_t, ConvertToList_uint16_t: 特定转换为16位有符号或无符号整数的字节列表。

ConvertToList_int32_t, ConvertToList_uint32_t: 特定转换为32位有符号或无符号整数的字节列表。

#### 3. 字节转换为整数

ConvertBytesToInt(): 将字节序列转换为整数，支持大端和小端对齐方式。

用来将接收的can数据帧原始数据(字节类型)，转换为整数，然后再调用上面的转换函数限定数据类型

### C_PiperParserV2 派生类

1. 类与继承关系

    C_PiperParserV2 继承自 C_PiperParserBase，是 Piper 机械臂解析数据类的 V2 版本。
    该类是基于一个抽象的或更通用的解析器框架来处理机械臂的协议数据。

2. 主要功能

    协议版本管理：提供了 GetParserProtocolVersion() 方法，返回当前使用的协议版本。
    消息解码：DecodeMessage() 解析 CAN 总线传输的消息，将其转换为程序内定义的数据类型。
    消息编码：EncodeMessage() 将程序内定义的数据类型转换为 CAN 数据帧以发送。

3. 关键方法

    GetParserProtocolVersion()
        返回当前协议版本 (ARM_PROTOCOL_V2)，标识解析器适配的协议版本。

    DecodeMessage(rx_can_frame, msg)
        主要用于解析 CAN 消息。
        根据 CAN 消息的 ID（can_id），将数据帧解码为特定的机械臂数据结构。
        使用了大量的 if-elif 判断语句，根据不同的 can_id 执行特定解码逻辑。
        数据解码方法包括：状态反馈、末端位姿、关节角度、夹爪反馈、驱动器信息（高速和低速）等。
        涉及多个数据转换方法，如 ConvertToNegative_*bit()，用于处理字节到数值的转换并保留数值符号。

    EncodeMessage(msg, tx_can_frame)
        主要用于将内部数据结构编码成 CAN 消息。
        根据 msg 的类型编码数据，构造 CAN 数据帧。
        支持多种机械臂控制指令的编码（例如运动控制、末端控制、关节控制等）。
        数据编码时调用了 ConvertToList_*bit() 方法，完成内部数值向 CAN 数据格式的转换。

4. 数据处理流程

    数据接收与解码：
        rx_can_frame 作为输入，包含接收到的 CAN 消息。
        DecodeMessage() 解析 rx_can_frame，将字节数据转换为程序定义的 msg 对象。
    数据发送与编码：
        msg 作为输入，包含需要发送的控制或反馈数据。
        EncodeMessage() 将 msg 数据编码为 tx_can_frame，准备通过 CAN 总线发送。
