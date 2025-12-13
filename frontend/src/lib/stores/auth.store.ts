import { writable } from 'svelte/store';

export const auth = writable({
	token: null,
	user: null
});