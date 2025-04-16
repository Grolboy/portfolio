<!-- filepath: d:\XAMPP\htdocs\Portfolio\Website\front-end\contact.php -->
<?php
$title = 'Contact - Portfolio'; // Page title
$custom_js = '../assets/js/contact.js'; // Path to the specific JavaScript file
ob_start(); // Start output buffering
?>

<!-- Contact Section -->
<div class="container mt-5">
    <h2 class="text-center">Contact Me</h2>
    <div class="row mt-4">
        <!-- Left Column: Contact Form -->
        <div class="col-md-8">
            <form id="contactForm">
                <div class="mb-3">
                    <label for="name" class="form-label">Your Name</label>
                    <input type="text" class="form-control" id="name" placeholder="Your name here" required>
                </div>
                <div class="mb-3">
                    <label for="email" class="form-label" >Your Email</label>
                    <input type="email" class="form-control" placeholder="mail@email.com" id="email" required>
                </div>
                <div class="mb-3">
                    <label for="phone" class="form-label">Your Phone</label>
                    <input type="tel" class="form-control" id="phone" placeholder="Enter your phone number">
                </div>
                <div class="mb-3">
                    <label for="message" class="form-label" >Your Message</label>
                    <textarea class="form-control" id="message" rows="5" required placeholder="Your message here"></textarea>
                </div>
                <div class="">
                <button type="submit" class="btn btn-secondary w-100">Send Message</button>
                </div>
            </form>
        </div>

        <!-- Right Column: Boxed Section with Image and Contact Info -->
        <div class="col-md-4 mb-4">
            <div class="card shadow-sm">
                <div class="card-body text-center">
                    <img src="../assets/images/me.jpg" alt="My Photo" class="img-fluid rounded-circle mb-3" style="width: 250px; height: 250px;">
                    <h5 class="card-title">Lucas Ingmar</h5>
                    <p><strong>Email:</strong> <a href="mailto:lucas@tech-racoon.net">lucas@tech-racoon.net</a></p>
                    <p><strong>Phone:</strong> +31636100452</p>
                </div>
            </div>
        </div>
    </div>
</div>

<?php
$content = ob_get_clean(); // Get the buffered content
include '../includes/layout.php'; // Include the layout template
?>