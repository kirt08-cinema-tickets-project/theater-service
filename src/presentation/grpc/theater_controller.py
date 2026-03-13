import grpc
from kirt08_contracts.theater import theater_pb2_grpc, theater_pb2

from src.application.usecases.theater import GetTheaterUsecase, ListTheaterUsecase, CreateTheaterUsecase

from src.domain.exceptions import (
    TheaterNotFoundException,
    TheaterNotUniqueException,
)

from src.presentation.grpc.theater_mapped import to_proto


class TheaterGrpcController(theater_pb2_grpc.TheaterServiceServicer):
    def __init__(
        self,
        create_usecase,
        get_usecase,
        list_usecase,
    ):
        self._create_usecase: CreateTheaterUsecase = create_usecase
        self._get_usecase: GetTheaterUsecase = get_usecase
        self._list_usecase: ListTheaterUsecase = list_usecase

    async def CreateTheater(self, request, context):
        entity = await self._create_usecase.execute(
            name = request.name,
            address = request.address
        )
        return theater_pb2.CreateTheaterResponse(
                theater=to_proto(entity)
            )
    
    async def GetTheater(self, request, context):
        try:
            entity = await self._get_usecase.execute(
                id = request.id
            )
            return theater_pb2.GetTheaterResponse(
                theater=to_proto(entity)
            )
        except TheaterNotFoundException as e:
            await context.abort(grpc.StatusCode.NOT_FOUND, str(e))
        except TheaterNotUniqueException as e:
            await context.abort(grpc.StatusCode.FAILED_PRECONDITION, str(e))
    
    async def ListTheaters(self, request, context):
        entities = await self._list_usecase.execute()
        return theater_pb2.ListTheatersResponse(
            theaters=[to_proto(e) for e in entities]
        )