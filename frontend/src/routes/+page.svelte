<script>
    import { onMount } from "svelte";
    import ColourSelector from "$lib/components/ColourSelector.svelte";
    import twin from "$lib/twin.js";

    import { Accordion, AccordionItem } from 'svelte-collapsible'

    // "data" automatically comes from the load 
    // function in +page.server.js
    export let data;

    twin.set(data.props.twin)

    let socket;
    $: messages = [];
    $: colour = $twin.properties.reported.colour

    async function handleMessage(event) {
        console.log(event)
        const message = JSON.parse(event.data);
        messages = [...messages, message]
        console.log(`Message is ${JSON.stringify(message)}`)

        if (message.body.properties.desired) {
            console.log("Received a desired property update - not doing anything with it")
            return
        }

        colour = message.body.properties.reported.colour
        console.log(`Colour is set to: ${colour}`)
        twin.update((currentTwin) => {
            currentTwin.properties.reported.colour = colour
            return currentTwin
        })

    }

    onMount(() => {
        socket = new WebSocket('ws://127.0.0.1:8000/ws')
        socket.addEventListener('message', handleMessage)
    })
</script>

<style>
    .container {
        padding: 1rem;
    }
    
    /* TODO understand how to syntax highlight/intellisense @apply from tailwind  */
    .scroll-container {
        border: 1px solid lightgrey;
        @apply overflow-y-auto;
    }

    pre {
        border: none;
    }
</style>

<div class="container">
    <h1>Device State <code>orin03-dev</code></h1>
    <ColourSelector/>

    <h2>Current Twin</h2>
    <div class="scroll-container h-96 p-1">
        <pre>{JSON.stringify($twin, null, 2)}</pre>
    </div>

    <h2>WebSocket Messages</h2>
    <div class="scroll-container h-screen p-1">
        <Accordion>
            {#each messages as message, index (message.id)}
                <AccordionItem key={message.id}>
                    <div slot='header' class='header'>
                        <div>
                            <h3>Websocket Message {index+1} ({message.body.properties.reported ? "reported" : "desired"})</h3>
                        </div>
                    </div>
                    <pre slot='body' class='body'>{JSON.stringify(message, null, 2)}</pre>
                </AccordionItem>
            { /each }
        </Accordion>
    </div>
</div>

