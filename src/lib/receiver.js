import { writable } from 'svelte/store'

// Initial store state
const initialState = [];

// Create a writable svelte store
export const messageStore = writable(initialState)

// Function to update the store state
// export const updateMessages = (newMessages) => {
//     messageStore.set(newMessages)
// }
