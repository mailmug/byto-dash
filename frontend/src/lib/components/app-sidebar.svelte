<script lang="ts">
	import DashboardIcon from "@tabler/icons-svelte/icons/dashboard";
	import InnerShadowTopIcon from "@tabler/icons-svelte/icons/inner-shadow-top";
	import NavMain from "./nav-main.svelte";
	import * as Sidebar from "$lib/components/ui/sidebar/index.js";
	import type { ComponentProps } from "svelte";
    import DeviceAirtag from "@tabler/icons-svelte/icons/device-airtag";
    import Logout from "@tabler/icons-svelte/icons/logout";
    import User from "@tabler/icons-svelte/icons/user";

	const data = {
		navMain: [
			{
				title: "Dashboard",
				url: "/dashboard",
				icon: DashboardIcon,
			},
			{
				title: "Devices",
				url: "/dashboard/devices",
				icon: DeviceAirtag,
			},
			{
				title: "Profile",
				url: "/dashboard/profile",
				icon: User,
			},
			{
				title: "Logout",
				url: "#",
				icon: Logout,
			},
		],
	};

	let { ...restProps }: ComponentProps<typeof Sidebar.Root> = $props();
</script>

<Sidebar.Root collapsible="offcanvas" {...restProps}>
	<Sidebar.Header>
		<Sidebar.Menu>
			<Sidebar.MenuItem>
				<Sidebar.MenuButton class="data-[slot=sidebar-menu-button]:!p-1.5">
					{#snippet child({ props })}
						<a href="##" {...props}>
							<InnerShadowTopIcon class="!size-5" />
							<span class="text-base font-semibold">Acme Inc.</span>
						</a>
					{/snippet}
				</Sidebar.MenuButton>
			</Sidebar.MenuItem>
		</Sidebar.Menu>
	</Sidebar.Header>
	<Sidebar.Content>
		<NavMain items={data.navMain} />
	</Sidebar.Content>
	<Sidebar.Footer>
	</Sidebar.Footer>
</Sidebar.Root>
