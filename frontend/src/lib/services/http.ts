import { goto } from "$app/navigation";

export async function api(url: string, options = {}) {
	const res = await fetch(import.meta.env.VITE_API_URL + url, {
		...options
	});

	if (res.status === 401) {
		goto('/login');
		return null;
	}

	if (!res.ok) throw await res.json();

	if (res.status !== 204) {
		return res.json();
	}

	return null;
}