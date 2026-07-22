from functools import lru_cache
from pathlib import Path
from typing import TYPE_CHECKING

from chatify.types.attachment import AttachmentObject
from chatify.types.core import AttachmentID
import json, secrets

if TYPE_CHECKING:
    from chatify.app import ChatApp


class AttachmentLib:
    def __init__(self, parent: "ChatApp") -> None:
        self.parent = parent

    @property
    def attachment_path(self):
        a=self.parent.config._folder / "attachments"
        a.mkdir(exist_ok=True)
        return a

    @lru_cache() #the little things add up
    def save_path(self, id: AttachmentID) -> tuple[Path, Path]:
        return (self.attachment_path / str(id)).resolve(),(self.attachment_path / (str(id) + ".meta")).resolve()
    
    async def exists(self, id: AttachmentID):
        file, meta = self.save_path(id)
        return file.exists()
    
    async def get_attachment(self, id: AttachmentID) -> AttachmentObject:
        '''Gets an attachment via its ID.'''
        save_path, meta = self.save_path(id)
        if not save_path.exists():
            raise FileNotFoundError(f'Attachment {id} is not found!')
        contents = save_path.read_bytes()
        _meta: dict = {}
        with open(meta, "r") as f:
            _meta = json.load(f)
        return AttachmentObject(data=contents, *_meta) # pyright: ignore[reportCallIssue]

    async def save_attachment(self, attachment: AttachmentObject):
        '''Saves an attachment to an ID.'''

        id = attachment.id
        if await self.exists(id):
            raise FileExistsError(f"Attachment {id} exists already!")

        file, meta = self.save_path(id)

        _meta = {}

        for prop in attachment.saveable_props:
            _meta[prop] = getattr(attachment, prop)

        with open(file, "wb") as f:
            f.write(attachment.data)

        with open(meta, "w") as f:
            f.write(json.dumps(_meta))
