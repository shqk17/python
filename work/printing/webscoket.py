import asyncio
import json
import logging
import websockets

logging.basicConfig()

STATE = {'value': 0}

USERS = set()

async def notify_users():
    if USERS:
        # asyncio.wait doesn't accept an empty list
        for user in USERS:
            recv_str = await user.recv()
            cred_dict = recv_str.split(";")
            # 密码可以使用 非对称加密 后期完善
            if cred_dict[0] == "admin" and cred_dict[1] == "123456":
                await user.send('{"type":"success"}')
                return True
            else:
                response_str = '{"type":"fail"}'
                await user.send(response_str)


async def register(websocket):
    USERS.add(websocket)
    await notify_users()


async def unregister(websocket):
    USERS.remove(websocket)
    await notify_users()


async def counter(websocket, path):
    # register(websocket) sends user_event() to websocket
    await register(websocket)
    try:
        async for message in websocket:
            print(str(message))
            cred_dict = message.split(";")
            print("通信2：" + str(message))
            if (len(cred_dict) == 1 and cred_dict[0] == '1'):
                # 打印列表
                await websocket.send('{"type":"1","data":"' + str("hhh") + '"}')
            elif len(cred_dict) == 3 and cred_dict[0] == '2':
                # 打印
                await websocket.send('{"type":"打印结束"}')
            else:
                logging.error(
                    "unsupported event: {}", "no user")
    finally:
        await unregister(websocket)


asyncio.set_event_loop(asyncio.new_event_loop())  # 防止出现RuntimeError
asyncio.get_event_loop().run_until_complete(
    websockets.serve(counter, '127.0.0.1', 6893)
)
asyncio.get_event_loop().run_forever()
