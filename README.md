# rtvc

https://rtvc.fly.dev - testbed for realtime voice calling (rtvc)

The following gets an OpenAI realtime voice model to call you!

```shell
curl \
  -u $RTVC_ADMIN_USER_USERNAME:$RTVC_ADMIN_USER_PASSWORD \
  -H "Content-type: application/json" \
  -d "{\"number\": \"$NUMBER\", \"system_message\": \"talk like a pirate\"}" \
  https://rtvc.fly.dev/api/v1/call
```

## TODO

List of things to resolve in order of priority before we can iterate:

1. [x] JSON API authentication
    * https://www.starlette.io/authentication/
    * https://chatgpt.com/share/678ebb6b-0cb4-800e-a598-122399435b18
1. [x] validate that only twilio makes websocket requests
    * https://www.twilio.com/docs/usage/webhooks/webhooks-security#validating-signatures-from-twilio
1. [ ] add some request parameters to control:
    * system message
    * whether AI messages first
    * what the AI messages first
1. [ ] store audio files + transcript log somewhere, probably s3
1. [ ] handle interruptions nicely
    * https://github.com/twilio-samples/speech-assistant-openai-realtime-api-python?tab=readme-ov-file#interrupt-handlingai-preemption
1. [ ] add a basic UI that:
    * lists historical call logs
    * allows initiating a new call given a phone number

## appendix

* https://www.twilio.com/en-us/blog/outbound-calls-python-openai-realtime-api-voice
    * initial code ripped from here
