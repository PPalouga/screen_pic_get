import pyautogui
import time
import tkinter as tk
import threading

flag_record = False
x = 100
y = 100
width = 300
height = 200
x0=None
y0=None
rect=None


def recordstart():
    global flag_record
    flag_record = True
    threading.Thread(target=recording_loop).start()
    

def recordend():
    global flag_record
    flag_record = False

def recording_loop():
    # 设置截图区域，例如：左上角坐标(x, y)和区域宽高(width, height)
    global x, y, width, height
    # 设置截图间隔时间（1000毫秒）
    interval = 5
    while flag_record:
        # 截取指定区域
        screenshot = pyautogui.screenshot(region=(x, y, width, height))
        # 可以选择保存截图到文件（可选）
        screenshot.save(f'screenshot_{int(time.time())}.png')
        # 等待100毫秒
        time.sleep(interval)


def start_selection():
    # 隐藏按钮窗口
    #root.withdraw()
    # 显示全屏窗口
    record_root.deiconify()
    # 绑定鼠标事件
    record_root.bind("<ButtonPress-1>", on_drag_start)
    record_root.bind("<B1-Motion>", on_dragging)
    record_root.bind("<ButtonRelease-1>", on_drag_end)

def on_drag_start(event):
    """记录拖拽开始时的鼠标位置"""
    global drag_start_x, drag_start_y, selection_rect
    drag_start_x, drag_start_y = event.x_root, event.y_root
    # 创建一个矩形来表示选择区域
    selection_rect = canvas.create_rectangle(event.x, event.y, event.x, event.y, outline='red', fill='', width=2)

def on_dragging(event):
    """更新拖拽过程中的选择区域"""
    global drag_start_x, drag_start_y, selection_rect
    canvas.coords(selection_rect, drag_start_x, drag_start_y, event.x_root, event.y_root)

def on_drag_end(event):
    global x, y, width, height
    global drag_start_x, drag_start_y, selection_rect
    """拖拽结束，计算区域坐标和尺寸"""
    x1, y1 = min(drag_start_x, event.x_root), min(drag_start_y, event.y_root)
    x2, y2 = max(drag_start_x, event.x_root), max(drag_start_y, event.y_root)
    width = x2 - x1
    height = y2 - y1
    x, y = x1, y1
    print(f"Selected area: x={x1}, y={y1}, width={width}, height={height}")
    # 清除画布上的矩形
    canvas.delete(selection_rect)
    # 关闭全屏窗口
    record_root.withdraw()
    # 显示按钮窗口
    root.deiconify()


if __name__ == '__main__':
    # 创建主窗口
    root = tk.Tk()
    root.title("简单窗口示例")
    # 设置窗口大小
    root.geometry("300x200")
    #root.attributes('-alpha', 0.5)  # 设置窗口半透明

    # 创建按钮，点击后开始选择区域
    button = tk.Button(root, text="选择区域", command=start_selection)
    button.pack(side='top', fill='x', expand=False)

    # 创建一个按钮，并设置点击时调用的函数
    button = tk.Button(root, text="开始录屏", command=recordstart)
    button.pack(side='top', fill='x', expand=False)

    # 创建一个按钮，并设置点击时调用的函数
    button = tk.Button(root, text="结束录屏", command=recordend)
    button.pack(side='top', fill='x', expand=False)


    # 创建全屏窗口
    record_root = tk.Tk()
    record_root.attributes('-fullscreen', True)  # 全屏
    record_root.attributes('-alpha', 0.3)  # 设置窗口半透明
    record_root.attributes('-topmost', True)  # 确保窗口在最上层
    record_root.configure(bg='white')  # Set background color to white
    record_root.withdraw()  # 初始时隐藏全屏窗口
    # 创建画布
    canvas = tk.Canvas(record_root, cursor="cross")
    canvas.pack(fill="both", expand=True)

    # 运行主循环
    root.mainloop()
