import json
from typing import Any, AsyncGenerator
from azure.servicebus.aio import ServiceBusClient
from azure.servicebus import ServiceBusReceivedMessage, ServiceBusReceiveMode
from azure.servicebus.exceptions import MessagingEntityNotFoundError
from loguru import logger


Message = dict[str, Any]


async def receive(conn_str: str, topic: str, subscription: str) -> AsyncGenerator[Message, Any]:
    try:
        servicebus_client = ServiceBusClient.from_connection_string(
            conn_str=conn_str,
            logging_enable=True,
        )
    except Exception:
        logger.exception("Failed to create the service bus client")
        # TODO proper error handling
        raise
    
    try:
        
        # TODO - maybe switch back to subscription instead of queue?
        # receiver = servicebus_client.get_subscription_receiver(
        #     topic_name=topic,
        #     subscription_name=subscription,

        # )
        receiver = servicebus_client.get_queue_receiver(
                queue_name=topic,
                receive_mode=ServiceBusReceiveMode.RECEIVE_AND_DELETE
            )
    except Exception:
        logger.exception("Failed to get queue receiver")
            # TODO proper error handling
        raise
    try:
        async for msg in receiver:
            # await receiver.complete_message(msg)
            message = parse_message(msg)
            logger.debug(f"Received {message}")
            yield message
    except MessagingEntityNotFoundError:
        # TODO better error handling
        raise
    except Exception:
        raise
        

def parse_message(msg: ServiceBusReceivedMessage) -> Message:
    body = str(msg.message)
    application_properties={key.decode(): val.decode() for key, val in msg.application_properties.items()}
    message_id = msg._raw_amqp_message.properties.message_id.decode()

    return {
        "body": json.loads(body),
        "application_properties": application_properties,
        "id": message_id,
    }
    
