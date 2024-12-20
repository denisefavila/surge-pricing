import logging
import os
import signal

from dotenv import load_dotenv

from app.driver_position.generate_data import generate_driver_position
from app.redis_stream.redis_client import redis_client
from app.redis_stream.redis_producer import RedisProducer, signal_handler

# Load environment variables from the .env file
load_dotenv()

DRIVER_POSITION_STREAM = os.getenv("REDIS_STREAM", "driver_position_stream")

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

shutdown_flag = False


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    with redis_client() as client:
        logger.info("Starting DriverPosition producer...")

        # Driver position producer
        driver_position_producer = RedisProducer(
            client=client,
            stream_name=DRIVER_POSITION_STREAM,
            generate_data_callback=generate_driver_position,
        )

        driver_position_producer.produce()
