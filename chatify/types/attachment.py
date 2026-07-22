from dataclasses import dataclass
from functools import cached_property
import secrets
import filetype

from chatify.types.core import AttachmentID

@dataclass(slots=True)
class AttachmentObject:
    data: bytes
    name: str
    id: AttachmentID


    @classmethod
    def new(cls, data: bytes, name: str):
        return cls(
            data=data,
            name=name,
            id=secrets.randbits(128)
        )
    
    @cached_property
    def guess(self):
        return filetype.guess(self.data)
    
    @property
    def mime(self):
        return self.guess.mime if self.guess else "application/octet-stream"

    @property
    def ext(self):
        return "."+self.guess.extension if self.guess is not None else ".raw"

    @property
    def saveable_props(self) -> tuple[str, ...]:
        return ("name",)