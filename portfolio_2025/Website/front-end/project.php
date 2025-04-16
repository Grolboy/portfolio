<?php
// Get the project slug from the URL (e.g., project.php?slug=project-title)
$slug = isset($_GET['slug']) ? $_GET['slug'] : null;

if (!$slug) {
    echo "Project slug not provided.";
    exit;
}

$title = 'Project Details - Portfolio'; // Page title
$custom_js = '../assets/js/project.js'; // Path to the specific JavaScript file
ob_start(); // Start output buffering
?>

<!-- Project Details Section -->
<section class="project-details container mt-5">
    <h2 class="text-center" id="project-title">Project Title</h2>
    <div id="project-content" class="row">
        <!-- Project details will be loaded here by JS -->
    </div>
</section>

<?php
$content = ob_get_clean(); // Get the buffered content
include '../includes/layout.php'; // Include the layout template
?>
