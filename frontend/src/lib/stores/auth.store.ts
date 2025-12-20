import { writable } from 'svelte/store';

type AuthState = {
	token: string | null;
	user: any | null;
};

export const authStore = writable<AuthState>({
	token: null,
	user: null
});