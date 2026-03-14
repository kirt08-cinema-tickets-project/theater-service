import grpc
from kirt08_contracts.hall import hall_pb2, hall_pb2_grpc

from src.domain.exceptions import (
    SeatNotFoundException,
    SeatNotUniqueException,
)

from src.application.usecases.hall import (
    CreateHallUsecase,
    GetHallUsecase,
    ListHallUsecase,
)


class HallGrpcController(hall_pb2_grpc.HallServiceServicer):
    def __init__(
        self,
        create_hall_usecase,
        get_hall_usecase,
        list_hall_usecase
    ):
        self._create_hall_usecase: CreateHallUsecase = create_hall_usecase
        self._get_hall_usecase: GetHallUsecase = get_hall_usecase
        self._list_hall_usecase: ListHallUsecase = list_hall_usecase

    async def CreateHall(self, request, context):
        entity = await self._create_hall_usecase.execute(
            name = request.name,
            theater_id = request.theater_id,
            layouts = request.layouts
        )
        return hall_pb2.CreateHallResponse(
            hall = hall_pb2.Hall(
                id = entity.id,
                name = entity.name,
                theater_id = entity.theater_id
            )
        )
    
    async def GetHall(self, request, context):
        try:
            entity = await self._get_hall_usecase.execute(
                id = request.id
            )
        except SeatNotFoundException as e:
            await context.abort(grpc.StatusCode.NOT_FOUND, str(e))
        except SeatNotUniqueException as e:
            await context.abort(grpc.StatusCode.FAILED_PRECONDITION, str(e))

        return hall_pb2.GetHallResponse(
            hall = hall_pb2.Hall(
                id = entity.id,
                name = entity.name,
                theater_id = entity.theater_id
            )
        )
    
    async def ListHallsByTheater(self, request, context):
        halls_entities = await self._list_hall_usecase.execute(
            theater_id = request.theater_id
        )
        halls = [
            hall_pb2.Hall(
                id = hall.id,
                name = hall.name,
                theater_id = hall.theater_id
            )
            for hall in halls_entities
        ]
        return hall_pb2.ListHallsResponse(halls = halls)