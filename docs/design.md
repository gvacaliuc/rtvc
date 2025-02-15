# design

## API

### `/api/v1/calls`

#### `/api/v1/calls/start`

## models

> [!CAUTION]
> These are still a work in progress, not yet sure exactly what form the call
> intent / directives / tool calling should take.

* Contact
    * represents something we can contact
* Call
    * represents an outbound call
    * in various states:
        * requested
        * active
        * completed
* CallTranscript
    * https://platform.openai.com/docs/api-reference/realtime-server-events/response/audio_transcript
    * https://platform.openai.com/docs/api-reference/realtime-server-events/response/audio

### requests

```
* intent
    * system message
    * voice
    * temperature
    * first message
```

### database

```
call:
  - id
  - twilio_sid
  - call intent / goal:
    - system message
    - goal?
    - output data schema?
    - opening message, could be generated based on the goal

transcript
  - call_id
  - object_store_path
```
