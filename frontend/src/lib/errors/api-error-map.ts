export type ApiFieldError = {
	field?: string;
	message: string;
};

export const apiErrorMap: Record<string, ApiFieldError> = {

    REGISTER_INVALID_PASSWORD: {
		field: 'password',
		message: 'Password does not meet security requirements'
	},
	REGISTER_USER_ALREADY_EXISTS: {
		field: 'email',
		message: 'An account with this email already exists'
	},


    OAUTH_NOT_AVAILABLE_EMAIL: {
		message: 'This OAuth provider does not provide an email address'
	},
	OAUTH_USER_ALREADY_EXISTS: {
		message: 'An account already exists with this OAuth provider'
	},


    LOGIN_BAD_CREDENTIALS: {
		message: 'Invalid email or password'
	},
	LOGIN_USER_NOT_VERIFIED: {
		message: 'Please verify your email before logging in'
	},


    RESET_PASSWORD_BAD_TOKEN: {
		message: 'This password reset link is invalid or has expired'
	},
	RESET_PASSWORD_INVALID_PASSWORD: {
		field: 'password',
		message: 'Password does not meet security requirements'
	},


    VERIFY_USER_BAD_TOKEN: {
		message: 'This verification link is invalid or has expired'
	},
	VERIFY_USER_ALREADY_VERIFIED: {
		message: 'Your email is already verified'
	},


    UPDATE_USER_EMAIL_ALREADY_EXISTS: {
		field: 'email',
		message: 'This email is already in use by another account'
	},
	UPDATE_USER_INVALID_PASSWORD: {
		field: 'password',
		message: 'Current password is incorrect'
	},


    ACCESS_TOKEN_ALREADY_EXPIRED: {
		message: 'Your session has expired. Please log in again'
	},
    
	ACCESS_TOKEN_DECODE_ERROR: {
		message: 'Authentication error. Please log in again'
	}
};
