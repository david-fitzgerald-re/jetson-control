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
        
        # TODO - maybe switch back to subscription topic instead of queue?
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
            if message is None:
                continue
            logger.debug(f"Received {message}")
            yield message
    except MessagingEntityNotFoundError as exc:
        logger.exception(exc)
        raise
    except Exception as exc:
        logger.exception(exc)
        raise
    # TODO it appears backend authentication timed out 
    # after (I think) 24-48hrs. Need to make the front 
    # end show an error if/when the backend disconnects.
    # Might have to poll the event queue task to 
"""
2024-01-08 05:12:44.302 | DEBUG    | backend.service_bus:parse_message:68 - Discarding robot-heartbeat message
Unexpected error occurred (TimeoutError('Authentication attempt timed-out.')). Handler shutting down.
Traceback (most recent call last):
  File "/Users/david/.pyenv/versions/3.11.4/lib/python3.11/site-packages/azure/servicebus/aio/_base_handler_async.py", line 269, in _do_retryable_operation
    return await operation(**kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/david/.pyenv/versions/3.11.4/lib/python3.11/site-packages/azure/servicebus/aio/_transport/_pyamqp_transport_async.py", line 226, in iter_next_async
    pyamqp_message = await cast(AsyncIterator["Message"], receiver._message_iter).__anext__()
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/david/.pyenv/versions/3.11.4/lib/python3.11/site-packages/azure/servicebus/_pyamqp/aio/_client_async.py", line 893, in _message_generator_async
    receiving = await self.do_work_async()
                ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/david/.pyenv/versions/3.11.4/lib/python3.11/site-packages/azure/servicebus/_pyamqp/aio/_client_async.py", line 354, in do_work_async
    if not await self.client_ready_async():
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/david/.pyenv/versions/3.11.4/lib/python3.11/site-packages/azure/servicebus/_pyamqp/aio/_client_async.py", line 331, in client_ready_async
    if not await self.auth_complete_async():
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/david/.pyenv/versions/3.11.4/lib/python3.11/site-packages/azure/servicebus/_pyamqp/aio/_client_async.py", line 317, in auth_complete_async
    if self._cbs_authenticator and not await self._cbs_authenticator.handle_token():
                                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/david/.pyenv/versions/3.11.4/lib/python3.11/site-packages/azure/servicebus/_pyamqp/aio/_cbs_async.py", line 258, in handle_token
    raise TimeoutError("Authentication attempt timed-out.")
TimeoutError: Authentication attempt timed-out.
2024-01-08 05:29:29.966 | ERROR    | backend.service_bus:receive:51 - Handler failed: Authentication attempt timed-out..
"""
        

def parse_message(msg: ServiceBusReceivedMessage) -> Message:
    body = str(msg.message)
    application_properties={key.decode(): val.decode() for key, val in msg.application_properties.items()}
    message_id = msg._raw_amqp_message.properties.message_id.decode()

    message = {
        "body": json.loads(body),
        "application_properties": application_properties,
        "id": message_id,
    }
    message_type = message["application_properties"].get("type")

    if message_type in ("robot-heartbeat", "heartbeat"):
        logger.debug(f"Discarding {message_type} message")
        return None
    
    if (
        message["application_properties"].get('moduleId') != 'config-manager'
    ):
        # breakpoint()
        pass

    return message
    
