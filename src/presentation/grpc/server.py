import grpc
import logging

from kirt08_contracts.theater import theater_pb2_grpc
from kirt08_contracts.hall import hall_pb2_grpc
from kirt08_contracts.seats import seats_pb2_grpc


from src.presentation.grpc.theater_controller import TheaterGrpcController
from src.presentation.grpc.hall_controller import HallGrpcController
from src.presentation.grpc.seat_controller import SeatGrpcController

from src.infrastructure.config import settings


log = logging.getLogger(__name__)

async def serve(
        theater_controller: TheaterGrpcController,
        hall_controller: HallGrpcController,
        seat_controller: SeatGrpcController,
    ):
    log.info("Server starting up...")
    server = grpc.aio.server()
    
    theater_pb2_grpc.add_TheaterServiceServicer_to_server(
        theater_controller,
        server = server
    )

    hall_pb2_grpc.add_HallServiceServicer_to_server(
        hall_controller,
        server = server
    )

    seats_pb2_grpc.add_SeatsServiceServicer_to_server(
        seat_controller,
        server = server
    )
    
    server.add_insecure_port(settings.grpc.server.host + ":" + settings.grpc.server.port)
    await server.start()

    log.info("Server successfully started!")

    await server.wait_for_termination()