# Q&A

[EN](Q&A(EN).MD)

## 一、 第一次使用夹爪/示教器无法控制以及无消息问题

注：**V1版本interface无此功能**

> 夹爪/示教器都为末端执行器，下统称为末端执行器

由于新版本夹爪出厂需要设定行程范围，如果没有设定，则会出现反馈值始终为零以及无法控制的问题

这里使用V2版本及以上interface来设定

1. 执行[piper_disable.py](../demo/V2/piper_disable.py)来失能机械臂，注意失能机械臂会令所有电机立刻失电
2. 执行[V2_gripper_param_config.py](../demo/V2/V2_gripper_param_config.py)来设定末端执行器行程
3. 然后执行[read_gripper_status.py](../demo/V2/read_gripper_status.py)查看末端执行器是否有数据
4. 如果发现末端执行器反馈的行程数据在闭合时的数值偏大，可以使用[piper_gripper_zero_set.py](../demo/V2/piper_gripper_zero_set.py)来设定末端执行器零点
