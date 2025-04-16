<?php
    // Check if user is logged in by verifying the token in localStorage
    $token = "<script>document.write(localStorage.getItem('access_token'));</script>";
    if (!$token) {
        header("Location: login.php");
        exit();
    }
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Dashboard - Portfolio</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Lexend:wght@300;400;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="../assets/css/styles.css">
</head>
<body>

<!-- Navbar with Dashboard link and Logout -->
<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container">
        <a class="navbar-brand" href="dashboard.php">Dashboard</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav ms-auto">
                <li class="nav-item">
                    <button id="logout" class="btn btn-danger">Logout</button>
                </li>
            </ul>
        </div>
    </div>
</nav>

<div class="container mt-5">
    <h2 class="text-center">Dashboard</h2>

    <!-- Button to Add New Project -->
    <div class="text-center mb-4">
        <button id="addProject" class="btn btn-primary">Add New Project</button>
    </div>

    <!-- Project List -->
    <div id="projectList" class="mt-4">
        <!-- Projects will be loaded here by JS -->
    </div>
</div>

<!-- Add New Project Modal -->
<div class="modal fade" id="addProjectModal" tabindex="-1" aria-labelledby="addProjectModalLabel" aria-hidden="true">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="addProjectModalLabel">Add New Project</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
                <form id="addProjectForm">
                    <div class="mb-3">
                        <label for="projectTitle" class="form-label">Title</label>
                        <input type="text" class="form-control" id="projectTitle" required>
                    </div>
                    <div class="mb-3">
                        <label for="projectDescription" class="form-label">Description</label>
                        <textarea class="form-control" id="projectDescription" rows="3" required></textarea>
                    </div>
                    <div class="mb-3">
                        <label for="projectLink" class="form-label">Project Link (Optional)</label>
                        <input type="url" class="form-control" id="projectLink" placeholder="https://example.com">
                    </div>
                    <div class="mb-3">
                        <label for="projectImageFile" class="form-label">Upload Image (Optional)</label>
                        <input type="file" class="form-control" id="projectImageFile" accept="image/*" multiple>
                    </div>
                    <button type="submit" class="btn btn-primary">Save</button>
                </form>
            </div>
        </div>
    </div>
</div>

<script src="../assets/js/dashboard.js"></script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
