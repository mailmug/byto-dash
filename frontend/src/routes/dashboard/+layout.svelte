<script lang="ts">
	import * as Sidebar from "$lib/components/ui/sidebar/index.js";
	import AppSidebar from "$lib/components/app-sidebar.svelte";
	import SiteHeader from "$lib/components/site-header.svelte";
    import { onMount } from "svelte";
    import { me } from "@/services/auth.service";
    import { goto } from "$app/navigation";
    import { authStore } from "@/stores/auth.store";
	let { children } = $props();
	onMount(()=>{
		me().then((data)=>{ 
            if(data.is_verified === false){  
                goto('/verify-user');
            }
            authStore.set({
				token: localStorage.getItem('token'),
				user: data
			});
        }).catch(e=>{
            localStorage.setItem('token', '');
            goto('/login');
        });
	});
</script>

<Sidebar.Provider
	style="--sidebar-width: calc(var(--spacing) * 72); --header-height: calc(var(--spacing) * 12);"
>
	<AppSidebar variant="inset" />
	<Sidebar.Inset>
		<SiteHeader />
		<div class="flex flex-1 flex-col">
			<div class="@container/main flex flex-1 flex-col gap-2">
				 
				{@render children()}
				 
			</div>
		</div>
	</Sidebar.Inset>
</Sidebar.Provider>
