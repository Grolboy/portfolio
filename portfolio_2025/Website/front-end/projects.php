<?php
$title = 'Projects - Portfolio'; // Page title
$custom_js = '../assets/js/project_viewing.js'; // Path to the specific JavaScript file
ob_start(); // Start output buffering
?>

<!-- Projects Section -->
<section class="projects container">
    <h2 class="text-center mt-5">My Projects</h2>
    <div class="row" id="project-list">
        <!-- Projects will be loaded here by JS -->
    </div>
</section>

<?php
$content = ob_get_clean(); // Get the buffered content
include '../includes/layout.php'; // Include the layout template
?>
