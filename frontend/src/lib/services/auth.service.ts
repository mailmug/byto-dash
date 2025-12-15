import { api } from './http';

export const login = (email: string, password: string) =>
	api('/auth/jwt/login', {
		headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
		method: 'POST',
		body: new URLSearchParams({ username: email, password })
	});


export const register = (name: string, email: string, password: string) =>
	api('/auth/register', {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body:  JSON.stringify({
			name:name,
			email: email,
			password:password
		})
	});

function sleep(ms:any) {
	return new Promise(resolve => setTimeout(resolve, ms));
}
export const me = () =>
	api('/users/me', {
		method: 'GET',
		headers: { 
			'Content-Type': 'application/json',
			'Authorization': 'Bearer ' + localStorage.getItem('token')
		},
	});