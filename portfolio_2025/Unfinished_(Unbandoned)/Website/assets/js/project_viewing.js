document.addEventListener("DOMContentLoaded", function () {
    fetch('http://127.0.0.1:8000/projects')
        .then(response => response.json())
        .then(projects => {
            const projectList = document.getElementById('project-list');

            if (!projects.length) {
                projectList.innerHTML = "<p>No projects available.</p>";
                return;
            }

            projects.sort((a, b) => b.id - a.id); // Newest first

            projects.forEach(project => {
                const projectItem = document.createElement('div');
                projectItem.classList.add('col-md-4', 'mb-4');

                const imageUrl = project.images.length > 0 ? `../${project.images[0]}` : '../assets/images/placeholder.jpg';
                const maxLen = 100;
                const desc = project.description.length > maxLen
                    ? `${project.description.substring(0, maxLen)}...`
                    : project.description;

                const createCardHTML = (imgSrc) => `
                    <div class="card project-card h-100 d-flex flex-column shadow-sm rounded-4 border-0">
                        <img src="${imgSrc}" class="card-img-top project-image rounded-top-4" alt="Project Image">
                        <div class="card-body d-flex flex-column">
                            <h5 class="card-title">${project.title}</h5>
                            <p class="card-text flex-grow-1">${desc}</p>
                            <a href="project.php?slug=${project.slug}" class="btn btn-secondary mt-auto">View Project</a>
                        </div>
                    </div>
                `;

                const img = new Image();
                img.src = imageUrl;

                img.onload = () => {
                    projectItem.innerHTML = createCardHTML(imageUrl);
                    projectList.appendChild(projectItem);
                };

                img.onerror = () => {
                    projectItem.innerHTML = createCardHTML('../assets/images/placeholder.jpg');
                    projectList.appendChild(projectItem);
                };
            });
        })
        .catch(err => {
            console.error('Error loading projects:', err);
            document.getElementById('project-list').innerHTML = "<p>Error loading projects. Please try again later.</p>";
        });
});
