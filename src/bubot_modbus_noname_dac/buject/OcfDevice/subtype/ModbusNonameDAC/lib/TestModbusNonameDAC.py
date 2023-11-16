import logging
import unittest

from aio_modbus_client.ModbusProtocolRtuHF5111 import ModbusProtocolRtuHF5111 as Protocol
# from aio_modbus_client.TransportSerial import TransportSerial as ModbusSerial
from aio_modbus_client.TransportSocket import TransportSocket as Modbus
# from aio_modbus_client.ModbusProtocolTcp import ModbusProtocolTcp as Protocol
# from bubot.Helper import async_test
from .ModbusNonameDAC import ModbusNonameDAC as Device


class TestModbusToVoltageNoname(unittest.IsolatedAsyncioTestCase):

    @classmethod
    def setUpClass(cls):
        logging.basicConfig(level=logging.DEBUG)
        device_address = 0x0a
        address = ('192.168.1.25', 502)
        cls.device = Device(device_address, Protocol(Modbus(host=address[0], port=address[1])))

    # async def asyncTearDown(self):
        # await self.device.close()

    async def test_set_slave_id(self):
        slave_id = 0x0a
        self.device = Device(0, Protocol(ModbusSerial(host='COM4')))
        res = await self.device.write_param('address', slave_id << 8)
        print(res)

    async def test_is_device(self):
        self.assertTrue(await self.device.is_device())

    async def test_simple_serial(self):
        # slave_id = 0x0a
        # self.device = Device(slave_id, Protocol(ModbusSerial(host='COM4')))
        # print(await self.device.read_param('v2'))
        # print('v0', await self.device.read_param('v0'))
        print('values', await self.device.read_param('values'))
        # print('v2', await self.device.read_param('v2'))
        # print('v3', await self.device.read_param('v3'))
        # print(await self.device.read_param('v2'))
        # print(await self.device.read_param('v3'))
        # res = await self.device.write_param('values', [0, 0, 0, 0])
        # res = await self.device.write_param('values', [9900, 9900, 9900, 9900])
        # print('v1', await self.device.read_param('v1'))
        # res = await self.device.read_param('v2')
        # self.assertEqual(res, True)
        # res = await self.device.read_param('v0')
        # self.assertEqual(res, 0)
        # res = await self.device.write_param('v0', 0)
        # self.assertEqual(res, True)
        # res = await self.device.read_param('v0')
        # self.assertEqual(res, 0)

    async def test_simple_socket(self):
        self.device = Device(0x0a, Protocol(Modbus(host='192.168.1.25', port=502)))
        print(await self.device.read_param('values'))
        # print(await self.device.read_param('v1'), await self.device.read_param('v2') , await self.device.read_param('v3'), await self.device.read_param('v4'))
        # res = await self.device.write_param('v0', 10000)
        # self.assertEqual(res, True)
        # res = await self.device.read_param('v0')
        # self.assertEqual(res, 10000)
        res = await self.device.write_param('v0', 0)
        self.assertEqual(res, True)
        res = await self.device.read_param('v0')
        self.assertEqual(res, 0)

    async def test_find(self):
        value = await self.device.find_devices()
        print(value)
