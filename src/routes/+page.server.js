import { env } from '$env/dynamic/private'
import pkg from 'azure-iothub';
const { Registry } = pkg;


const CONN_STRING = env.DEV_IOTHUB_CONNECTION_STRING
const DEVICE_ID = "orin03-dev"
const MODULE_ID = "config-manager"


export async function load({ params }) {
    const serverData = await fetchTwin(params);

    // Return data that will be passed to the page component
    return {
        props: {
            serverData,
        },
    };
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