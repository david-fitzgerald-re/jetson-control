import { messageStore } from '$lib/receiver';
import { ServiceBusClient } from '@azure/service-bus'
// import { inspect } from 'util';


export async function receiveMessages() {
    console.log("Running receiveMessages")
    messageStore.update((prevMessages) => [
        ...prevMessages,
        "Hello, World!"
    ])
}


export async function receiveMessages2() {
    console.log("Running receiver")

    const CONN_STRING="REDACTED"
    const QUEUE="orin03-dev"
    const serviceBusClient = new ServiceBusClient(CONN_STRING)
    const receiver = serviceBusClient.createReceiver(QUEUE)
    
    for await (let message of receiver.getMessageIterator()) {
        // console.log(inspect(message))
        // debugger;
        console.log(`Received message: ${message}`)
        console.log(`Received message: ${message.body}`)
        
        messageStore.update((prevMessages) => [
            ...prevMessages,
            message.body
        ])

        receiver.completeMessage(message)
    }
}