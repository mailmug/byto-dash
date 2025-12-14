export type ApiFieldError = {
	field?: string;
	message: string;
};

export const apiErrorMap: Record<string, ApiFieldError> = {
	REGISTER_USER_ALREADY_EXISTS: {
		field: 'email',
		message: 'An account with this email already exists'
	}
};