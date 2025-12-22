<script lang="ts">
    import { goto } from "$app/navigation";
    import { Button } from "$lib/components/ui/button/index.js";
    import * as Field from "$lib/components/ui/field/index.js";
    import { Input } from "$lib/components/ui/input/index.js";
    import { apiErrorMap } from "@/errors/api-error-map";
    import { me } from "@/services/auth.service";
    import { api } from "@/services/http";
    import { authStore } from "@/stores/auth.store";
    import { passwordSchema, registerSchema } from "@/validation/register.schema";
    import { onMount } from "svelte";
    import { toast } from "svelte-sonner";
	import { z } from "zod";

    let name = $state('');
	let email = $state('');
	let password = $state('');
	let confirmPassword = $state('');
	let loading = $state(false);
	let psdLoading = $state(false);
	let error = $state('');
	let msg = $state('');
	
	let errors = $state<Record<string, string[]>>({});

    function validatePasswords() {
		let result;
        psdLoading = true;
		result = passwordSchema
				.safeParse({ password, confirmPassword });
		 
		if (!result.success) {  
			errors = z.flattenError(result.error).fieldErrors;
			psdLoading = false; 
			return false; 
		}
		errors = {};
		return true;
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
			result = registerSchema.safeParse({password: true, confirmPassword: true});
		}

		if (!result.success) { 
			errors = z.flattenError(result.error).fieldErrors;
			loading = false; 
			return false; 
		}
		errors = {};
		return true;
	}  

    function passwordUpdate(event: SubmitEvent){
		event.preventDefault();   
        if (!validatePasswords()) {  
			loading = false;  
			return false;  
		}
        profileUpdate(event);
    }

    function profileUpdate(event: SubmitEvent){  
		event.preventDefault(); 
        loading = true; 

        if (!validate('name')) {  
			loading = false; 
			return false; 
		}

        try {
            let profileData: Record<string, string> = {};
            if (name) profileData.name = name;
            if (password) profileData.password = password;

            api('/api/v1/auth/update-profile', {
                method: 'PATCH',
                headers: { 
                    'Content-Type': 'application/json',
			        'Authorization': 'Bearer ' + $authStore.token
                },
                body:  JSON.stringify(profileData)
			}).then(data=>{
                if(data?.id){
                    msg = 'Updated successfully.';
                    toast.success(msg);
                }
            });
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
			psdLoading = false;
		}
    }

    onMount(()=>{
        me().then((data)=>{ 
            if(data.is_verified === false){  
                goto('/verify-user');
            }
            name = data.name;
            email = data.email;
        }).catch(e=>{
            localStorage.setItem('token', '');
            goto('/login');
        });
    });

</script>
 
<div class="flex flex-col gap-4 md:gap-6 p-6">
    <div class="profile">
        <h3 class="text-lg font-medium text-gray-900 filament-breezy-grid-title">Personal Information</h3>

        <p class="mt-1 text-sm text-gray-600 filament-breezy-grid-description">
            Manage your personal information.
        </p>
    </div>
    <div class="w-full max-w-md">
        <form method="post" onsubmit={profileUpdate}>
            <Field.Group>
                <Field.Field>
                    <Field.Label for="profile-name">Name *</Field.Label>
                    <Input
                        id="profile-name"
                        bind:value={name}
                        aria-invalid={errors.name?.length > 0} onblur={()=> validate('name')}
                    />
                    {#if errors.name}   
                        <Field.Description>{errors.name}</Field.Description>
                    {/if}
                </Field.Field>
                <Field.Field>
                    <Field.Label for="profile-email">Email</Field.Label>
                    <Input
                        id="profile-email"
                        value={email}
                        disabled
                    />
                </Field.Field>
                <Field.Field orientation="horizontal">
                    <Button type="submit" disabled={loading} class="cursor-pointer">
						{#if loading}
							<span class="loader w-4 h-4 border-2 border-t-transparent rounded-full animate-spin"></span>
							Updating...
						{:else}
							Update
						{/if}Update</Button>
                </Field.Field>
            </Field.Group>
            
            <Field.Separator class="mt-6"/>
        </form>
    </div>

    <div class="profile">
        <h3 class="text-lg font-medium text-gray-900 filament-breezy-grid-title">Password</h3>

        <p class="mt-1 text-sm text-gray-600 filament-breezy-grid-description">
            Must be at least 8 characters long.
        </p>
    </div>
    <div class="w-full max-w-md">
        <form method="post" onsubmit={passwordUpdate}>
            <Field.Group>
                <Field.Field>
                    <Field.Label>New password *</Field.Label>
                    <Input
                        type='password'
                        bind:value={password}
                        aria-invalid={errors.password?.length > 0} onblur={()=> validate('password')}
                    />
                    {#if errors.password}   
                        <Field.Description>{errors.password}</Field.Description>
                    {/if}
                </Field.Field>
                <Field.Field>
                    <Field.Label>Confirm password *</Field.Label>
                    <Input 
                        bind:value={confirmPassword}
                        type='password'
                        aria-invalid={errors.confirmPassword?.length > 0} onblur={()=> validate('confirmPassword')}
                    />
                    {#if errors.confirmPassword}   
                        <Field.Description>{errors.confirmPassword}</Field.Description>
                    {/if}
                </Field.Field>
                <Field.Field orientation="horizontal">
                    <Button type="submit" disabled={psdLoading} class="cursor-pointer">
						{#if psdLoading}
							<span class="loader w-4 h-4 border-2 border-t-transparent rounded-full animate-spin"></span>
							Updating...
						{:else}
							Update
						{/if}
                    </Button>
                </Field.Field>

            </Field.Group>
        </form>
    </div>

</div>