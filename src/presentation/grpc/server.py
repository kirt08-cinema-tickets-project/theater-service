import grpc
import logging

from kirt08_contracts.theater import theater_pb2_grpc

from src.presentation.grpc.theater_controller import TheaterGrpcController

from src.infrastructure.config import settings


log = logging.getLogger(__name__)

async def serve(create_usecase, get_usecase, list_usecase):
    log.info("Server starting up...")
    server = grpc.aio.server()
    
    theater_pb2_grpc.add_TheaterServiceServicer_to_server(
        TheaterGrpcController(
            create_usecase = create_usecase,
            get_usecase = get_usecase,
            list_usecase = list_usecase 
        ),
        server = server
    )
    
    server.add_insecure_port(settings.grpc.server.host + ":" + settings.grpc.server.port)
    await server.start()

    log.info("Server successfully started!")

    await server.wait_for_termination()