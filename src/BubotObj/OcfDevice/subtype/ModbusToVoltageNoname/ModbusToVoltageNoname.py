from BubotObj.OcfDevice.subtype.ModbusSlave.ModbusSlave import ModbusSlave
from BubotObj.OcfDevice.subtype.ModbusToVoltageNoname.__init__ import __version__ as device_version
from BubotObj.OcfDevice.subtype.ModbusToVoltageNoname.lib.ModbusToVoltageNoname import \
    ModbusToVoltageNoname as ModbusDevice


# import logging

# _logger = logging.getLogger(__name__)


class ModbusToVoltageNoname(ModbusSlave):
    ModbusDevice = ModbusDevice
    version = device_version
    template = False

    file = __file__

    async def on_retrieve_switch(self, number, message):
        open_level = await self.modbus.read_param(f'v{number}')
        if open_level > 0:
            value = {'openLevel': open_level, 'value': True}
        else:
            value = {'openLevel': open_level, 'value': False}

        self.set_param(f'/v{number}', 'value', value);
        return self.get_param(f'/v{number}')

    async def on_update_v(self, number, message):
        open_level = message.cn.get('openLevel')
        value = message.cn.get('value')
        if open_level is not None:
            if 1 <= open_level <= 100:
                value = {'openLevel': open_level, value: True}
            elif open_level == 0:
                value = {'openLevel': open_level, value: False}
            else:
                raise Exception(f'not valud range openLevel. need 0..100, current {open_level}')
        elif value is not None:
            try:
                if value:
                    open_level = 100
                    value = {'openLevel': open_level, value: True}
                else:
                    open_level = 0
                    value = {'openLevel': open_level, value: False}
                await self.modbus.write_param(f'v{number}', open_level)
            except KeyError:
                pass
            except Exception as err:
                self.log.error(err)
        self.update_param(f'/v{number}', None, value)
        return self.get_param(f'/v{number}')

    async def on_retrieve_v0(self, message):
        return await self.on_retrieve_switch(0, message)

    async def on_retrieve_v1(self, message):
        return await self.on_retrieve_switch(1, message)

    async def on_retrieve_v2(self, message):
        return await self.on_retrieve_switch(2, message)

    async def on_retrieve_v3(self, message):
        return await self.on_retrieve_switch(3, message)

    async def on_update_v0(self, message):
        return await self.on_update_v(0, message)

    async def on_update_v1(self, message):
        return await self.on_update_v(1, message)

    async def on_update_v2(self, message):
        return await self.on_update_v(2, message)

    async def on_update_v3(self, message):
        return await self.on_update_v(3, message)

    async def on_idle(self):
        try:
            for i in range(4):
                res = await self.modbus.read_param(f'switch_{i}')
                self.set_param(f'/switch/{i}', 'value', res)
        except Exception as err:
            self.log.error(err)
