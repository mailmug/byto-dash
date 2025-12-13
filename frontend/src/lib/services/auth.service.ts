import { api } from './http';

export const login = (email: string, password: string) =>
	api('/auth/jwt/login', {
		method: 'POST',
		body: new URLSearchParams({ username: email, password })
	});