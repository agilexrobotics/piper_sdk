# Piper 机械臂 SDK使用说明

## 安装方法

### 安装依赖

```shell
pip3 install python-can
```

## 快速使用

### 使能can模块

**can模块设定脚本`can_config.sh`**

首先需要设置好shell脚本参数

#### 单条机械臂

在`can_config.sh`中，`EXPECTED_CAN_COUNT`参数设置为`1`，因为一条机械臂使用一个can模块

##### pc只插入一个usb转can模块

直接执行

```bash
bash can_config.sh can0 1000000
```

##### pc插入多个usb转can模块

拔掉所有can模块

只将连接到机械臂的can模块插入PC，执行`sudo ethtool -i can0 | grep bus`，并记录下`bus-info`的数值例如`1-2:1.0`

ps:**一般第一个插入的can模块会默认是can0，如果没有查询到can可以使用`ip link show`来显示所有can，然后先后插入查看can编号**

假设上面的操作记录的`bus-info`数值为`1-2:1.0`

然后执行,查看can设备是否激活成功

```bash
bash can_config.sh can_piper 1000000 "1-2:1.0"
```

ps:**此处的意思是，1-2:1.0硬件编码的usb端口插入的can设备，名字被重命名为can_piper，波特率为1000000，并激活**

然后执行`ifconfig`查看是否有`can_piper`，如果有则can模块设置成功

#### 两对机械臂(四条)

如果是四条机械臂，也就是两对主从机械臂

在`can_config.sh`中，`EXPECTED_CAN_COUNT`参数一般设置为`2`，因为四条机械臂使用两个can模块

然后将两个can模块中的其中一个(一般第一个插入左臂所在的模块)单独插入PC，执行`sudo ethtool -i can0 | grep bus`，并记录下`bus-info`的数值例如`1-2:1.0`

接着插入下一个can模块，注意不可以与上次can模块插入的usb口相同，然后执行`sudo ethtool -i can1 | grep bus`

ps:**一般第一个插入的can模块会默认是can0，第二个为can1，如果没有查询到can可以使用`ip link show`来显示所有can，然后先后插入查看can编号**

假设上面的操作记录的`bus-info`数值分别为`1-2:1.0`、`1-4:1.0`

则将下面的`USB_PORTS["1-9:1.0"]="can_left:1000000"`中的中括号内部的双引号内部的参数换为`1-2:1.0`，另一个同理
`USB_PORTS["1-5:1.0"]="can_right:1000000"` -> `USB_PORTS["1-4:1.0"]="can_right:1000000"`

ps:**此处的意思是，1-2:1.0硬件编码的usb端口插入的can设备，名字被重命名为can_left，波特率为1000000，并激活**

然后执行`bash can_config.sh`,查看两个can设备是不是激活成功

然后执行`ifconfig`查看是不是有`can_left`和`can_right`，如果有则can模块设置成功

## 注意事项

- 需要先激活can设备，并且设置正确的波特率，才可以读取机械臂消息或者控制机械臂
