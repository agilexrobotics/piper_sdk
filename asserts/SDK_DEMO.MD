# 有关sdk的所有demo

## 读取机械臂消息并打印

```python
#!/usr/bin/env python3
# -*-coding:utf8-*-
# 注意demo无法直接运行，需要pip安装sdk后才能运行
# 读取机械臂消息并打印,需要先安装piper_sdk
from typing import (
    Optional,
)
from piper_sdk import *

# 测试代码
if __name__ == "__main__":
    piper = C_PiperInterface()
    piper.ConnectPort()
    while True:
        import time
        print(piper.GetArmStatus())
        time.sleep(0.005)
        pass
```

## 机械臂使能

```python
#!/usr/bin/env python3
# -*-coding:utf8-*-
# 注意demo无法直接运行，需要pip安装sdk后才能运行
# 使能机械臂
from typing import (
    Optional,
)
import time
from piper_sdk import *

def enable_fun(piper:C_PiperInterface, enable:bool):
    '''
    使能机械臂并检测使能状态,尝试5s,如果使能超时则退出程序
    '''
    enable_flag = False
    loop_flag = False
    # 设置超时时间（秒）
    timeout = 5
    # 记录进入循环前的时间
    start_time = time.time()
    elapsed_time_flag = False
    while not (loop_flag):
        elapsed_time = time.time() - start_time
        print(f"--------------------")
        enable_list = []
        enable_list.append(piper.GetArmLowSpdInfoMsgs().motor_1.foc_status.driver_enable_status)
        enable_list.append(piper.GetArmLowSpdInfoMsgs().motor_2.foc_status.driver_enable_status)
        enable_list.append(piper.GetArmLowSpdInfoMsgs().motor_3.foc_status.driver_enable_status)
        enable_list.append(piper.GetArmLowSpdInfoMsgs().motor_4.foc_status.driver_enable_status)
        enable_list.append(piper.GetArmLowSpdInfoMsgs().motor_5.foc_status.driver_enable_status)
        enable_list.append(piper.GetArmLowSpdInfoMsgs().motor_6.foc_status.driver_enable_status)
        if(enable):
            enable_flag = all(enable_list)
            piper.EnableArm(7)
            piper.GripperCtrl(0,1000,0x01, 0)
        else:
            enable_flag = any(enable_list)
            piper.DisableArm(7)
            piper.GripperCtrl(0,1000,0x02, 0)
        print(f"使能状态: {enable_flag}")
        print(f"--------------------")
        if(enable_flag == enable):
            loop_flag = True
            enable_flag = True
        else: 
            loop_flag = False
            enable_flag = False
        # 检查是否超过超时时间
        if elapsed_time > timeout:
            print(f"超时....")
            elapsed_time_flag = True
            enable_flag = False
            loop_flag = True
            break
        time.sleep(0.5)
    resp = enable_flag
    print(f"Returning response: {resp}")
    return resp

# 测试代码
if __name__ == "__main__":
    piper = C_PiperInterface()
    piper.ConnectPort()
    import time
    flag = enable_fun(piper=piper, enable=False)
    if(flag == True):
        print("失能成功!!!!")
        exit(0)
    pass
```

## 机械臂失能

```python
#!/usr/bin/env python3
# -*-coding:utf8-*-
# 注意demo无法直接运行，需要pip安装sdk后才能运行
# 使能机械臂
from typing import (
    Optional,
)
import time
from piper_sdk import *

def enable_fun(piper:C_PiperInterface, enable:bool):
    '''
    使能机械臂并检测使能状态,尝试5s,如果使能超时则退出程序
    '''
    enable_flag = False
    loop_flag = False
    # 设置超时时间（秒）
    timeout = 5
    # 记录进入循环前的时间
    start_time = time.time()
    elapsed_time_flag = False
    while not (loop_flag):
        elapsed_time = time.time() - start_time
        print(f"--------------------")
        enable_list = []
        enable_list.append(piper.GetArmLowSpdInfoMsgs().motor_1.foc_status.driver_enable_status)
        enable_list.append(piper.GetArmLowSpdInfoMsgs().motor_2.foc_status.driver_enable_status)
        enable_list.append(piper.GetArmLowSpdInfoMsgs().motor_3.foc_status.driver_enable_status)
        enable_list.append(piper.GetArmLowSpdInfoMsgs().motor_4.foc_status.driver_enable_status)
        enable_list.append(piper.GetArmLowSpdInfoMsgs().motor_5.foc_status.driver_enable_status)
        enable_list.append(piper.GetArmLowSpdInfoMsgs().motor_6.foc_status.driver_enable_status)
        if(enable):
            enable_flag = all(enable_list)
            piper.EnableArm(7)
            piper.GripperCtrl(0,1000,0x01, 0)
        else:
            enable_flag = any(enable_list)
            piper.DisableArm(7)
            piper.GripperCtrl(0,1000,0x02, 0)
        print(f"使能状态: {enable_flag}")
        print(f"--------------------")
        if(enable_flag == enable):
            loop_flag = True
            enable_flag = True
        else: 
            loop_flag = False
            enable_flag = False
        # 检查是否超过超时时间
        if elapsed_time > timeout:
            print(f"超时....")
            elapsed_time_flag = True
            enable_flag = False
            loop_flag = True
            break
        time.sleep(0.5)
    resp = enable_flag
    print(f"Returning response: {resp}")
    return resp

# 测试代码
if __name__ == "__main__":
    piper = C_PiperInterface()
    piper.ConnectPort()
    import time
    flag = enable_fun(piper=piper, enable=True)
    if(flag == True):
        print("使能成功!!!!")
        exit(0)
    pass
```

## 机械臂关节角读取

没有夹爪可以注释夹爪部分

```python
#!/usr/bin/env python3
# -*-coding:utf8-*-
# 注意demo无法直接运行，需要pip安装sdk后才能运行
# 读取机械臂消息并打印,需要先安装piper_sdk
from typing import (
    Optional,
)
from piper_sdk import *

# 测试代码
if __name__ == "__main__":
    piper = C_PiperInterface()
    piper.ConnectPort()
    while True:
        import time
        print(piper.GetArmJointMsgs())
        print(piper.GetArmGripperMsgs())
        time.sleep(0.005)
        pass
```

## 机械臂关节角控制

没有夹爪可以注释夹爪部分

```python
#!/usr/bin/env python3
# -*-coding:utf8-*-
# 注意demo无法直接运行，需要pip安装sdk后才能运行
from typing import (
    Optional,
)
import time
from piper_sdk import *

def enable_fun(piper:C_PiperInterface):
    '''
    使能机械臂并检测使能状态,尝试5s,如果使能超时则退出程序
    '''
    enable_flag = False
    # 设置超时时间（秒）
    timeout = 5
    # 记录进入循环前的时间
    start_time = time.time()
    elapsed_time_flag = False
    while not (enable_flag):
        elapsed_time = time.time() - start_time
        print("--------------------")
        enable_flag = piper.GetArmLowSpdInfoMsgs().motor_1.foc_status.driver_enable_status and \
            piper.GetArmLowSpdInfoMsgs().motor_2.foc_status.driver_enable_status and \
            piper.GetArmLowSpdInfoMsgs().motor_3.foc_status.driver_enable_status and \
            piper.GetArmLowSpdInfoMsgs().motor_4.foc_status.driver_enable_status and \
            piper.GetArmLowSpdInfoMsgs().motor_5.foc_status.driver_enable_status and \
            piper.GetArmLowSpdInfoMsgs().motor_6.foc_status.driver_enable_status
        print("使能状态:",enable_flag)
        piper.EnableArm(7)
        piper.GripperCtrl(0,1000,0x01, 0)
        print("--------------------")
        # 检查是否超过超时时间
        if elapsed_time > timeout:
            print("超时....")
            elapsed_time_flag = True
            enable_flag = True
            break
        time.sleep(1)
        pass
    if(elapsed_time_flag):
        print("程序自动使能超时,退出程序")
        exit(0)

if __name__ == "__main__":
    piper = C_PiperInterface("can0")
    piper.ConnectPort()
    piper.EnableArm(7)
    enable_fun(piper=piper)
    # piper.DisableArm(7)
    piper.GripperCtrl(0,1000,0x01, 0)
    factor = 57324.840764 #1000*180/3.14
    position = [0,0,0,0,0,0,0]
    count = 0
    while True:
        print(piper.GetArmStatus())
        import time
        count  = count + 1
        # print(count)
        if(count == 0):
            print("1-----------")
            position = [0,0,0,0,0,0,0]
        elif(count == 500):
            print("2-----------")
            position = [0.2,0.2,-0.2,0.3,-0.2,0.5,0.08]
        elif(count == 1000):
            print("1-----------")
            position = [0,0,0,0,0,0,0]
            count = 0
        
        joint_0 = round(position[0]*factor)
        joint_1 = round(position[1]*factor)
        joint_2 = round(position[2]*factor)
        joint_3 = round(position[3]*factor)
        joint_4 = round(position[4]*factor)
        joint_5 = round(position[5]*factor)
        joint_6 = round(position[6]*1000*1000)
        # piper.MotionCtrl_1()
        piper.MotionCtrl_2(0x01, 0x01, 50, 0x00)
        piper.JointCtrl(joint_0, joint_1, joint_2, joint_3, joint_4, joint_5)
        piper.GripperCtrl(abs(joint_6), 1000, 0x01, 0)
        piper.MotionCtrl_2(0x01, 0x01, 50, 0x00)
        time.sleep(0.005)
        pass
```

## 设置机械臂为主臂

```python
#!/usr/bin/env python3
# -*-coding:utf8-*-
# 注意demo无法直接运行，需要pip安装sdk后才能运行
# 设置机械臂为主动臂，直接设置即可
from typing import (
    Optional,
)
from piper_sdk import *
import time

# 测试代码
if __name__ == "__main__":
    piper = C_PiperInterface()
    piper.ConnectPort()
    piper.MasterSlaveConfig(0xFA, 0, 0, 0)
```

## 设置机械臂为从臂

```python
#!/usr/bin/env python3
# -*-coding:utf8-*-
# 注意demo无法直接运行，需要pip安装sdk后才能运行
# 设置机械臂为从动臂
# 注意，如果是在机械臂处于主动臂模式下，发送设置指令后需要重新启动机械臂
from typing import (
    Optional,
)
import time
from piper_sdk import *

# 测试代码
if __name__ == "__main__":
    piper = C_PiperInterface()
    piper.ConnectPort()
    piper.MasterSlaveConfig(0xFC, 0, 0, 0)
```

## 读取机械臂的所有电机的最大加速度限制

```python
#!/usr/bin/env python3
# -*-coding:utf8-*-
# 注意demo无法直接运行，需要pip安装sdk后才能运行
# 读取机械臂的所有电机的最大加速度限制

from typing import (
    Optional,
)
import time
from piper_sdk import *

# 测试代码
if __name__ == "__main__":
    piper = C_PiperInterface()
    piper.ConnectPort()
    while True:
        # piper.SearchAllMotorMaxAccLimit() # 这个函数放在ConnectPort中了，每次执行程序都会发送一次读取指令
        print(piper.GetAllMotorMaxAccLimit())
        time.sleep(0.01)
```

## 读取机械臂的所有电机的最大角度和速度限制

```python
#!/usr/bin/env python3
# -*-coding:utf8-*-
# 注意demo无法直接运行，需要pip安装sdk后才能运行
# 读取机械臂的所有电机的最大加速度限制

from typing import (
    Optional,
)
import time
from piper_sdk import *

# 测试代码
if __name__ == "__main__":
    piper = C_PiperInterface()
    piper.ConnectPort()
    while True:
        # piper.SearchAllMotorMaxAngleSpd() # 这个函数放在ConnectPort中了，每次执行程序都会发送一次读取指令
        print(piper.GetAllMotorAngleLimitMaxSpd())
        time.sleep(0.01)
```

## 机械臂重置

```python
#!/usr/bin/env python3
# -*-coding:utf8-*-
# 注意demo无法直接运行，需要pip安装sdk后才能运行
# 设置机械臂重置，需要在mit或者示教模式切换为位置速度控制模式时执行

from typing import (
    Optional,
)
import time
from piper_sdk import *

# 测试代码
if __name__ == "__main__":
    piper = C_PiperInterface()
    piper.ConnectPort()
    piper.MotionCtrl_1(0x02,0,0)#恢复
    piper.MotionCtrl_2(0, 0, 0, 0x00)#位置速度模式
```

## 设置机械臂为mit控制模式

```python
#!/usr/bin/env python3
# -*-coding:utf8-*-
# 注意demo无法直接运行，需要pip安装sdk后才能运行
# 设置机械臂为mit控制模式，这个模式下，机械臂相应最快

from typing import (
    Optional,
)
import time
from piper_sdk import *

# 测试代码
if __name__ == "__main__":
    piper = C_PiperInterface()
    piper.ConnectPort()
    piper.MotionCtrl_2(0, 0, 0, 0xAD)# 0xFC
```
