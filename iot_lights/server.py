import argparse
import json
import logging
import os
from weakref import WeakSet

from aiohttp import WSMsgType, web

logger = logging.getLogger(__name__)

async def update_lightbulb(app, data, key):
    for light in app.lights:
        if light['id'] == data['id']:
            light.update(data)
            await app.broadcast(light)
            return

    if key == os.environ.get('SECRET_KEY'):
        print(f"Adding light {data['id']}")
        app.lights.append(data)
        await app.broadcast(data)

def is_valid(data):
    return 'id' in data        

async def handle_message(app, message):
    data = json.loads(message.data)
    if not is_valid(data):
        return
    key = data.pop('key', None)
    await update_lightbulb(app, data, key)

async def get_websocket(request: web.Request) -> web.WebSocketResponse:
    websocket = web.WebSocketResponse()
    await websocket.prepare(request)

    request.app.websockets.add(websocket)

    for light in request.app.lights:
        await websocket.send_json(light)

    async for message in websocket:
        if message.type == WSMsgType.TEXT:
            await handle_message(request.app, message)
        elif message.type == WSMsgType.ERROR:
            logger.error(message.exception())

    return websocket


async def broadcast(app, message):
    for websocket in app.websockets:
        await websocket.send_json(message)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=8080)
    parser.add_argument('-H', '--host', type=str, default="0.0.0.0")
    args = parser.parse_args()

    application = web.Application()
    application.websockets = WeakSet()
    application.lights = []
    application.broadcast = lambda message: broadcast(application, message)
    application.add_routes([
        web.get('/websocket', get_websocket)
    ])


    web.run_app(application, host=args.host, port=args.port)


if __name__ == '__main__':
    main()