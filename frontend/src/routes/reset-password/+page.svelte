<script lang="ts">
	import { Button } from "$lib/components/ui/button/index.js";
	import * as Card from "$lib/components/ui/card/index.js";
	import { Input } from "$lib/components/ui/input/index.js";
	import * as Field from "$lib/components/ui/field/index.js";


	import { z } from "zod";
	import { page } from "$app/state";

	import { me } from '$lib/services/auth.service';
	import { goto } from '$app/navigation';
	import { loginSchema } from "$lib/validation/login.schema";
    import { onMount } from "svelte";
    import { api } from "@/services/http";
    import { toast } from "svelte-sonner";
    import { passwordSchema, registerSchema } from "@/validation/register.schema";

	const id = $props.id();

	let password = $state('');
	let confirmPassword = $state('');
	let loading = $state(false);
	let error = $state('');
	let msg = $state('');

	const emailToken = page.url.searchParams.get("email-token");

	let errors = $state<Record<string, string[]>>({});

	function validate() {
		let result;
		result = passwordSchema
				.safeParse({ password, confirmPassword });
		 
		if (!result.success) {  
			errors = z.flattenError(result.error).fieldErrors;
			loading = false; 
			return false; 
		}
		errors = {};
		return true;
	}  

	function validatePasswordOnly() {
		const schema = passwordSchema.pick({ password: true });
		const result = schema.safeParse({ password });

		if (!result.success) {
			errors = z.flattenError(result.error).fieldErrors;
		}
	}


	async function handleRest(event: SubmitEvent) {
		event.preventDefault();
		error = '';
		loading = true;
		
		if (!validate()){
			loading = false;
			return;
		}

		try {
            api('/auth/reset-password', {
                method: 'POST',
                headers: { 
                    'Content-Type': 'application/json',
                },
                body:  JSON.stringify({token: emailToken, password: password})
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
				Or
				<a href="/login" class="font-medium text-primary hover:underline">
					sign in to your account
				</a>
			</Card.Description>
		</Card.Header>

		<Card.Content>
			<form class="space-y-5" onsubmit={handleRest}>
				<Field.Group>
					<Field.Field>
						<Field.Label for="password">Password</Field.Label>
						<Input id="password" type="password" bind:value={password} aria-invalid={errors.password?.length > 0} onblur={()=>validate()} />
						{#if errors.password}   
							<Field.Description>{errors.password}</Field.Description>
						{/if}
					</Field.Field>
					<Field.Field>
						<Field.Label for="confirm-password">Confirm Password</Field.Label>
						<Input id="confirm-password" type="password" bind:value={confirmPassword}  aria-invalid={errors.confirmPassword?.length > 0} onblur={()=>validatePasswordOnly()} />
						{#if errors.confirmPassword}   
							<Field.Description>{errors.confirmPassword}</Field.Description>
						{/if}
					</Field.Field>

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
				</Field.Group>
			</form>
		</Card.Content>

		<Card.Footer class="flex justify-center text-xs text-muted-foreground">
		</Card.Footer>
	</Card.Root>
</div>


