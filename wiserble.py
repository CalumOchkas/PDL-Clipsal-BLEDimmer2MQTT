#!/usr/bin/env python3
# from bluepy.btle import Peripheral, Characteristic


class WiserDimmer:
    """
    Represents a Clipsal/PDL Iconic BLE-enabled dimmer.

    Assumes the device has already been paired with the host controller (for now) 
    """
    SVC_CONTROL_UUID = "720a9080-9c7d-11e5-a7e3-0002a5d5c51b"

    CHR_STATE = { 
        "UUID": "720a9081-9c7d-11e5-a7e3-0002a5d5c51b",
        "ON":   b'\x01',
        "OFF":  b'\x00'
    }

    CHR_LEVEL = {
        "UUID": "720a9082-9c7d-11e5-a7e3-0002a5d5c51b",
        "MIN":  0,
        "MAX":  10000
    }

    def __init__(self, address: str):
        self.address = address
        self.peripheral = Peripheral(address)
        self.__characteristics = dict()

    def disconnect(self):
        self.peripheral.disconnect()

    def state_on(self):
        return self.state_set(self.CHR_STATE['ON'])

    def state_off(self):
        return self.state_set(self.CHR_STATE['OFF'])

    def state_set(self, state: bytes):
        char = self.__get_characteristic(self.CHR_STATE['UUID'])
        return self.__write(char, state)

    @property
    def state(self):
        char = self.__get_characteristic(self.CHR_STATE['UUID'])
        value = self.__read(char)
        return list(self.CHR_STATE.keys())[list(self.CHR_STATE.values()).index(value)]

    def level_set(self, level: int):
        char = self.__get_characteristic(self.CHR_LEVEL['UUID'])
        value = self.__level_to_bytes(level)
        return self.__write(char, value)

    @property
    def level(self):
        char = self.__get_characteristic(self.CHR_LEVEL['UUID'])
        value = self.__read(char)
        return self.__level_to_int(value)

    def __level_to_bytes(self, as_int: int):
        level = max(min(as_int, self.CHR_LEVEL['MAX']), self.CHR_LEVEL['MIN'])
        return level.to_bytes(2, 'little')
    
    def __level_to_int(self, as_bytes: bytes):
        level = int.from_bytes(as_bytes, 'little')
        return max(min(level, self.CHR_LEVEL['MAX']), self.CHR_LEVEL['MIN'])

    def __get_characteristic(self, uuid):
        if(uuid not in self.__characteristics):
            char = self.peripheral.getCharacteristics(uuid=uuid)[0]
            self.__characteristics[uuid] = char

        return self.__characteristics[uuid]
        
    def __read(self, char: Characteristic):
        return char.read()

    def __write(self, char: Characteristic, value: bytes):
        response = char.write(value, True)
        return response['rsp'][0] == 'wr'