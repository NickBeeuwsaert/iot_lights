import argparse
import asyncio
import json

import aiohttp
import requests
from aiohttp import WSMsgType
from .schema import EventSchema

SERVER_URL = 'ws://127.0.0.1:8080/websocket'
API_ENDPOINT = 'http://hassio.local:8123/api'


class IoTLightCient:
    def __init__(self, endpoint, websocket, token, secret):
        self.endpoint = endpoint
        self.websocket = websocket
        self.token = token
        self.secret = secret
        self.schema = EventSchema().bind(secret_key=self.secret)
    
    @property
    def headers(self):
        if self.token is None:
            return {}
        
        return {
            'Authorization': f'Bearer {self.token}'
        }

    async def handle_message(self, session, message):
        data = self.schema.deserialize(json.loads(message.data))
        if data['type'] != 'changeLight':
            return

        light = data['light']

        if light['state']:
            await session.post(
                f"{self.endpoint}/services/light/turn_on",
                headers=self.headers,
                json={
                    'entity_id': light['id'],
                    'brightness_pct': light['brightness'],
                    'hs_color': (light['hue'], 100)
                }
            )
        else:
            await session.post(
                f"{self.endpoint}/services/light/turn_off",
                headers=self.headers,
                json={
                    'entity_id': light['id']
                }
            )

    async def run(self):
        async with aiohttp.ClientSession() as session:
            initial_states = requests.get(
                f"{self.endpoint}/states",
                headers=self.headers
            ).json()

            light_states = [
                state
                for state in initial_states
                if state['entity_id'].startswith('light.')
            ]
            color_lights = [
                {
                    "id": state['entity_id'],
                    "name": state['attributes']['friendly_name'],
                    "hue": state['attributes']['hs_color'][0],
                    "brightness": 100 * state['attributes']['brightness'] // 255,
                    "state": state['state'] == 'on'
                }
                for state in light_states
                if "hs_color" in state['attributes']
            ]

            while True:
                async with session.ws_connect(self.websocket) as websocket:
                    for color_light in color_lights:
                        await websocket.send_json(
                            {
                                'type': 'addLight',
                                'light': color_light,
                                "key": self.secret
                            }
                        )

                    async for message in websocket:
                        if message.type == WSMsgType.TEXT:
                            await self.handle_message(session, message)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--websocket', type=str, default=SERVER_URL)
    parser.add_argument('--endpoint', type=str, default=API_ENDPOINT)
    parser.add_argument('-t', '--token', type=str, default=None)
    parser.add_argument('--secret', type=str, default='')
    args = parser.parse_args()
    
    client = IoTLightCient(
        args.endpoint,
        args.websocket,
        args.token,
        args.secret
    )

    loop = asyncio.get_event_loop()
    loop.run_until_complete(client.run())

if __name__ == '__main__':
    main()
