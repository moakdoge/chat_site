import asyncio
import secrets

import time
from chatify.types.core import ChannelID
from chatify.types.channel import *
from chatify.types.message import Message
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from chatify.app import ChatApp

class ChannelSubsystem:
    #TODO: Make this not dogshit
    def __init__(self, parent: "ChatApp") -> None:
        self.CACHE: dict[ChannelID, Channel] = {} 
        self.parent = parent
        self.channel_ids: list[int] = []

        self.load_all()
        self.parent.schedule_task(self._load_loop, repeat_interval=5)
        self.parent.on_exit(self._on_exit)

    async def _on_exit(self):
        for id, chl in self.CACHE.copy().items():
            print(f"Unloading: {chl} ({id})")
            await self._unload(chl)

    def load_all(self):
        for file in (self.parent.config._folder / "channels").glob("*.json"):
            self.channel_ids.append(int(file.stem))

    async def load_channel(self, channelID: ChannelID) -> Channel | None:
        channel = self.CACHE.get(channelID, None)

        if channel is None:
            channel = await self.load(channelID)

        if channel:
            channel.last_loaded = int(time.time())
            return channel
    
    async def register_message(self,channelID: ChannelID, message: Message):
        chan = await self.load_channel(channelID)
        if chan is None:
            raise
        chan.messages.append(message)

    async def export_metadata(self, metadata: ChannelMetadata) -> dict:
        '''exports channel metadata or smth idk im tired as shit just work'''
        return {
            "name": metadata.name,
            "description": metadata.description
        }
    async def export_channel(self, channel: Channel) -> dict:
        '''Exports a channel to a JSON format'''
        return {
            "metadata": await self.export_metadata(channel.metadata),
            "messages": [await self.parent.messages.export_message(m) for m in channel.messages],
            "id": channel.id,            
        }
    
    async def save(self, channel: Channel):
        config = self.parent.config
        config.save_custom(f"channels/{channel.id}.json", await self.export_channel(channel))

    async def load(self, channelID: ChannelID) -> Channel:
        print("LOADING", channelID)
        file = f"channels/{channelID}.json"
        config = self.parent.config
        data = config.load_custom(file)

        if data == {}:
            raise Exception("Channel does not exist!")
        self.CACHE[data["id"]] = Channel(
            metadata=ChannelMetadata(**data["metadata"]),
            messages=[await self.parent.messages.import_message(m) for m in data["messages"]],
            id=data["id"],
            last_loaded=round(time.time())
        )
        return self.CACHE[data["id"]] 

    async def _unload(self, channel: Channel):
        print("UNLOADING", channel.id)
        await self.save(channel)
        del self.CACHE[channel.id]

    async def _load_loop(self):
        for _, channel in self.CACHE.copy().items():
            if time.time() - channel.last_loaded > self.parent.config.lazy_load_time:
                await self._unload(channel)

        
    async def generate_channel_snowflake(self) -> int:
        return secrets.randbits(40)

    async def new_channel(
        self,
        metadata: ChannelMetadata
    ):
        #TODO: implement channel manager over this bs
        new_id = await self.generate_channel_snowflake()
        self.CACHE[new_id] = Channel(
            metadata,
            [],
            new_id
        )
        self.channel_ids.append(new_id)
        await self.save(self.CACHE[new_id])
        return self.CACHE[new_id]
    


