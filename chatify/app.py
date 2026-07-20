from pathlib import Path

import chatify.api.channel
import chatify.api.messages
import chatify.api.files
import chatify.api.config
class ChatApp:
    def __init__(self, base: Path) -> None:
        self.channels = chatify.api.channel.ChannelSubsystem(self)
        self.messages = chatify.api.messages.MessageLib(self)
        self.files = chatify.api.files.FileManager(self)
        self.config = chatify.api.config.Config(base, self)