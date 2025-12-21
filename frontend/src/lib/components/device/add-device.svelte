<script lang="ts">
    import * as Dialog from "$lib/components/ui/dialog";
    import Plus from "@tabler/icons-svelte/icons/plus";
    import Button from "../ui/button/button.svelte";
</script>

<Dialog.Root>
    <Dialog.Trigger class="w-full sm:w-auto flex items-center justify-center gap-2">
        <Button size='lg' class="w-full sm:w-auto flex items-center justify-center gap-2">
            <Plus class="h-4 w-4" />
            Add Device
        </Button>
    </Dialog.Trigger>

    <Dialog.Content>
        <Dialog.Header>
        <Dialog.Title>Add New Device</Dialog.Title>
        <Dialog.Description>
            Register a new device to your account.
        </Dialog.Description>
        </Dialog.Header>

        <!-- form goes here -->

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
                class="flex-1 sm:flex-none"
            >
                Add
            </Button>
        </Dialog.Footer>
    </Dialog.Content>
</Dialog.Root>