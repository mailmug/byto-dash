<script lang="ts">
    import * as Dialog from "$lib/components/ui/dialog";
    import Plus from "@tabler/icons-svelte/icons/plus";

    import { Button } from "$lib/components/ui/button";
    import { Input } from "$lib/components/ui/input";
    import { Textarea } from "$lib/components/ui/textarea";
    import * as Select from "$lib/components/ui/select";
    import * as Field from "$lib/components/ui/field";
    import { api } from "@/services/http";
    import { toast } from "svelte-sonner";
    import { authStore } from "@/stores/auth.store";

    let deviceName  = $state("");
    let description = $state("");
    let deviceType = $state("");
	let errors = $state<Record<string, string[]>>({});
    let open = $state(false);
    let loading = $state(false);

    const deviceTypes = [
        { value: "switch", label: "Switch" },
        { value: "sensor", label: "Sensor" },
        { value: "controller", label: "Controller" },
        { value: "other", label: "other" },
    ];

    const triggerContent = $derived(
        deviceTypes.find((f) => f.value === deviceType)?.label ?? "Select a device type"
    );

    function submit(e: SubmitEvent) {
        e.preventDefault();
        errors = {};
        if(deviceName?.length <= 0){
            errors = {
            ...errors,
                deviceName: ['Device name is required!']
            };        
        }
        if(deviceType?.length <= 0){
            errors = {
            ...errors,
                deviceType: ['Device type is required!']
            };        
        }

        if (Object.keys(errors).length > 0) return;

        const payload = {
            title: deviceName,
            type: deviceType,
            description
        };
        loading = true;
        api('/api/v1/devices/', {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + localStorage.getItem('token')
            },
            body:  JSON.stringify(payload)
        }).then(data=>{
            if(data?.id){
                toast.success("Device added successfully");
                open = false;
                loading = false;
                deviceName  = "";
                description = "";
                deviceType = "";
            }
        });
    }
</script>

<Dialog.Root bind:open>
    <Dialog.Trigger class="w-full sm:w-auto flex items-center justify-center gap-2">
        <Button size='lg' class="w-full sm:w-auto flex items-center justify-center gap-2">
            <Plus class="h-4 w-4" />
            Add Device
        </Button>
    </Dialog.Trigger>

    <Dialog.Content>
        <form onsubmit={submit} class="space-y-4">
            <Dialog.Header>
            <Dialog.Title>Add New Device</Dialog.Title>
            <Dialog.Description>
                Register a new device to your account.
            </Dialog.Description>
            </Dialog.Header>

                <!-- Device Name -->
                <Field.Field>
                    <Field.Label>Device Name *</Field.Label>
                    <Input
                        placeholder="e.g. Temperature Sensor"
                        bind:value={deviceName}
                        aria-invalid={errors.deviceName?.length > 0} 
                        onblur={() => {
                            if (deviceName.length > 0) {
                                errors = { ...errors, deviceName: [] };
                            }
                        }}
                    />
                    {#if errors.deviceName}   
					    <p class="text-sm text-red-500 mt-1">{errors.deviceName}</p>
				    {/if}
                </Field.Field>

                <!-- Device Type -->
                <Field.Field>
                    <Field.Label>Device Type *</Field.Label>
                    <Select.Root type="single" bind:value={deviceType}  
                    onValueChange={(value) => {
                        deviceType = value;
                        if (errors.deviceType) {
                            errors = { ...errors, deviceType: [] };
                        }
                    }}>
                        <Select.Trigger class="w-[180px]"  aria-invalid={!!errors.deviceType?.length}>
                            {triggerContent}
                        </Select.Trigger>
                        <Select.Content>
                            <Select.Group>
                            <Select.Label>Device Tpes</Select.Label>
                            {#each deviceTypes as type (type.value)}
                                <Select.Item
                                value={type.value}
                                label={type.label}
                                >
                                {type.label}
                                </Select.Item>
                            {/each}
                            </Select.Group>
                        </Select.Content>
                    </Select.Root>
                    {#if errors.deviceType}   
					    <p class="text-sm text-red-500 mt-1">{errors.deviceType}</p>
				    {/if}
                </Field.Field>

                <!-- Description -->
                <Field.Field>
                    <Field.Label>Description</Field.Label>
                    <Textarea
                    rows={3}
                    placeholder="Optional description about the device"
                    bind:value={description}
                    />
                </Field.Field>

            <Dialog.Footer class="flex flex-row justify-center gap-2">
                <Dialog.Close>
                    <Button
                        variant="secondary"
                        class="flex-1 sm:flex-none"
                    >
                        Cancel
                    </Button>
                </Dialog.Close>

                <Button
                    type="submit"
                    class="flex-1 sm:flex-none"
                    disabled={loading}>
						{#if loading}
							<span class="loader w-4 h-4 border-2 border-t-transparent rounded-full animate-spin"></span>
							Adding...
						{:else}
							Add Device
						{/if}
				</Button>
            </Dialog.Footer>
        </form>
    </Dialog.Content>
</Dialog.Root>