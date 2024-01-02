<script>
    import { onMount } from "svelte";
    import ColourSelector from "$lib/components/ColourSelector.svelte";
    import twin from "$lib/twin.js";

    // "data" automatically comes from the load 
    // function in +page.server.js
    export let data;

    setTimeout(() => {
        // TODO - remove this
        // Just to simulate delay of getting the twin
        twin.set(data.props.twin)
    }, 3000)

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
    
    /* TODO understand how to syntax highlight @apply from tailwind  */
    .message {
        @apply mb-3 ;
    }

    .scroll-container {
        border: 1px solid lightgrey;
        @apply h-96 overflow-y-auto;
    }

    pre {
        border: none;
    }
    .operative { font-weight: bold; border: 1px solid yellow; }
    /* #quine { border: 4px solid #88c; } */
</style>

<div class="container">
    <h1 class="text-2xl font-bold mb-4">Device State <code>orin03-dev</code></h1>
    <ColourSelector/>
    <!-- <p>Colour: <b>{colour}</b></p> -->
    <h2>Current Twin</h2>

    <div class="scroll-container" id="quine">
        <pre>{JSON.stringify($twin, null, 2)}</pre>
    </div>
    <h2>Etag</h2>
    <pre><code>{$twin.etag}</code></pre>
    <h2>WebSocket Messages</h2>

    <ul>
        {#each messages as message (message.id)}
            <li>
                <ul>
                    <li class="message">
                        <pre>{JSON.stringify(message, null, 2)}</pre>
                    </li>
                </ul>
            </li>
        {/each}
    </ul>
</div>

