<script>
    import { onMount } from "svelte";
    // import { inspect } from 'util';
    // import { messageStore } from "$lib/receiver";

    let socket;
    let messages = [];

    async function handleMessage(event) {
        console.log(event)
        const message = JSON.parse(event.data);
        messages = [...messages, message]
    }

    onMount(() => {
        socket = new WebSocket('ws://127.0.0.1:8000/ws')
        socket.addEventListener('message', handleMessage)
    })
</script>

<div>
    <h1>WebSocket Messages from <code>orin03-dev</code></h1>

    <ul>
        {#each messages as message (message.id)}
            <li>
                <ul>
                    <li>{JSON.stringify(message.body)}</li>
                    <li>{JSON.stringify(message.application_properties)}</li>
                </ul>
            </li>
        {/each}
    </ul>
</div>
