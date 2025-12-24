<script lang="ts">
	import { Button } from "$lib/components/ui/button";
    import { Switch } from "$lib/components/ui/switch/index.js";
    import { Card, CardHeader, CardTitle, CardContent, CardFooter } from "$lib/components/ui/card";
    import { Badge } from "$lib/components/ui/badge";
    import ArrowRight from "@tabler/icons-svelte/icons/arrow-right";
    import { onMount } from "svelte";
    import { api } from "@/services/http";
    import { goto } from "$app/navigation";   
    import { devices } from "$lib/stores/devices";

    onMount(()=>{
        api('/api/v1/devices/', {
            method: 'GET',
            headers: { 
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + localStorage.getItem('token')
            },
        }).then(data=>{
            devices.set(data);
        });
    });


    function toggleDevice(device:any) {
        device.isOn = !device.isOn;
    }

</script>

<!-- Devices Grid -->
<div
  class="*:data-[slot=card]:from-primary/5 
         *:data-[slot=card]:to-card 
         dark:*:data-[slot=card]:bg-card
         grid grid-cols-1 gap-4 
         *:data-[slot=card]:bg-gradient-to-t
         *:data-[slot=card]:shadow-xs
         lg:grid-cols-3"
>
{#each $devices as device (device.id)}
    <Card>
        <CardHeader>
            <CardTitle class="text-xl">{device.title}</CardTitle>
        </CardHeader>

        <CardContent class="space-y-4">
            <!-- Status + Switch -->
            <div class="flex justify-between items-center">
                <div class="space-y-1">
                    <div class="flex items-center gap-2">
                    <span class="text-sm text-muted-foreground">Status:</span>
                    <Badge
                    variant={device.status === "online" ? "secondary" : "destructive"}
                    class={device.status === "online"
                        ? "bg-blue-500 text-white dark:bg-blue-600"
                        : "bg-red-500 text-white dark:bg-red-600"
                    }
                    >
                        {device.status}
                    </Badge>
                    </div>
                    <p class="text-sm text-muted-foreground">
                        {#if device.status === "offline"}
                        Last Active: {device.last_active}
                        {/if} &nbsp;
                    </p>
                </div>

                {#if device.type === "Switch"}
                    <Switch
                        disabled={device.status=='offline'}
                        checked={device.isOn}
                        onchange={() => toggleDevice(device)}
                    />
                {/if}
            </div>

            <!-- Device Info -->
            <div class="rounded-md bg-muted p-3 text-sm text-muted-foreground space-y-1">
                <p>
                    <strong>Type:</strong> {device.type}
                </p>
                <p>{device.description}</p>
            </div>
        </CardContent>

        <CardFooter class="flex gap-2">
            <Button
            class="flex-1 cursor-pointer"
            onclick={() => {
                goto('/dashboard/devices/'+device.id)
            }}
            >
                Device
                <ArrowRight />
            </Button>
        </CardFooter>
    </Card>
{/each}
</div>