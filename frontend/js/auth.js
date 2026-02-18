// backend server address
const API_URL = 'http://localhost:5000/api';   

//gets the saved JWT token from local storage, which is used to authenticate API requests
function getToken() {
    return localStorage.getItem('access_token');
}

// saves the JWT token to local storage after successful login, allowing the user to stay authenticated across page reloads and sessions
function setToken(token) {
    localStorage.setItem('access_token', token);
}

// removes the JWT token from local storage, effectively logging the user out and requiring them to log in again to access protected resources
function removeToken() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
}

// Check if user is authenticated
// Redirect to login page if not
/*function checkAuth() {
    const token = getToken();
    if (!token) {
        window.location.href = 'login.html';
    }
} */

    // when user logs out, it removes token and returns to login page
function logout() {
    removeToken();
    window.location.href = 'login.html';
}

// This event listener waits for the DOM to fully load, then attaches a submit event handler to the login form. When the form is submitted, it prevents the default form submission behavior, collects the username and password from the input fields, and sends a POST request to the backend API to authenticate the user. If the login is successful, it saves the JWT token and user information in local storage and redirects to the dashboard. If there is an error, it displays an appropriate error message to the user.
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    
    // NEW: Handle login form submission
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault(); //stops the browseer from reloading the page
            
            // Collect form data
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            const errorDiv = document.getElementById('error-message');
            
            // Clear previous error 
            // sends login request to backend
            try {
                const response = await fetch(`${API_URL}/auth/login`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ username, password })
                });
                
                const data = await response.json();
                
                /* if login is successful,
                    saves JWT token, saves user data and redirects to dashboard
                */
                if (response.ok) {
                    setToken(data.access_token);
                    localStorage.setItem('user', JSON.stringify(data.user));
                    window.location.href = 'dashboard.html';
                } 
                
                /* if login fails,
                    shows error message
                */
                else {
                    errorDiv.textContent = data.error || 'Login failed';
                    errorDiv.classList.remove('hidden');
                }
            } 
            
            /* if backend is down,
                it displays 'connection error'            
            */

            catch (error) {
                errorDiv.textContent = 'Connection error';
                errorDiv.classList.remove('hidden');
            }
        });
    }
});

// helps you call any protected API route
async function apiCall(endpoint, method = 'GET', data = null) {
    const token = getToken();
    const options = {
        method,
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        }
    };
    
    if (data) {
        options.body = JSON.stringify(data);
    }
    
    try {
        const response = await fetch(`${API_URL}${endpoint}`, options);
        
        /*if token is expired, invalid or missing,
            it logs user out automatically
        */
        if (response.status === 401) {
            logout();
            return null;
        }
        
        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        return null;
    }
}