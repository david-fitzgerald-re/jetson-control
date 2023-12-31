<script>
    import { onMount } from "svelte";
    import ColourSelector from "$lib/components/ColourSelector.svelte";

    // data automatically comes from the load 
    // function in +page.server.js
    export let data;

    let socket;
    let messages = [];
    let colour = data.props.serverData.reported.colour

    async function handleMessage(event) {
        console.log(event)
        const message = JSON.parse(event.data);
        messages = [...messages, message]
        console.log(`Message is ${JSON.stringify(message)}`)
        colour = message.body.properties.reported.colour
        console.log(`Colour is set to: ${colour}`)
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
</style>

<div class="container">
    <h1>Device State <code>orin03-dev</code></h1>
    <p>Colour: <b>{colour}</b></p>
    <h2>WebSocket Messages</h2>
    
    <ul>
        {#each messages as { id, body, application_properties} (id)}
            <li>
                <ul>
                    <li>{JSON.stringify(body)}</li>
                    <li>{JSON.stringify(application_properties)}</li>
                </ul>
            </li>
        {/each}
    </ul>
</div>

<ColourSelector currentColour={colour}/>
