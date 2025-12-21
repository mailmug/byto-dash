<script lang="ts">
    import { goto } from "$app/navigation";
    import { Button } from "$lib/components/ui/button/index.js";
    import { Checkbox } from "$lib/components/ui/checkbox/index.js";
    import * as Field from "$lib/components/ui/field/index.js";
    import { Input } from "$lib/components/ui/input/index.js";
    import * as Select from "$lib/components/ui/select/index.js";
    import { me } from "@/services/auth.service";
    import { onMount } from "svelte";
    import { any } from "zod";

    let name = $state<string>();
    let email = $state<string>();
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
        <form>
            <Field.Group>
                <Field.Field>
                    <Field.Label for="profile-name">Name</Field.Label>
                    <Input
                        id="profile-name"
                        bind:value={name}
                        required
                    />
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
                    <Button type="submit">Update</Button>
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
        <form>
            <Field.Group>
                <Field.Field>
                    <Field.Label>New password *</Field.Label>
                    <Input
                        type='password'
                        required
                    />
                </Field.Field>
                <Field.Field>
                    <Field.Label>Confirm password *</Field.Label>
                    <Input 
                        type='password'
                    />
                </Field.Field>
                <Field.Field orientation="horizontal">
                    <Button type="submit">Update</Button>
                </Field.Field>

            </Field.Group>
        </form>
    </div>

</div>