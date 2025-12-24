<script lang="ts">
	import { page } from '$app/state';
	import { onMount } from 'svelte';
	import * as Card from '$lib/components/ui/card';
	import { Button } from '$lib/components/ui/button';
	import { Switch } from '$lib/components/ui/switch';
	import { Badge } from '$lib/components/ui/badge';
	import type { Device } from '@/types/device';
	import { api } from '@/services/http';

	const id = page.params.id;
	let device = $state<Device>();
	let power = true;
	let speed = 60;

	onMount(() => {
		api('/api/v1/devices/' + id, {
			method: 'GET',
			headers: {
				'Content-Type': 'application/json',
				'Authorization': 'Bearer ' + localStorage.getItem('token')
			}
		}).then(data=>{
            device = data;
        });
	});
</script>

<!-- Page BG -->
<div class="min-h-screen p-4 md:p-8 space-y-8">

  <!-- Header -->
  <div class="flex items-center justify-between">
    <div>
      <h1 class="text-3xl font-bold text-gray-900 dark:text-gray-100">{device?.title || 'Device Name'}</h1>
      <div class="flex items-center gap-3 mt-2">
        <Badge class="bg-green-500 text-white">Online</Badge>
        <span class="text-sm text-gray-500 dark:text-gray-400">Last seen: 2s ago</span>
      </div>
    </div>
    <Button variant="outline" class="hover:bg-gray-100 dark:hover:bg-gray-700">Settings</Button>
  </div>

  <!-- Stats & Controls Grid -->
  <div
    class="*:data-[slot=card]:from-primary/5 *:data-[slot=card]:to-card 
           dark:*:data-[slot=card]:bg-card 
           grid grid-cols-1 gap-4 
           *:data-[slot=card]:bg-gradient-to-t 
           *:data-[slot=card]:shadow-xs 
           @xl/main:grid-cols-2 
           @5xl/main:grid-cols-4"
  >
    <!-- Status Card -->
    <Card.Root class="@container/card">
      <Card.Header>
        <Card.Title>Status</Card.Title>
      </Card.Header>
      <Card.Content class="text-lg font-semibold">Running</Card.Content>
    </Card.Root>

    <!-- Signal Card -->
    <Card.Root class="@container/card">
      <Card.Header>
        <Card.Title>Signal</Card.Title>
      </Card.Header>
      <Card.Content class="text-lg font-semibold">-62 dBm</Card.Content>
    </Card.Root>

    <!-- Uptime Card -->
    <Card.Root class="@container/card">
      <Card.Header>
        <Card.Title>Uptime</Card.Title>
      </Card.Header>
      <Card.Content class="text-lg font-semibold">3h 12m</Card.Content>
    </Card.Root>

    <!-- Firmware Card -->
    <Card.Root class="@container/card">
      <Card.Header>
        <Card.Title>Firmware</Card.Title>
      </Card.Header>
      <Card.Content class="text-lg font-semibold">v1.0.4</Card.Content>
    </Card.Root>

    <!-- Controls Card -->
    <Card.Root class="@container/card col-span-full lg:col-span-2">
      <Card.Header>
        <Card.Title>Controls</Card.Title>
      </Card.Header>
      <Card.Content class="space-y-6">
        <div class="flex items-center justify-between">
          <span class="font-medium text-gray-700 dark:text-gray-300">Power</span>
          <Switch bind:checked={power} />
        </div>
        <div class="space-y-1">
          <span class="font-medium text-gray-700 dark:text-gray-300">Motor Speed</span>
          <div class="text-sm text-gray-500 dark:text-gray-400">{speed}%</div>
        </div>
      </Card.Content>
    </Card.Root>
  </div>

  <!-- Actions -->
  <div class="flex flex-wrap gap-3">
    <Button variant="outline" class="hover:bg-gray-100 dark:hover:bg-gray-700">Restart</Button>
    <Button variant="outline" class="hover:bg-gray-100 dark:hover:bg-gray-700">OTA Update</Button>
    <Button variant="destructive" class="hover:bg-red-600">Delete Device</Button>
  </div>
</div>
