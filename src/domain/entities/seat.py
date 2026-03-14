from datetime import datetime
from enum import Enum
from dataclasses import dataclass


class StatusType(str, Enum):
    reserved = "reserved"
    availible = "availible"


@dataclass
class SeatEntity:
    id: str
    row: int
    number: int
    price: int
    type: str
    hall_id: str
    status: StatusType
