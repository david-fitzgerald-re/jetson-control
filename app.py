import asyncio
import json
from azure.servicebus.aio import ServiceBusClient
from azure.servicebus.amqp import AmqpMessageBodyType
from azure.servicebus import ServiceBusReceivedMessage
from loguru import logger
from settings import settings


async def receiver(conn_str: str, queue: str):
    try:
        servicebus_client = ServiceBusClient.from_connection_string(
            conn_str=conn_str,
            logging_enable=True,
        )
    except Exception:
        logger.exception("Failed to create the service bus client")
        # TODO proper error handling
        raise 

    async with servicebus_client:
        try:
            receiver = servicebus_client.get_queue_receiver(
                queue_name=queue,
            )
        except Exception:
            logger.exception("Failed to get queue receiver")
            # TODO proper error handling
            raise

        async for msg in receiver:
            msg: ServiceBusReceivedMessage

            if msg.body_type is not AmqpMessageBodyType.DATA:
                raise TypeError(f"Expected msg.body_type to be DATA but it was {msg.body_type}")
                
            messages_bytes = [bytes_ for bytes_ in msg.body]
            if len(messages_bytes) > 1:
                logger.info("Got more than one messages in bytes")
            
            for bytes_ in messages_bytes:
                bytes_: bytes
                try:
                    decoded = bytes_.decode('utf-8')
                except UnicodeDecodeError:
                    logger.exception(f"Failed to decode bytes with utf-8: {bytes_}")
                    raise
                
                try:
                    message = json.loads(decoded)
                except json.decoder.JSONDecodeError:
                    logger.exception(f"Failed to load json {decoded}")
                    raise

                logger.info(f"Received {message}")

            await receiver.complete_message(msg)  # Only necessary with ServiceBusReceiveMode.PEEK_LOCK
            yield message




async def main():
    QUEUE_NAME="orin03-dev"

    async for message in receiver(
        conn_str=settings.SERVICE_BUS_CONN_STRING,
        queue=QUEUE_NAME,
    ):
        pass



if __name__ == "__main__":
    asyncio.run(main())