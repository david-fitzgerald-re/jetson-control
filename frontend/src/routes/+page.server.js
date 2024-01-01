import { env } from '$env/dynamic/private'
import pkg from 'azure-iothub';
const { Registry } = pkg;
import { fail } from '@sveltejs/kit';

const CONN_STRING = env.DEV_IOTHUB_CONNECTION_STRING
const DEVICE_ID = "orin03-dev"
const MODULE_ID = "config-manager"


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
    const registry = Registry.fromConnectionString(CONN_STRING)
    const twin = await registry.getModuleTwin(
        DEVICE_ID,
        MODULE_ID,
    )
    const properties = twin.responseBody.properties
    console.log('Module twin properties retrieved:', properties);

    return properties;
}