// Signup functionality for School Management System
const API_URL = 'http://localhost:5000/api';

// Get form elements
const signupForm = document.getElementById('signupForm');
const signupBtn = document.getElementById('signupBtn');
const errorMessage = document.getElementById('error-message');
const successMessage = document.getElementById('success-message');

// Show error message
function showError(message) {
    errorMessage.textContent = message;
    errorMessage.classList.remove('hidden');
    successMessage.classList.add('hidden');
}

// Show success message
function showSuccess(message) {
    successMessage.textContent = message;
    successMessage.classList.remove('hidden');
    errorMessage.classList.add('hidden');
}

// Hide all messages
function hideMessages() {
    errorMessage.classList.add('hidden');
    successMessage.classList.add('hidden');
}

// Validate form
function validateForm(formData) {
    // Check if all required fields are filled
    if (!formData.firstName || !formData.lastName || !formData.username || 
        !formData.email || !formData.password || !formData.confirmPassword || !formData.role) {
        showError('Please fill in all required fields');
        return false;
    }

    // Check username length
    if (formData.username.length < 3) {
        showError('Username must be at least 3 characters long');
        return false;
    }

    // Check password length
    if (formData.password.length < 6) {
        showError('Password must be at least 6 characters long');
        return false;
    }

    // Check if passwords match
    if (formData.password !== formData.confirmPassword) {
        showError('Passwords do not match');
        return false;
    }

    // Validate email format
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(formData.email)) {
        showError('Please enter a valid email address');
        return false;
    }

    // Check terms agreement
    const termsCheckbox = document.getElementById('terms');
    if (!termsCheckbox.checked) {
        showError('Please accept the Terms and Conditions');
        return false;
    }

    return true;
}

// Handle form submission
signupForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    hideMessages();

    // Disable submit button
    signupBtn.disabled = true;
    signupBtn.textContent = 'Creating Account...';

    // Get form data
    const formData = {
        firstName: document.getElementById('firstName').value.trim(),
        lastName: document.getElementById('lastName').value.trim(),
        username: document.getElementById('username').value.trim(),
        email: document.getElementById('email').value.trim(),
        password: document.getElementById('password').value,
        confirmPassword: document.getElementById('confirmPassword').value,
        role: document.getElementById('role').value
    };

    // Validate form
    if (!validateForm(formData)) {
        signupBtn.disabled = false;
        signupBtn.textContent = 'Create Account';
        return;
    }

    try {
        // Send registration request
        const response = await fetch(`${API_URL}/auth/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        const data = await response.json();

        if (response.ok) {
            // Registration successful
            showSuccess('Account created successfully! Redirecting to login...');
            
            // Clear form
            signupForm.reset();

            // Redirect to login page after 2 seconds
            setTimeout(() => {
                window.location.href = 'login.html';
            }, 2000);

        } else {
            // Registration failed
            showError(data.error || 'Registration failed. Please try again.');
            signupBtn.disabled = false;
            signupBtn.textContent = 'Create Account';
        }

    } catch (error) {
        console.error('Signup error:', error);
        showError('Connection error. Please check if the server is running.');
        signupBtn.disabled = false;
        signupBtn.textContent = 'Create Account';
    }
});

// Real-time password match validation
document.getElementById('confirmPassword').addEventListener('input', function() {
    const password = document.getElementById('password').value;
    const confirmPassword = this.value;
    
    if (confirmPassword && password !== confirmPassword) {
        this.setCustomValidity('Passwords do not match');
        this.style.borderColor = '#e74c3c';
    } else {
        this.setCustomValidity('');
        this.style.borderColor = '#ddd';
    }
});

// Clear error when user starts typing
const inputs = signupForm.querySelectorAll('input, select');
inputs.forEach(input => {
    input.addEventListener('input', hideMessages);
});