<script lang="ts">
	import { page } from '$app/state';
	import { onMount } from 'svelte';
	import * as Card from '$lib/components/ui/card';
	import { Button } from '$lib/components/ui/button';
	import { Switch } from '$lib/components/ui/switch';
	import { Badge } from '$lib/components/ui/badge';
	import type { Device } from '@/types/device';
	import { api } from '@/services/http';
    import { devices } from '@/stores/devices';
    import { goto } from '$app/navigation';
    import Dialog from '@/components/ui/dialog/dialog.svelte';
    import DialogContent from '@/components/ui/dialog/dialog-content.svelte';
    import DialogHeader from '@/components/ui/dialog/dialog-header.svelte';
    import DialogTitle from '@/components/ui/dialog/dialog-title.svelte';
    import DialogDescription from '@/components/ui/dialog/dialog-description.svelte';
    import DialogFooter from '@/components/ui/dialog/dialog-footer.svelte';
    import DialogClose from '@/components/ui/dialog/dialog-close.svelte';
    import { toast } from 'svelte-sonner';

	const id = page.params.id;
	let device: Device;
	let power = false;
    let deleteLoading = $state(false);
    let openDeleteConfirm = $state(false);


	onMount(() => {
		api('/api/v1/devices/' + id, {
			method: 'GET',
			headers: {
				'Content-Type': 'application/json',
				'Authorization': 'Bearer ' + localStorage.getItem('token')
			}
		}).then(data=>device = data);
		// power = device.isOn;
	});

	async function togglePower() {
		await api('/api/v1/devices/' + id + '/toggle', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'Authorization': 'Bearer ' + localStorage.getItem('token')
			},
			body: JSON.stringify({ isOn: power })
		});
	}

	async function deleteDevice() {
        deleteLoading = true;
		await api('/api/v1/devices/' + id, {
			method: 'DELETE',
			headers: {
				'Content-Type': 'application/json',
				'Authorization': 'Bearer ' + localStorage.getItem('token')
			},
		});

        toast.success('Successfully deleted!')
        api('/api/v1/devices/', {
            method: 'GET',
            headers: { 
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + localStorage.getItem('token')
            },
        }).then(data=>{
            devices.set(data);
            deleteLoading = false;
            goto('/dashboard/devices');
        });
	}
</script>

<div class="min-h-screen p-4 md:p-8 space-y-8">

  <!-- Header -->
  <div class="flex items-center justify-between">
    <div>
      <h1 class="text-3xl font-bold text-gray-900 dark:text-gray-100">{device?.title || 'Device'}</h1>
      <div class="flex items-center gap-3 mt-2">
        <Badge class={power ? 'bg-green-500 text-white' : 'bg-red-500 text-white'}>
          {power ? 'On' : 'Off'}
        </Badge>
        <span class="text-sm text-gray-500 dark:text-gray-400">Last seen: {device?.last_active || 'N/A'}</span>
      </div>
    </div>
    <Button variant="outline" class="hover:bg-gray-100 dark:hover:bg-gray-700">Settings</Button>
  </div>

  <!-- Cards Grid -->
  <div
    class="*:data-[slot=card]:from-primary/5 *:data-[slot=card]:to-card
           dark:*:data-[slot=card]:bg-card
           grid grid-cols-1 gap-4
           *:data-[slot=card]:bg-gradient-to-t
           *:data-[slot=card]:shadow-xs
           @xl/main:grid-cols-2"
  >
    <!-- Status Card -->
    <Card.Root class="@container/card">
      <Card.Header><Card.Title>Status</Card.Title></Card.Header>
      <Card.Content class="text-lg font-semibold">{power ? 'Running' : 'Stopped'}</Card.Content>
    </Card.Root>

    <!-- Signal Card -->
    <Card.Root class="@container/card">
      <Card.Header><Card.Title>Signal</Card.Title></Card.Header>
      <Card.Content class="text-lg font-semibold">{device?.signal || '- dBm'}</Card.Content>
    </Card.Root>

    <!-- Controls Card -->
    <Card.Root class="@container/card col-span-full lg:col-span-2">
      <Card.Header><Card.Title>Controls</Card.Title></Card.Header>
      <Card.Content class="space-y-6">
        <div class="flex items-center justify-between">
          <span class="font-medium text-gray-700 dark:text-gray-300">Power</span>
          <Switch bind:checked={power} onchange={togglePower} />
        </div>
      </Card.Content>
    </Card.Root>
  </div>

  <!-- Actions -->
  <div class="flex flex-wrap gap-3">
    <Button variant="outline" class="hover:bg-gray-100 dark:hover:bg-gray-700 cursor-pointer">Restart</Button>
    <Button variant="destructive" onclick={()=>openDeleteConfirm=true} class="hover:bg-red-700 cursor-pointer">
        Delete Device
    </Button>
  </div>


    <Dialog bind:open={openDeleteConfirm}>
        <DialogContent class="sm:max-w-sm">
            <DialogHeader>
                <DialogTitle>Confirm Delete</DialogTitle>
                <DialogDescription>
                    Are you sure you want to delete this device? 

                    This action cannot be undone.
                </DialogDescription>
            </DialogHeader>

            <DialogFooter class="flex justify-end gap-2">
                <DialogClose>
                    <Button class="hover:bg-gray-100 dark:hover:bg-gray-700 cursor-pointer" variant="outline">Cancel</Button>
                </DialogClose>
                <Button class="dark:hover:bg-gray-700 cursor-pointer" 
                variant="destructive" onclick={deleteDevice} disabled={deleteLoading}>
                    {deleteLoading ? 'Deleting...' : 'Delete'}
                </Button>
            </DialogFooter>
        </DialogContent>
    </Dialog>
</div>
