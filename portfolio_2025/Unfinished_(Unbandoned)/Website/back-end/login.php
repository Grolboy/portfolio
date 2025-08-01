<?php
$title = 'Login - Portfolio'; // Page title
$custom_js = '../assets/js/login.js'; // Path to the specific JavaScript file
ob_start(); // Start output buffering
?>

<!-- Login Form Section -->
<div class="container mt-5">
    <h2 class="text-center">Login</h2>
    <form id="loginForm">
        <div class="mb-3">
            <label for="username" class="form-label">Username</label>
            <input type="text" class="form-control" id="username" required>
        </div>
        <div class="mb-3">
            <label for="password" class="form-label">Password</label>
            <input type="password" class="form-control" id="password" required>
        </div>
        <button type="submit" class="btn btn-primary w-100">Login</button>
    </form>

    <!-- Go back button -->
    <div class="mt-3 text-center">
        <a href="../index.php" class="btn btn-secondary">Go Back to Home Page</a>
    </div>
</div>

<?php
$content = ob_get_clean(); // Get the buffered content
include '../includes/layout.php'; // Include the layout template
?>
