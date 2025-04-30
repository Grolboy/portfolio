<?php
$custom_js = '../assets/js/project_viewing.js'; // Path to the specific JavaScript file
function renderProjectsSection() {
    ob_start(); // Start output buffering
    ?>
    <!-- Projects Section -->
    <section class="projects container">
        <div class="row" id="project-list">
            <!-- Projects will be loaded here by JS -->
        </div>
    </section>
    <?php
    return ob_get_clean(); // Return the buffered content
}
?>
