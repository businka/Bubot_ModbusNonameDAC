import asyncio
import logging
import unittest

from bubot.buject.OcfDevice.subtype.Device.Device import Device
from bubot.core.TestHelper import wait_run_device, wait_cancelled_device

logging.basicConfig()


class TestThermostat(unittest.IsolatedAsyncioTestCase):
    net_interface = "192.168.1.11"
    config = {
        '/oic/con': {
            'master': dict(),
            'slave': 0x0a,
            'udpCoapIPv6': None
        }
    }

    async def asyncSetUp(self) -> None:
        def set_modbus(device):
            device.data['/oic/con']['master']['anchor'] = self.modbus_device.link['anchor']
            device.data['/oic/con']['master']['eps'] = self.modbus_device.link['eps']
            device.data['/oic/con']['master']['eps'][0]['net_interface'] = self.net_interface

        self.modbus_device = Device.init_from_file(di='2', class_name='SerialServerHF511')
        self.modbus_task = await wait_run_device(self.modbus_device)

        self.device = Device.init_from_config(self.config, di='1', class_name='ModbusNonameDAC')
        set_modbus(self.device)
        self.task = await wait_run_device(self.device)

        # self.actuator = Device.init_from_config(self.config, di='1')
        # self.device_task = await wait_run_device(self.device)

    async def asyncTearDown(self) -> None:
        print('asyncTearDown')
        await asyncio.gather(
            wait_cancelled_device(self.device, self.task),
            wait_cancelled_device(self.modbus_device, self.modbus_task)
        )

    async def test_init(self):
        pass

    async def test_update(self):
        number = 1
        try:
            result1 = await self.device.retrieve_switch(number)
            result2 = await self.device.update_switch(number, not result1)
            result3 = await self.device.retrieve_switch(number)
            self.assertEqual(result3, not result1)
            result4 = await self.device.update_switch(number, result1)
            result5 = await self.device.retrieve_switch(number)
            self.assertEqual(result5, result1)
        except Exception as err:
            print(err)

    async def test_all_on(self):
        await self.device.update_switch(1, True)
        await self.device.update_switch(2, True)
        await self.device.update_switch(3, True)
        await self.device.update_switch(4, True)
