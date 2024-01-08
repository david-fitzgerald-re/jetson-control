import { writable } from "svelte/store";
import * as Types from "$lib/types.js"

/**
 * @type {Types.Twin}
 */
const initialTwinState = {
  // TODO - this would possibly use a schema of the twin?
  deviceId: "",
  moduleId: "",
  etag: "",
  deviceEtag: "",
  status: "",
  statusUpdateTime: "",
  connectionState: "",
  lastActivityTime: "",
  cloudToDeviceMessageCount: "",
  authenticationType: "",
  x509Thumbprint: {
    primaryThumbprint: "",
    secondaryThumbprint: "",
  },
  modelId: "",
  version: NaN,
  properties: {
    desired: {
      colour: "unknown"
    },
    reported: {
      colour: "unknown"
    }
  }
}

let twin = writable(initialTwinState)

export default twin;