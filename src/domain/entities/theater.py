from datetime import datetime
from dataclasses import dataclass


@dataclass
class TheaterEntity:
    id: str
    name: str
    address: str
    created_at: datetime
    updated_at: datetime