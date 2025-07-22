# detect arm 文件使用文档

## 1 首先需要使用0.3.0以上的piper_sdk版本

查看pip包版本

```bash
pip3 show piper_sdk
```

输出

```bash
Name: piper_sdk
Version: 0.3.0
Summary: A sdk to control Agilex piper arm
Home-page: https://github.com/agilexrobotics/piper_sdk
Author: RosenYin
Author-email: 
License: MIT License
Location: .../.local/lib/python3.8/site-packages
Requires: python-can
Required-by: 
```

## 2 执行detect_arm.py

注意路径，使用上述`Location`路径内部的`piper_sdk`包，可以通过下述指令获取

```bash
export PIPER_SDK_PATH=$(pip3 show piper_sdk | grep ^Location: | awk '{print $2}')
```

```bash
echo $PIPER_SDK_PATH
```

文件有三个输入参数：

- `--can_port`用来设定读取的can名称
- `--hz`用来设定终端打印刷新的频率
- `--req_flag`用来设定是否在执行脚本时给机械臂发送请求查询指令来获取机械臂的一些静态参数，比如固件版本、关节最大速度等

正常情况下执行下述指令即可

注意`PIPER_SDK_PATH`是由上述指令获取

```bash
python3 $PIPER_SDK_PATH/piper_sdk/demo/detect_arm.py --can_port can0 --hz 10 --req_flag 1
```
