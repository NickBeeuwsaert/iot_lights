import argparse
import json
import logging
import os
from weakref import WeakSet

from aiohttp import WSMsgType, web

from .schema import EventSchema

logger = logging.getLogger(__name__)


async def add_light(app, data):
    if app.secret_key != data.get('key'):
        logger.error("Key Mismatch")
        return

    logger.info("adding light")

    app.lights[data['light']['id']] = data['light']
    await app.broadcast({
        "type": "addLight",
        "light": data['light']
    })


async def update_light(app, data):
    light = data['light']
    app.lights[light['id']] = light

    await app.broadcast({
        'type': 'changeLight',
        'light': light
    })

async def handle_message(app, message):
    schema = EventSchema().bind(secret_key=app.secret_key)

    data = schema.deserialize(
        json.loads(message.data)
    )

    if data['type'] == 'addLight':
        await add_light(app, data)
    elif data['type'] == 'changeLight':
        await update_light(app, data)

async def get_websocket(request: web.Request) -> web.WebSocketResponse:
    websocket = web.WebSocketResponse()
    await websocket.prepare(request)

    request.app.websockets.add(websocket)

    for light in request.app.lights.values():
        await websocket.send_json({
            'type': 'addLight',
            'light': light
        })

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
    application.lights = {}
    application.broadcast = lambda message: broadcast(application, message)
    # if no secret key is provided, make sure no secret key will ever match
    application.secret_key = os.environ.get('SECRET_KEY', object())
    application.add_routes([
        web.get('/websocket', get_websocket)
    ])


    web.run_app(application, host=args.host, port=args.port)


if __name__ == '__main__':
    main()