from kirt08_contracts.theater import theater_pb2
from src.domain.entities import TheaterEntity


def to_proto(entity: TheaterEntity) -> theater_pb2.Theater:
    return theater_pb2.Theater(
        id=entity.id,
        name=entity.name,
        address=entity.address,
    )
