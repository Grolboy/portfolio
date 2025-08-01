<?php
$title = 'Portfolio';
ob_start();
?>
<section id="home">
    <header class="hero">
        <div class="container text-center">
            <h1>Welcome to My Portfolio</h1>
            <p>Discover my latest projects and work.</p>
        </div>
    </header>
</section>

<section id="about">
    <div class="container mt-5">
        <h2 class="text-center">About Me</h2>
        <div class="row mt-4">
            <div class="col-md-6">
                <p>Hello! I'm Lucas Ingmar, a passionate developer with a love for creating innovative solutions. I specialize in web development and have experience in various programming languages and frameworks.</p>
            </div>
        </div>
    </div>
</section>

<section class="projects container mt-5">
    <h2 class="text-center">Featured Projects</h2>
    <div class="row" id="project-list">
        <?php include '../includes/projects.php'; ?>
    </div>
</section>

<?php
$content = ob_get_clean();
include '../includes/layout.php';
?>