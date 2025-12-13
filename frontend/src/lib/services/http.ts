export async function api(url: string, options = {}) {
	const res = await fetch(import.meta.env.VITE_API_URL + url, {
		headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
		...options
	});

	if (!res.ok) throw await res.json();
	return res.json();
}