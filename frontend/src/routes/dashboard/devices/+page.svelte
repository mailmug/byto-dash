<script lang="ts">
    import AddDevice from "@/components/device/add-device.svelte";
    import DevicesList from "@/components/device/devices-list.svelte";
    import { pageTitle } from "@/stores/title";
    import { onMount } from "svelte";

    onMount(()=>{
        pageTitle.set('Devices');
    });
</script>

<div class="flex flex-col gap-4 py-4 md:p-8 md:gap-6 md:py-6">
    <div class="flex w-full sm:justify-end">
        <AddDevice />
    </div>
  
    <DevicesList />

</div>