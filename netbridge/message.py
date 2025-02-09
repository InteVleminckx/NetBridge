from dataclasses import dataclass
from .message_code import MessageCode
import pickle
import base64
from uuid import UUID

@dataclass
class Message:
    code: MessageCode = None
    data: str = None
    id: UUID = None



