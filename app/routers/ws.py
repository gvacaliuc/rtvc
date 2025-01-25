import json
import base64
import asyncio

from fastapi import FastAPI, WebSocket
from fastapi.websockets import WebSocketDisconnect
from starlette.middleware.authentication import AuthenticationMiddleware
import websockets

from ..authn import BasicAuthBackend
from ..config import *

app = FastAPI()

SYSTEM_MESSAGE = (
    "You are a helpful and bubbly AI assistant who loves to chat about "
    "anything the user is interested in and is prepared to offer them facts. "
    "You have a penchant for dad jokes, owl jokes, and rickrolling – subtly. "
    "Always stay positive, but work in a joke when appropriate."
)

# TODO: experiment w/ this
VOICE = 'alloy'

# TODO: experiment w/ this, i think there is a mini model
# https://platform.openai.com/docs/models#gpt-4o-realtime 
MODEL = 'gpt-4o-realtime-preview-2024-12-17'

# TODO: to receive transcripts, collect more
LOG_EVENT_TYPES = [
    'error', 'response.content.done', 'rate_limits.updated', 'response.done',
    'input_audio_buffer.committed', 'input_audio_buffer.speech_stopped',
    'input_audio_buffer.speech_started', 'session.created'
]

@app.websocket('/media-stream')
async def handle_media_stream(websocket: WebSocket):
    """Handle WebSocket connections between Twilio and OpenAI."""
    # NOTE:
    # 1. twilio connects to this after a phone call is ...answered?
    # 2. we connect to OpenAI
    # 3. we pass audio messages back and forth
    print("Client connected")
    await websocket.accept()

    async with websockets.connect(
        f'wss://api.openai.com/v1/realtime?model={MODEL}',
        additional_headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "OpenAI-Beta": "realtime=v1"
        }
    ) as openai_ws:
        await initialize_session(openai_ws)
        stream_sid = None

        async def receive_from_twilio():
            """Receive audio data from Twilio and send it to the OpenAI Realtime API."""
            nonlocal stream_sid
            try:
                async for message in websocket.iter_text():
                    data = json.loads(message)
                    # TODO: remove state check?
                    #
                    # State of the WebSocket connection, defined in RFC 6455.
                    #
                    # This attribute is provided for completeness. Typical
                    # applications shouldn’t check its value. Instead, they
                    # should call recv() or send() and handle ConnectionClosed
                    # exceptions.
                    if data['event'] == 'media' and openai_ws.state == websockets.State.OPEN:
                        audio_append = {
                            "type": "input_audio_buffer.append",
                            "audio": data['media']['payload']
                        }
                        await openai_ws.send(json.dumps(audio_append))
                    elif data['event'] == 'start':
                        stream_sid = data['start']['streamSid']
                        print(f"Incoming stream has started {stream_sid}")
            except WebSocketDisconnect | websockets.ConnectionClosed:
                print("Client disconnected.")
                # TODO: remove state check?
                #
                # State of the WebSocket connection, defined in RFC 6455.
                #
                # This attribute is provided for completeness. Typical
                # applications shouldn’t check its value. Instead, they should
                # call recv() or send() and handle ConnectionClosed exceptions.
                if openai_ws.state == websockets.State.OPEN:
                    await openai_ws.close()

        async def send_to_twilio():
            """Receive events from the OpenAI Realtime API, send audio back to Twilio."""
            nonlocal stream_sid
            try:
                async for openai_message in openai_ws:
                    response = json.loads(openai_message)
                    if response['type'] in LOG_EVENT_TYPES:
                        print(f"Received event: {response['type']}", response)
                    if response['type'] == 'session.updated':
                        print("Session updated successfully:", response)
                    if response['type'] == 'response.audio.delta' and response.get('delta'):
                        try:
                            audio_payload = base64.b64encode(base64.b64decode(response['delta'])).decode('utf-8')
                            audio_delta = {
                                "event": "media",
                                "streamSid": stream_sid,
                                "media": {
                                    "payload": audio_payload
                                }
                            }
                            await websocket.send_json(audio_delta)
                        except Exception as e:
                            print(f"Error processing audio data: {e}")
            except Exception as e:
                print(f"Error in send_to_twilio: {e}")
        await asyncio.gather(receive_from_twilio(), send_to_twilio())

async def send_initial_conversation_item(openai_ws):
    """Send initial conversation so AI talks first."""
    initial_conversation_item = {
        "type": "conversation.item.create",
        "item": {
            "type": "message",
            "role": "user",
            "content": [
                {
                    "type": "input_text",
                    "text": (
                        "Greet the user with 'Hello there! I am an AI voice assistant powered by "
                        "Twilio and the OpenAI Realtime API. You can ask me for facts, jokes, or "
                        "anything you can imagine. How can I help you?'"
                    )
                }
            ]
        }
    }
    await openai_ws.send(json.dumps(initial_conversation_item))
    await openai_ws.send(json.dumps({"type": "response.create"}))

async def initialize_session(openai_ws):
    """Control initial session with OpenAI."""
    session_update = {
        "type": "session.update",
        "session": {
            "turn_detection": {"type": "server_vad"},
            "input_audio_format": "g711_ulaw",
            "output_audio_format": "g711_ulaw",
            "voice": VOICE,
            "instructions": SYSTEM_MESSAGE,
            "modalities": ["text", "audio"],
            # TODO: experiment
            "temperature": 0.8,
        }
    }
    print('Sending session update:', json.dumps(session_update))
    await openai_ws.send(json.dumps(session_update))

    # Have the AI speak first
    await send_initial_conversation_item(openai_ws)
