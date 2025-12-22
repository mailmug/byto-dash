<script lang="ts">
	import * as Dialog from "$lib/components/ui/dialog";
	import { Button } from "$lib/components/ui/button";
	import { authStore } from "$lib/stores/auth.store";
	import { goto } from "$app/navigation";
    import { pageTitle } from "$lib/stores/title";

	let open = $state(true);

	function logout() {
		authStore.set({ token: null, user: null });
		localStorage.removeItem("token");
		goto("/login");
		open = false;
	}
</script>

<div class="flex flex-col gap-4 py-4 md:gap-6 md:py-6 p-4">

    <Dialog.Root bind:open>
        <Dialog.Content>
            <Dialog.Header>
                <Dialog.Title>Log out</Dialog.Title>
                <Dialog.Description>
                    Are you sure you want to log out? You’ll need to sign in again to
                    access your account.
                </Dialog.Description>
            </Dialog.Header>

            <Dialog.Footer class="gap-2 sm:justify-end">
                <Button
                    variant="outline"
                    onclick={()=>{goto('/dashboard'); pageTitle.set('Dashboard')}}
                >
                    Cancel
                </Button>

                <Button
                    variant="destructive"
                    onclick={logout}
                >
                    Log out
                </Button>
            </Dialog.Footer>
        </Dialog.Content>
    </Dialog.Root>

</div>

