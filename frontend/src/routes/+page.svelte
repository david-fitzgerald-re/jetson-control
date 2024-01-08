<script>
    import { onMount } from "svelte";
	import Module from "$lib/components/Module.svelte";
    import twin from "$lib/stores/twin.js";
    import messages from "$lib/stores/messages.js";

    // "data" automatically comes from the load 
    // function in +page.server.js
    export let data;

    twin.set(data.props.twin)

    let socket;
    // $: messages = [];
    // $: colour = $twin.properties.reported.colour

    async function handleMessage(event) {
        // console.log(event)
        console.log("Received a message from backend")
        const message = JSON.parse(event.data);
        messages.update((currentMessages) => {
            currentMessages.push(message)
            return currentMessages
        })
        // messages = [...messages, message]
        // console.log(`Message is ${JSON.stringify(message)}`)

        if (message.body.properties.desired) {
            console.log("Received a desired property update - not doing anything with it")
            return
        }
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
    <Module/>
</div>

