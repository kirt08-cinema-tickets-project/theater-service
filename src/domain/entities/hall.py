from datetime import datetime
from dataclasses import dataclass


@dataclass
class HallEntity:
    id: str
    name: str
    theater_id: str
    created_at: datetime
    updated_at: datetime