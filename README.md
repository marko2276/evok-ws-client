# evok-ws-client
A simple wrapper/library for a client using websockets to connect to [Evok API](https://github.com/UniPiTechnology/evok) running on Unipi devices.
The library was implemented primarily to be used with home-assistant but hopefully it might find also other usage as well.

Functionality wise it supports bare minimum so that my home-assitent project can function.

# Example
```
import asyncio
from evok_ws_client import *

ip_addr = "192.168.77.21"

async def main():
    neuron = UnipiEvokWsClient(ip_addr, "M203", "test_neuron")
    try:
        await neuron.evok_connect()
        await neuron.evok_full_state_sync()
        print (await neuron.evok_receive())
    except:
        pass

if __name__ == "__main__":
    asyncio.run(main())
```
# License
MIT License
