import threading
import time
from collections import defaultdict


class C_FPSCounter:
    def __init__(self):
        """
        初始化 FPSCounter 类
        """
        self.fps_data = defaultdict(int)  # 记录连续加的数值
        self.fps_results = defaultdict(float)  # 存储计算的 FPS 结果
        self.prev_data = defaultdict(int)  # 暂存上一次的计数值
        self.lock = threading.Lock()  # 确保线程安全
        self.running = False  # 用于控制线程循环
        self.thread = None  # 存储线程对象

    def add_variable(self, name):
        """
        添加一个新的 FPS 变量
        :param name: 变量名称
        """
        with self.lock:
            if name not in self.fps_data:
                self.fps_data[name] = 0
                self.fps_results[name] = 0.0
                print(f"Added variable: {name}")

    def increment(self, name):
        """
        为指定变量计数加 1
        :param name: 变量名称
        """
        with self.lock:
            if name in self.fps_data:
                self.fps_data[name] += 1

    def get_fps(self, name):
        """
        获取指定变量的 FPS
        :param name: 变量名称
        :return: 当前 FPS 值
        """
        with self.lock:
            return self.fps_results.get(name, 0.0)

    def start(self):
        """
        启动 FPS 计算线程
        """
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._calculate_fps, daemon=True)
            self.thread.start()

    def stop(self):
        """
        停止 FPS 计算线程
        """
        self.running = False
        if self.thread:
            self.thread.join()
    
    def cal_average(self, *args):
        # 如果任意一个数是 0，则返回 0
        if 0 in args:
            return 0

        # 计算正常平均值
        return sum(args) / len(args) if args else 0  # 防止没有参数时除以0

    def _calculate_fps(self):
        """
        定期计算 FPS 的线程方法
        """
        while self.running:
            with self.lock:
                for name in self.fps_data.keys():
                    # 计算 FPS = 当前计数 - 上一次计数
                    self.fps_results[name] = self.fps_data[name] - self.prev_data[name]
                    # 更新 prev_data
                    self.prev_data[name] = self.fps_data[name]
            
            time.sleep(1)  # 每秒计算一次 FPS


def camera_simulation(fps_counter, name, interval, stop_after=None):
    """
    模拟相机帧生成并调用 increment
    :param fps_counter: FPSCounter 实例
    :param name: 相机变量名称
    :param interval: 模拟帧生成的时间间隔
    :param stop_after: 停止生成数据的时间（秒），为 None 时不停止
    """
    start_time = time.time()
    while True:
        if stop_after is not None and time.time() - start_time > stop_after:
            print(f"{name} stopped generating data.")
            break
        fps_counter.increment(name)
        time.sleep(interval)


if __name__ == "__main__":
    fps_counter = C_FPSCounter()
    fps_counter.add_variable("camera1")
    fps_counter.add_variable("camera2")

    fps_counter.start()

    try:
        # 创建线程模拟相机1和相机2的帧生成
        camera1_thread = threading.Thread(target=camera_simulation, args=(fps_counter, "camera1", 0.01, 5), daemon=True)
        camera2_thread = threading.Thread(target=camera_simulation, args=(fps_counter, "camera2", 0.01, None), daemon=True)

        camera1_thread.start()
        camera2_thread.start()

        # 打印 10 秒的 FPS
        while True:
            print(f"FPS for camera1: {fps_counter.get_fps('camera1')}")
            print(f"FPS for camera2: {fps_counter.get_fps('camera2')}")
            time.sleep(0.1)

    finally:
        fps_counter.stop()
