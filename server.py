import asyncio
import math

import websockets
import pyautogui
import win32api
import win32con
import json
from websockets.server import serve
import threading
from screeninfo import get_monitors

from concurrent.futures import ThreadPoolExecutor

threadPool = ThreadPoolExecutor(max_workers=20, thread_name_prefix="test_")

pyautogui.PAUSE = 0.005

MAX_MOVE_SIZE = 50


def move_mouse_relative(x_offset, y_offset):
    # 获取当前鼠标的位置
    current_x, current_y = win32api.GetCursorPos()
    # 计算新的鼠标位置
    new_x = current_x + x_offset
    new_y = current_y + y_offset
    # 设置鼠标到新的位置
    win32api.SetCursorPos((new_x, new_y))


async def handle_client(websocket):
    lock = threading.Lock()

    def process_move(data):
        try:
            screen = get_monitors()[0]
            x = data['x'] * screen.width * 0.9
            y = data['y'] * screen.height * 0.9
            # 计时
            # pyautogui.moveRel(x, y)
            move_mouse_relative(min(int(x), int(math.copysign(x, MAX_MOVE_SIZE))), min(int(y), int(math.copysign(y, MAX_MOVE_SIZE))))
        except Exception as e:
            print(f"Error: {e}")
        finally:
            return

    async def process_click(data):
        button = 'left' if data['button'] == 0 else 'right'
        pyautogui.mouseDown(button=button)
        await asyncio.sleep(0.1)
        pyautogui.mouseUp(button=button)

    async for message in websocket:
        try:
            data = json.loads(message)
            if data['type'] == 'move':
                # threadPool.submit(process_move, data)
                process_move(data)
            elif data['type'] == 'click':
                await process_click(data)
        except Exception as e:
            print(f"Error: {e}")


async def main():
    # 假设这里使用的是较新的websockets库，可能需要使用serve方法的正确导入方式
    async with serve(handle_client, "0.0.0.0", 6789):
        print("WebSocket server started on ws://0.0.0.0:6789")
        await asyncio.Future()


if __name__ == "__main__":
    print("Starting server...")
    asyncio.run(main())

if __name__ == "__main__1":
    for i in range(1, 192):
        win32api.SetCursorPos((i, 500))
