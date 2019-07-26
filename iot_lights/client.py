import argparse
import asyncio
import json
import re

import aiohttp
import requests
from aiohttp import WSMsgType

HEX_RE = r'^#(?P<red>[A-Fa-f0-9]{2})(?P<green>[A-Fa-f0-9]{2})(?P<blue>[A-Fa-f0-9]{2})'
def hex_to_rgb(color):
    match = re.match(HEX_RE, color)

    if not match:
        return (255, 255, 255)
    
    return (
        int(match.group('red'), 16),
        int(match.group('green'), 16),
        int(match.group('blue'), 16)
    )

SERVER_URL = 'ws://127.0.0.1:8080/websocket'
API_ENDPOINT = 'http://hassio.local:8123/api'


class IoTLightCient:
    def __init__(self, endpoint, websocket, token):
        self.endpoint = endpoint
        self.websocket = websocket
        self.token = token
    
    def handle_message(self, message):
        data = json.loads(message.data)
        headers = {
            'Authorization': f'Bearer {self.token}'
        } if self.token else {}

        if data['state']:
            requests.post(
                f"{self.endpoint}/services/light/turn_on",
                headers=headers,
                json={
                    'entity_id': data['id'],
                    'brightness_pct': data['brightness'],
                    'rgb_color': hex_to_rgb(data['color'])
                }
            )
        else:
            requests.post(
                f"{self.endpoint}/services/light/turn_off",
                headers=headers,
                json={
                    'entity_id': data['id']
                }
            )
    async def run(self):
        async with aiohttp.ClientSession() as session:
            while True:
                async with session.ws_connect(self.websocket) as websocket:
                    async for message in websocket:
                        if message.type == WSMsgType.TEXT:
                            self.handle_message(message)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--websocket', type=str, default=SERVER_URL)
    parser.add_argument('--endpoint', type=str, default=API_ENDPOINT)
    parser.add_argument('-t', '--token', type=str, default=None)
    args = parser.parse_args()
    
    client = IoTLightCient(
        args.endpoint,
        args.websocket,
        args.token
    )

    loop = asyncio.get_event_loop()
    loop.run_until_complete(client.run())

if __name__ == '__main__':
    main()
