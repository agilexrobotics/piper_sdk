# 机械臂协议v3版本更新内容

注: 基于固件V1.8-8版本及后的使用v2版本

## 0x2A1 机械臂状态反馈

修改：

Byte 2 模式反馈修改 MOVE M 反馈为0x06，为mit模式反馈

## 0x151 模式控制协议

修改

Byte 1 模式控制修改 MOVE M 反馈为0x06，为mit模式设定

## MIT控制指令

去除crc，扩充t_ref的有效位

|机械臂关节1～6MIT控制指令|                                       |ID  0x15A ~ 0x15F|      len 8      |
|----------------------|---------------------------------------|-----------------|-----------------|
|        数据          |                  功能                  |        类型      |                 |
|       Byte 0        |  Pos_ref [bit15~bit8] 高8位            |       uint8     |                 |
|       Byte 1        |  Pos_ref [bit7~bit0]  低8位            |       uint8     |                 |
|       Byte 2        |  Vel_ref [bit11~bit4] 低12位           |       uint8     |                 |
|       Byte 3        |  Vel_ref [bit3~bit0] Kp [bit11~bit8]  |       uint8     |                 |
|       Byte 4        |  Kp [bit7~bit0]                       |       uint8     | Kp给定参考值：10  |
|       Byte 5        |  Kd [bit11~bit4]      低12位           |       uint8     | Kd给定参考值：0.8 |
|       Byte 6        |  Kd [bit3~bit0] T_ref [bit11~bit8]      |       uint8     |                 |
|       Byte 7        |  T_ref [bit7~bit0]                     |       uint8     |                 |
