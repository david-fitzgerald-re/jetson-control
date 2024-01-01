import { writable } from "svelte/store";

const initialTwinState = {
  // TODO - this would possibly use a schema of the twin?
  reported: {
    colour: "unknown"
  }
}

let currentTwin = writable(initialTwinState)

export default currentTwin;