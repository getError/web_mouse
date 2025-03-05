import asyncio
import websockets
import pyautogui
import json
from websockets.server import serve
import threading
from screeninfo import get_monitors

from concurrent.futures import ThreadPoolExecutor

threadPool = ThreadPoolExecutor(max_workers=20, thread_name_prefix="test_")

pyautogui.PAUSE = 0.005


async def handle_client(websocket):
    lock = threading.Lock()

    def process_move(data):
        if lock.acquire(blocking=False):
            try:
                screen = get_monitors()[0]
                x = data['x'] * screen.width * 0.1
                y = data['y'] * screen.height * 0.1
                # 计时
                pyautogui.moveRel(x, y)
            except Exception as e:
                print(f"Error: {e}")
            finally:
                lock.release()
                return
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
                threadPool.submit(process_move, data)
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
