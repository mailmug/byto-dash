<script lang="ts">
	import { Button } from "$lib/components/ui/button";
    import AddDevice from "@/components/device/add-device.svelte";
    import DevicesList from "@/components/device/devices-list.svelte";
</script>

<div class="flex flex-col gap-4 py-4 md:gap-6 md:py-6 p-4">
    <div class="flex w-full sm:justify-end">
        <AddDevice />
    </div>
  
    <DevicesList />

</div>