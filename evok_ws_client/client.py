import asyncio
import json
import logging
import websockets

_LOGGER = logging.getLogger(__name__)

'''Note: There are far more neuron or unipi devices that should work
   The conf types are unused for now'''
CONF_NEURON_TYPES = ["L203", "M203", "S203"]
supportedEvokDev = ["relay", "led", "input"]

class UnipiEvokWsClient:
    """Wrapper class for connection to Unipi Neuron via EVOK and websocket"""

    def __init__(self, ip_address, neuron_type, name):
        self._ws_address = "ws://" + ip_address + "/ws"
        self._type = neuron_type
        self._ws = None
        self._name = name
        self._bin_state = {}
        for i in supportedEvokDev:
            self._bin_state[i] = {}

    async def evok_connect(self):
        _LOGGER.debug("Connecting to: %s", self._ws_address)
        try:
            self._ws = await websockets.connect(self._ws_address)
        except:
            _LOGGER.warning("Connection FAILED on: %s", self._ws_address)
            return False
        return True

    async def evok_close(self):
        if self._ws == None:
            return True

        _LOGGER.debug("Closing ws to %s", self._ws_address)
        try:
            self._ws = await websockets.close(self._ws)
        except:
            _LOGGER.warning("Unable to close ws : %s", self._ws_address)
            return False
        return True

    async def evok_receive(self, decode = True, state_change_event_callback = None):
        try:
            message = await self._ws.recv()
        except websockets.exceptions.ConnectionClosedError:
            _LOGGER.warning("Evok WS conn CLOSED with Error on: %s", self._ws_address)
            return False
        except websockets.exceptions.ConnectionClosed:
            _LOGGER.warning("Evok WS conn CLOSED on: %s", self._ws_address)
            return False
            
        message = json.loads(message)
        _LOGGER.debug("Evok Received: %s", message)

        if not decode:
            return message

        for section in message:
            if "dev" in section.keys():
                device = section["dev"]
                if device in supportedEvokDev:
                    try:
                        circuit = section["circuit"]
                        value = section["value"]
                    except:
                        continue

                    try:
                        old_val = self._bin_state[device][circuit]
                    except:
                        old_val = None
                        pass

                    if old_val != value:
                        self._bin_state[device][circuit] = value
                        if state_change_event_callback:
                            state_change_event_callback(self._name, device, circuit, value)
        
        return message

    async def evok_send(self, device, circuit, value):
        cmd = {}
        cmd["cmd"] = "set"
        cmd["dev"] = device
        cmd["circuit"] = circuit
        cmd["value"] = value
        cmdjson = json.dumps(cmd)
        _LOGGER.debug("Evok SEND: %s", cmdjson)
        await self._evok_send_over_ws(cmdjson)

    async def evok_send_raw(self, data):
        await self._evok_send_over_ws(data)
                            
    async def evok_full_state_sync(self):
        # Get current state from the device
        cmd = {}
        cmd["cmd"] = "all"
        cmdjson = json.dumps(cmd)
        await self._evok_send_over_ws(cmdjson)

    ''' This should be extended allow configuration of filters '''
    async def evok_register_default_filter_dev(self):
        # Register filter to get notification changes from the contoller
        # Currently supported filter on device level only
        cmd = {}
        cmd["cmd"] = "filter"
        cmd["devices"] = "relay", "led", "input"
        cmdjson = json.dumps(cmd)
        _LOGGER.debug("Setting Filter: %s", cmdjson)
        await self._evok_send_over_ws(cmdjson)

    def evok_state_get(self, device, circuit):
        try:
            return self._bin_state[device][circuit]
        except:
            return "0"

    async def _evok_send_over_ws(self, cmd):
        _LOGGER.debug("Evok Raw SEND: %s", cmd)
        await self._ws.send(cmd)

