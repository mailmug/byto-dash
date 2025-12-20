<script lang="ts">
	import { cn } from "$lib/utils.js";
	import { Button } from "$lib/components/ui/button/index.js";
	import * as Card from "$lib/components/ui/card/index.js";
	import * as Field from "$lib/components/ui/field/index.js";
	import { Input } from "$lib/components/ui/input/index.js";
	import type { HTMLAttributes } from "svelte/elements";
	import { z } from "zod";
	import { register } from '$lib/services/auth.service';
	import { goto } from '$app/navigation';
	import { apiErrorMap } from '$lib/errors/api-error-map';

	let { class: className, ...restProps }: HTMLAttributes<HTMLDivElement> = $props();

	import { registerSchema } from "$lib/validation/register.schema";
    import { api } from "@/services/http";
    import { authStore } from "@/stores/auth.store";

	let name = $state('');
	let email = $state('');
	let password = $state('');
	let confirmPassword = $state('');
	let loading = $state(false);
	let error = $state('');
	let msg = $state('');
	
	let errors = $state<Record<string, string[]>>({});

	function resetForm() {
		name = '';
		email = '';
		password = '';
		confirmPassword = '';
		errors = {};
		error = '';
	}

	function validate(field?: 'name' | 'email' | 'password' | 'confirmPassword') {
		let result;
		const valueMap = {
			name,
			email,
			password,
			confirmPassword
		};
		if (field) {

			if (field === "password" || field === "confirmPassword") { 
				result = registerSchema
					.pick({ password: true, confirmPassword: true })
					.safeParse({ password, confirmPassword });
			}else{

				const schema = registerSchema.pick({ [field]: true });

				result = schema.safeParse({
					[field]: valueMap[field]
				});
			}

		} else {
			result = registerSchema.safeParse(valueMap);
		}

		if (!result.success) { 
			errors = z.flattenError(result.error).fieldErrors;
			loading = false; 
			return false; 
		}
		errors = {};
		return true;
	}  

	async function submit(event: SubmitEvent) {
		event.preventDefault();
		if (!validate()) return;

		try {
			const data = await register(name, email, password);
			if(data?.user?.id){

				authStore.set({
					token: data.token,
					user: data.user
				});

				localStorage.setItem('token', data.token);

				msg = 'Account created successfully. Please login.';
				resetForm();
				api('/auth/request-verify-token', {
					method: 'POST',
					headers: { 'Content-Type': 'application/json' },
					body:  JSON.stringify({
						email: data.user.email
					})
				});
				setTimeout(()=>goto('/login'), 3000);
			}
		} catch (e: any) {
			const detail = e?.detail;
			const mapped = apiErrorMap[detail];

			if (mapped) {
				if (mapped.field) {
					errors = {
						...errors,
						[mapped.field]: [mapped.message]
					};
				} else {
					error = mapped.message;
				}
			} else {
				error = 'Something went wrong';
			}
		} finally {
			loading = false;
		}
	}
</script>

<div class={cn("flex flex-col gap-6", className)} {...restProps}>
	<Card.Root>
		<Card.Header class="text-center">
			<Card.Title class="text-xl">Create your account</Card.Title>
			<Card.Description>Enter your email below to create your account</Card.Description>
		</Card.Header>
		<Card.Content>
			<form  method="post" onsubmit={submit}>
				<Field.Group>
					<Field.Field>
						<Field.Label for="name">Full Name</Field.Label>
						<Input id="name" type="text"  bind:value={name}  aria-invalid={errors.name?.length > 0} onblur={()=>validate('name')} />
						{#if errors.name}   
							<Field.Description>{errors.name}</Field.Description>
						{/if}
					</Field.Field>
					<Field.Field>
						<Field.Label for="email">Email</Field.Label>
						<Input id="email" type="email" bind:value={email}  aria-invalid={errors.email?.length > 0} onblur={()=>validate('email')} />
						{#if errors.email}   
							<Field.Description>{errors.email}</Field.Description>
						{/if}
					</Field.Field>
					<Field.Field>
						<Field.Label for="password">Password</Field.Label>
						<Input id="password" type="password" bind:value={password} aria-invalid={errors.password?.length > 0} onblur={()=>validate('password')} />
						{#if errors.password}   
							<Field.Description>{errors.password}</Field.Description>
						{/if}
					</Field.Field>
					<Field.Field>
						<Field.Label for="confirm-password">Confirm Password</Field.Label>
						<Input id="confirm-password" type="password" bind:value={confirmPassword}  aria-invalid={errors.confirmPassword?.length > 0} onblur={()=>validate('confirmPassword')} />
						{#if errors.confirmPassword}   
							<Field.Description>{errors.confirmPassword}</Field.Description>
						{/if}
					</Field.Field>
					{#if error}
						<p class="text-sm text-center text-red-500 mt-1">{error}</p>
					{/if}
					{#if msg}
						<div class="mb-4 rounded-lg bg-green-100 text-green-700 px-4 py-2 text-sm">
							{msg}
						</div>
					{/if}
					<Field.Field>
						<Button type="submit" disabled={loading}>
						{#if loading}
							<span class="loader w-4 h-4 border-2 border-t-transparent rounded-full animate-spin"></span>
							Submitting...
						{:else}
							Create Account
						{/if}</Button>
						<Field.Description class="text-center">
							Already have an account? <a href="/login">Sign in</a>
						</Field.Description>
					</Field.Field>
				</Field.Group>
			</form>
		</Card.Content>
	</Card.Root>
	<!-- <Field.Description class="px-6 text-center">
		By clicking continue, you agree to our <a href="#/">Terms of Service</a>
		and <a href="#/">Privacy Policy</a>.
	</Field.Description> -->
</div>
