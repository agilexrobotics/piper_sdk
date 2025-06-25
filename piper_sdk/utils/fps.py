import threading
import time
from collections import defaultdict
from collections import deque

class C_FPSCounter:
    def __init__(self,
                 start_realtime_fps:bool = False):
        """ 初始化 FPS 统计器 """
        self.start_realtime_fps = start_realtime_fps
        self.fps_data = defaultdict(int)  # 记录帧计数
        self.fps_results = defaultdict(float)  # 计算出的 FPS 结果
        self.prev_data = defaultdict(int)  # 上一次的计数值
        if(self.start_realtime_fps):
            self.time_stamps = defaultdict(deque)  # 存储时间戳
        self.last_time = defaultdict(float)  # 记录上次帧的时间
        self.lock = threading.Lock()  # 确保线程安全
        self.running = False  # 控制线程状态
        self.thread = None  # 线程对象
        self.stop_event = threading.Event()  # 用于控制线程退出
        self.__interval = 0.1

    def set_cal_fps_time_interval(self, interval:float=0.1):
        self.__interval = interval
        return self.__interval
    
    def get_cal_fps_time_interval(self):
        return self.__interval

    def add_variable(self, name, window_size=5000):
        """ 添加新的 FPS 变量，并限制时间窗口大小 """
        with self.lock:
            if name not in self.fps_data:
                self.fps_data[name] = 0
                self.fps_results[name] = 0.0
                if(self.start_realtime_fps):
                    self.time_stamps[name] = deque(maxlen=window_size)  # 限制最大存储窗口
                self.last_time[name] = time.perf_counter()

    def increment(self, name):
        """ 递增帧计数，并记录时间戳 """
        current_time = time.perf_counter()
        with self.lock:
            if name in self.fps_data:
                self.fps_data[name] += 1
                if(self.start_realtime_fps):
                    self.time_stamps[name].append(current_time)  # `deque` 自动管理过期数据
                self.last_time[name] = current_time

    def get_fps(self, name):
        """ 获取 1 秒内的 FPS 计算结果 """
        multiple = 1 / self.__interval
        with self.lock:
            return self.fps_results.get(name, 0.0) * multiple

    def get_real_time_fps(self, name, window=1.0):
        """ 计算过去 window 秒的实时 FPS """
        now = time.perf_counter()
        with self.lock:
            if(self.start_realtime_fps):
                while self.time_stamps[name] and now - self.time_stamps[name][0] > window:
                    self.time_stamps[name].popleft()  # 直接丢弃最早的时间戳
                
                return len(self.time_stamps[name]) / window if self.time_stamps[name] else 0.0
            else: return -1

    def start(self):
        """ 启动 FPS 计算线程，防止重复启动 """
        with self.lock:
            if self.running:
                return  # 已经在运行，避免重复启动
            self.running = True
            self.stop_event.clear()
        
        self.thread = threading.Thread(target=self._calculate_fps, daemon=True)
        self.thread.start()

    def stop(self):
        """ 停止 FPS 计算线程 """
        with self.lock:
            if not self.running:
                return  # 已经停止
            self.running = False
            self.stop_event.set()  # 设置事件，确保线程退出
        
        if self.thread and self.thread.is_alive():
            self.thread.join()

    def cal_average(self, *args):
        """ 计算一组数的平均值，但是只在所有数都不是0的情况下才算；如果有0，就直接返回0 """
        return round(sum(args) / len(args) if args and all(args) else 0,3)

    def _calculate_fps(self):
        """ 定期计算 FPS """
        while not self.stop_event.is_set():
            with self.lock:
                for name in self.fps_data:
                    self.fps_results[name] = self.fps_data[name] - self.prev_data[name]
                    self.prev_data[name] = self.fps_data[name]
            self.stop_event.wait(self.__interval)  # 用 wait() 代替 sleep()，更易控制

# def camera_simulation(fps_counter, name, interval, stop_after=None):
#     """
#     模拟相机帧生成并调用 increment
#     :param fps_counter: FPSCounter 实例
#     :param name: 相机变量名称
#     :param interval: 模拟帧生成的时间间隔
#     :param stop_after: 停止生成数据的时间（秒），为 None 时不停止
#     """
#     start_time = time.perf_counter()
#     while True:
#         if stop_after is not None and time.perf_counter() - start_time > stop_after:
#             print(f"{name} stopped generating data.")
#             break
#         fps_counter.increment(name)
#         time.sleep(interval)


# if __name__ == "__main__":
#     fps_counter = C_FPSCounter()
#     fps_counter.add_variable("camera1")
#     fps_counter.add_variable("camera2")

#     fps_counter.start()

#     try:
#         # 创建线程模拟相机1和相机2的帧生成
#         camera1_thread = threading.Thread(target=camera_simulation, args=(fps_counter, "camera1", 0.01, 5), daemon=True)
#         camera2_thread = threading.Thread(target=camera_simulation, args=(fps_counter, "camera2", 0.01, None), daemon=True)

#         camera1_thread.start()
#         camera2_thread.start()

#         # 打印 FPS
#         while True:
#             print(f"FPS for camera1 (1s avg): {fps_counter.get_fps('camera1')}")
#             print(f"FPS for camera2 (1s avg): {fps_counter.get_fps('camera2')}")
#             print(f"Real-time FPS for camera1: {fps_counter.get_real_time_fps('camera1', window=1.0)}")
#             print(f"Real-time FPS for camera2: {fps_counter.get_real_time_fps('camera2', window=1.0)}")
#             print(f"Instant FPS for camera1: {fps_counter.get_instant_fps('camera1')}")
#             print(f"Instant FPS for camera2: {fps_counter.get_instant_fps('camera2')}")
#             time.sleep(0.01)

#     finally:
#         fps_counter.stop()
