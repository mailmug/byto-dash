<script lang="ts">
	import { Button } from "$lib/components/ui/button/index.js";
	import * as Card from "$lib/components/ui/card/index.js";
	import { Input } from "$lib/components/ui/input/index.js";
	import {
		FieldGroup,
		Field,
		FieldLabel,
		FieldDescription,
	} from "$lib/components/ui/field/index.js";
	import { z } from "zod";

	import { login, me } from '$lib/services/auth.service';
	import { authStore } from '$lib/stores/auth.store';
	import { goto } from '$app/navigation';
	import { loginSchema } from "$lib/validation/login.schema";
    import { onMount } from "svelte";
    import { api } from "@/services/http";
    import { toast } from "svelte-sonner";

	const id = $props.id();

	let email = $state('');
	let loading = $state(false);
	let error = $state('');
	let msg = $state('');

	let errors = $state<Record<string, string[]>>({});

	function validate(field: 'email') {
		let result;
		const value = { email };
		const schema = loginSchema.pick({ [field]: true });
		result = schema.safeParse(value);
		if (!result.success) { 
			errors = z.flattenError(result.error).fieldErrors;
			loading = false; 
			return false; 
		}
		errors = {};
		return true;
	}  


	async function handleRest(event: SubmitEvent) {
		event.preventDefault();
		error = '';
		loading = true;
		
		if (!validate('email')){
			loading = false;
			return;
		}

		try {
            api('/auth/forgot-password', {
                method: 'POST',
                headers: { 
                    'Content-Type': 'application/json',
                },
                body:  JSON.stringify({email})
			}).then(data=>{
				msg = "Check your inbox for instructions!"
                toast.success(msg);
            });
			
		} catch (e: any) {
			error = e?.detail.message || '';
			toast.error(error);
		} finally {
			loading = false;
		}
	}

	onMount(()=>{
		me().then((data)=>{ 
	
			if(data.is_verified){  
				goto('/dashboard');
			}
			if(data.is_verified === false){  
				goto('/verify-user');
			}
		})
	})

</script>

<div class="bg-muted flex h-screen w-full items-center justify-center px-4">
	<Card.Root class="w-full max-w-sm shadow-lg border bg-background ">
		<Card.Header class="space-y-2 text-center">
			<Card.Title class="text-2xl font-semibold tracking-tight">
				Reset your password
			</Card.Title>
			<Card.Description class="text-sm text-muted-foreground">
				Enter your email to continue or
				<a href="/login" class="font-medium text-primary hover:underline">
					sign in
				</a>
			</Card.Description>
		</Card.Header>

		<Card.Content>
			<form class="space-y-5" onsubmit={handleRest}>
				<FieldGroup>
					{#if !msg}
					<Field>
						<FieldLabel
							for="email-{id}"
							class="text-sm font-medium"
						>
							Email address
						</FieldLabel>

						<Input
							id="email-{id}"
							type="email"
							aria-invalid={errors.email?.length > 0}
							bind:value={email}
							onblur={() => validate('email')}
						/>

						{#if errors.email}
							<p class="text-xs text-destructive mt-1">
								{errors.email}
							</p>
						{/if}
					</Field>
					{/if}

					{#if error}
						<div class="rounded-md bg-destructive/10 px-3 py-2 text-sm text-destructive">
							{error}
						</div>
					{/if}

					{#if msg}
						<div class="mb-4 rounded-lg bg-green-100 text-green-700 px-4 py-2 text-sm mb-8">
							{msg}
						</div>
					{/if}

					{#if !msg}
					<Button
						type="submit"
						class="w-full h-11 text-base"
						disabled={loading}
					>
						{#if loading}
							<span class="animate-pulse">Processing…</span>
						{:else}
							Continue
						{/if}
					</Button>
					{/if}
				</FieldGroup>
			</form>
		</Card.Content>

		<Card.Footer class="flex justify-center text-xs text-muted-foreground">
		</Card.Footer>
	</Card.Root>
</div>


