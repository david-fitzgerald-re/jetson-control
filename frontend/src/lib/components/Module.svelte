<script>
    import { onMount } from "svelte";
    import ColourSelector from "$lib/components/ColourSelector.svelte";
    import twin from "$lib/stores/twin.js";
    import messages from "$lib/stores/messages";

    import { Accordion, AccordionItem } from 'svelte-collapsible'

    $: colour = $twin.properties.reported.colour

    messages.subscribe((messages) => {
        console.log("Messages changed!")
        if (messages.length > 0) {
            const [latestMessage, ...olderMessages] = messages.reverse()
            console.log(`latestMessage: ${JSON.stringify(latestMessage)}`)

            if (!("body" in latestMessage)) {
                // TODO improve message validation/handling/filtering
                console.error("Message is missing body")
                return
            }

            if (!("properties" in latestMessage.body)) {
                console.error("Message is missing properties")
                // TODO improve message validation/handling/filtering
                return
            }
            
            if (!("reported" in latestMessage.body.properties)) {
                console.warn("Message is missing reported properties")
                // TODO improve message validation/handling/filtering
                return
            }

            colour = latestMessage.body.properties.reported.colour
            console.log(`Colour was just set to: ${colour}`)
            twin.update((currentTwin) => {
                currentTwin.properties.reported.colour = colour
                return currentTwin
            })
        }
    })

    onMount(() => {
        console.log("Module component mounted")
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
    <h1> <code>config-manager</code> Module</h1>
    <ColourSelector/>

    <h2>Current Twin</h2>
    <div class="scroll-container h-96 p-1">
        <pre>{JSON.stringify($twin, null, 2)}</pre>
    </div>

    <h2>WebSocket Messages</h2>
    <div class="scroll-container h-screen p-1">
        <Accordion>
            {#each $messages as message, index (message.id)}
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

