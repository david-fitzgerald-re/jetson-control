import { env } from '$env/dynamic/private'
import pkg from 'azure-iothub';
const { Registry } = pkg;
import { fail } from '@sveltejs/kit';

const CONN_STRING = env.DEV_IOTHUB_CONNECTION_STRING
const IOTHUB_DEVICE_ID = env.IOTHUB_DEVICE_ID;
const IOTHUB_MODULE_ID = env.IOTHUB_MODULE_ID;


if (!CONN_STRING) {
    throw new Error("DEV_IOTHUB_CONNECTION_STRING is not set")
}
if (!IOTHUB_DEVICE_ID) {
    throw new Error("IOTHUB_DEVICE_ID is not set")
}
if (!IOTHUB_MODULE_ID) {
    throw new Error("IOTHUB_MODULE_ID is not set")
}


const registry = Registry.fromConnectionString(CONN_STRING)


/** @type {import('./$types').PageServerLoad} */
export async function load({ params }) {
    const twinProperties = await fetchTwin();

    // Return data that will be passed to the page component
    return {
        props: {
            twinProperties,
        },
    };
}


export const actions = {
    /**
     * 
     * @param {import("./$types").RequestEvent} event
     * @returns 
     */
    default: async (event) => {
        console.log("Default action called!")
        const { cookies, request } = event

        const data = await request.formData();
        const jsonData = Object.fromEntries(data)
        const colour = data.get("colour")
    
        console.log(`jsonData: ${JSON.stringify(jsonData)}`)
        console.log(`Chosen colour ${colour}`)
        
        if (Math.random() < 0.5) {
            return fail(400)
        } else {
            return { success: true }
        }
    }
}


async function fetchTwin() {
    const result = await registry.getModuleTwin(
        IOTHUB_DEVICE_ID,
        IOTHUB_MODULE_ID,
    )
    const properties = twin.responseBody.properties
    console.log('Module twin properties retrieved:', properties);

    return properties;
}