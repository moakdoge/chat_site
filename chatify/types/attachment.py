import base64
from dataclasses import dataclass
from functools import cached_property
import secrets
import filetype, uuid

from chatify.types.core import AttachmentID

@dataclass(slots=True, unsafe_hash=True)
class AttachmentObject:
    data: bytes
    name: str
    id: AttachmentID
    mime_type: str

    @classmethod
    def new(cls, data: bytes, name: str, mime_type: str = "application/octet-stream"):
        if mime_type == "application/octet-stream":
            m = filetype.guess(data)
            if m:
                mime_type = m.mime
        
        id = "attachment-"+base64.urlsafe_b64encode(
            secrets.token_bytes(16)
        ).decode().rstrip("=")
        return cls(
            data=data,
            name=name,
            id=id,
            mime_type=mime_type
        )
    
    @cached_property
    def guess(self):
        return filetype.guess(self.data)
    
    @property
    def ext(self):
        return "."+self.guess.extension if self.guess is not None else ".raw"

    @property
    def saveable_props(self) -> tuple[str, ...]:
        return ("name","mime_type",)