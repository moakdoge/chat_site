from pydantic import BaseModel, Field
from ..core import *

class AttachmentReturn(BaseModel):
    data: bytes
    content_type: str
    file_name: str
    size: int
    id: AttachmentID


class AttachmentAccepted(BaseModel):
    success: bool
    id: AttachmentID