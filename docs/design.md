# design

## models

> [!CAUTION]
> These are still a work in progress, not yet sure exactly what form the call
> intent / directives / tool calling should take.

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
