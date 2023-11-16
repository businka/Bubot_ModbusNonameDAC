from bubot_helpers.ExtException import ExtException
from bubot_modbus.buject.OcfDevice.subtype.ModbusSlave.ModbusSlave import ModbusSlave
from bubot_modbus_noname_dac import __version__ as device_version
from .OicRSwitchBinary import OicRSwitchBinary
from .lib.ModbusNonameDAC import \
    ModbusNonameDAC as ModbusDevice


class ModbusNonameDAC(ModbusSlave):
    ModbusDevice = ModbusDevice
    version = device_version
    template = False
    reversed = True
    max_open_level = 10000
    default_open_level = 0
    file = __file__

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for num in range(3):
            self.resource_layer.add_handler(f'/v{num + 1}', OicRSwitchBinary)

    async def retrieve_switch(self, number):
        await self.retrieve_values()
        return self.get_param(f'/v{number}', 'value')

    async def update_switch(self, number, value):
        open_level, value = await self.update_value(number, value=value)
        return value

    async def update_value(self, number, *, open_level=None, value=None):
        try:
            current_values = await self.retrieve_values()
            if open_level is not None or value is not None:
                _new_value = self.convert_to_raw(open_level, value)

                if _new_value != current_values[number - 1]:
                    current_values[number - 1] = _new_value
                    await self.modbus.write_param('values', current_values)
                    open_level, value = self.convert_from_raw(_new_value)
                    self.update_param(f'/v{number}', None, {'openLevel': open_level, 'value': value})
            return open_level, value
        except Exception as err:
            raise ExtException(parent=err, action=f'{self.__class__.__name__}.update_switch')

    def convert_to_raw(self, open_level, value):
        if open_level is not None:
            raw_value = min(int(open_level * 100 / self.max_open_level), self.max_open_level)
            if self.reversed:
                raw_value = self.max_open_level - value
        elif value is not None:
            raw_value = self.max_open_level if value else 0
            if self.reversed:
                raw_value = self.max_open_level - raw_value
        else:
            raw_value = self.default_open_level
        return raw_value

    def convert_from_raw(self, value):
        open_level = min(int(value * 100 / self.max_open_level), self.max_open_level)
        if self.reversed:
            open_level = 100 - open_level
        value = True if open_level else False
        return open_level, value

    async def retrieve_values(self):
        try:
            res = await self.modbus.read_param('values')
            for i, value in enumerate(res):
                open_level, value = self.convert_from_raw(value)
                self.update_param(f'/v{i + 1}', None, {'openLevel': open_level, 'value': value})
            return res
        except Exception as err:
            ext_err = ExtException(parent=err)

    async def on_idle(self):
        try:
            await self.retrieve_values()
        except Exception as err:
            ext_err = ExtException(parent=err)
            self.log.error(ext_err)
            await self.return_to_pending(ext_err)
