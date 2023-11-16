from bubot.OcfResource.OcfResource import OcfResource


class OicRSwitchBinary(OcfResource):
    async def on_get(self, request):
        await self.device.retrieve_values()
        return await super().on_get(request)

    async def on_post(self, request, response):
        self.debug('post', request)
        number = int(request.uri_path[1])
        payload = request.decode_payload()
        await self.device.update_value(
            number,
            open_level=payload.get('openLevel'),
            value=payload.get('value')
        )
        return await super().on_post(request, response)
