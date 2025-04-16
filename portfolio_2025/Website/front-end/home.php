<?php
$title = 'Portfolio';
$custom_js = '../assets/js/project_viewing.js'; // Path to the specific JavaScript file
ob_start();
?>
<header class="hero">
    <div class="container text-center">
        <h1>Welcome to My Portfolio</h1>
        <p>Discover my latest projects and work.</p>
    </div>
</header>

<section class="projects container mt-5">
    <h2 class="text-center">Featured Projects</h2>
    <div class="row" id="project-list">
        <!-- Projects will be loaded here by JS -->
    </div>
</section>
<?php
$content = ob_get_clean();
include '../includes/layout.php';
?>