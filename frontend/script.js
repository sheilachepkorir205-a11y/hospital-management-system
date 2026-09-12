const passwordInput = document.querySelector('#password');
const passwordToggle = document.querySelector('#password-toggle');
const loginForm = document.querySelector('#login-form');
const formStatus = document.querySelector('#form-status');

passwordToggle.addEventListener('click', () => {
	const isVisible = passwordInput.type === 'text';
	passwordInput.type = isVisible ? 'password' : 'text';
	passwordToggle.setAttribute('aria-pressed', String(!isVisible));
	passwordToggle.setAttribute('aria-label', isVisible ? 'Show password' : 'Hide password');
});

loginForm.addEventListener('submit', () => {
	formStatus.textContent = 'Signing in...';
});
