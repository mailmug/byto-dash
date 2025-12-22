<script lang="ts">
    import { goto } from "$app/navigation";
	import { Button } from "$lib/components/ui/button";
	import * as Card from "$lib/components/ui/card";
    import { me } from "@/services/auth.service";
    import { api } from "@/services/http";
    import { onMount } from "svelte";
	import { authStore } from '$lib/stores/auth.store';
	import { page } from "$app/state";
	import { toast } from "svelte-sonner";
    import { apiErrorMap } from "@/errors/api-error-map";
	let error = $state('');

	let loading = $state(false);

	const emailToken = page.url.searchParams.get("email-token");
	let errors = $state<Record<string, string[]>>({});

	async function logout() {  
		loading = true;
		try {
			localStorage.setItem('token', '');
            goto('/login');
		} finally {
			loading = false;
		}
	}

	async function resendVerification() {
		api('/auth/request-verify-token', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body:  JSON.stringify({
                email: $authStore.user?.email
            })
        });
	}

    onMount(()=>{

		if(emailToken){
			
			api('/auth/verify', {
				method: 'POST',
				headers: { 
					'Content-Type': 'application/json',
				},
				body: JSON.stringify({ token: emailToken })
				})
				.then((data) => {
					if (data.id) {
						toast.success("Email verified successfully!");
						goto('/dashboard');
					} else {
						toast.error("Verification failed!");
					}
				})
				.catch((e: any) => {
					const detail = e?.detail;
					const mapped = apiErrorMap[detail];
				
					if (mapped) {
						
						toast.error(mapped.message);
						error = mapped.message;
						
					} else {
						toast.error("Something went wrong");
					}
				}
			);
		}


		me().then((data)=>{ 
            authStore.set({
                token: localStorage.getItem('token'),
                user: data
            });

			if(data.is_verified === true){  
				goto('/dashboard');
			}
            
		}).catch(()=>{
            goto('/');
        });
	})
</script>

<div class="min-h-screen flex items-center justify-center bg-background px-4">
	<Card.Card class="w-full max-w-md bg-white/50 backdrop-blur-xl border shadow-2xl rounded-2xl">
		<Card.CardHeader class="flex items-center justify-center">
			<!-- Logo -->
			<div class="py-2">
				<!-- keep your SVG as-is -->
				<svg class="w-32" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 304.651 77.422">
					<!-- SVG CONTENT UNCHANGED -->
				</svg>
			</div>
		</Card.CardHeader>

		<Card.CardContent class="space-y-6 text-center">
			<h2 class="text-2xl font-bold tracking-tight">
				Email verification required
			</h2>

			<p class="text-sm text-muted-foreground">
				Before proceeding, please check your email for a verification link.
				If you did not receive the email,
				<button
					type="button"
					onclick={resendVerification}
					class="text-primary underline underline-offset-4 ml-1"
				>
					click here to request another one
				</button>.
			</p>
		</Card.CardContent>

		<Card.CardFooter>
			<Button
				class="w-full"
				onclick={logout}
				disabled={loading}
			>
				{#if loading}
					<span class="loader w-4 h-4 border-2 border-t-transparent rounded-full animate-spin"></span>
					Signing out…
				{:else}
					Sign out
				{/if}
			</Button>
		</Card.CardFooter>
	</Card.Card>
</div>
