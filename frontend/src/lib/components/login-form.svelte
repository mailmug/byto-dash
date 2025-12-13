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
	import { z, ZodError } from "zod";

	import { login } from '$lib/services/auth.service';
	import { auth } from '$lib/stores/auth.store';
	import { goto } from '$app/navigation';
	import { registerSchema } from '$lib/validation/auth.schema';

	const id = $props.id();

	let email = $state('');
	let password = $state('');
	let loading = $state(false);
	let error = $state('');

	let errors = $state<Record<string, string[]>>({});

	function validate(field?: 'email' | 'password') {
		let result;
		if (field) {

			const value = field === 'email' ? { email } : { password };
			const schema = registerSchema.pick({ [field]: true });
			result = schema.safeParse(value);

		} else {
			result = registerSchema.safeParse({ email, password });
		}
		if (!result.success) { 
			errors = z.flattenError(result.error).fieldErrors;
			loading = false; 
			return false; 
		}
		errors = {};
		return true;
	}  


	async function handleLogin(event: SubmitEvent) {
		event.preventDefault();
		error = '';
		loading = true;
		
		if (!validate()) return;

		try {
			const data = await login(email, password);

			auth.set({
				token: data.access_token,
				user: data.user ?? null
			});

			localStorage.setItem('token', data.access_token);

			goto('/dashboard');
		} catch (e: any) {
			error = e?.detail.message || 'Invalid login credentials';
		} finally {
			loading = false;
		}
	}

</script>

<Card.Root class="mx-auto w-full max-w-sm">
	<Card.Header>
		<Card.Title class="text-2xl">Login</Card.Title>
		<Card.Description>Enter your email below to login to your account</Card.Description>
	</Card.Header>
	<Card.Content>
		<form method="POST" onsubmit={handleLogin}>
			<FieldGroup>
				<Field>
					<FieldLabel for="email-{id}">Email</FieldLabel>
					<Input  id="email-{id}" bind:value={email} type="email" placeholder="m@example.com" aria-invalid={errors.email?.length > 0} onblur={()=>validate('email')} />
				{#if errors.email?.length}   
					<p class="text-sm text-red-500 mt-1">{errors.email[0]}</p>
				{/if}
				</Field>
				<Field>
					<div class="flex items-center">
						<FieldLabel for="password-{id}">Password</FieldLabel>
						<a href="##" class="ms-auto inline-block text-sm underline">
							Forgot your password?
						</a>
					</div>
					<Input id="password-{id}" bind:value={password} type="password" aria-invalid={errors.password?.length > 0}   onblur={()=>validate('password')}/>
				</Field>
				{#if error}
					<p class="text-sm text-center text-red-500 mt-1">{error}</p>
				{/if}
				<Field>
					<Button type="submit"  class="w-full" disabled={loading}>
						{#if loading}
							<span class="loader w-4 h-4 border-2 border-t-transparent rounded-full animate-spin"></span>
							Logging in...
						{:else}
							Login
						{/if}
					</Button>
					<Button variant="outline" class="w-full">
						<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
							<path
								d="M12.48 10.92v3.28h7.84c-.24 1.84-.853 3.187-1.787 4.133-1.147 1.147-2.933 2.4-6.053 2.4-4.827 0-8.6-3.893-8.6-8.72s3.773-8.72 8.6-8.72c2.6 0 4.507 1.027 5.907 2.347l2.307-2.307C18.747 1.44 16.133 0 12.48 0 5.867 0 .307 5.387.307 12s5.56 12 12.173 12c3.573 0 6.267-1.173 8.373-3.36 2.16-2.16 2.84-5.213 2.84-7.667 0-.76-.053-1.467-.173-2.053H12.48z"
								fill="currentColor"
							/>
						</svg>
						Login with Google
					</Button>
					<FieldDescription class="text-center">
						Don't have an account? <a href="##">Sign up</a>
					</FieldDescription>
				</Field>
			</FieldGroup>
		</form>
	</Card.Content>
</Card.Root>
