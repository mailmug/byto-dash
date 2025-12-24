<script lang="ts">
	import { page } from '$app/state';
    import { api } from '@/services/http';
    import { onMount } from 'svelte';

	const id = page.params.id;


    type Device = {
        id: number;
        title: string;
        type: string;
        status: string;
        isOn: boolean;
        last_active: string;
        description?: string;
    };

    let device = $state<Device>(); 

    onMount(()=>{
        api('/api/v1/devices/'+id, {
            method: 'GET',
            headers: { 
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + localStorage.getItem('token')
            },
        }).then(data=>{
            device = data;
        });
    });
</script>

