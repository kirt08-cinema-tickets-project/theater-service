import grpc
from kirt08_contracts.seats import seats_pb2, seats_pb2_grpc

from src.domain.exceptions import (
    SeatNotFoundException,
    SeatNotUniqueException,
)

from src.application.usecases.seat import (
    GetSeatUsecase,
    ListSeatUsecase,
)


class SeatGrpcController(seats_pb2_grpc.SeatsServiceServicer):
    def __init__(
        self,
        get_seat_usecase,
        list_seat_usecase
    ):
        self._get_seat_usecase: GetSeatUsecase = get_seat_usecase
        self._list_seat_usecase: ListSeatUsecase = list_seat_usecase

    async def GetSeat(self, request, context):
        try:
            entity = await self._get_seat_usecase.execute(
                id = request.id
            )
        except SeatNotFoundException as e:
            await context.abort(grpc.StatusCode.NOT_FOUND, str(e))
        except SeatNotUniqueException as e:
            await context.abort(grpc.StatusCode.FAILED_PRECONDITION, str(e))

        return seats_pb2.GetSeatResponse(
            seat = seats_pb2.Seat(
                id = entity.id,
                row = entity.row,
                number = entity.number,
                price = entity.price,
                status = entity.status.value,
                type = entity.type,
                hall_id = entity.hall_id
            )
        )
    
    async def ListSeatsByHall(self, request, context):
        seats_entities = await self._list_seat_usecase.execute(
            hall_id = request.hall_id,
            screening_id = request.screening_id
        )
        seats = [
            seats_pb2.Seat(
                id = seat.id,
                row = seat.row,
                number = seat.number,
                price = seat.price,
                status = seat.status.value,
                type = seat.type,
                hall_id = seat.hall_id
            )
            for seat in seats_entities
        ]
        return seats_pb2.ListSeatsResponse(seats = seats)