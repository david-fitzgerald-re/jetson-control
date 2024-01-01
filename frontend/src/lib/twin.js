import { writable } from "svelte/store";

/**
 * @typedef {Object} Twin
 * @property {Object.<string, any>} reported - The reported properties
 * @property {Object.<string, any>} desired - The desired properties
 */


/**
 * @type {Twin}
 */
const initialTwinState = {
  // TODO - this would possibly use a schema of the twin?
  desired: {
    colour: "unknown"
  },
  reported: {
    colour: "unknown"
  }
}

// { reported: { [key: string]: any; }; desired: { [key: string]: any; }; }

let currentTwin = writable(initialTwinState)

export default currentTwin;