<script lang="ts">
	import './layout.css';
	import favicon from '$lib/assets/favicon.svg';
    import { Toaster } from 'svelte-sonner';
	import { SvelteKitTopLoader } from 'sveltekit-top-loader';

	let { children } = $props();
</script>

<SvelteKitTopLoader color='#438BFF' height={2} />
<svelte:head><link rel="icon" href={favicon} /></svelte:head>
<Toaster richColors position="top-right" />
{@render children()}
