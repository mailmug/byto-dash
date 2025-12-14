export async function api(url: string, options = {}) {
	const res = await fetch(import.meta.env.VITE_API_URL + url, {
		...options
	});

	if (!res.ok) throw await res.json();
	return res.json();
}