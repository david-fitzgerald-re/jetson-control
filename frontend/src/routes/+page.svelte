<script>
    import { onMount } from "svelte";
    import ColourSelector from "$lib/components/ColourSelector.svelte";
    import twinStore from "$lib/twin.js";
	import { stringify } from "postcss";
    // data automatically comes from the load 
    // function in +page.server.js
    export let data;

    setTimeout(() => {
        // Just to simulate delay to get the twin
        twinStore.set(data.props.twinProperties)
    }, 1000)

    let socket;
    $: messages = [];
    // $: colour = data.props.twinProperties.reported.colour
    $: colour = $twinStore.reported.colour

    async function handleMessage(event) {
        console.log(event)
        const message = JSON.parse(event.data);
        messages = [...messages, message]
        console.log(`Message is ${JSON.stringify(message)}`)
        colour = message.body.properties.reported.colour
        console.log(`Colour is set to: ${colour}`)
        twinStore.update((currentTwin) => {
            currentTwin.reported.colour = colour
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
</style>

<div class="container">
    <h1 class="text-2xl font-bold mb-4">Device State <code>orin03-dev</code></h1>
    <ColourSelector currentColour={colour}/>
    <!-- <p>Colour: <b>{colour}</b></p> -->
    <h2>Current Twin</h2>
    <p>{JSON.stringify($twinStore)}</p>
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

