document.addEventListener("DOMContentLoaded", function () {
    // Get the project slug from the URL (e.g., project.php?slug=project-title)
    const urlParams = new URLSearchParams(window.location.search);
    const slug = urlParams.get('slug');

    if (!slug) {
        alert('No project slug provided.');
        return;
    }

    // Fetch project details using the slug
    fetch(`http://127.0.0.1:8000/projects/${slug}`)  // Ensure FastAPI endpoint returns the correct data
        .then(response => response.json())
        .then(project => {
            if (project) {
                // Set the project title
                document.getElementById('project-title').textContent = project.title;

                // Set the project content (e.g., description, images)
                const projectContent = document.getElementById('project-content');
                let content = `
                    <div class="col-12">
                        <h3>Description</h3>
                        <p>${project.description}</p>
                        <h3>Images</h3>
                        <div class="row">
                `;

                // Add images if they exist
                if (project.images && project.images.length > 0) {
                    project.images.forEach(image => {
                        // Prepend '../' to the image URL
                        const imageUrl = `../${image}`;
                        content += `
                            <div class="col-md-4 mb-4">
                                <img src="${imageUrl}" class="img-fluid" alt="Image for ${project.title}">
                            </div>
                        `;
                    });
                } else {
                    content += `
                        <div class="col-12">
                            <p>No images available for this project.</p>
                        </div>
                    `;
                }

                content += `
                        </div>
                    </div>
                `;

                projectContent.innerHTML = content;
            } else {
                alert("Project not found.");
            }
        })
        .catch(error => {
            console.error('Error fetching project details:', error);
            alert("Error loading project details.");
        });
});