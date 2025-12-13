import { z } from 'zod';

export const registerSchema = z.object({
	email: z.email(),

	password: z
		.string()
		.min(3, 'Password must be at least 3 characters')
});

export type RegisterInput = z.infer<typeof registerSchema>;
