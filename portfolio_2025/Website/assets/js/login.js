document.getElementById('loginForm').addEventListener('submit', function (e) {
    e.preventDefault();
    const username = document.getElementById('username').value;  // Use username instead of email
    const password = document.getElementById('password').value;

    fetch('http://127.0.0.1:8000/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password })  // Send username and password to the API
    })
    .then(response => response.json())
    .then(data => {
        if (data.access_token) {
            // Save token in localStorage
            localStorage.setItem('access_token', data.access_token);
            window.location.href = 'dashboard.php';  // Redirect to dashboard
        } else {
            alert('Invalid credentials');
        }
    })
    .catch(error => console.error('Error logging in:', error));
});
