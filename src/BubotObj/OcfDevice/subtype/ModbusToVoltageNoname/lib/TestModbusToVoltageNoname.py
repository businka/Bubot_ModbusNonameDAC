import unittest
import asyncio
from aio_modbus_client.TransportSerial import TransportSerial as ModbusSerial
from aio_modbus_client.TransportSocket import TransportSocket as Modbus
from aio_modbus_client.ModbusProtocolRtuHF5111 import ModbusProtocolRtuHF5111 as Protocol
# from aio_modbus_client.ModbusProtocolTcp import ModbusProtocolTcp as Protocol
import logging
import time
import inspect
# from bubot.Helper import async_test
from .ModbusToVoltageNoname import ModbusToVoltageNoname as Device


def async_test(f):
    def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        # kwargs['loop'] = loop
        if inspect.iscoroutinefunction(f):
            future = f(*args)
        else:
            coroutine = asyncio.coroutine(f)
            future = coroutine(*args, **kwargs)
        loop.run_until_complete(future)

    return wrapper


class TestModbusToVoltageNoname(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logging.basicConfig(level=logging.DEBUG)


    @async_test
    async def test_set_slave_id(self):
        slave_id = 0x0a
        self.device = Device(0, Protocol(ModbusSerial(host='COM4')))
        res = await self.device.write_param('address', slave_id<<8)
        print(res)

    @async_test
    async def test_simple_serial(self):
        slave_id = 0x0a
        self.device = Device(slave_id, Protocol(ModbusSerial(host='COM4')))
        # print(await self.device.read_param('v2'))
        print(await self.device.read_param('v1'))
        # print(await self.device.read_param('v2'))
        # print(await self.device.read_param('v3'))
        # res = await self.device.write_param('v2', 1000)
        # res = await self.device.read_param('v2')
        # self.assertEqual(res, True)
        # res = await self.device.read_param('v0')
        # self.assertEqual(res, 0)
        # res = await self.device.write_param('v0', 0)
        # self.assertEqual(res, True)
        # res = await self.device.read_param('v0')
        # self.assertEqual(res, 0)

    @async_test
    async def test_simple_socket(self):
        self.device = Device(0x0a, Protocol(Modbus(host='192.168.1.25', port=502)))
        print(await self.device.read_param('v1'))
        # print(await self.device.read_param('v1'), await self.device.read_param('v2') , await self.device.read_param('v3'), await self.device.read_param('v4'))
        # res = await self.device.write_param('v0', 10000)
        # self.assertEqual(res, True)
        # res = await self.device.read_param('v0')
        # self.assertEqual(res, 10000)
        res = await self.device.write_param('v0', 0)
        self.assertEqual(res, True)
        res = await self.device.read_param('v0')
        self.assertEqual(res, 0)
