import { z } from "zod";

export const registerSchema = z
	.object({
		name: z.string().min(1, "Full name is required"),
		email: z.email("Invalid email address"),
		password: z.string().min(5, "Password must be at least 5 characters"),
		confirmPassword: z.string().min(3, "Confirm Password is required"),
	})
	.refine((data) => data.password === data.confirmPassword, {
		path: ["confirmPassword"],
		message: "Passwords do not match"
	});

export type RegisterInput = z.infer<typeof registerSchema>;