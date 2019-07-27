# IoT Lights
Let strangers on the internet control my smart lights

## Requirements
* Smart RGB Lights (I use [IKEA TR&#197;DFRI](https://www.ikea.com/us/en/catalog/products/20411562/))
* A [Home-Assistant](https://www.home-assistant.io/) setup

## Setup
1. Log into home assistant and create a [long lived access token](https://www.home-assistant.io/docs/authentication/#your-account-profile)
2. Create a secret key for the python client to use
    ```python
    import os, base64

    print(base64.b64encode(os.urandom(32)))
    ```

## Runing Locally
1. Save your access token and secret key in environment variables:
    ```sh
    export ACCESS_TOKEN="Home assistant access token"
    export SECRET_KEY="..."
    export WS_ENDPOINT="ws://127.0.0.1:8080/websocket"
    ```
2. Setup the virtual environment
    ```sh
    python3 -m venv venv
    venv/bin/pip install -r requirements.txt
    ```
3. Start the server
    ```sh
    venv/bin/python -m iot_lights.server --host "127.0.0.1" --port 8080
    ```
4. Start the client
    ```sh
    venv/bin/python -m iot_lights.client \
        --websocket="$WS_ENDPOINT" \
        --secret="$SECRET_KEY" \
        --token="$ACCESS_TOKEN"
    ```
