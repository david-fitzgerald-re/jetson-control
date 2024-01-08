import { writable } from "svelte/store";
import * as Types from "$lib/types.js"

/**
 * @type {Types.Message[]}
 */
const initialState = [
]

let messages = writable(initialState)

export default messages
